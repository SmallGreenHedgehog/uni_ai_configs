import json

from application.builders.base_config_builder import BaseConfigBuilder
from entities import IgnoreEntry, Role, Rule
from utils.filesystem.directories import replace_dir
from utils.yaml.values import quote_value_if_needed


class OpenHandsBuilder(BaseConfigBuilder):
    _CONFIG_DIR = ".openhands"
    _SKILLS_DIR = "skills"
    _HOOKS_DIR = "hooks"
    _HOOKS_FILE = "hooks.json"
    _HOOK_SCRIPT_FILE = "block_ignored.py"
    _HOOK_COMMAND = "python3 .openhands/hooks/block_ignored.py"
    _HOOK_FILE_MODE = 0o755
    _IGNORED_PATTERNS_PLACEHOLDER = "__IGNORED_PATTERNS__"
    _HOOK_SCRIPT_TEMPLATE = """#!/usr/bin/env python3
import fnmatch
import json
import sys

IGNORED_PATTERNS = __IGNORED_PATTERNS__


def normalize(value):
    text = value.strip().strip("\\"'")
    text = text.replace("\\\\", "/")
    while text.startswith("./"):
        text = text[2:]
    return text.rstrip("/")


def collect_strings(data):
    values = []
    if isinstance(data, dict):
        for item in data.values():
            values.extend(collect_strings(item))
    elif isinstance(data, list):
        for item in data:
            values.extend(collect_strings(item))
    elif isinstance(data, str):
        values.append(data)
    return values


def matches_pattern(value, pattern):
    candidates = [value]
    candidates.extend(value.split("/"))
    matched = any(fnmatch.fnmatch(candidate, pattern) for candidate in candidates)
    return matched


def find_match(values, patterns):
    matched = None
    for pattern in patterns:
        negated = pattern.startswith("!")
        raw_pattern = pattern[1:] if negated else pattern
        clean_pattern = normalize(raw_pattern)
        if not clean_pattern:
            continue
        for value in values:
            if matches_pattern(value, clean_pattern):
                matched = None if negated else (value, pattern)
                break
    return matched


def main():
    try:
        payload = json.loads(sys.stdin.read())
    except ValueError:
        return 0
    values = []
    for string in collect_strings(payload):
        normalized = normalize(string)
        values.append(normalized)
        for token in normalized.split():
            values.append(normalize(token))
    matched = find_match(values, IGNORED_PATTERNS)
    if matched is not None:
        value, pattern = matched
        print(f'Access denied: "{value}" matches ignore pattern "{pattern}"', file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
"""

    @property
    def _success_message(self) -> str:
        message = (
            "Built OpenHands config: AGENTS.md, .openhands/skills/, "
            ".openhands/hooks.json, .openhands/hooks/block_ignored.py"
        )
        return message

    def _build_roles(self, roles: list[Role]) -> None:
        skills_dir = self._root_dir / self._CONFIG_DIR / self._SKILLS_DIR
        replace_dir(skills_dir)
        for role in roles:
            content = self.__render_skill(role)
            (skills_dir / f"{role.slug}.md").write_text(content, encoding="utf-8")

    @staticmethod
    def __render_skill(role: Role) -> str:
        frontmatter = [
            "---",
            f"name: {quote_value_if_needed(role.slug)}",
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
        config_dir = self._root_dir / self._CONFIG_DIR
        hooks_dir = config_dir / self._HOOKS_DIR
        replace_dir(hooks_dir)
        patterns = [entry.pattern for entry in ignore_entries if entry.pattern]
        hooks_data = self.__render_hooks_data()
        hooks_content = json.dumps(hooks_data, indent=2, ensure_ascii=False) + "\n"
        (config_dir / self._HOOKS_FILE).write_text(hooks_content, encoding="utf-8")
        script = self.__render_hook_script(patterns)
        script_path = hooks_dir / self._HOOK_SCRIPT_FILE
        script_path.write_text(script, encoding="utf-8")
        script_path.chmod(self._HOOK_FILE_MODE)

    @classmethod
    def __render_hooks_data(cls) -> dict:
        hooks_data = {
            "hooks": {
                "pre_tool_use": [
                    {
                        "matcher": "*",
                        "hooks": [
                            {
                                "type": "command",
                                "command": cls._HOOK_COMMAND,
                            }
                        ],
                    }
                ]
            }
        }
        return hooks_data

    @classmethod
    def __render_hook_script(cls, patterns: list[str]) -> str:
        rendered_patterns = json.dumps(patterns, ensure_ascii=False)
        script = cls._HOOK_SCRIPT_TEMPLATE.replace(cls._IGNORED_PATTERNS_PLACEHOLDER, rendered_patterns)
        return script
