from pathlib import Path
from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_name: str = "Private Investment Office"
    broker_mode: Literal["paper", "ibkr_paper", "ibkr_live"] = "paper"
    enable_live_trading: bool = False
    database_path: Path = Path("investment_office.db")

    max_position_pct: float = Field(default=0.05, gt=0, le=0.25)
    max_single_order_base: float = Field(default=100.0, gt=0)
    min_committee_score: float = Field(default=72.0, ge=0, le=100)
    allow_fractional: bool = False

    sec_user_agent: str | None = None

    ibkr_host: str = "127.0.0.1"
    ibkr_paper_port: int = 7947
    ibkr_live_port: int = 7946
    ibkr_client_id: int = 17


settings = Settings()
