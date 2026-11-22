1. Общие сведения

Команда [`build-uni-ai`](pyproject.toml:29) создаёт нативные файлы в корне проекта. Набор файлов зависит от выбранного сборщика.

2. Zoo Code

Создаваемые файлы:

- [`.roomodes`](src/application/builders/zoocode_builder.py:18) - список режимов customModes
- [`.roo/rules/`](src/application/builders/zoocode_builder.py:46) - файлы правил
- [`.rooignore`](src/application/builders/zoocode_builder.py:53) - ignore-шаблоны

Каталог `.roo/rules` пересоздаётся заново и содержит только файлы правил из исходной конфигурации.

| Элемент конфигурации | Файл результата |
|---|---|
| роли | [`.roomodes`](src/application/builders/zoocode_builder.py:18) |
| правила | [`.roo/rules/`](src/application/builders/zoocode_builder.py:46) |
| ignore-записи | [`.rooignore`](src/application/builders/zoocode_builder.py:53) |

Каждая роль превращается в запись режима с полями `slug`, `name`, `description`, `roleDefinition`, `whenToUse`, `customInstructions`, `groups` и `source`.

3. Codex

Создаваемые файлы:

- [`AGENTS.md`](src/application/builders/codex_builder.py:43) - правила, объединённые в один файл
- [`.codex/config.toml`](src/application/builders/codex_builder.py:18) - секции агентов `agents.<slug>`
- [`.codexignore`](src/application/builders/codex_builder.py:47) - ignore-шаблоны

| Элемент конфигурации | Файл результата |
|---|---|
| роли | [`.codex/config.toml`](src/application/builders/codex_builder.py:18) |
| правила | [`AGENTS.md`](src/application/builders/codex_builder.py:43) |
| ignore-записи | [`.codexignore`](src/application/builders/codex_builder.py:47) |

Правила объединяются в [`AGENTS.md`](src/application/builders/codex_builder.py:43) пустой строкой, в алфавитном порядке имён файлов. Для каждой роли создаётся секция `agents.<slug>` с полями `description` и `prompt`. Поле `prompt` объединяет определение роли, условия применения и инструкции, разделённые пустыми строками.

4. Claude Agent

Создаваемые файлы:

- [`.claude/agents/`](src/application/builders/claude_agent_builder.py:13) - по одному файлу на роль
- [`.claude/rules/`](src/application/builders/claude_agent_builder.py:39) - файлы правил
- [`.claudeignore`](src/application/builders/claude_agent_builder.py:45) - ignore-шаблоны

| Элемент конфигурации | Файл результата |
|---|---|
| роли | [`.claude/agents/`](src/application/builders/claude_agent_builder.py:13) |
| правила | [`.claude/rules/`](src/application/builders/claude_agent_builder.py:39) |
| ignore-записи | [`.claudeignore`](src/application/builders/claude_agent_builder.py:45) |

Для каждой роли создаётся отдельный Markdown-файл с именем `{index}-{slug}.md`, где `index` - номер роли в [`roles.yaml`](config/agents/roles.yaml) начиная с 1, дополненный нулём до двух знаков. Метаданное `name` совпадает с именем файла без расширения, поэтому список агентов в Claude Agent отображается в порядке ролей из [`roles.yaml`](config/agents/roles.yaml). Файл содержит метаданные `name` и `description`, а также тело, объединяющее определение роли, условия применения и инструкции, разделённые пустыми строками. Каталог `.claude/rules` пересоздаётся заново и содержит только файлы правил из исходной конфигурации.

5. OpenHands

Создаваемые файлы:

- [`AGENTS.md`](src/application/builders/openhands_builder.py:121) - правила, объединённые в один файл
- [`.openhands/skills/`](src/application/builders/openhands_builder.py:100) - по одному файлу навыка на роль
- [`.openhands/hooks.json`](src/application/builders/openhands_builder.py:126) - объявление хука pre_tool_use
- [`.openhands/hooks/block_ignored.py`](src/application/builders/openhands_builder.py:18) - скрипт блокировки доступа к игнорируемым путям

| Элемент конфигурации | Файл результата |
|---|---|
| роли | [`.openhands/skills/`](src/application/builders/openhands_builder.py:100) |
| правила | [`AGENTS.md`](src/application/builders/openhands_builder.py:121) |
| ignore-записи | [`.openhands/hooks.json`](src/application/builders/openhands_builder.py:126), [`.openhands/hooks/block_ignored.py`](src/application/builders/openhands_builder.py:18) |

Правила объединяются в [`AGENTS.md`](src/application/builders/openhands_builder.py:121) пустой строкой, в алфавитном порядке имён файлов. Для каждой роли создаётся файл навыка `<slug>.md`. Файл начинается с YAML-метаданных `name` и `triggers` со значением slug роли, а тело объединяет определение роли и пользовательские инструкции, разделённые пустой строкой; условия применения в тело не попадают. Каталог `.openhands/skills` пересоздаётся заново, поэтому устаревшие файлы удаляются.

Файл [`.openhands/hooks.json`](src/application/builders/openhands_builder.py:126) объявляет хук `pre_tool_use` с matcher `*`, который запускает [`.openhands/hooks/block_ignored.py`](src/application/builders/openhands_builder.py:18) перед каждым вызовом инструмента. Скрипт не зависит от пакета и использует только стандартную библиотеку Python. Шаблоны из файла ignore записываются в скрипт при сборке. Если аргумент инструмента совпадает с шаблоном, скрипт завершается с кодом 2 и выводит сообщение о запрете; иначе завершается с кодом 0. Отрицание `!шаблон` возвращает доступ.

6. Общие правила

Сгенерированные файлы не редактируются вручную и исключены из Git.
