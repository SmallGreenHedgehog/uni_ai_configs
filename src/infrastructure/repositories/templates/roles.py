from importlib.resources import files
from pathlib import Path

from application.interfaces.repositories import RolesTemplateRepository
from entities import AgentConfigTemplate


class PackageRolesTemplateRepository(RolesTemplateRepository):
    def get_role_templates(self) -> list[AgentConfigTemplate]:
        source = files("templates") / "roles.yaml"
        content = source.read_text(encoding="utf-8")
        template = AgentConfigTemplate(relative_path=Path("roles.yaml"), content=content)
        templates = [template]
        return templates
