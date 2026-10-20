import json
import shutil
from pathlib import Path

from application.builders.base_config_builder import BaseConfigBuilder
from entities import IgnoreEntry, Role, Rule


class ZooCodeBuilder(BaseConfigBuilder):
    @property
    def _success_message(self) -> str:
        message = "Built Zoo Code config: .roomodes, .roo/rules/, .rooignore"
        return message

    def _build_roles(self, roles: list[Role]) -> None:
        lines = ["customModes:"]
        for role in roles:
            lines.extend(self.__render_role(role))
        rendered = "\n".join(lines) + "\n"
        (self._root_dir / ".roomodes").write_text(rendered, encoding="utf-8")

    def __render_role(self, role: Role) -> list[str]:
        lines = [
            f"  - slug: {role.slug}",
            f"    name: {role.name}",
            f"    description: {self.__escape_with_quotes_if_needed(role.description)}",
            f"    roleDefinition: {self.__escape_with_quotes_if_needed(role.role_definition)}",
            f"    whenToUse: {self.__escape_with_quotes_if_needed(role.when_to_use)}",
            "    customInstructions: |-",
        ]
        lines.extend(self.__render_instructions(role.custom_instructions))
        lines.append("    groups:")
        lines.extend(f"      - {group}" for group in role.groups)
        lines.append(f"    source: {role.source}")
        return lines

    @staticmethod
    def __escape_with_quotes_if_needed(value: str) -> str:
        unsafe_start = set("!&*{}[],#|>@`\"'-?:")
        needs_quoting = not value or ": " in value or " #" in value or value[0] in unsafe_start
        rendered = json.dumps(value, ensure_ascii=False) if needs_quoting else value
        return rendered

    @staticmethod
    def __render_instructions(value: str) -> list[str]:
        lines = []
        for line in value.splitlines():
            if line:
                lines.append(f"      {line}")
            else:
                lines.append("")
        return lines

    def _build_rules(self, rules: list[Rule]) -> None:
        rules_dir = self._root_dir / ".roo" / "rules"
        self.__replace_dir(rules_dir)
        for rule in rules:
            (rules_dir / rule.filename).write_text(rule.content, encoding="utf-8")

    @staticmethod
    def __replace_dir(path: Path) -> None:
        if path.exists():
            shutil.rmtree(path)
        path.mkdir(parents=True)

    def _build_ignore(self, ignore_entries: list[IgnoreEntry]) -> None:
        content = "".join(f"{entry.pattern}\n" for entry in ignore_entries)
        (self._root_dir / ".rooignore").write_text(content, encoding="utf-8")
