from abc import ABC, abstractmethod


class BaseCommand(ABC):
    @classmethod
    def run(cls) -> None:
        cls._execute()

    @classmethod
    @abstractmethod
    def _execute(cls) -> None: ...
