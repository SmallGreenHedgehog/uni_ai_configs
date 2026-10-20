from importlib.resources import files
from pathlib import Path

from application.interfaces.repositories import IgnoreTemplateRepository
from entities import AgentConfigTemplate


class PackageIgnoreTemplateRepository(IgnoreTemplateRepository):
    def get_ignore_templates(self) -> list[AgentConfigTemplate]:
        source = files("templates") / "ignore"
        content = source.read_text(encoding="utf-8")
        template = AgentConfigTemplate(relative_path=Path("ignore"), content=content)
        templates = [template]
        return templates
