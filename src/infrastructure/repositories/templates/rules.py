from importlib.resources import files
from pathlib import Path

from application.interfaces.repositories import RulesTemplateRepository
from entities import AgentConfigTemplate


class PackageRulesTemplateRepository(RulesTemplateRepository):
    def get_rule_templates(self) -> list[AgentConfigTemplate]:
        templates_dir = files("templates") / "rules"
        templates: list[AgentConfigTemplate] = []
        for source in sorted(templates_dir.iterdir(), key=lambda item: item.name):
            if source.is_file():
                relative_path = Path("rules") / source.name
                content = source.read_text(encoding="utf-8")
                templates.append(AgentConfigTemplate(relative_path=relative_path, content=content))
        return templates
