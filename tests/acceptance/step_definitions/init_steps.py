import shutil
from importlib.resources import files
from pathlib import Path

import pytest
from pytest_bdd import given, parsers, then, when

from infrastructure.settings import settings
from tests.acceptance.support.context import ScenarioState

INIT_FILES = ["roles.yaml", "ignore", "rules/architecture.md", "rules/code-style.md"]


@given("каталог конфигурации агентов не содержит файлов конфигурации")
def agents_dir_is_empty() -> None:
    agents_dir = settings.agents_dir
    if agents_dir.exists():
        shutil.rmtree(agents_dir)
    agents_dir.mkdir(parents=True)


@when("инициализация конфигурации агентов выполнена")
def init_executed(init_client, scenario_state: ScenarioState) -> None:
    scenario_state.command_output = init_client.run()


@when("инициализация конфигурации агентов выполнена повторно")
def init_executed_again(init_client, scenario_state: ScenarioState) -> None:
    scenario_state.command_output = init_client.run()


@then(
    "в каталоге конфигурации агентов созданы файлы конфигурации roles.yaml, ignore, rules/architecture.md и rules/code-style.md"
)
def all_init_files_created() -> None:
    for relative_path in INIT_FILES:
        assert (settings.agents_dir / relative_path).exists()


@then(parsers.parse("в каталоге конфигурации агентов создан файл конфигурации {relative_path}"))
def init_file_created(relative_path: str) -> None:
    assert (settings.agents_dir / relative_path).exists()


@then(parsers.parse("содержимое файла конфигурации {relative_path} совпадает с содержимым соответствующего шаблона"))
def init_file_matches_template(relative_path: str) -> None:
    generated = (settings.agents_dir / relative_path).read_text(encoding="utf-8")
    resource = files("templates")
    for part in relative_path.split("/"):
        resource = resource / part
    template = resource.read_text(encoding="utf-8")
    assert generated == template


@then("файлы конфигурации правил создаются во вложенном каталоге rules внутри каталога конфигурации агентов")
def rules_are_nested() -> None:
    rules_dir = settings.agents_dir / "rules"
    assert rules_dir.is_dir()
    assert (rules_dir / "architecture.md").exists()
    assert (rules_dir / "code-style.md").exists()


@then("вывод команды сообщает о созданных файлах конфигурации")
def report_lists_created(scenario_state: ScenarioState) -> None:
    assert "Initialized agent configs:" in scenario_state.command_output


@then("вывод команды перечисляет каждый созданный файл конфигурации")
def report_lists_each_created_file(scenario_state: ScenarioState) -> None:
    for relative_path in INIT_FILES:
        path = str(settings.agents_dir / relative_path)
        assert path in scenario_state.command_output


@given("в каталоге конфигурации агентов уже существует файл конфигурации roles.yaml")
def existing_roles_file() -> None:
    settings.agents_dir.mkdir(parents=True, exist_ok=True)
    (settings.agents_dir / "roles.yaml").write_text("roles: []\n", encoding="utf-8")


@then("существующий файл конфигурации roles.yaml не перезаписан")
def roles_file_untouched() -> None:
    content = (settings.agents_dir / "roles.yaml").read_text(encoding="utf-8")
    assert content == "roles: []\n"


@then("остальные файлы конфигурации созданы")
def other_init_files_created() -> None:
    for relative_path in ["ignore", "rules/architecture.md", "rules/code-style.md"]:
        assert (settings.agents_dir / relative_path).exists()


@then("вывод команды сообщает о пропущенных файлах конфигурации")
def report_lists_skipped(scenario_state: ScenarioState) -> None:
    assert "Skipped existing agent configs:" in scenario_state.command_output


@then("вывод команды перечисляет файл конфигурации roles.yaml как пропущенный")
def report_lists_roles_as_skipped(scenario_state: ScenarioState) -> None:
    path = str(settings.agents_dir / "roles.yaml")
    assert path in scenario_state.command_output


@given("инициализация конфигурации агентов уже выполнена")
def init_already_executed(init_client, scenario_state: ScenarioState) -> None:
    init_client.run()
    scenario_state.file_mtimes = {
        relative_path: (settings.agents_dir / relative_path).stat().st_mtime_ns for relative_path in INIT_FILES
    }


@then("ни один файл конфигурации не изменён")
def no_init_file_changed(scenario_state: ScenarioState) -> None:
    for relative_path, recorded_mtime in scenario_state.file_mtimes.items():
        current_mtime = (settings.agents_dir / relative_path).stat().st_mtime_ns
        assert current_mtime == recorded_mtime


@then("вывод команды не сообщает о созданных файлах конфигурации")
def report_has_no_created(scenario_state: ScenarioState) -> None:
    assert "Initialized agent configs:" not in scenario_state.command_output


@given("каталог конфигурации агентов задан настраиваемым путём")
def custom_agents_dir(workspace: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    custom_dir = workspace / "custom" / "agents"
    monkeypatch.setattr(settings, "agents_dir", custom_dir)
    if custom_dir.exists():
        shutil.rmtree(custom_dir)
    custom_dir.mkdir(parents=True)


@then("файлы конфигурации создаются в настраиваемом каталоге конфигурации агентов")
def init_files_in_custom_dir() -> None:
    for relative_path in INIT_FILES:
        assert (settings.agents_dir / relative_path).exists()
