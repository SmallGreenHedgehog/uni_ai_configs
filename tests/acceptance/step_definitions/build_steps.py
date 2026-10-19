import shutil
from pathlib import Path

from pytest_bdd import given, parsers, then, when

from infrastructure.repositories import MarkdownRulesRepository, TextIgnoreRepository, YamlRolesRepository
from infrastructure.settings import settings
from tests.acceptance.support.context import ScenarioState
from tests.acceptance.support.expectations import CodexExpectations, RoomodesExpectations
from tests.acceptance.support.factories import RoleFactory


@given("сборщик настроен на Codex")
def set_codex_builder() -> None:
    settings.builder = "codex"


@given("сборщик настроен на Zoo Code")
def set_zoocode_builder() -> None:
    settings.builder = "zoocode"


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


@given("сгенерированные файлы конфигурации Codex отсутствуют")
def codex_outputs_absent(workspace: Path) -> None:
    shutil.rmtree(workspace / ".codex", ignore_errors=True)
    (workspace / "AGENTS.md").unlink(missing_ok=True)
    (workspace / ".codexignore").unlink(missing_ok=True)


@given("сгенерированные файлы конфигурации Zoo Code отсутствуют")
def zoocode_outputs_absent(workspace: Path) -> None:
    (workspace / ".roomodes").unlink(missing_ok=True)
    shutil.rmtree(workspace / ".roo", ignore_errors=True)
    (workspace / ".rooignore").unlink(missing_ok=True)


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


@given("роль, чьи пользовательские инструкции содержат обратный слеш")
def role_with_backslash_instructions(yaml_file_client) -> None:
    role = RoleFactory.build(custom_instructions='C:\\temp and "quoted"')
    roles_data = {"roles": [role.model_dump(by_alias=True)]}
    yaml_file_client.write(settings.agents_dir / "roles.yaml", roles_data)


@when("сборка конфигурации Codex выполнена")
def build_codex_executed(build_client, scenario_state: ScenarioState) -> None:
    scenario_state.command_output = build_client.run()


@when("сборка конфигурации Zoo Code выполнена")
def build_zoocode_executed(build_client, scenario_state: ScenarioState) -> None:
    scenario_state.command_output = build_client.run()


@then(parsers.parse("файл конфигурации существует по пути {path}"))
def config_file_exists(workspace: Path, path: str) -> None:
    assert (workspace / path).exists()


@then(parsers.parse("файл существует по пути {path}"))
def file_exists(workspace: Path, path: str) -> None:
    assert (workspace / path).exists()


@then("файл содержит одну секцию agents.<slug> для каждой роли из roles.yaml")
def codex_has_section_per_role(workspace: Path, codex_config_file_client) -> None:
    roles = YamlRolesRepository(settings.agents_dir).get_roles()
    agents = codex_config_file_client.read(workspace / ".codex" / "config.toml")
    assert [agent["slug"] for agent in agents] == [role.slug for role in roles]


@then("каждая секция agents.<slug> содержит соответствующее поле description")
def codex_agents_have_description(workspace: Path, codex_config_file_client) -> None:
    roles = YamlRolesRepository(settings.agents_dir).get_roles()
    agents = codex_config_file_client.read(workspace / ".codex" / "config.toml")
    descriptions = {role.slug: role.description for role in roles}
    for agent in agents:
        expected = CodexExpectations.quote_description(descriptions[agent["slug"]])
        assert agent["description"] == expected


@then("каждая секция agents.<slug> содержит соответствующее поле prompt")
def codex_agents_have_prompt(workspace: Path, codex_config_file_client) -> None:
    roles = YamlRolesRepository(settings.agents_dir).get_roles()
    agents = codex_config_file_client.read(workspace / ".codex" / "config.toml")
    prompts = {role.slug: CodexExpectations.render_prompt(role) for role in roles}
    for agent in agents:
        assert agent["prompt"] == prompts[agent["slug"]]


@then(
    "для каждой роли поле prompt содержит определение роли, условия применения и пользовательские инструкции, разделённые пустыми строками"
)
def codex_prompt_combines_sections(workspace: Path, codex_config_file_client) -> None:
    roles = YamlRolesRepository(settings.agents_dir).get_roles()
    agents = codex_config_file_client.read(workspace / ".codex" / "config.toml")
    prompts = {role.slug: CodexExpectations.render_prompt(role) for role in roles}
    for agent in agents:
        assert agent["prompt"] == prompts[agent["slug"]]


@then(parsers.parse("итоговое поле description равно {rendered}"))
def description_matches_rendered(workspace: Path, rendered: str, codex_config_file_client) -> None:
    if settings.builder == "codex":
        agents = codex_config_file_client.read(workspace / ".codex" / "config.toml")
        value = agents[0]["description"]
    else:
        content = (workspace / ".roomodes").read_text(encoding="utf-8")
        value = RoomodesExpectations.read_description(content)
    assert value == rendered


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


@then("файл содержит каждый непустой ignore-шаблон на отдельной строке")
def ignore_file_has_patterns(workspace: Path, ignore_file_client) -> None:
    entries = TextIgnoreRepository(settings.agents_dir).get_ignore_entries()
    if settings.builder == "codex":
        path = workspace / ".codexignore"
    else:
        path = workspace / ".rooignore"
    lines = ignore_file_client.read(path)
    assert lines == [entry.pattern for entry in entries]


@then("вывод команды сообщает об успешной сборке конфигурации Codex")
def codex_success_reported(scenario_state: ScenarioState) -> None:
    assert "Built Codex config" in scenario_state.command_output


@then("вывод команды сообщает об успешной сборке конфигурации Zoo Code")
def zoocode_success_reported(scenario_state: ScenarioState) -> None:
    assert "Built Zoo Code config" in scenario_state.command_output


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
    instruction_lines = RoomodesExpectations.extract_instruction_lines(content)
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


@then("итоговое поле description является пустой строкой в кавычках")
def description_is_quoted_empty_string(workspace: Path) -> None:
    content = (workspace / ".roomodes").read_text(encoding="utf-8")
    value = RoomodesExpectations.read_description(content)
    assert value == '""'


@then("каталог .roo/rules содержит только файлы правил из каталога конфигурации агентов")
def roomodes_rules_dir_matches(workspace: Path) -> None:
    rules = MarkdownRulesRepository(settings.agents_dir).get_rules()
    generated_names = {path.name for path in (workspace / ".roo" / "rules").glob("*")}
    expected_names = {rule.filename for rule in rules}
    assert generated_names == expected_names


@then("каждый файл правила сохраняет исходное имя файла и содержимое")
def roomodes_rule_files_match(workspace: Path) -> None:
    rules = MarkdownRulesRepository(settings.agents_dir).get_rules()
    for rule in rules:
        content = (workspace / ".roo" / "rules" / rule.filename).read_text(encoding="utf-8")
        assert content == rule.content
