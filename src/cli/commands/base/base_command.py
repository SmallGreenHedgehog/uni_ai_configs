from abc import ABC, abstractmethod


class BaseCommand(ABC):
    @property
    @abstractmethod
    def name(self) -> str: ...

    @property
    @abstractmethod
    def help_text(self) -> str: ...

    def run(self) -> None:
        self._execute()

    @abstractmethod
    def _execute(self) -> None: ...
