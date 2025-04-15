from pydantic_settings import BaseSettings
from typing import Optional
from pathlib import Path
from pydantic import Field, computed_field
import os

class Settings(BaseSettings):
    # DATABASE_URL: str
    WIKIQUOTE_BASE_URL: str
    MAX_RETRIES: int = 3
    TIMEOUT_SECONDS: int = 10
    QUOTES_CONFIG_PATH: str = str(os.path.join("backfill_historical_featured_quotes_app", "quotes-extraction-config.json"))
    
    # Database settings with correct field aliases for .env mapping
    db_host: str = Field(alias="DB_HOST")
    db_user: str = Field(alias="DB_USER")
    db_password: str = Field(alias="DB_PASSWORD")
    db_name: str = Field(alias="DB_NAME")
    db_port: str = Field(alias="DB_PORT")

    model_config = {
        "env_file": ".env",
        "populate_by_name": True
    }
    
    # @computed_field
    # @property
    # def DATABASE_URL(self) -> str:
    #     """Construct database URL from components."""
    #     return f"mysql://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"

settings = Settings()
