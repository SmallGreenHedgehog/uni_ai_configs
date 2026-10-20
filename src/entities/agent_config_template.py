from pathlib import Path

from pydantic import BaseModel


class AgentConfigTemplate(BaseModel):
    relative_path: Path
    content: str
