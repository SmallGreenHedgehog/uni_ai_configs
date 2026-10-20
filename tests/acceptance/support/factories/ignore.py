from polyfactory.factories.pydantic_factory import ModelFactory

from entities import IgnoreEntry


class IgnoreFactory(ModelFactory[IgnoreEntry]):
    __model__ = IgnoreEntry

    pattern = ".env"

    @classmethod
    def create_defaults(cls) -> list[IgnoreEntry]:
        entries = [
            cls.build(),
            cls.build(pattern=""),
            cls.build(pattern=".venv"),
        ]
        return entries
