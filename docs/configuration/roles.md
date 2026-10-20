1. Файл ролей

Роли хранятся в roles.yaml под ключом roles. Каждая роль содержит обязательные поля:

| Поле | Назначение |
|---|---|
| slug | идентификатор роли |
| name | имя роли |
| description | краткое описание |
| roleDefinition | определение роли |
| whenToUse | условия применения |
| customInstructions | инструкции роли |
| groups | группы, к которым относится роль |
| source | источник роли |

2. Пример записи

```yaml
roles:
  - slug: example
    name: Example
    description: Example role
    roleDefinition: You are an example assistant
    whenToUse: When an example is needed
    customInstructions: |-
      Instruction line
    groups:
      - read
    source: project
```
