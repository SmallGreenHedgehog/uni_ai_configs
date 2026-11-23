import json

from application.builders.base_config_builder import BaseConfigBuilder
from entities import IgnoreEntry, Role, Rule
from utils.filesystem.directories import replace_dir
from utils.yaml.values import quote_value_if_needed


class OpenHandsBuilder(BaseConfigBuilder):
    __full_permission_tool_names = ("terminal", "file_editor", "task_tracker")

    @property
    def _success_message(self) -> str:
        message = "Built OpenHands config: .openhands/agents/, AGENTS.md, .openhands/hooks.json"
        return message

    def _build_roles(self, roles: list[Role]) -> None:
        agents_dir = self._root_dir / ".openhands" / "agents"
        replace_dir(agents_dir)
        for role in roles:
            content = self.__render_agent(role)
            (agents_dir / f"{role.slug}.md").write_text(content, encoding="utf-8")

    @staticmethod
    def __render_agent(role: Role) -> str:
        tool_lines = [f"  - {tool_name}" for tool_name in OpenHandsBuilder.__full_permission_tool_names]
        frontmatter = [
            "---",
            f"name: {role.slug}",
            f"description: {quote_value_if_needed(role.description)}",
            "tools:",
            *tool_lines,
            "---",
            "",
        ]
        body = f"{role.role_definition}\n\n{role.when_to_use}\n\n{role.custom_instructions}"
        content = "\n".join(frontmatter) + body + "\n"
        return content

    def _build_rules(self, rules: list[Rule]) -> None:
        sections = [rule.content.rstrip() for rule in rules]
        content = "\n\n".join(sections) + "\n"
        (self._root_dir / "AGENTS.md").write_text(content, encoding="utf-8")

    def _build_ignore(self, ignore_entries: list[IgnoreEntry]) -> None:
        hooks = {
            "pre_tool_use": [
                {
                    "matcher": "*",
                    "hooks": [
                        {
                            "type": "command",
                            "command": self.__render_ignore_hook(ignore_entries),
                        }
                    ],
                }
            ]
        }
        content = json.dumps(hooks, indent=2) + "\n"
        hooks_path = self._root_dir / ".openhands" / "hooks.json"
        hooks_path.parent.mkdir(parents=True, exist_ok=True)
        hooks_path.write_text(content, encoding="utf-8")

    @staticmethod
    def __render_ignore_hook(ignore_entries: list[IgnoreEntry]) -> str:
        patterns = [entry.pattern for entry in ignore_entries]
        patterns_literal = json.dumps(patterns)
        command_parts = [
            "python3 -c '",
            "import json,sys;",
            "event=json.load(sys.stdin);",
            'data=event.get("tool_input") or {};',
            f"patterns={patterns_literal};",
            "text=json.dumps(data);",
            "denied=[p for p in patterns if p in text];",
            'print(json.dumps({"decision":"deny","reason":'
            '"ignored path: "+",".join(denied)} if denied else '
            '{"decision":"allow"}));',
            "'",
        ]
        command = "".join(command_parts)
        return command
