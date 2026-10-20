from abc import abstractmethod
from pathlib import Path

from cli.commands.base.base_command import BaseCommand
from infrastructure.settings import settings


class AgentConfigCommand(BaseCommand):
    def _execute(self) -> None:
        root_dir = Path.cwd()
        agents_dir = self.__resolve_agents_dir(root_dir)
        self._execute_for_agents_dir(root_dir, agents_dir)

    @abstractmethod
    def _execute_for_agents_dir(self, root_dir: Path, agents_dir: Path) -> None: ...

    @staticmethod
    def __resolve_agents_dir(root_dir: Path) -> Path:
        configured_agents_dir = settings.agents_dir
        if configured_agents_dir.is_absolute():
            agents_dir = configured_agents_dir
        else:
            agents_dir = root_dir / configured_agents_dir
        return agents_dir
