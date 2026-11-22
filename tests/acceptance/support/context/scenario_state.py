from pydantic import BaseModel, Field


class ScenarioState(BaseModel):
    command_output: str = ""
    file_mtimes: dict[str, int] = Field(default_factory=dict)
    hook_exit_code: int = 0
    hook_output: str = ""
