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

Сборщик OpenHands создаёт общие правила для репозитория, навык для каждой роли и хук pre_tool_use, который запрещает инструментам доступ к игнорируемым путям.

Создаваемые файлы:

- [`AGENTS.md`](src/application/builders/openhands_builder.py:43) - правила, объединённые в один файл
- [`.agents/skills/`](src/application/builders/openhands_builder.py:19) - навык для каждой роли
- [`.openhands/hooks.json`](src/application/builders/openhands_builder.py:48) - настройка хука pre_tool_use
- [`.openhands/hooks/block_ignored.py`](src/application/builders/openhands_hook_script.py:4) - скрипт хука, запрещающий доступ к игнорируемым путям

| Элемент конфигурации | Файл результата |
|---|---|
| роли | [`.agents/skills/`](src/application/builders/openhands_builder.py:19) |
| правила | [`AGENTS.md`](src/application/builders/openhands_builder.py:43) |
| ignore-записи | [`.openhands/hooks.json`](src/application/builders/openhands_builder.py:48), [`.openhands/hooks/block_ignored.py`](src/application/builders/openhands_hook_script.py:4) |

Каждая роль превращается в навык OpenHands: каталог `.agents/skills/<slug>/` с файлом `SKILL.md`. Навык - это нативный механизм OpenHands для повторно используемых инструкций, в том числе для отдельной роли. Файл начинается с метаданных `name`, `description` и `triggers`, где `name` и `triggers` равны slug роли. Тело навыка объединяет определение роли и пользовательские инструкции, разделённые пустой строкой; условия применения в тело не попадают. Каталог `.agents/skills` пересоздаётся заново, поэтому устаревшие навыки удаляются.

Правила объединяются в [`AGENTS.md`](src/application/builders/openhands_builder.py:43) пустой строкой, в алфавитном порядке имён файлов.

Хук pre_tool_use - это скрипт, который OpenHands запускает перед каждым вызовом инструмента. Файл [`.openhands/hooks.json`](src/application/builders/openhands_builder.py:48) объявляет хук с matcher `*` и командой запуска [`.openhands/hooks/block_ignored.py`](src/application/builders/openhands_hook_script.py:4). Скрипт не зависит от пакета и использует только стандартную библиотеку Python. Шаблоны из файла ignore записываются в скрипт при сборке. Если переданный инструменту путь совпадает с шаблоном, скрипт останавливает вызов с кодом 2 и сообщением о запрете; иначе вызов выполняется.

6. Общие правила

Сгенерированные файлы не редактируются вручную и исключены из Git.
