from pathlib import Path

import yaml
from pydantic import TypeAdapter

from application.interfaces.repositories import RolesRepository
from entities import Role


class YamlRolesRepository(RolesRepository):
    def __init__(self, agents_dir: Path) -> None:
        self._roles_path = agents_dir / "roles.yaml"

    def get_roles(self) -> list[Role]:
        raw = yaml.safe_load(self._roles_path.read_text(encoding="utf-8"))
        roles = TypeAdapter(list[Role]).validate_python(raw["roles"])
        return roles
