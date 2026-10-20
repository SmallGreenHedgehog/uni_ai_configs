from abc import ABC, abstractmethod
from pathlib import Path

from application.interfaces.repositories import (
    IgnoreRepository,
    RolesRepository,
    RulesRepository,
)
from entities import IgnoreEntry, Role, Rule


class BaseConfigBuilder(ABC):
    def __init__(
        self,
        root_dir: Path,
        roles_repository: RolesRepository,
        rules_repository: RulesRepository,
        ignore_repository: IgnoreRepository,
    ) -> None:
        self._root_dir = root_dir
        self._roles_repository = roles_repository
        self._rules_repository = rules_repository
        self._ignore_repository = ignore_repository

    def build(self) -> str:
        roles = self._roles_repository.get_roles()
        self._build_roles(roles)

        rules = self._rules_repository.get_rules()
        self._build_rules(rules)

        ignore_entries = self._ignore_repository.get_ignore_entries()
        self._build_ignore(ignore_entries)

        message = self._success_message
        return message

    @abstractmethod
    def _build_roles(self, roles: list[Role]) -> None: ...

    @abstractmethod
    def _build_rules(self, rules: list[Rule]) -> None: ...

    @abstractmethod
    def _build_ignore(self, ignore_entries: list[IgnoreEntry]) -> None: ...

    @property
    @abstractmethod
    def _success_message(self) -> str: ...
