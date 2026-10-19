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

4.1. Установка зависимостей

    python3 -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt

4.2. Настройка пути к конфигам

    cp .env.example .env

По умолчанию используется путь config/agents. При необходимости задайте другой путь через переменную UNI_AGENTS_PATH в файле .env.

4.3. Сборка конфигураций

    ./src/build_zoocode.sh
    ./src/build_codex.sh

5. Результат сборки

- Zoo Code: .roomodes, .roo/rules/, .rooignore
- Codex: AGENTS.md, .codex/config.toml, .codexignore

Сгенерированные файлы исключены из Git и не редактируются вручную.
