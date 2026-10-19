Feature: Сборка конфигурации Zoo Code

  Проект хранит единый источник истины для ролей агентов, правил и
  ignore-записей в agents/. Сборка Zoo Code преобразует этот источник в
  нативные конфигурационные файлы Zoo Code.

  Background:
    Given исходная конфигурация агентов существует в agents/roles.yaml, agents/rules/ и agents/ignore
    And сгенерированные файлы конфигурации Zoo Code отсутствуют

  Scenario: Сборка создаёт файл режимов Zoo Code
    When сборка конфигурации Zoo Code выполнена
    Then файл конфигурации существует по пути .roomodes
    And файл начинается со списка customModes
    And файл содержит одну запись режима для каждой роли из agents/roles.yaml

  Scenario: Каждый режим Zoo Code содержит метаданные роли
    When сборка конфигурации Zoo Code выполнена
    Then каждая запись режима содержит соответствующие поля slug, name, description, roleDefinition и whenToUse

  Scenario: Режим Zoo Code выводит инструкции как литеральный блок с отступом
    When сборка конфигурации Zoo Code выполнена
    Then каждая запись режима выводит пользовательские инструкции как литеральный блок с отступом в шесть пробелов
    And пустые строки внутри инструкций сохраняются

  Scenario: Режим Zoo Code содержит группы роли и источник
    When сборка конфигурации Zoo Code выполнена
    Then каждая запись режима перечисляет свои группы
    And каждая запись режима содержит соответствующее поле source

  Scenario Outline: Zoo Code заключает значение поля в кавычки только при необходимости
    Given роль с description <raw>
    When сборка конфигурации Zoo Code выполнена
    Then итоговое поле description равно <rendered>

    Examples:
      | raw      | rendered        |
      | plain    | plain           |
      | a: b     | "a: b"          |
      | a #b     | "a #b"          |
      | -item    | "-item"         |
      | "quoted" | "\"quoted\""    |

  Scenario: Zoo Code заключает пустое значение поля в кавычки
    Given роль с пустым полем description
    When сборка конфигурации Zoo Code выполнена
    Then итоговое поле description является пустой строкой в кавычках

  Scenario: Сборка заменяет каталог правил Zoo Code исходными правилами
    When сборка конфигурации Zoo Code выполнена
    Then каталог .roo/rules содержит только файлы правил из agents/rules
    And каждый файл правила сохраняет исходное имя файла и содержимое

  Scenario: Сборка записывает ignore-записи в файл игнорирования Zoo Code
    When сборка конфигурации Zoo Code выполнена
    Then файл существует по пути .rooignore
    And файл содержит каждый непустой ignore-шаблон на отдельной строке
