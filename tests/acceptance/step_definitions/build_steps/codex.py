import shutil
from pathlib import Path

from pytest_bdd import given, parsers, then, when

from infrastructure.repositories import MarkdownRulesRepository, YamlRolesRepository
from infrastructure.settings import settings
from tests.acceptance.support.context import ScenarioState
from tests.acceptance.support.expectations import build_codex_prompt
from tests.acceptance.support.factories import RoleFactory


@given("сборщик настроен на Codex")
def set_codex_builder() -> None:
    settings.builder = "Codex"


@given("сгенерированные файлы конфигурации Codex отсутствуют")
def codex_outputs_absent(workspace: Path) -> None:
    shutil.rmtree(workspace / ".codex", ignore_errors=True)
    (workspace / "AGENTS.md").unlink(missing_ok=True)
    (workspace / ".codexignore").unlink(missing_ok=True)


@given("роль, чьи пользовательские инструкции содержат обратный слеш")
def role_with_backslash_instructions(yaml_file_client) -> None:
    role = RoleFactory.build(custom_instructions='C:\\temp and "quoted"')
    roles_data = {"roles": [role.model_dump(by_alias=True)]}
    yaml_file_client.write(settings.agents_dir / "roles.yaml", roles_data)


@when("сборка конфигурации Codex выполнена")
def build_codex_executed(build_client, scenario_state: ScenarioState) -> None:
    scenario_state.command_output = build_client.run()


@then(parsers.re(r"файл содержит одну секцию agents\.<slug> для каждой роли из roles\.yaml"))
def codex_has_section_per_role(workspace: Path, codex_config_file_client) -> None:
    roles = YamlRolesRepository(settings.agents_dir).get_roles()
    agents = codex_config_file_client.read(workspace / ".codex" / "config.toml")
    assert [agent["slug"] for agent in agents] == [role.slug for role in roles]


@then(parsers.re(r"каждая секция agents\.<slug> содержит соответствующее поле description"))
def codex_agents_have_description(workspace: Path, codex_config_file_client) -> None:
    roles = YamlRolesRepository(settings.agents_dir).get_roles()
    agents = codex_config_file_client.read(workspace / ".codex" / "config.toml")
    descriptions = {role.slug: role.description for role in roles}
    for agent in agents:
        description = descriptions[agent["slug"]]
        expected = '"' + description.replace("\\", "\\\\").replace('"', '\\"') + '"'
        assert agent["description"] == expected


@then(parsers.re(r"каждая секция agents\.<slug> содержит соответствующее поле prompt"))
def codex_agents_have_prompt(workspace: Path, codex_config_file_client) -> None:
    roles = YamlRolesRepository(settings.agents_dir).get_roles()
    agents = codex_config_file_client.read(workspace / ".codex" / "config.toml")
    prompts = {role.slug: build_codex_prompt(role) for role in roles}
    for agent in agents:
        assert agent["prompt"] == prompts[agent["slug"]]


@then(
    "для каждой роли поле prompt содержит определение роли, условия применения и пользовательские инструкции, "
    "разделённые пустыми строками"
)
def codex_prompt_combines_sections(workspace: Path, codex_config_file_client) -> None:
    codex_agents_have_prompt(workspace, codex_config_file_client)


@then("поле prompt экранирует обратный слеш как удвоенный обратный слеш")
def codex_prompt_escapes_backslash(workspace: Path, codex_config_file_client) -> None:
    agents = codex_config_file_client.read(workspace / ".codex" / "config.toml")
    prompt = agents[0]["prompt"]
    assert "C:\\\\temp" in prompt


@then("поле prompt оставляет двойные кавычки без изменений")
def codex_prompt_keeps_quotes(workspace: Path, codex_config_file_client) -> None:
    agents = codex_config_file_client.read(workspace / ".codex" / "config.toml")
    prompt = agents[0]["prompt"]
    assert '"quoted"' in prompt
    assert '\\"' not in prompt


@then("файл содержит все содержимые правила, объединённые пустой строкой, с завершающим переводом строки")
def codex_rules_joined(workspace: Path, markdown_file_client) -> None:
    rules = MarkdownRulesRepository(settings.agents_dir).get_rules()
    expected = "\n\n".join(rule.content.rstrip() for rule in rules) + "\n"
    content = markdown_file_client.read(workspace / "AGENTS.md")
    assert content == expected


@then("содержимое правил в AGENTS.md идёт в алфавитном порядке имён исходных файлов")
def codex_rules_alphabetical(workspace: Path, markdown_file_client) -> None:
    rules = MarkdownRulesRepository(settings.agents_dir).get_rules()
    content = markdown_file_client.read(workspace / "AGENTS.md")
    positions = [content.index(rule.content.rstrip()) for rule in rules]
    assert positions == sorted(positions)


@then("вывод команды сообщает об успешной сборке конфигурации Codex")
def codex_success_reported(scenario_state: ScenarioState) -> None:
    assert "Built Codex config" in scenario_state.command_output
