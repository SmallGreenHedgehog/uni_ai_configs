uni_ai_configs

1. Назначение

Пакет готовит конфигурации окружения для AI-агентов из единого источника истины: ролей, правил и ignore-записей. Источником служит каталог config/agents, из которого команда build-uni-ai собирает нативные конфигурации для выбранного инструмента.

2. Структура проекта

- src/entities - модели данных: роль, правило, ignore-запись, шаблон
- src/application - прикладная логика: сборка и инициализация конфигурации, контракты репозиториев
- src/infrastructure - чтение данных и шаблонов, настройки окружения
- src/cli - консольные команды
- src/templates - универсальные шаблоны конфигурации
- config/agents - исходная конфигурация целевого проекта
- tests - тесты

3. Разделы документации

3.1. Использование

- [installation.md](usage/installation.md) - установка и настройка окружения
- [commands.md](usage/commands.md) - консольные команды
- [build-output.md](usage/build-output.md) - результаты сборки

3.2. Конфигурация

- [overview.md](configuration/overview.md) - структура исходной конфигурации
- [roles.md](configuration/roles.md) - роли
- [rules.md](configuration/rules.md) - правила
- [ignore.md](configuration/ignore.md) - ignore-записи

3.3. Разработка

- [architecture.md](development/architecture.md) - архитектура и структура кода
- [data-flow.md](development/data-flow.md) - поток данных
- [workflow.md](development/workflow.md) - работа с репозиторием пакета
- [testing.md](development/testing.md) - тесты

4. Краткий сценарий работы

1. Установить пакет: pip install .
2. Развернуть исходную конфигурацию: init-uni-ai
3. Донастроить config/agents под проект
4. Собрать конфигурацию: build-uni-ai
