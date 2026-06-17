"""Application configuration."""

from __future__ import annotations

import os
from dataclasses import dataclass

from dotenv import load_dotenv


@dataclass(frozen=True)
class AppConfig:
    app_env: str
    postgres_host: str
    postgres_port: int
    postgres_db: str
    postgres_user: str
    postgres_password: str
    dgis_api_key: str
    default_city: str
    default_limit: int
    enrichment_enabled: bool
    export_csv: bool
    export_path: str
    request_timeout_seconds: int
    request_delay_seconds: int


def _to_bool(value: str | None, default: bool = False) -> bool:
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "y", "on"}


def load_config() -> AppConfig:
    load_dotenv()

    return AppConfig(
        app_env=os.getenv("APP_ENV", "demo"),
        postgres_host=os.getenv("POSTGRES_HOST", "localhost"),
        postgres_port=int(os.getenv("POSTGRES_PORT", "5432")),
        postgres_db=os.getenv("POSTGRES_DB", "lead_parser_demo_db"),
        postgres_user=os.getenv("POSTGRES_USER", "demo_user"),
        postgres_password=os.getenv("POSTGRES_PASSWORD", "CHANGE_ME_LOCALLY"),
        dgis_api_key=os.getenv("DGIS_API_KEY", "DEMO_DGIS_API_KEY"),
        default_city=os.getenv("DGIS_DEFAULT_CITY", "Москва"),
        default_limit=int(os.getenv("DGIS_DEFAULT_LIMIT", "10")),
        enrichment_enabled=_to_bool(os.getenv("ENRICHMENT_ENABLED"), True),
        export_csv=_to_bool(os.getenv("EXPORT_CSV"), True),
        export_path=os.getenv("EXPORT_PATH", "exports/leads_demo.csv"),
        request_timeout_seconds=int(os.getenv("REQUEST_TIMEOUT_SECONDS", "15")),
        request_delay_seconds=int(os.getenv("REQUEST_DELAY_SECONDS", "2")),
    )


def build_database_url(config: AppConfig) -> str:
    return (
        f"postgresql://{config.postgres_user}:{config.postgres_password}"
        f"@{config.postgres_host}:{config.postgres_port}/{config.postgres_db}"
    )
