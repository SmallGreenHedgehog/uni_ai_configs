from pathlib import Path

from application.builders import ZooCodeBuilder
from infrastructure.repositories import (
    MarkdownRulesRepository,
    TextIgnoreRepository,
    YamlRolesRepository,
)
from infrastructure.settings import settings


def main() -> None:
    root_dir = Path.cwd()
    configured_agents_dir = settings.agents_dir
    if configured_agents_dir.is_absolute():
        agents_dir = configured_agents_dir
    else:
        agents_dir = root_dir / configured_agents_dir
    builder = ZooCodeBuilder(
        root_dir=root_dir,
        roles_repository=YamlRolesRepository(agents_dir),
        rules_repository=MarkdownRulesRepository(agents_dir),
        ignore_repository=TextIgnoreRepository(agents_dir),
    )
    builder.build()
    print("Built Zoo Code config: .roomodes, .roo/rules/, .rooignore")


if __name__ == "__main__":
    main()
