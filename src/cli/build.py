from pathlib import Path

from application.builders import CodexBuilder, ZooCodeBuilder
from application.builders.base_config_builder import BaseConfigBuilder
from application.interfaces.repositories import (
    IgnoreRepository,
    RolesRepository,
    RulesRepository,
)
from infrastructure.repositories import (
    MarkdownRulesRepository,
    TextIgnoreRepository,
    YamlRolesRepository,
)
from infrastructure.settings import settings


class BuildCommand:
    @staticmethod
    def run() -> None:
        root_dir = Path.cwd()
        agents_dir = BuildCommand.__resolve_agents_dir(root_dir)
        roles_repository = YamlRolesRepository(agents_dir)
        rules_repository = MarkdownRulesRepository(agents_dir)
        ignore_repository = TextIgnoreRepository(agents_dir)
        builder = BuildCommand.__create_builder(
            root_dir=root_dir,
            roles_repository=roles_repository,
            rules_repository=rules_repository,
            ignore_repository=ignore_repository,
        )
        builder.build()
        message = BuildCommand.__render_success_message()
        print(message)

    @staticmethod
    def __resolve_agents_dir(root_dir: Path) -> Path:
        configured_agents_dir = settings.agents_dir
        if configured_agents_dir.is_absolute():
            agents_dir = configured_agents_dir
        else:
            agents_dir = root_dir / configured_agents_dir
        return agents_dir

    @staticmethod
    def __create_builder(
        root_dir: Path,
        roles_repository: RolesRepository,
        rules_repository: RulesRepository,
        ignore_repository: IgnoreRepository,
    ) -> BaseConfigBuilder:
        builder: BaseConfigBuilder
        if settings.builder == "codex":
            builder = CodexBuilder(
                root_dir=root_dir,
                roles_repository=roles_repository,
                rules_repository=rules_repository,
                ignore_repository=ignore_repository,
            )
        else:
            builder = ZooCodeBuilder(
                root_dir=root_dir,
                roles_repository=roles_repository,
                rules_repository=rules_repository,
                ignore_repository=ignore_repository,
            )
        return builder

    @staticmethod
    def __render_success_message() -> str:
        messages = {
            "codex": "Built Codex config: AGENTS.md, .codex/config.toml, .codexignore",
            "zoocode": "Built Zoo Code config: .roomodes, .roo/rules/, .rooignore",
        }
        message = messages[settings.builder]
        return message
