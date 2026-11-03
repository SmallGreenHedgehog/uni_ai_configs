1. Общие сведения

Пакет предоставляет две консольные команды: [`init-uni-ai`](pyproject.toml:30) и [`build-uni-ai`](pyproject.toml:29). Обе выполняются из корня целевого проекта.

2. init-uni-ai

Назначение: разворачивает исходную конфигурацию агентов из шаблонов пакета в каталог, заданный через [`UNI_AGENTS_PATH`](src/infrastructure/settings.py:18).

Создаваемые файлы:

- [`roles.yaml`](config/agents/roles.yaml) - роли
- [`ignore`](config/agents/ignore) - ignore-шаблоны
- [`rules/architecture.md`](config/agents/rules/architecture.md) - заглушка для описания архитектуры проекта
- [`rules/code-style.md`](config/agents/rules/code-style.md) - правила оформления кода

Существующие файлы не перезаписываются. Команда выводит списки созданных и пропущенных файлов.

Пример:

    init-uni-ai

3. build-uni-ai

Назначение: собирает нативную конфигурацию из исходного каталога [`UNI_AGENTS_PATH`](src/infrastructure/settings.py:18) для сборщика, заданного через [`UNI_BUILDER`](src/infrastructure/settings.py:23).

Доступные сборщики:

- Codex
- ZooCode
- ClaudeAgent

Пример:

    build-uni-ai

Выбор сборщика без изменения `.env`:

    UNI_BUILDER=ClaudeAgent build-uni-ai

Команда выводит сообщение об успешной сборке с перечнем созданных файлов.
