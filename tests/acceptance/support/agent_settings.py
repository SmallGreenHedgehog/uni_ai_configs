from abc import ABC, abstractmethod
from pathlib import Path

from tests.acceptance.support.clients import CodexConfigFileClient
from tests.acceptance.support.expectations import (
    extract_claude_description,
    extract_roomodes_description,
)
from tests.utils.reflection import get_subclass_by_name


class AgentBuildSettings(ABC):
    @abstractmethod
    def rendered_description(self, workspace: Path) -> str: ...

    @abstractmethod
    def ignore_file_path(self, workspace: Path) -> Path: ...

    def rules_dir(self, workspace: Path) -> Path:
        raise NotImplementedError


class CodexBuildSettings(AgentBuildSettings):
    def __init__(self) -> None:
        self._config_file_client = CodexConfigFileClient()

    def rendered_description(self, workspace: Path) -> str:
        agents = self._config_file_client.read(workspace / ".codex" / "config.toml")
        rendered = agents[0]["description"]
        return rendered

    def ignore_file_path(self, workspace: Path) -> Path:
        path = workspace / ".codexignore"
        return path


class ZooCodeBuildSettings(AgentBuildSettings):
    def rendered_description(self, workspace: Path) -> str:
        content = (workspace / ".roomodes").read_text(encoding="utf-8")
        rendered = extract_roomodes_description(content)
        return rendered

    def ignore_file_path(self, workspace: Path) -> Path:
        path = workspace / ".rooignore"
        return path

    def rules_dir(self, workspace: Path) -> Path:
        rules_dir = workspace / ".roo" / "rules"
        return rules_dir


class ClaudeAgentBuildSettings(AgentBuildSettings):
    def rendered_description(self, workspace: Path) -> str:
        agent_path = next((workspace / ".claude" / "agents").glob("*.md"))
        content = agent_path.read_text(encoding="utf-8")
        rendered = extract_claude_description(content)
        return rendered

    def ignore_file_path(self, workspace: Path) -> Path:
        path = workspace / ".claudeignore"
        return path

    def rules_dir(self, workspace: Path) -> Path:
        rules_dir = workspace / ".claude" / "rules"
        return rules_dir


def get_agent_settings(builder: str) -> AgentBuildSettings:
    settings_class = get_subclass_by_name(AgentBuildSettings, f"{builder}BuildSettings")
    agent_settings = settings_class()
    return agent_settings
