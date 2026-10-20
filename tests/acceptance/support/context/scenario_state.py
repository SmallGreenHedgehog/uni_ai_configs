from pydantic import BaseModel, Field


class ScenarioState(BaseModel):
    command_output: str = ""
    file_mtimes: dict[str, int] = Field(default_factory=dict)
