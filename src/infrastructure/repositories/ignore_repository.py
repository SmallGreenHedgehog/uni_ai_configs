from pathlib import Path

from application.interfaces.repositories import IgnoreRepository
from entities import IgnoreEntry


class TextIgnoreRepository(IgnoreRepository):
    def __init__(self, agents_dir: Path) -> None:
        self._ignore_path = agents_dir / "ignore"

    def get_ignore_entries(self) -> list[IgnoreEntry]:
        content = self._ignore_path.read_text(encoding="utf-8")
        ignore_entries = [IgnoreEntry(pattern=line) for line in content.splitlines() if line]
        return ignore_entries
