"""Bounded repository retrieval and session history search."""

import json
import os
from dataclasses import dataclass
from pathlib import Path

from .workspace import READ_LIMIT, ignore_files

CLEARED = "[cleared: call the tool again if needed]"


def prompt_window(messages):
    old = [index for index, message in enumerate(messages) if message["role"] == "tool"][:-4]
    outgoing = list(messages)
    for index in old:
        outgoing[index] = {**outgoing[index], "content": CLEARED}
    return outgoing


@dataclass(frozen=True)
class Chunk:
    path: str
    start: int
    end: int
    text: str


def repository_chunks(workspace):
    eligible = []
    for directory, dirs, files in os.walk(workspace.root):
        dirs[:] = sorted(set(dirs) - set(ignore_files(directory, dirs)))
        for name in set(files) - set(ignore_files(directory, files)):
            if name.endswith((".py", ".md")) or name == "pyproject.toml":
                relative = str((Path(directory) / name).relative_to(workspace.root))
                if relative not in workspace.staged:
                    eligible.append(relative)
    chunks = []
    for relative in sorted(eligible)[:500]:
        try:
            file = workspace.path(relative)
            if not file.is_file():
                continue
            with file.open("rb") as source:
                data = source.read(READ_LIMIT + 1)
            # Decode a whole prefix ending at a line boundary when the file is capped.
            if len(data) > READ_LIMIT:
                data = data[:READ_LIMIT].rpartition(b"\n")[0]
            if b"\0" in data:
                continue
            lines = data.decode("utf-8").splitlines()
        except (OSError, ValueError):
            continue
        for offset in range(0, len(lines), 30):
            excerpt = lines[offset:offset + 40]
            if any(line.strip() for line in excerpt):
                chunks.append(Chunk(relative, offset + 1, offset + len(excerpt), "\n".join(excerpt)))
            if offset + 40 >= len(lines):
                break
    return chunks


def load_embeddings():
    from sentence_transformers import SentenceTransformer

    return SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2", local_files_only=True)


class RankedIndex:
    def __init__(self, texts, *, hybrid=False):
        from sklearn.feature_extraction.text import TfidfVectorizer

        self.vectorizer = TfidfVectorizer(
            token_pattern=r"(?u)\b\w+\b", ngram_range=(1, 2), sublinear_tf=True,
        )
        self.keywords = self.encoder = self.embeddings = None
        try:
            self.keywords = self.vectorizer.fit_transform(texts)
        except ValueError:
            pass  # Empty corpus or vocabulary.
        if hybrid and texts:
            try:
                self.encoder = load_embeddings()
                self.embeddings = self.encoder.encode(texts, normalize_embeddings=True)
            except Exception:
                self.encoder = None  # Optional backend and cached assets may be missing.

    def search(self, query):
        if not query.strip():
            raise ValueError("Expected a nonempty search query")
        if self.keywords is None:
            return []
        scores = (self.keywords @ self.vectorizer.transform([query]).T).toarray().ravel()
        if self.encoder is not None:
            try:
                embedding = self.encoder.encode([query], normalize_embeddings=True)[0]
                scores = 0.6 * (self.embeddings @ embedding) + 0.4 * scores
            except Exception:
                self.encoder = None  # Later queries can continue with keyword ranking.
        return [index for index in sorted(range(len(scores)), key=lambda i: -scores[i])
                if scores[index] > 0][:5]


class RepositorySearch:
    def __init__(self, workspace):
        self.chunks = repository_chunks(workspace)
        self.index = None

    def search(self, query):
        if self.index is None:
            self.index = RankedIndex(
                [f"{chunk.path}\n{chunk.text}" for chunk in self.chunks], hybrid=True,
            )
        hits = [self.chunks[index] for index in self.index.search(query)]
        return {"results": [
            {"path": hit.path, "start": hit.start, "end": hit.end, "text": hit.text[:1600]}
            for hit in hits
        ]}


class HistorySearch:
    def __init__(self, entries):
        self.entries = entries
        self.index = None
        self.excerpts = []

    def search(self, query):
        if self.index is None:
            for entry_id, (label, content) in self.entries.items():
                for start in range(0, max(len(content), 1), 1000):
                    text = content[start:start + 1200]
                    self.excerpts.append((entry_id, start, label, text))
                    if start + 1200 >= len(content):
                        break
            self.index = RankedIndex([f"{label} {text}" for _, _, label, text in self.excerpts])
        hits = [self.excerpts[index] for index in self.index.search(query)]
        return {"results": [
            {"entry_id": f"{entry_id}:{start}", "label": label, "text": text}
            for entry_id, start, label, text in hits
        ]}

    def read(self, entry_id):
        key, separator, offset = entry_id.partition(":")
        if key not in self.entries or (separator and not offset.isascii()) or (
            separator and (not offset.isdecimal() or len(offset) > 12)
        ):
            raise ValueError("Unknown history entry")
        label, content = self.entries[key]
        start = int(offset) if separator else 0
        if start and start >= len(content):
            raise ValueError("Unknown history entry")
        return {"entry_id": entry_id, "label": label, "text": content[start:start + 8000],
                "truncated": start > 0 or len(content) > start + 8000}


def history_entries(turns):
    entries = {}
    for number, (question, answer, result) in enumerate(turns, 1):
        prefix = f"turn-{number}"
        entries[f"{prefix}-question"] = (f"Turn {number} question", question)
        entries[f"{prefix}-answer"] = (f"Turn {number} answer", answer)
        if result.diff:
            entries[f"{prefix}-diff"] = (f"Turn {number} generated diff", result.diff)
        for index, event in enumerate(result.tool_trace, 1):
            if "tool" in event:
                entries[f"{prefix}-tool-{index}"] = (
                    f"Turn {number} tool {event['tool']}",
                    json.dumps(event, ensure_ascii=False),
                )
    return entries
