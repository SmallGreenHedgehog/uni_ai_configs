Feature: Сборка конфигурации Claude Agent

  Команда build-uni-ai с выбранным Claude Agent-сборщиком преобразует единый
  источник истины агентной конфигурации в нативные файлы Claude Agent:
  .claude/agents/, .claude/rules/ и .claudeignore.

  Background:
    Given сборщик настроен на Claude Agent
    And исходная конфигурация агентов существует в каталоге конфигурации агентов
    And сгенерированные файлы конфигурации Claude Agent отсутствуют

  Scenario: Сборка создаёт каталог агентов Claude Agent
    When сборка конфигурации Claude Agent выполнена
    Then каталог существует по пути .claude/agents
    And каталог содержит один файл агента для каждой роли из roles.yaml

  Scenario: Каждый агент Claude Agent содержит метаданные роли
    When сборка конфигурации Claude Agent выполнена
    Then каждый файл агента содержит соответствующие поля name и description

  Scenario: Тело агента Claude Agent объединяет определение роли, условия применения и инструкции
    When сборка конфигурации Claude Agent выполнена
    Then для каждой роли тело файла агента содержит определение роли, условия применения и пользовательские инструкции, разделённые пустыми строками

  Scenario Outline: Claude Agent заключает значение поля description в кавычки только при необходимости
    Given роль с description <raw>
    When сборка конфигурации Claude Agent выполнена
    Then итоговое поле description равно <rendered>

    Examples:
      | raw      | rendered     |
      | plain    | plain        |
      | a: b     | "a: b"       |
      | a #b     | "a #b"       |
      | -item    | "-item"      |
      | "quoted" | "\"quoted\"" |

  Scenario: Claude Agent заключает пустое значение поля description в кавычки
    Given роль с пустым полем description
    When сборка конфигурации Claude Agent выполнена
    Then итоговое поле description является пустой строкой в кавычках

  Scenario: Сборка заменяет каталог правил Claude Agent исходными правилами
    When сборка конфигурации Claude Agent выполнена
    Then каталог .claude/rules содержит только файлы правил из каталога конфигурации агентов
    And каждый файл правила сохраняет исходное имя файла и содержимое

  Scenario: Сборка записывает ignore-записи в файл игнорирования Claude Agent
    When сборка конфигурации Claude Agent выполнена
    Then файл существует по пути .claudeignore
    And файл содержит каждый непустой ignore-шаблон на отдельной строке

  Scenario: Сборка сообщает об успехе
    When сборка конфигурации Claude Agent выполнена
    Then вывод команды сообщает об успешной сборке конфигурации Claude Agent
