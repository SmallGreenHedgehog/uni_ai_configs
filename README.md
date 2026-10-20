uni_ai_configs

1. Назначение

Пакет готовит конфигурации окружения для AI-агентов из единого источника истины: ролей, правил и ignore-записей.

2. Состав

- src/templates/ - универсальные шаблоны конфигов агентов
- config/agents/ - рабочая конфигурация целевого проекта (роли, правила, ignore); создаётся командой init из шаблонов и донастраивается под проект
- src/cli/ - консольные команды
- src/entities/ - модели ролей, правил и ignore-записей
- src/application/ - сборщики конфигураций и инициализация конфигураций из шаблонов
- src/infrastructure/ - чтение исходных данных и шаблонов, настройки окружения

3. Требования

- Python 3.9+ (generic-типы list[...] используются в рантайме)
- pip

4. Quick start

4.1. Установка пакета

    python3 -m venv .venv
    source .venv/bin/activate
    pip install .

После установки становятся доступны консольные команды `init-uni-ai` и `build-uni-ai`.

4.2. Установка из ветки develop

    pip install "git+https://github.com/SmallGreenHedgehog/uni_ai_configs.git@develop"

Для editable-установки:

    pip install -e "git+https://github.com/SmallGreenHedgehog/uni_ai_configs.git@develop"

4.3. Установка в режиме разработки

    pip install -e ".[dev]"

4.4. Настройка окружения

    cp .env.example .env

В файле .env задаются:
- UNI_AGENTS_PATH - путь к каталогу с исходными конфигами (по умолчанию config/agents)
- UNI_BUILDER - сборщик: Codex или ZooCode (по умолчанию ZooCode)

Через UNI_AGENTS_PATH можно указать другой каталог, если стандартный config/agents не подходит. Путь может быть относительным (разрешается от корня проекта, где выполняется команда) или абсолютным.

4.5. Инициализация конфигов агентов

    init-uni-ai

Команда выполняется из корня целевого проекта, создаёт каталог из UNI_AGENTS_PATH и копирует в него шаблоны из пакета: роли (roles.yaml), правила (rules/) и ignore-шаблоны (ignore). Создаются файлы roles.yaml, ignore, rules/architecture.md и rules/code-style.md. Файл rules/architecture.md создаётся как заглушка и предназначен для описания архитектуры проекта. Существующие файлы не перезаписываются; команда выводит списки созданных и пропущенных файлов.

После инициализации файлы можно донастроить под проект.

4.6. Сборка конфигураций

    build-uni-ai

Пример вызова с выбором сборщика без изменения .env:

    UNI_BUILDER=Codex build-uni-ai

Команда выполняется из корня целевого проекта и собирает конфигурацию для сборщика, заданного в UNI_BUILDER. По завершении команда выводит сообщение об успешной сборке с перечнем созданных файлов.

5. Результат сборки

- Zoo Code: .roomodes, .roo/rules/, .rooignore
- Codex: AGENTS.md, .codex/config.toml, .codexignore

Сгенерированные файлы исключены из Git и не редактируются вручную.

6. Проверка

    pytest

Тесты размещены в tests/unit, tests/integration и tests/acceptance. Приёмочные сценарии (pytest-bdd) находятся в tests/acceptance/features.
