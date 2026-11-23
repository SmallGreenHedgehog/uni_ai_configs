Feature: Сборка конфигурации OpenHands

  Команда build-uni-ai с выбранным OpenHands-сборщиком преобразует единый
  источник истины агентной конфигурации в нативные файлы OpenHands:
  .openhands/agents/, AGENTS.md и .openhands/hooks.json.

  Background:
    Given сборщик настроен на OpenHands
    And исходная конфигурация агентов существует в каталоге конфигурации агентов
    And сгенерированные файлы конфигурации OpenHands отсутствуют

  Scenario: Сборка создаёт каталог субагентов OpenHands
    When сборка конфигурации OpenHands выполнена
    Then каталог существует по пути .openhands/agents
    And каталог .openhands/agents содержит один файл субагента для каждой роли из roles.yaml

  Scenario: Файлы субагентов OpenHands именуются по slug роли
    When сборка конфигурации OpenHands выполнена
    Then каждый файл субагента OpenHands называется по slug соответствующей роли

  Scenario: Каждый субагент OpenHands содержит метаданные роли
    When сборка конфигурации OpenHands выполнена
    Then каждый файл субагента OpenHands содержит frontmatter с полями name и description
    And значение поля name каждого субагента OpenHands соответствует slug роли
    And значение поля description каждого субагента OpenHands соответствует описанию роли

  Scenario: Системный промпт субагента OpenHands объединяет определение роли, условия применения и инструкции
    When сборка конфигурации OpenHands выполнена
    Then для каждой роли тело файла субагента OpenHands содержит определение роли, условия применения и пользовательские инструкции, разделённые пустыми строками

  Scenario Outline: OpenHands заключает значение поля description в кавычки только при необходимости
    Given роль с description <raw>
    When сборка конфигурации OpenHands выполнена
    Then итоговое поле description равно <rendered>

    Examples:
      | raw      | rendered     |
      | plain    | plain        |
      | a: b     | "a: b"       |
      | a #b     | "a #b"       |
      | -item    | "-item"      |
      | "quoted" | "\"quoted\"" |

  Scenario: OpenHands заключает пустое значение поля description в кавычки
    Given роль с пустым полем description
    When сборка конфигурации OpenHands выполнена
    Then итоговое поле description является пустой строкой в кавычках

  Scenario: Сборка объединяет правила в общий файл инструкций OpenHands
    When сборка конфигурации OpenHands выполнена
    Then файл существует по пути AGENTS.md
    And файл содержит все содержимые правила, объединённые пустой строкой, с завершающим переводом строки

  Scenario: Правила OpenHands объединяются в алфавитном порядке имён файлов
    When сборка конфигурации OpenHands выполнена
    Then содержимое правил в AGENTS.md идёт в алфавитном порядке имён исходных файлов

  Scenario: Сборка записывает ignore-записи в хуки OpenHands
    When сборка конфигурации OpenHands выполнена
    Then файл существует по пути .openhands/hooks.json
    And файл .openhands/hooks.json содержит pre_tool_use hook, запрещающий доступ к игнорируемым путям
    And pre_tool_use hook содержит каждый непустой ignore-шаблон

  Scenario: Сборка сообщает об успехе
    When сборка конфигурации OpenHands выполнена
    Then вывод команды сообщает об успешной сборке конфигурации OpenHands
