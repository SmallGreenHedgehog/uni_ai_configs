import shutil
from pathlib import Path

from pytest_bdd import given, then, when

from infrastructure.repositories import TextIgnoreRepository, YamlRolesRepository
from infrastructure.settings import settings
from tests.acceptance.support.context import ScenarioState
from tests.acceptance.support.expectations import (
    build_openhands_subagent_body,
    extract_openhands_hook_commands,
)


@given("сборщик настроен на OpenHands")
def set_openhands_builder() -> None:
    settings.builder = "OpenHands"


@given("сгенерированные файлы конфигурации OpenHands отсутствуют")
def openhands_outputs_absent(workspace: Path) -> None:
    shutil.rmtree(workspace / ".openhands", ignore_errors=True)
    (workspace / "AGENTS.md").unlink(missing_ok=True)


@when("сборка конфигурации OpenHands выполнена")
def build_openhands_executed(build_client, scenario_state: ScenarioState) -> None:
    scenario_state.command_output = build_client.run()


@then("каталог .openhands/agents содержит один файл субагента для каждой роли из roles.yaml")
def openhands_agents_have_file_per_role(workspace: Path) -> None:
    roles = YamlRolesRepository(settings.agents_dir).get_roles()
    generated_names = {
        path.stem for path in (workspace / ".openhands" / "agents").glob("*.md")
    }
    expected_names = {role.slug for role in roles}
    assert generated_names == expected_names


@then("каждый файл субагента OpenHands называется по slug соответствующей роли")
def openhands_agent_filenames_follow_slugs(workspace: Path) -> None:
    openhands_agents_have_file_per_role(workspace)


@then("каждый файл субагента OpenHands содержит frontmatter с полями name и description")
def openhands_agents_have_metadata(workspace: Path, openhands_subagent_file_client) -> None:
    roles = YamlRolesRepository(settings.agents_dir).get_roles()
    for role in roles:
        subagent = openhands_subagent_file_client.read(
            workspace / ".openhands" / "agents" / f"{role.slug}.md"
        )
        assert "name" in subagent
        assert "description" in subagent


@then("значение поля name каждого субагента OpenHands соответствует slug роли")
def openhands_agents_have_slug_names(
    workspace: Path, openhands_subagent_file_client
) -> None:
    roles = YamlRolesRepository(settings.agents_dir).get_roles()
    for role in roles:
        subagent = openhands_subagent_file_client.read(
            workspace / ".openhands" / "agents" / f"{role.slug}.md"
        )
        assert subagent["name"] == role.slug


@then("значение поля description каждого субагента OpenHands соответствует описанию роли")
def openhands_agents_have_descriptions(
    workspace: Path, openhands_subagent_file_client
) -> None:
    roles = YamlRolesRepository(settings.agents_dir).get_roles()
    for role in roles:
        subagent = openhands_subagent_file_client.read(
            workspace / ".openhands" / "agents" / f"{role.slug}.md"
        )
        assert subagent["description"] == role.description


@then(
    "для каждой роли тело файла субагента OpenHands содержит определение роли, "
    "условия применения и пользовательские инструкции, разделённые пустыми строками"
)
def openhands_agents_have_body(
    workspace: Path, openhands_subagent_file_client
) -> None:
    roles = YamlRolesRepository(settings.agents_dir).get_roles()
    for role in roles:
        subagent = openhands_subagent_file_client.read(
            workspace / ".openhands" / "agents" / f"{role.slug}.md"
        )
        assert subagent["body"] == build_openhands_subagent_body(role)


@then(
    "файл .openhands/hooks.json содержит pre_tool_use hook, "
    "запрещающий доступ к игнорируемым путям"
)
def openhands_hooks_have_pre_tool_use(workspace: Path, json_file_client) -> None:
    hooks_data = json_file_client.read(workspace / ".openhands" / "hooks.json")
    pre_tool_use = hooks_data.get("pre_tool_use", [])
    assert pre_tool_use
    commands = extract_openhands_hook_commands(hooks_data)
    assert commands


@then("pre_tool_use hook содержит каждый непустой ignore-шаблон")
def openhands_hooks_contain_ignore_patterns(workspace: Path, json_file_client) -> None:
    entries = TextIgnoreRepository(settings.agents_dir).get_ignore_entries()
    hooks_data = json_file_client.read(workspace / ".openhands" / "hooks.json")
    commands = extract_openhands_hook_commands(hooks_data)
    rendered = "\n".join(commands)
    for entry in entries:
        assert entry.pattern in rendered


@then("вывод команды сообщает об успешной сборке конфигурации OpenHands")
def openhands_success_reported(scenario_state: ScenarioState) -> None:
    assert "Built OpenHands config" in scenario_state.command_output
