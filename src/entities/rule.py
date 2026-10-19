from pydantic import BaseModel


class Rule(BaseModel):
    filename: str
    content: str
