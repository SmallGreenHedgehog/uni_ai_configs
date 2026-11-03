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

- [`.claude/agents/`](src/application/builders/claude_agent_builder.py:14) - по одному файлу на роль
- [`.claude/rules/`](src/application/builders/claude_agent_builder.py:34) - файлы правил
- [`.claudeignore`](src/application/builders/claude_agent_builder.py:41) - ignore-шаблоны

| Элемент конфигурации | Файл результата |
|---|---|
| роли | [`.claude/agents/`](src/application/builders/claude_agent_builder.py:14) |
| правила | [`.claude/rules/`](src/application/builders/claude_agent_builder.py:34) |
| ignore-записи | [`.claudeignore`](src/application/builders/claude_agent_builder.py:41) |

Для каждой роли создаётся отдельный Markdown-файл с именем `{slug}.md`. Файл содержит метаданные `name` и `description`, а также тело, объединяющее определение роли, условия применения и инструкции, разделённые пустыми строками. Каталог `.claude/rules` пересоздаётся заново и содержит только файлы правил из исходной конфигурации.

5. Общие правила

Сгенерированные файлы не редактируются вручную и исключены из Git.
