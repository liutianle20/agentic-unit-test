"""Small, intentionally conservative safety helpers for the teaching agent.

These checks are defense in depth, not a replacement for an operating-system
sandbox.  They keep the policy easy to inspect in class while stopping a few
high-impact mistakes before untrusted text reaches the model or generated code
reaches pytest.
"""

from __future__ import annotations

import ast
from pathlib import Path
import re


_PROMPT_INJECTION_PATTERNS = (
    ("instruction override", re.compile(
        r"\b(?:ignore|disregard|override|forget)\b.{0,40}"
        r"\b(?:previous|prior|above|system|developer)\b.{0,30}"
        r"\b(?:instructions?|messages?|prompts?|rules?)\b", re.IGNORECASE | re.DOTALL,
    )),
    ("prompt disclosure", re.compile(
        r"\b(?:reveal|show|print|return|leak|exfiltrate)\b.{0,60}"
        r"\b(?:system|developer)\b.{0,20}\b(?:prompt|message|instructions?)\b",
        re.IGNORECASE | re.DOTALL,
    )),
    ("role impersonation", re.compile(
        r"<\s*(?:system|developer|assistant)\s*>|\[\s*(?:system|developer)\s*\]",
        re.IGNORECASE,
    )),
)
_DIRECT_ROLE_PATTERN = re.compile(
    r"^\s*(?:please\s+)?(?:" + _PROMPT_INJECTION_PATTERNS[2][1].pattern + ")",
    _PROMPT_INJECTION_PATTERNS[2][1].flags,
)
_QUOTED_TEXT = re.compile(r'"[^"\n]*"|`[^`\n]*`')

_PRIVATE_KEY = re.compile(
    r"-----BEGIN[^\n]*PRIVATE KEY-----.*?-----END[^\n]*PRIVATE KEY-----",
    re.IGNORECASE | re.DOTALL,
)
_TOKEN_PATTERNS = (
    ("OpenAI-style API key", re.compile(r"\bsk-(?:proj-)?[A-Za-z0-9_-]{16,}\b")),
    ("GitHub token", re.compile(r"\bgh[pousr]_[A-Za-z0-9]{20,}\b")),
    ("AWS access key", re.compile(r"\b(?:AKIA|ASIA)[A-Z0-9]{16}\b")),
    ("bearer token", re.compile(r"(?i)\bBearer\s+[A-Za-z0-9._~+/=-]{16,}")),
)
_QUOTED_SECRET = re.compile(
    r"(?i)(\b(?:api[_-]?key|access[_-]?token|auth[_-]?token|password|passwd|secret)\b"
    r"\s*[:=]\s*)(['\"])([^'\"\n]{8,})(\2)"
)
_ENV_SECRET = re.compile(
    r"(?im)^(\s*(?:API_KEY|ACCESS_TOKEN|AUTH_TOKEN|PASSWORD|PASSWD|SECRET)\s*=\s*)"
    r"([^\s#]{8,})"
)
_EMAIL = re.compile(r"\b[A-Z0-9._%+-]+@([A-Z0-9.-]+\.[A-Z]{2,})\b", re.IGNORECASE)
_SSN = re.compile(r"(?<!\d)\d{3}-\d{2}-\d{4}(?!\d)")
_SAFE_EXAMPLE_DOMAINS = {"example.com", "example.net", "example.org"}

_SENSITIVE_DIRECTORIES = {".git", ".aws", ".ssh", ".gnupg"}
_SENSITIVE_NAMES = {
    ".netrc", ".npmrc", ".pypirc", "id_rsa", "id_ed25519",
    "credentials", "credentials.json", "secrets", "secrets.json",
}
_SENSITIVE_SUFFIXES = {".pem", ".key", ".p12", ".pfx"}

_BLOCKED_IMPORTS = {
    "ctypes", "ftplib", "httpx", "importlib", "multiprocessing", "paramiko", "requests",
    "socket", "subprocess", "telnetlib", "urllib", "webbrowser",
}
_BLOCKED_BUILTINS = {"compile", "eval", "exec", "__import__"}
_BLOCKED_MODULE_CALLS = {
    "builtins": {"compile", "eval", "exec", "__import__"},
    "os": {
        "system", "popen", "open", "remove", "unlink", "rmdir", "removedirs",
        "rename", "renames", "replace", "kill", "putenv", "chdir", "chmod",
        "chown", "mkdir", "makedirs", "link", "symlink",
    },
    "shutil": {"rmtree", "move"},
}


