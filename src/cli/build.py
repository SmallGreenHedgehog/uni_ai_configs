from pathlib import Path

import application.builders as builders
from application.builders.base_config_builder import BaseConfigBuilder
from application.interfaces.repositories import (
    IgnoreRepository,
    RolesRepository,
    RulesRepository,
)
from cli.agent_config_command import AgentConfigCommand
from infrastructure.repositories import (
    MarkdownRulesRepository,
    TextIgnoreRepository,
    YamlRolesRepository,
)
from infrastructure.settings import settings


class BuildCommand(AgentConfigCommand):
    @classmethod
    def _execute_for_agents_dir(cls, root_dir: Path, agents_dir: Path) -> None:
        roles_repository = YamlRolesRepository(agents_dir)
        rules_repository = MarkdownRulesRepository(agents_dir)
        ignore_repository = TextIgnoreRepository(agents_dir)
        builder = cls.__create_builder(
            root_dir=root_dir,
            roles_repository=roles_repository,
            rules_repository=rules_repository,
            ignore_repository=ignore_repository,
        )
        message = builder.build()
        print(message)

    @staticmethod
    def __create_builder(
        root_dir: Path,
        roles_repository: RolesRepository,
        rules_repository: RulesRepository,
        ignore_repository: IgnoreRepository,
    ) -> BaseConfigBuilder:
        builder_class = getattr(builders, f"{settings.builder}Builder")
        builder = builder_class(
            root_dir=root_dir,
            roles_repository=roles_repository,
            rules_repository=rules_repository,
            ignore_repository=ignore_repository,
        )
        return builder
