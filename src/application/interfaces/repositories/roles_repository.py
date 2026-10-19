from abc import ABC, abstractmethod

from entities import Role


class RolesRepository(ABC):
    @abstractmethod
    def get_roles(self) -> list[Role]:
        ...
