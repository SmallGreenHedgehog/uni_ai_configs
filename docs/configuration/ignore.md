1. Ignore-записи

Файл [`ignore`](config/agents/ignore) содержит один шаблон на строку. Пустые строки пропускаются.

2. Использование при сборке

Шаблоны из файла [`ignore`](config/agents/ignore) попадают в файл игнорирования выбранного инструмента: [`.rooignore`](src/application/builders/zoocode_builder.py:53) для Zoo Code, [`.codexignore`](src/application/builders/codex_builder.py:47) для Codex и [`.claudeignore`](src/application/builders/claude_agent_builder.py:45) для Claude Agent.
