uni_ai_configs

1. Назначение

Пакет готовит конфигурации окружения для AI-агентов из единого источника истины: ролей, правил и ignore-записей.

2. Состав

- src/templates/ - универсальные шаблоны конфигов агентов
- config/agents/ - рабочая конфигурация целевого проекта (роли, правила, ignore); создаётся командой init из шаблонов и донастраивается под проект
- src/cli/ - консольные команды
- src/entities/ - модели ролей, правил и ignore-записей
- src/application/ - сборщики конфигураций
- src/infrastructure/ - чтение исходных данных и настройки окружения

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
- UNI_BUILDER - сборщик: codex или zoocode (по умолчанию zoocode)

Через UNI_AGENTS_PATH можно указать другой каталог, если стандартный config/agents не подходит.

4.5. Инициализация конфигов агентов

    init-uni-ai

Команда выполняется из корня целевого проекта, создаёт каталог из UNI_AGENTS_PATH и копирует в него все файлы из src/templates: роли (roles.yaml), правила (rules/) и ignore-шаблоны (ignore). Файл rules/architecture.md создаётся как заглушка и предназначен для описания архитектуры проекта. Существующие файлы не перезаписываются.

После инициализации файлы можно донастроить под проект.

4.6. Сборка конфигураций

    build-uni-ai

Пример вызова с выбором сборщика без изменения .env:

    UNI_BUILDER=codex build-uni-ai

Команда выполняется из корня целевого проекта и собирает конфигурацию для сборщика, заданного в UNI_BUILDER.

5. Результат сборки

- Zoo Code: .roomodes, .roo/rules/, .rooignore
- Codex: AGENTS.md, .codex/config.toml, .codexignore

Сгенерированные файлы исключены из Git и не редактируются вручную.
