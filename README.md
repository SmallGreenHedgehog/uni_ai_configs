<h1>uni_ai_configs</h1>

Готовые бинарники публикуются на [странице релизов](https://github.com/SmallGreenHedgehog/uni_ai_configs/releases).

1. Назначение

Пакет готовит конфигурации окружения для AI-агентов из единого источника истины: ролей, правил и ignore-записей.

2. Состав

- [`src/templates/`](src/templates) - универсальные шаблоны конфигов агентов
- [`config/agents/`](config/agents) - рабочая конфигурация целевого проекта (роли, правила, ignore); создаётся командой init из шаблонов и донастраивается под проект
- [`src/cli/`](src/cli) - консольные команды
- [`src/entities/`](src/entities) - модели ролей, правил и ignore-записей
- [`src/application/`](src/application) - сборщики конфигураций и инициализация конфигураций из шаблонов
- [`src/infrastructure/`](src/infrastructure) - чтение исходных данных и шаблонов, настройки окружения
- [`docs/`](docs) - документация проекта

3. Требования

- Python 3.12
- pip

4. Quick start

4.1. Установка пакета

    python3 -m venv .venv
    source .venv/bin/activate
    pip install .

После установки становятся доступны консольные команды [`init-uni-ai`](pyproject.toml:30) и [`build-uni-ai`](pyproject.toml:29).

4.2. Установка из ветки develop

    pip install "git+https://github.com/SmallGreenHedgehog/uni_ai_configs.git@develop"

Для editable-установки:

    pip install -e "git+https://github.com/SmallGreenHedgehog/uni_ai_configs.git@develop"

4.3. Разработка пакета

При работе с репозиторием самого пакета выполняется установка или переустановка пакета:

    pip install -e ".[dev]"

После изменения конфигов пакета в [`config/agents`](config/agents) выполняется сборка под выбранную среду:

    build-uni-ai

4.4. Настройка окружения

    cp .env.example .env

В файле `.env` задаются:
- [`UNI_AGENTS_PATH`](src/infrastructure/settings.py:18) - путь к каталогу с исходными конфигами (по умолчанию [`config/agents`](config/agents))
- [`UNI_BUILDER`](src/infrastructure/settings.py:23) - сборщик: Codex, ZooCode или ClaudeAgent (по умолчанию ZooCode)

Через [`UNI_AGENTS_PATH`](src/infrastructure/settings.py:18) можно указать другой каталог, если стандартный [`config/agents`](config/agents) не подходит. Путь может быть относительным (разрешается от корня проекта, где выполняется команда) или абсолютным.

4.5. Инициализация конфигов агентов

    init-uni-ai

Команда выполняется из корня целевого проекта, создаёт каталог из [`UNI_AGENTS_PATH`](src/infrastructure/settings.py:18) и копирует в него шаблоны из пакета: роли ([`roles.yaml`](config/agents/roles.yaml)), правила ([`rules/`](config/agents/rules)) и ignore-шаблоны ([`ignore`](config/agents/ignore)). Создаются файлы [`roles.yaml`](config/agents/roles.yaml), [`ignore`](config/agents/ignore), [`rules/architecture.md`](config/agents/rules/architecture.md) и [`rules/code-style.md`](config/agents/rules/code-style.md). Файл [`rules/architecture.md`](config/agents/rules/architecture.md) создаётся как заглушка и предназначен для описания архитектуры проекта. Существующие файлы не перезаписываются; команда выводит списки созданных и пропущенных файлов.

После инициализации файлы можно донастроить под проект.

4.6. Сборка конфигураций

    build-uni-ai

Пример вызова с выбором сборщика без изменения `.env`:

    UNI_BUILDER=ClaudeAgent build-uni-ai

Команда выполняется из корня целевого проекта и собирает конфигурацию для сборщика, заданного в [`UNI_BUILDER`](src/infrastructure/settings.py:23): Codex, ZooCode или ClaudeAgent. По завершении команда выводит сообщение об успешной сборке с перечнем созданных файлов.

4.7. Сборка бинарника (Nuitka)

Для сборки нужен компилятор C (gcc или clang) и Nuitka:

    pip install -e ".[nuitka]"
    sh scripts/build_nuitka.sh

Скрипт создаёт один исполняемый файл `dist/uni-ai.bin`. Бинарник содержит обе команды:

    ./dist/uni-ai.bin init
    ./dist/uni-ai.bin build

Подкоманды повторяют поведение [`init-uni-ai`](pyproject.toml:30) и [`build-uni-ai`](pyproject.toml:29).

5. Результат сборки

- Zoo Code: [`.roomodes`](src/application/builders/zoocode_builder.py:18), [`.roo/rules/`](src/application/builders/zoocode_builder.py:46), [`.rooignore`](src/application/builders/zoocode_builder.py:53)
- Codex: [`AGENTS.md`](src/application/builders/codex_builder.py:43), [`.codex/config.toml`](src/application/builders/codex_builder.py:18), [`.codexignore`](src/application/builders/codex_builder.py:47)
- Claude Agent: [`.claude/agents/`](src/application/builders/claude_agent_builder.py:13), [`.claude/rules/`](src/application/builders/claude_agent_builder.py:39), [`.claudeignore`](src/application/builders/claude_agent_builder.py:45)

Сгенерированные файлы исключены из Git и не редактируются вручную.

6. Проверка

    pytest

Тесты размещены в `tests/unit`, `tests/integration` и `tests/acceptance`. Приёмочные сценарии (pytest-bdd) находятся в `tests/acceptance/features`.
