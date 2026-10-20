from pathlib import Path

from application.initializers import ConfigInitializer
from cli.agent_config_command import AgentConfigCommand
from infrastructure.repositories import (
    PackageIgnoreTemplateRepository,
    PackageRolesTemplateRepository,
    PackageRulesTemplateRepository,
)


class InitCommand(AgentConfigCommand):
    @classmethod
    def _execute_for_agents_dir(cls, root_dir: Path, agents_dir: Path) -> None:
        roles_template_repository = PackageRolesTemplateRepository()
        rules_template_repository = PackageRulesTemplateRepository()
        ignore_template_repository = PackageIgnoreTemplateRepository()
        initializer = ConfigInitializer(
            agents_dir=agents_dir,
            roles_template_repository=roles_template_repository,
            rules_template_repository=rules_template_repository,
            ignore_template_repository=ignore_template_repository,
        )
        created_files, skipped_files = initializer.initialize()
        report = cls.__render_report(created_files, skipped_files)
        print(report)

    @staticmethod
    def __render_report(created_files: list[Path], skipped_files: list[Path]) -> str:
        lines: list[str] = []
        if created_files:
            lines.append("Initialized agent configs:")
            lines.extend(f"- {path}" for path in created_files)
        if skipped_files:
            lines.append("Skipped existing agent configs:")
            lines.extend(f"- {path}" for path in skipped_files)
        if not lines:
            lines.append("No agent configs to initialize.")
        report = "\n".join(lines)
        return report
