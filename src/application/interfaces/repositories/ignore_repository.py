from abc import ABC, abstractmethod

from entities import IgnoreEntry


class IgnoreRepository(ABC):
    @abstractmethod
    def get_ignore_entries(self) -> list[IgnoreEntry]:
        ...
