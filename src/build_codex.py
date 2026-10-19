from pathlib import Path

from application.builders import CodexBuilder
from infrastructure.repositories import (
    MarkdownRulesRepository,
    TextIgnoreRepository,
    YamlRolesRepository,
)
from infrastructure.settings import settings


def main() -> None:
    root_dir = Path(__file__).resolve().parents[1]
    configured_agents_dir = settings.agents_dir
    if configured_agents_dir.is_absolute():
        agents_dir = configured_agents_dir
    else:
        agents_dir = root_dir / configured_agents_dir
    builder = CodexBuilder(
        root_dir=root_dir,
        roles_repository=YamlRolesRepository(agents_dir),
        rules_repository=MarkdownRulesRepository(agents_dir),
        ignore_repository=TextIgnoreRepository(agents_dir),
    )
    builder.build()
    print("Built Codex config: AGENTS.md, .codex/config.toml, .codexignore")


if __name__ == "__main__":
    main()
