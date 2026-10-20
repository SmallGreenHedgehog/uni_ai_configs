from polyfactory.factories.pydantic_factory import ModelFactory

from entities import Rule


class RuleFactory(ModelFactory[Rule]):
    __model__ = Rule

    filename = "alpha.md"
    content = "alpha rule\n"

    @classmethod
    def create_defaults(cls) -> list[Rule]:
        rules = [
            cls.build(),
            cls.build(filename="beta.md", content="beta rule\n"),
        ]
        return rules
