from abc import ABC, abstractmethod

from entities import Rule


class RulesRepository(ABC):
    @abstractmethod
    def get_rules(self) -> list[Rule]:
        ...
