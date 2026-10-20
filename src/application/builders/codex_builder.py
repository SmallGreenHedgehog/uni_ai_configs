from application.builders.base_config_builder import BaseConfigBuilder
from entities import IgnoreEntry, Role, Rule


class CodexBuilder(BaseConfigBuilder):
    @property
    def _success_message(self) -> str:
        message = "Built Codex config: AGENTS.md, .codex/config.toml, .codexignore"
        return message

    def _build_roles(self, roles: list[Role]) -> None:
        config_dir = self._root_dir / ".codex"
        config_dir.mkdir(parents=True, exist_ok=True)
        rendered_agents: list[str] = []
        for role in roles:
            rendered_agents.extend(self.__render_agent(role))
        content = "\n".join(rendered_agents) + "\n"
        (config_dir / "config.toml").write_text(content, encoding="utf-8")

    def __render_agent(self, role: Role) -> list[str]:
        prompt = f"{role.role_definition}\n\n{role.when_to_use}\n\n{role.custom_instructions}"
        lines = [
            f"[agents.{role.slug}]",
            f"description = {self.__render_toml_string(role.description)}",
            f"prompt = {self.__render_toml_multiline_string(prompt)}",
            "",
        ]
        return lines

    @staticmethod
    def __render_toml_string(value: str) -> str:
        escaped = value.replace("\\", "\\\\").replace('"', '\\"')
        return f'"{escaped}"'

    @staticmethod
    def __render_toml_multiline_string(value: str) -> str:
        escaped = value.replace("\\", "\\\\")
        return f'"""{escaped}"""'

    def _build_rules(self, rules: list[Rule]) -> None:
        sections = [rule.content.rstrip() for rule in rules]
        content = "\n\n".join(sections) + "\n"
        (self._root_dir / "AGENTS.md").write_text(content, encoding="utf-8")

    def _build_ignore(self, ignore_entries: list[IgnoreEntry]) -> None:
        content = "".join(f"{entry.pattern}\n" for entry in ignore_entries)
        (self._root_dir / ".codexignore").write_text(content, encoding="utf-8")
