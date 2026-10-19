from pydantic import BaseModel, ConfigDict, Field


class Role(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    slug: str
    name: str
    description: str
    role_definition: str = Field(alias="roleDefinition")
    when_to_use: str = Field(alias="whenToUse")
    custom_instructions: str = Field(alias="customInstructions")
    groups: list[str]
    source: str