def prompt_injection_reasons(text: str) -> list[str]:
    """Return high-confidence prompt-injection categories without echoing text."""
    return [label for label, pattern in _PROMPT_INJECTION_PATTERNS if pattern.search(text)]


def goal_prompt_injection_reasons(text: str) -> list[str]:
    """Screen direct goals narrowly so quoted attack strings can still be tested."""
    unquoted = _QUOTED_TEXT.sub("[quoted data]", text)
    reasons = [
        label for label, pattern in _PROMPT_INJECTION_PATTERNS[:2]
        if pattern.search(unquoted)
    ]
    if _DIRECT_ROLE_PATTERN.search(unquoted):
        reasons.append("role impersonation")
    return reasons


def redact_sensitive_text(text: str, *, include_pii: bool = True) -> tuple[str, list[str]]:
    """Redact common credentials and optional PII, returning finding categories."""
    findings: list[str] = []

    if _PRIVATE_KEY.search(text):
        findings.append("private key")
        text = _PRIVATE_KEY.sub("[REDACTED PRIVATE KEY]", text)

    for label, pattern in _TOKEN_PATTERNS:
        if pattern.search(text):
            findings.append(label)
            text = pattern.sub(f"[REDACTED {label.upper()}]", text)

    if _QUOTED_SECRET.search(text):
        findings.append("named secret")
        text = _QUOTED_SECRET.sub(
            lambda match: f"{match.group(1)}{match.group(2)}[REDACTED]{match.group(4)}",
            text,
        )
    if _ENV_SECRET.search(text):
        findings.append("environment secret")
        text = _ENV_SECRET.sub(lambda match: f"{match.group(1)}[REDACTED]", text)

    if include_pii:
        def redact_email(match: re.Match) -> str:
            if match.group(1).lower() in _SAFE_EXAMPLE_DOMAINS:
                return match.group(0)
            findings.append("email address")
            return "[REDACTED EMAIL]"

        text = _EMAIL.sub(redact_email, text)
        if _SSN.search(text):
            findings.append("US social security number")
            text = _SSN.sub("[REDACTED SSN]", text)

    return text, sorted(set(findings))


def redact_data(value):
    """Recursively redact strings before structured data is logged or displayed."""
    findings: set[str] = set()

    def visit(item):
        if isinstance(item, str):
            redacted, labels = redact_sensitive_text(item)
            findings.update(labels)
            return redacted
        if isinstance(item, list):
            return [visit(child) for child in item]
        if isinstance(item, tuple):
            return tuple(visit(child) for child in item)
        if isinstance(item, dict):
            return {key: visit(child) for key, child in item.items()}
        return item

    return visit(value), sorted(findings)


def is_sensitive_path(value: str | Path) -> bool:
    """Identify file names that should never be copied or exposed to the model."""
    path = Path(value)
    lowered_parts = [part.lower() for part in path.parts]
    if any(part in _SENSITIVE_DIRECTORIES for part in lowered_parts):
        return True
    name = path.name.lower()
    return (
        name == ".env"
        or name.startswith(".env.")
        or name in _SENSITIVE_NAMES
        or name.startswith("credentials.")
        or name.startswith("secrets.")
        or path.suffix.lower() in _SENSITIVE_SUFFIXES
    )


