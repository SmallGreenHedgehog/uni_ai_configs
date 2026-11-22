import json

from application.builders.base_config_builder import BaseConfigBuilder
from application.builders.openhands_hook_script import render_hook_script
from entities import IgnoreEntry, Role, Rule
from utils.filesystem.directories import replace_dir
from utils.yaml.values import quote_value_if_needed


class OpenHandsBuilder(BaseConfigBuilder):
    @property
    def _success_message(self) -> str:
        message = (
            "Built OpenHands config: AGENTS.md, .agents/skills/, "
            ".openhands/hooks.json, .openhands/hooks/block_ignored.py"
        )
        return message

    def _build_roles(self, roles: list[Role]) -> None:
        skills_dir = self._root_dir / ".agents" / "skills"
        replace_dir(skills_dir)
        for role in roles:
            skill_dir = skills_dir / role.slug
            skill_dir.mkdir()
            content = self.__render_skill(role)
            (skill_dir / "SKILL.md").write_text(content, encoding="utf-8")

    @staticmethod
    def __render_skill(role: Role) -> str:
        frontmatter = [
            "---",
            f"name: {quote_value_if_needed(role.slug)}",
            f"description: {quote_value_if_needed(role.description)}",
            "triggers:",
            f"  - {quote_value_if_needed(role.slug)}",
            "---",
            "",
        ]
        body = f"{role.role_definition}\n\n{role.custom_instructions}"
        content = "\n".join(frontmatter) + body + "\n"
        return content

    def _build_rules(self, rules: list[Rule]) -> None:
        sections = [rule.content.rstrip() for rule in rules]
        content = "\n\n".join(sections) + "\n"
        (self._root_dir / "AGENTS.md").write_text(content, encoding="utf-8")

    def _build_ignore(self, ignore_entries: list[IgnoreEntry]) -> None:
        config_dir = self._root_dir / ".openhands"
        hooks_dir = config_dir / "hooks"
        replace_dir(hooks_dir)
        patterns = [entry.pattern for entry in ignore_entries if entry.pattern]
        hooks_data = {
            "pre_tool_use": [
                {
                    "matcher": "*",
                    "hooks": [
                        {
                            "type": "command",
                            "command": "python3 .openhands/hooks/block_ignored.py",
                        }
                    ],
                }
            ]
        }
        hooks_content = json.dumps(hooks_data, indent=2, ensure_ascii=False) + "\n"
        (config_dir / "hooks.json").write_text(hooks_content, encoding="utf-8")
        script = render_hook_script(patterns)
        script_path = hooks_dir / "block_ignored.py"
        script_path.write_text(script, encoding="utf-8")
        script_path.chmod(0o755)
