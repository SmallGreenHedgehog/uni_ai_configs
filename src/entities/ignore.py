from pydantic import BaseModel


class IgnoreEntry(BaseModel):
    pattern: str
