uni_ai_configs

1. Назначение

Пакет готовит конфигурации окружения для AI-агентов из единого источника истины: ролей, правил и ignore-записей.

2. Состав

- config/agents/roles.yaml - роли агентов
- config/agents/rules/ - правила в Markdown
- config/agents/ignore - ignore-шаблоны
- src/ - сборщики конфигураций для конкретных инструментов

3. Требования

- Python 3.9+ (generic-типы list[...] используются в рантайме)
- pip

4. Quick start

4.1. Установка пакета

    python3 -m venv .venv
    source .venv/bin/activate
    pip install .

После установки становятся доступны консольные команды `build-codex` и `build-zoocode`.

4.2. Установка из ветки develop

    pip install "git+https://github.com/SmallGreenHedgehog/uni_ai_configs.git@develop"

Для editable-установки:

    pip install -e "git+https://github.com/SmallGreenHedgehog/uni_ai_configs.git@develop"

4.3. Установка в режиме разработки

    pip install -e ".[dev]"

4.4. Настройка пути к конфигам

    cp .env.example .env

По умолчанию используется путь config/agents. При необходимости задайте другой путь через переменную UNI_AGENTS_PATH в файле .env.

4.5. Сборка конфигураций

    build-zoocode
    build-codex

Команды выполняются из корня целевого проекта.

5. Результат сборки

- Zoo Code: .roomodes, .roo/rules/, .rooignore
- Codex: AGENTS.md, .codex/config.toml, .codexignore

Сгенерированные файлы исключены из Git и не редактируются вручную.
