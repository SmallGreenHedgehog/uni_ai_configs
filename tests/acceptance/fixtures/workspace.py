from pathlib import Path

import pytest

from infrastructure.settings import settings


@pytest.fixture
def workspace(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    agents_dir = tmp_path / "config" / "agents"
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(settings, "agents_dir", agents_dir)
    monkeypatch.setattr(settings, "builder", "zoocode")
    return tmp_path
