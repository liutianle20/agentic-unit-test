from pathlib import Path

import numpy as np
import pytest

from unit_agent import retrieval
from unit_agent.workspace import Workspace


def test_repository_chunks_keep_line_ranges_and_skip_generated_files(tmp_path):
    workspace = Workspace(tmp_path)
    lines = [f"line_{number}" for number in range(1, 72)]
    (tmp_path / "sample.py").write_text("\n".join(lines))
    (tmp_path / "binary.md").write_bytes(b"ignore\0this")
    (tmp_path / ".git").mkdir()
    (tmp_path / ".git" / "config.md").write_text("secret")
    (tmp_path / "link.md").symlink_to(Path("sample.py"))
    workspace.stage_tests("tests/test_agent_sample.py", "def test_sample(): pass")
    chunks = retrieval.repository_chunks(workspace)
    assert [(chunk.path, chunk.start, chunk.end) for chunk in chunks] == [
        ("sample.py", 1, 40), ("sample.py", 31, 70), ("sample.py", 61, 71),
    ]
    assert workspace.read_lines("sample.py", 31, 70)["text"] == chunks[1].text
    with pytest.raises(ValueError, match="Symlinks"):
        workspace.read_lines("link.md", 1, 2)
    with pytest.raises(ValueError, match="80 lines"):
        workspace.read_lines("sample.py", 1, 81)


def test_hybrid_ranking_and_keyword_fallback(monkeypatch):
    class Encoder:
        def encode(self, texts, **options):
            assert options == {"normalize_embeddings": True}
            if texts == ["offline"]:
                raise RuntimeError("Embedding inference failed")
            return np.array([[0, 1]] if len(texts) == 1 else [[1, 0], [0, 1]])

    monkeypatch.setattr(retrieval, "load_embeddings", Encoder)
    index = retrieval.RankedIndex(["retry offline", "limit"], hybrid=True)
    assert index.search("retry") == [1, 0]
    assert index.search("offline") == [0]
    assert index.search("retry") == [0]
    assert retrieval.RankedIndex([]).search("retry") == []


def test_history_search_recovers_excerpt_beyond_first_page():
    history = retrieval.HistorySearch({
        "turn-1-tool-1": ("Turn 1 tool read_file", "prefix " * 1800 + " rare_marker"),
    })
    hit, = history.search("rare_marker")["results"]
    assert "rare_marker" in hit["text"]
    assert "rare_marker" in history.read(hit["entry_id"])["text"]
