import shutil
from pathlib import Path

from pytest_bdd import given, then, when

from infrastructure.repositories import MarkdownRulesRepository, YamlRolesRepository
from infrastructure.settings import settings
from tests.acceptance.support.context import ScenarioState
from tests.acceptance.support.expectations import extract_roomodes_instruction_lines


@given("сборщик настроен на Zoo Code")
def set_zoocode_builder() -> None:
    settings.builder = "ZooCode"


@given("сгенерированные файлы конфигурации Zoo Code отсутствуют")
def zoocode_outputs_absent(workspace: Path) -> None:
    (workspace / ".roomodes").unlink(missing_ok=True)
    shutil.rmtree(workspace / ".roo", ignore_errors=True)
    (workspace / ".rooignore").unlink(missing_ok=True)


@when("сборка конфигурации Zoo Code выполнена")
def build_zoocode_executed(build_client, scenario_state: ScenarioState) -> None:
    scenario_state.command_output = build_client.run()


@then("файл начинается со списка customModes")
def roomodes_starts_with_custom_modes(workspace: Path) -> None:
    content = (workspace / ".roomodes").read_text(encoding="utf-8")
    assert content.splitlines()[0] == "customModes:"


@then("файл содержит одну запись режима для каждой роли из roles.yaml")
def roomodes_has_mode_per_role(workspace: Path, yaml_file_client) -> None:
    roles = YamlRolesRepository(settings.agents_dir).get_roles()
    modes = yaml_file_client.read(workspace / ".roomodes")["customModes"]
    assert [mode["slug"] for mode in modes] == [role.slug for role in roles]


@then("каждая запись режима содержит соответствующие поля slug, name, description, roleDefinition и whenToUse")
def modes_have_metadata(workspace: Path, yaml_file_client) -> None:
    roles = YamlRolesRepository(settings.agents_dir).get_roles()
    modes = yaml_file_client.read(workspace / ".roomodes")["customModes"]
    for role, mode in zip(roles, modes):
        assert mode["slug"] == role.slug
        assert mode["name"] == role.name
        assert mode["description"] == role.description
        assert mode["roleDefinition"] == role.role_definition
        assert mode["whenToUse"] == role.when_to_use


@then("каждая запись режима выводит пользовательские инструкции как литеральный блок с отступом в шесть пробелов")
def modes_instructions_indented(workspace: Path, yaml_file_client) -> None:
    content = (workspace / ".roomodes").read_text(encoding="utf-8")
    modes = yaml_file_client.read(workspace / ".roomodes")["customModes"]
    assert content.count("customInstructions: |-") == len(modes)
    instruction_lines = extract_roomodes_instruction_lines(content)
    assert instruction_lines
    for line in instruction_lines:
        assert line.startswith("      ")
        assert not line.startswith("       ")


@then("пустые строки внутри инструкций сохраняются")
def modes_preserve_empty_lines(workspace: Path, yaml_file_client) -> None:
    roles = YamlRolesRepository(settings.agents_dir).get_roles()
    modes = yaml_file_client.read(workspace / ".roomodes")["customModes"]
    for role, mode in zip(roles, modes):
        assert mode["customInstructions"] == role.custom_instructions


@then("каждая запись режима перечисляет свои группы")
def modes_list_groups(workspace: Path, yaml_file_client) -> None:
    roles = YamlRolesRepository(settings.agents_dir).get_roles()
    modes = yaml_file_client.read(workspace / ".roomodes")["customModes"]
    for role, mode in zip(roles, modes):
        assert mode["groups"] == role.groups


@then("каждая запись режима содержит соответствующее поле source")
def modes_have_source(workspace: Path, yaml_file_client) -> None:
    roles = YamlRolesRepository(settings.agents_dir).get_roles()
    modes = yaml_file_client.read(workspace / ".roomodes")["customModes"]
    for role, mode in zip(roles, modes):
        assert mode["source"] == role.source


@then("каталог .roo/rules содержит только файлы правил из каталога конфигурации агентов")
def roomodes_rules_dir_matches(workspace: Path) -> None:
    rules = MarkdownRulesRepository(settings.agents_dir).get_rules()
    generated_names = {path.name for path in (workspace / ".roo" / "rules").glob("*")}
    expected_names = {rule.filename for rule in rules}
    assert generated_names == expected_names


@then("вывод команды сообщает об успешной сборке конфигурации Zoo Code")
def zoocode_success_reported(scenario_state: ScenarioState) -> None:
    assert "Built Zoo Code config" in scenario_state.command_output
