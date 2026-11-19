"""Repository tools for the disposable preview workspace."""

import ast
import difflib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
from xml.etree import ElementTree

IGNORED = {".git", ".venv", "__pycache__", ".pytest_cache", ".env", ".coverage"}
READ_LIMIT = 32_768
TEST_PATH = re.compile(r"tests/test_agent_[A-Za-z0-9_]+\.py")


def ignore_files(directory, names):
    return [
        name for name in names
        if name in IGNORED or name.startswith(".env.") or (Path(directory) / name).is_symlink()
    ]


class Workspace:
    def __init__(self, root):
        self.root = root
        self.staged = {}
        self.revision = 0

    def path(self, value):
        path = Path(value)
        if path.is_absolute() or ".." in path.parts:
            raise ValueError("Expected a workspace-relative path")
        current = self.root
        for part in path.parts:
            current = current / part
            if current.is_symlink():
                raise ValueError("Symlinks are excluded")
        return current

    def list_files(self, pattern):
        self.path(pattern)
        if not pattern:
            raise ValueError("Expected a nonempty glob")
        return [
            str(path.relative_to(self.root))
            for path in sorted(self.root.glob(pattern))
            if path.is_file() and self.path(str(path.relative_to(self.root)))
        ][:200]

    def read_file(self, path):
        file = self.path(path)
        if not file.is_file():
            raise ValueError("Expected a regular file")
        with file.open("rb") as source:
            data = source.read(READ_LIMIT + 1)
        return {"text": data[:READ_LIMIT].decode("utf-8", errors="replace"),
                "truncated": len(data) > READ_LIMIT}

    def inspect_python(self, path):
        source = self.read_file(path)
        if source["truncated"]:
            raise ValueError("Source exceeds the AST inspection limit")
        tree = ast.parse(source["text"])
        return [
            {"line": node.lineno, "kind": type(node).__name__, "definition": definition}
            for node in ast.walk(tree)
            if (definition := self.definition(node)) is not None
        ]

    def read_lines(self, path, start, end):
        if not 1 <= start <= end or end - start >= 80:
            raise ValueError("Expected an inclusive line range of at most 80 lines")
        source = self.read_file(path)
        lines = source["text"].splitlines()
        if source["truncated"]:
            lines = lines[:-1] if not source["text"].endswith("\n") else lines
        if start > len(lines):
            raise ValueError("Line range starts beyond the readable file")
        return {"path": path, "start": start, "end": min(end, len(lines)),
                "text": "\n".join(lines[start - 1:end]), "truncated": source["truncated"]}

    @staticmethod
    def definition(node):
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            return ast.unparse(node)
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            returns = f" -> {ast.unparse(node.returns)}" if node.returns else ""
            return f"{node.name}({ast.unparse(node.args)}){returns}"
        if isinstance(node, ast.ClassDef):
            return node.name
        return None

    def stage_tests(self, path, content):
        if not TEST_PATH.fullmatch(path):
            raise ValueError("Use tests/test_agent_<name>.py")
        if not content.strip() or len(content.encode()) > READ_LIMIT:
            raise ValueError("Expected nonempty test content within the size limit")
        file = self.path(path)
        if file.exists() and path not in self.staged:
            raise ValueError("Existing repository files cannot be overwritten")
        content = content.rstrip("\n") + "\n"
        if self.staged.get(path) != content:
            file.parent.mkdir(exist_ok=True)
            file.write_text(content, encoding="utf-8")
            self.staged[path] = content
            self.revision += 1
        return {"revision": self.revision, "diff": self.diff()}

    def diff(self):
        return "".join(
            f"diff --git a/{path} b/{path}\nnew file mode 100644\n" + "".join(
                difflib.unified_diff([], content.splitlines(keepends=True),
                                     fromfile="/dev/null", tofile=f"b/{path}")
            )
            for path, content in sorted(self.staged.items())
        )

    def pytest(self, target, timeout, coverage=False, counts=False):
        if target != "." or not self.staged:
            raise ValueError("Use target '.' after staging tests")
        command = [sys.executable, "-B", "-m", "pytest", "-q", "-p", "no:cacheprovider"]
        report = self.root / ".agent-coverage.json"
        junit = self.root / ".agent-tests.xml"
        if counts:
            junit.unlink(missing_ok=True)
            command += ["--junitxml=.agent-tests.xml"]
        if coverage:
            report.unlink(missing_ok=True)
            command += ["-p", "pytest_cov.plugin", "--cov=.", "--cov-branch",
                        "--cov-report=json:.agent-coverage.json"]
        # Pass only runtime settings needed by the current Python interpreter.
        env = {key: os.environ[key] for key in ("PATH", "LANG", "LC_ALL", "SYSTEMROOT")
               if key in os.environ}
        env["PYTEST_DISABLE_PLUGIN_AUTOLOAD"] = "1"
        if coverage:
            env["COVERAGE_FILE"] = str(self.root / ".coverage")
        try:
            completed = subprocess.run(
                [*command, *sorted(self.staged)], cwd=self.root, env=env,
                stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True,
                errors="replace", timeout=timeout, check=False,
            )
        except subprocess.TimeoutExpired:
            return {"status": "timeout", "revision": self.revision}
        status = {0: "passed", 1: "failed"}.get(completed.returncode, "error")
        if completed.stdout.strip().endswith("No module named pytest"):
            status = "error"
        result = {"status": status, "revision": self.revision,
                  "exit_code": completed.returncode, "output": completed.stdout[-8000:]}
        if counts and completed.returncode in (0, 1, 5) and junit.is_file() and not junit.is_symlink():
            cases = list(ElementTree.parse(junit).iter("testcase"))
            result["test_counts"] = {
                "passed": sum(not any(case.find(tag) is not None
                                      for tag in ("failure", "error", "skipped")) for case in cases),
                "generated": len({(case.get("classname"), case.get("name")) for case in cases}),
            }
        if coverage and status == "passed" and report.is_file() and not report.is_symlink():
            files = json.loads(report.read_text(encoding="utf-8"))["files"]
            source_summaries = [
                entry["summary"] for path, entry in files.items()
                if "tests" not in Path(path).parts and not Path(path).name.startswith("test_")
            ]
            totals = {
                key: sum(summary[key] for summary in source_summaries)
                for key in ("covered_lines", "num_statements", "covered_branches", "num_branches")
            }
            result["coverage"] = {
                "line_percent": self.percent(totals["covered_lines"], totals["num_statements"]),
                "branch_percent": self.percent(totals["covered_branches"], totals["num_branches"]),
            }
        return result

    @staticmethod
    def percent(covered, total):
        return 100 * covered / total if total else None