def validate_test_source(source: str) -> None:
    """Reject obvious secret leakage and unsafe actions in generated pytest code."""
    _, sensitive = redact_sensitive_text(source)
    if sensitive:
        raise ValueError(
            "Generated test rejected by safety policy: sensitive value in test source"
        )

    try:
        tree = ast.parse(source)
    except SyntaxError:
        # Syntax errors cannot execute; pytest reports them through the normal repair flow.
        return

    module_aliases: dict[str, str] = {}
    imported_calls: dict[str, tuple[str, str]] = {}
    path_constructors = {"Path"}
    findings: set[str] = set()

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                root = alias.name.split(".", 1)[0]
                local = alias.asname or root
                module_aliases[local] = root
                if root in _BLOCKED_IMPORTS:
                    findings.add(f"blocked import: {root}")
        elif isinstance(node, ast.ImportFrom) and node.module:
            root = node.module.split(".", 1)[0]
            if root in _BLOCKED_IMPORTS:
                findings.add(f"blocked import: {root}")
            for alias in node.names:
                local = alias.asname or alias.name
                imported_calls[local] = (root, alias.name)
                if root == "pathlib" and alias.name == "Path":
                    path_constructors.add(local)

    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        if isinstance(node.func, ast.Name):
            name = node.func.id
            if name in _BLOCKED_BUILTINS:
                findings.add(f"blocked builtin: {name}")
            imported = imported_calls.get(name)
            if imported and imported[0] in _BLOCKED_MODULE_CALLS:
                if imported[1] in _BLOCKED_MODULE_CALLS[imported[0]]:
                    findings.add(f"blocked call: {imported[0]}.{imported[1]}")
            if name == "open" or imported and imported in {("builtins", "open"), ("io", "open")}:
                if _has_sensitive_literal_path(node):
                    findings.add("sensitive or external file access")
                if _opens_for_writing(node):
                    findings.add("file write through open")
        elif isinstance(node.func, ast.Attribute):
            root_name, attribute = _attribute_root(node.func)
            module = module_aliases.get(root_name, root_name)
            blocked = _BLOCKED_MODULE_CALLS.get(module, set())
            if attribute in blocked or any(
                attribute.startswith(prefix) for prefix in ("exec", "spawn")
            ) and module == "os":
                findings.add(f"blocked call: {module}.{attribute}")
            if attribute == "open" and module in {"builtins", "io"}:
                if _has_sensitive_literal_path(node):
                    findings.add("sensitive or external file access")
                if _opens_for_writing(node):
                    findings.add("file write through open")
            if attribute in {
                "open", "read_text", "read_bytes", "write_text", "write_bytes",
                "unlink", "rmdir", "rename", "replace", "touch", "mkdir",
            }:
                owner = node.func.value
                if isinstance(owner, ast.Call) and _is_path_constructor(
                    owner, module_aliases, path_constructors
                ):
                    if _has_sensitive_literal_path(owner):
                        findings.add("sensitive or external file access")
                    if attribute in {
                        "write_text", "write_bytes", "unlink", "rmdir", "rename",
                        "replace", "touch", "mkdir",
                    }:
                        findings.add("literal-path file modification")
            if attribute == "home" and (
                root_name in path_constructors
                or _is_path_class(node.func.value, module_aliases, path_constructors)
            ):
                findings.add("home directory access")

        if _is_path_constructor(node, module_aliases, path_constructors):
            if _has_sensitive_literal_path(node):
                findings.add("sensitive or external path")

    if findings:
        raise ValueError(
            "Generated test rejected by safety policy: " + ", ".join(sorted(findings))
        )


def _has_sensitive_literal_path(call: ast.Call) -> bool:
    if not call.args or not isinstance(call.args[0], ast.Constant):
        return False
    value = call.args[0].value
    if not isinstance(value, str):
        return False
    path = Path(value).expanduser()
    return path.is_absolute() or ".." in Path(value).parts or is_sensitive_path(value)


def _is_path_constructor(call, module_aliases, path_constructors) -> bool:
    function = call.func
    if isinstance(function, ast.Name):
        return function.id in path_constructors
    if isinstance(function, ast.Attribute) and function.attr == "Path":
        root, _ = _attribute_root(function)
        return module_aliases.get(root, root) == "pathlib"
    return False


def _is_path_class(node, module_aliases, path_constructors) -> bool:
    if isinstance(node, ast.Name):
        return node.id in path_constructors
    if isinstance(node, ast.Attribute) and node.attr == "Path":
        root, _ = _attribute_root(node)
        return module_aliases.get(root, root) == "pathlib"
    return False


def _opens_for_writing(call: ast.Call) -> bool:
    mode = None
    if len(call.args) > 1 and isinstance(call.args[1], ast.Constant):
        mode = call.args[1].value
    for keyword in call.keywords:
        if keyword.arg == "mode" and isinstance(keyword.value, ast.Constant):
            mode = keyword.value.value
    return isinstance(mode, str) and any(flag in mode for flag in "wax+")


def _attribute_root(node: ast.Attribute) -> tuple[str, str]:
    attribute = node.attr
    value: ast.AST = node.value
    while isinstance(value, ast.Attribute):
        value = value.value
    return (value.id if isinstance(value, ast.Name) else "", attribute)
