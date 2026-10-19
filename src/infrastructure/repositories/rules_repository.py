from pathlib import Path

from application.interfaces.repositories import RulesRepository
from entities import Rule


class MarkdownRulesRepository(RulesRepository):
    def __init__(self, agents_dir: Path) -> None:
        self._rules_dir = agents_dir / "rules"

    def get_rules(self) -> list[Rule]:
        rules = [
            Rule(filename=path.name, content=path.read_text(encoding="utf-8"))
            for path in sorted(self._rules_dir.glob("*.md"))
        ]
        return rules
