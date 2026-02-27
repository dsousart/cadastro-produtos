import os
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Settings:
    app_env: str = "development"
    log_level: str = "INFO"
    database_url: str = ""
    bk_base_path: str = str(Path(__file__).resolve().parents[3] / "base_conhecimento")


def get_settings() -> Settings:
    default_bk_path = str(Path(__file__).resolve().parents[3] / "base_conhecimento")
    return Settings(
        app_env=os.getenv("APP_ENV", "development"),
        log_level=os.getenv("LOG_LEVEL", "INFO"),
        database_url=os.getenv("DATABASE_URL", ""),
        bk_base_path=os.getenv("BK_BASE_PATH", default_bk_path),
    )
