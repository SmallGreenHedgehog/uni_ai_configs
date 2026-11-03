from pathlib import Path

from pytest_bdd import given, parsers, then

from infrastructure.repositories import MarkdownRulesRepository, TextIgnoreRepository
from infrastructure.settings import settings
from tests.acceptance.support.agent_settings import get_agent_settings
from tests.acceptance.support.factories import RoleFactory


@given("исходная конфигурация агентов существует в каталоге конфигурации агентов")
def source_config_exists(
    default_roles, default_rules, default_ignore_entries, yaml_file_client, markdown_file_client, ignore_file_client
) -> None:
    agents_dir = settings.agents_dir
    roles_data = {"roles": [role.model_dump(by_alias=True) for role in default_roles]}
    yaml_file_client.write(agents_dir / "roles.yaml", roles_data)
    for rule in default_rules:
        markdown_file_client.write(agents_dir / "rules" / rule.filename, rule.content)
    ignore_patterns = [entry.pattern for entry in default_ignore_entries]
    ignore_file_client.write(agents_dir / "ignore", ignore_patterns)


@given(parsers.parse("роль с description {raw}"))
def role_with_description(raw: str, yaml_file_client) -> None:
    role = RoleFactory.build(description=raw)
    roles_data = {"roles": [role.model_dump(by_alias=True)]}
    yaml_file_client.write(settings.agents_dir / "roles.yaml", roles_data)


@given("роль с пустым полем description")
def role_with_empty_description(yaml_file_client) -> None:
    role = RoleFactory.build(description="")
    roles_data = {"roles": [role.model_dump(by_alias=True)]}
    yaml_file_client.write(settings.agents_dir / "roles.yaml", roles_data)


@then(parsers.parse("файл конфигурации существует по пути {path}"))
def config_file_exists(workspace: Path, path: str) -> None:
    assert (workspace / path).exists()


@then(parsers.parse("файл существует по пути {path}"))
def file_exists(workspace: Path, path: str) -> None:
    assert (workspace / path).exists()


@then(parsers.parse("каталог существует по пути {path}"))
def directory_exists(workspace: Path, path: str) -> None:
    assert (workspace / path).is_dir()


@then(parsers.parse("итоговое поле description равно {rendered}"))
def description_matches_rendered(workspace: Path, rendered: str) -> None:
    agent_settings = get_agent_settings(settings.builder)
    value = agent_settings.rendered_description(workspace)
    assert value == rendered


@then("итоговое поле description является пустой строкой в кавычках")
def description_is_quoted_empty_string(workspace: Path) -> None:
    agent_settings = get_agent_settings(settings.builder)
    value = agent_settings.rendered_description(workspace)
    assert value == '""'


@then("файл содержит каждый непустой ignore-шаблон на отдельной строке")
def ignore_file_has_patterns(workspace: Path, ignore_file_client) -> None:
    entries = TextIgnoreRepository(settings.agents_dir).get_ignore_entries()
    agent_settings = get_agent_settings(settings.builder)
    path = agent_settings.ignore_file_path(workspace)
    lines = ignore_file_client.read(path)
    assert lines == [entry.pattern for entry in entries]


@then("каждый файл правила сохраняет исходное имя файла и содержимое")
def rule_files_match(workspace: Path) -> None:
    rules = MarkdownRulesRepository(settings.agents_dir).get_rules()
    agent_settings = get_agent_settings(settings.builder)
    rules_dir = agent_settings.rules_dir(workspace)
    for rule in rules:
        content = (rules_dir / rule.filename).read_text(encoding="utf-8")
        assert content == rule.content
