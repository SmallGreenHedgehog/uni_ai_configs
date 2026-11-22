1. Ignore-записи

Файл [`ignore`](config/agents/ignore) содержит один шаблон на строку. Пустые строки пропускаются.

2. Использование при сборке

Шаблоны из файла [`ignore`](config/agents/ignore) попадают в файл игнорирования выбранного инструмента: [`.rooignore`](src/application/builders/zoocode_builder.py:53) для Zoo Code, [`.codexignore`](src/application/builders/codex_builder.py:47) для Codex и [`.claudeignore`](src/application/builders/claude_agent_builder.py:45) для Claude Agent.

3. OpenHands

Для OpenHands файла игнорирования нет. Шаблоны из файла [`ignore`](config/agents/ignore) записываются в генерируемый скрипт хука `pre_tool_use` ([`.openhands/hooks/block_ignored.py`](src/application/builders/openhands_builder.py:18)), поэтому после изменения [`ignore`](config/agents/ignore) нужна повторная сборка.

Хук применяет шаблоны по порядку. Значение совпадает, если шаблон подходит ко всему пути или к любому его сегменту. Отрицание `!шаблон` снимает ранее найденное совпадение, поэтому запись `!.env.example` возвращает доступ к файлу при наличии шаблона `.env.*`. При совпадении хук блокирует вызов инструмента с кодом 2 и сообщением о запрете, иначе разрешает вызов с кодом 0.
