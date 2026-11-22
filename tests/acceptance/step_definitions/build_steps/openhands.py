import os
import shutil
from pathlib import Path

from pytest_bdd import given, parsers, then, when

from infrastructure.repositories import YamlRolesRepository
from infrastructure.settings import settings
from tests.acceptance.support.context import ScenarioState
from tests.acceptance.support.expectations import build_openhands_skill_body


@given("сборщик настроен на OpenHands")
def set_openhands_builder() -> None:
    settings.builder = "OpenHands"


@given("сгенерированные файлы конфигурации OpenHands отсутствуют")
def openhands_outputs_absent(workspace: Path) -> None:
    shutil.rmtree(workspace / ".openhands", ignore_errors=True)
    shutil.rmtree(workspace / ".agents", ignore_errors=True)
    (workspace / "AGENTS.md").unlink(missing_ok=True)


@given("ignore-записи содержат отрицание для .env.example")
def ignore_entries_with_negation(ignore_file_client) -> None:
    patterns = [".env", ".env.*", "!.env.example"]
    ignore_file_client.write(settings.agents_dir / "ignore", patterns)


@given("в каталоге .agents/skills существует устаревший навык stale")
def stale_skill_exists(workspace: Path) -> None:
    stale_path = workspace / ".agents" / "skills" / "stale" / "SKILL.md"
    stale_path.parent.mkdir(parents=True, exist_ok=True)
    stale_path.write_text("stale", encoding="utf-8")


@when("сборка конфигурации OpenHands выполнена")
def build_openhands_executed(build_client, scenario_state: ScenarioState) -> None:
    scenario_state.command_output = build_client.run()


@when(parsers.parse("хук получает нагрузку доступа к файлу {path}"))
def hook_receives_file_access(
    workspace: Path, hook_script_client, scenario_state: ScenarioState, path: str
) -> None:
    script_path = workspace / ".openhands" / "hooks" / "block_ignored.py"
    payload = {"tool_name": "file_editor", "tool_input": {"command": "view", "path": path}}
    result = hook_script_client.run(script_path, payload, workspace)
    scenario_state.hook_exit_code = result.returncode
    scenario_state.hook_output = result.stderr


@when(parsers.re(r"хук получает нагрузку команды (?P<command>.+)"))
def hook_receives_command(
    workspace: Path, hook_script_client, scenario_state: ScenarioState, command: str
) -> None:
    script_path = workspace / ".openhands" / "hooks" / "block_ignored.py"
    payload = {"tool_name": "terminal", "tool_input": {"command": command}}
    result = hook_script_client.run(script_path, payload, workspace)
    scenario_state.hook_exit_code = result.returncode
    scenario_state.hook_output = result.stderr


@then(parsers.parse("хук завершается с кодом {code:d}"))
def hook_exit_code_matches(scenario_state: ScenarioState, code: int) -> None:
    assert scenario_state.hook_exit_code == code


@then(parsers.parse("хук сообщает о запрете доступа к {path}"))
def hook_reports_denied_path(scenario_state: ScenarioState, path: str) -> None:
    assert "Access denied" in scenario_state.hook_output
    assert path in scenario_state.hook_output


@then("хук не сообщает о запрете доступа")
def hook_does_not_report_denial(scenario_state: ScenarioState) -> None:
    assert "Access denied" not in scenario_state.hook_output


@then("каталог .agents/skills содержит одну папку навыка для каждой роли из roles.yaml")
def skills_have_dir_per_role(workspace: Path) -> None:
    roles = YamlRolesRepository(settings.agents_dir).get_roles()
    generated_names = {path.name for path in (workspace / ".agents" / "skills").iterdir() if path.is_dir()}
    expected_names = {role.slug for role in roles}
    assert generated_names == expected_names


@then("каждый навык содержит name и triggers, равные slug роли из roles.yaml")
def skills_have_identity_metadata(workspace: Path, openhands_skill_file_client) -> None:
    roles = YamlRolesRepository(settings.agents_dir).get_roles()
    for role in roles:
        skill = openhands_skill_file_client.read(workspace / ".agents" / "skills" / role.slug / "SKILL.md")
        assert skill["name"] == role.slug
        assert skill["triggers"] == [role.slug]


@then("каждый навык содержит description роли из roles.yaml")
def skills_have_description(workspace: Path, openhands_skill_file_client) -> None:
    roles = YamlRolesRepository(settings.agents_dir).get_roles()
    for role in roles:
        skill = openhands_skill_file_client.read(workspace / ".agents" / "skills" / role.slug / "SKILL.md")
        assert skill["description"] == role.description


@then(
    "для каждой роли тело навыка содержит определение роли и пользовательские инструкции, "
    "разделённые пустой строкой"
)
def skills_have_body(workspace: Path, openhands_skill_file_client) -> None:
    roles = YamlRolesRepository(settings.agents_dir).get_roles()
    for role in roles:
        skill = openhands_skill_file_client.read(workspace / ".agents" / "skills" / role.slug / "SKILL.md")
        assert skill["body"] == build_openhands_skill_body(role)


@then("тело навыка не содержит условия применения")
def skills_body_omits_when_to_use(workspace: Path, openhands_skill_file_client) -> None:
    roles = YamlRolesRepository(settings.agents_dir).get_roles()
    for role in roles:
        skill = openhands_skill_file_client.read(workspace / ".agents" / "skills" / role.slug / "SKILL.md")
        assert role.when_to_use not in skill["body"]


@then(parsers.parse("файл не существует по пути {path}"))
def file_does_not_exist(workspace: Path, path: str) -> None:
    assert not (workspace / path).exists()


@then('hooks.json объявляет хук pre_tool_use с matcher "*" и командой запуска block_ignored.py')
def hooks_config_declares_pre_tool_use(workspace: Path, json_file_client) -> None:
    data = json_file_client.read(workspace / ".openhands" / "hooks.json")
    entries = data["pre_tool_use"]
    assert entries[0]["matcher"] == "*"
    command = entries[0]["hooks"][0]["command"]
    assert "block_ignored.py" in command


@then("файл .openhands/hooks/block_ignored.py исполняем")
def hook_script_is_executable(workspace: Path) -> None:
    script_path = workspace / ".openhands" / "hooks" / "block_ignored.py"
    assert os.access(script_path, os.X_OK)


@then("вывод команды сообщает об успешной сборке конфигурации OpenHands")
def openhands_success_reported(scenario_state: ScenarioState) -> None:
    assert "Built OpenHands config" in scenario_state.command_output
