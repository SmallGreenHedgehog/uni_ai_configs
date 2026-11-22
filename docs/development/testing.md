1. Запуск тестов

    pytest

2. Структура тестов

- tests/unit - модульные тесты
- tests/integration - интеграционные тесты
- tests/acceptance - приёмочные сценарии pytest-bdd, размещённые в tests/acceptance/features

3. Зависимости для разработки

Режим разработки устанавливает инструменты для тестов и проверок: pytest, pytest-bdd, polyfactory, ruff и pylint.

4. Полная проверка

    sh scripts/quality.sh

Скрипт последовательно запускает ruff, pylint (только ошибки) и pytest.
