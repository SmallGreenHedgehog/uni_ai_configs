import shutil
from pathlib import Path

from pytest_bdd import given, then, when

from infrastructure.repositories import MarkdownRulesRepository, YamlRolesRepository
from infrastructure.settings import settings
from tests.acceptance.support.context import ScenarioState
from tests.acceptance.support.expectations import build_claude_agent_body


@given("сборщик настроен на Claude Agent")
def set_claude_agent_builder() -> None:
    settings.builder = "ClaudeAgent"


@given("сгенерированные файлы конфигурации Claude Agent отсутствуют")
def claude_agent_outputs_absent(workspace: Path) -> None:
    shutil.rmtree(workspace / ".claude", ignore_errors=True)
    (workspace / ".claudeignore").unlink(missing_ok=True)


@when("сборка конфигурации Claude Agent выполнена")
def build_claude_agent_executed(build_client, scenario_state: ScenarioState) -> None:
    scenario_state.command_output = build_client.run()


@then("каталог содержит один файл агента для каждой роли из roles.yaml")
def claude_agents_have_file_per_role(workspace: Path) -> None:
    roles = YamlRolesRepository(settings.agents_dir).get_roles()
    generated_slugs = {path.stem for path in (workspace / ".claude" / "agents").glob("*.md")}
    assert generated_slugs == {role.slug for role in roles}


@then("каждый файл агента содержит соответствующие поля name и description")
def claude_agents_have_metadata(workspace: Path, claude_agent_config_file_client) -> None:
    roles = YamlRolesRepository(settings.agents_dir).get_roles()
    for role in roles:
        agent = claude_agent_config_file_client.read(workspace / ".claude" / "agents" / f"{role.slug}.md")
        assert agent["name"] == role.slug
        assert agent["description"] == role.description


@then(
    "для каждой роли тело файла агента содержит определение роли, условия применения и "
    "пользовательские инструкции, разделённые пустыми строками"
)
def claude_agents_have_body(workspace: Path, claude_agent_config_file_client) -> None:
    roles = YamlRolesRepository(settings.agents_dir).get_roles()
    for role in roles:
        agent = claude_agent_config_file_client.read(workspace / ".claude" / "agents" / f"{role.slug}.md")
        assert agent["body"] == build_claude_agent_body(role)


@then("каталог .claude/rules содержит только файлы правил из каталога конфигурации агентов")
def claude_rules_dir_matches(workspace: Path) -> None:
    rules = MarkdownRulesRepository(settings.agents_dir).get_rules()
    generated_names = {path.name for path in (workspace / ".claude" / "rules").glob("*")}
    expected_names = {rule.filename for rule in rules}
    assert generated_names == expected_names


@then("вывод команды сообщает об успешной сборке конфигурации Claude Agent")
def claude_agent_success_reported(scenario_state: ScenarioState) -> None:
    assert "Built Claude Agent config" in scenario_state.command_output
