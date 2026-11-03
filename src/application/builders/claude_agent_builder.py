from application.builders.base_config_builder import BaseConfigBuilder
from entities import IgnoreEntry, Role, Rule
from utils.filesystem.directories import replace_dir
from utils.yaml.values import quote_value_if_needed


class ClaudeAgentBuilder(BaseConfigBuilder):
    @property
    def _success_message(self) -> str:
        message = "Built Claude Agent config: .claude/agents/, .claude/rules/, .claudeignore"
        return message

    def _build_roles(self, roles: list[Role]) -> None:
        agents_dir = self._root_dir / ".claude" / "agents"
        replace_dir(agents_dir)
        for role in roles:
            content = self.__render_agent(role)
            (agents_dir / f"{role.slug}.md").write_text(content, encoding="utf-8")

    @staticmethod
    def __render_agent(role: Role) -> str:
        frontmatter = [
            "---",
            f"name: {role.slug}",
            f"description: {quote_value_if_needed(role.description)}",
            "---",
            "",
        ]
        body = f"{role.role_definition}\n\n{role.when_to_use}\n\n{role.custom_instructions}"
        content = "\n".join(frontmatter) + body + "\n"
        return content

    def _build_rules(self, rules: list[Rule]) -> None:
        rules_dir = self._root_dir / ".claude" / "rules"
        replace_dir(rules_dir)
        for rule in rules:
            (rules_dir / rule.filename).write_text(rule.content, encoding="utf-8")

    def _build_ignore(self, ignore_entries: list[IgnoreEntry]) -> None:
        content = "".join(f"{entry.pattern}\n" for entry in ignore_entries)
        (self._root_dir / ".claudeignore").write_text(content, encoding="utf-8")
