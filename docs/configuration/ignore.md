1. Ignore-записи

Файл [`ignore`](config/agents/ignore) содержит один шаблон на строку. Пустые строки пропускаются.

2. Использование при сборке

Шаблоны из файла [`ignore`](config/agents/ignore) попадают в файл игнорирования выбранного инструмента: [`.rooignore`](src/application/builders/zoocode_builder.py:53) для Zoo Code, [`.codexignore`](src/application/builders/codex_builder.py:47) для Codex и [`.claudeignore`](src/application/builders/claude_agent_builder.py:45) для Claude Agent.

3. OpenHands

Для OpenHands отдельного файла игнорирования нет. Вместо него сборщик создаёт хук pre_tool_use: скрипт [`.openhands/hooks/block_ignored.py`](src/application/builders/openhands_hook_script.py:4), который OpenHands запускает перед каждым вызовом инструмента. Шаблоны из файла [`ignore`](config/agents/ignore) записываются в скрипт при сборке, поэтому хук проверяет те же пути, что и файлы игнорирования других инструментов.

Хук сравнивает переданный инструменту путь с шаблонами. Шаблон подходит, если совпадает с путём целиком или с одним из его сегментов. Записи просматриваются в порядке файла, а результат определяет последнее совпадение:

- `.env` запрещает файл `.env`
- `!.env.example` разрешает `.env.example`, даже если он подходит под более ранний шаблон `.env.*`

Если путь запрещён, хук останавливает вызов инструмента с кодом 2 и сообщением о запрете. В остальных случаях вызов выполняется.
