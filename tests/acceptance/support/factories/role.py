from polyfactory.factories.pydantic_factory import ModelFactory

from entities import Role


class RoleFactory(ModelFactory[Role]):
    __model__ = Role

    slug = "architect"
    name = "Architect"
    description = "Plans the architecture"
    role_definition = "You plan systems"
    when_to_use = "When planning"
    custom_instructions = "Line one"
    groups = ["read"]
    source = "project"

    @classmethod
    def create_defaults(cls) -> list[Role]:
        roles = [
            cls.build(custom_instructions="Line one\n\nLine two"),
            cls.build(
                slug="reviewer",
                name="Reviewer",
                description="Reviews code",
                role_definition="You review code",
                when_to_use="When reviewing",
                custom_instructions="Review carefully",
                groups=["read", "edit"],
            ),
        ]
        return roles
