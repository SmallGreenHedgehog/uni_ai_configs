from pathlib import Path
from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        populate_by_name=True,
    )

    agents_dir: Path = Field(
        default=Path("config/agents"),
        validation_alias="UNI_AGENTS_PATH",
    )

    builder: Literal["Codex", "ZooCode"] = Field(
        default="ZooCode",
        validation_alias="UNI_BUILDER",
    )


settings = Settings()
