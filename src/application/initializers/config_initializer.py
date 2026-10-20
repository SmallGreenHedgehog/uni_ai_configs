from pathlib import Path

from application.interfaces.repositories import (
    IgnoreTemplateRepository,
    RolesTemplateRepository,
    RulesTemplateRepository,
)
from entities import AgentConfigTemplate


class ConfigInitializer:
    def __init__(
        self,
        agents_dir: Path,
        roles_template_repository: RolesTemplateRepository,
        rules_template_repository: RulesTemplateRepository,
        ignore_template_repository: IgnoreTemplateRepository,
    ) -> None:
        self.__agents_dir = agents_dir
        self.__roles_template_repository = roles_template_repository
        self.__rules_template_repository = rules_template_repository
        self.__ignore_template_repository = ignore_template_repository

    def initialize(self) -> tuple[list[Path], list[Path]]:
        templates = self.__collect_templates()
        created_files: list[Path] = []
        skipped_files: list[Path] = []
        for template in templates:
            target_path = self.__agents_dir / template.relative_path
            if target_path.exists():
                skipped_files.append(target_path)
            else:
                self.__write_template(target_path, template.content)
                created_files.append(target_path)
        return created_files, skipped_files

    def __collect_templates(self) -> list[AgentConfigTemplate]:
        templates = []
        templates.extend(self.__roles_template_repository.get_role_templates())
        templates.extend(self.__rules_template_repository.get_rule_templates())
        templates.extend(self.__ignore_template_repository.get_ignore_templates())
        return templates

    @staticmethod
    def __write_template(target_path: Path, content: str) -> None:
        target_path.parent.mkdir(parents=True, exist_ok=True)
        target_path.write_text(content, encoding="utf-8")
