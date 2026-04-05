"""Configuration helpers for the weather desktop application."""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv


# Load values from a local .env file when one is present.
PROJECT_ROOT = Path(__file__).resolve().parent.parent
ENV_PATH = PROJECT_ROOT / ".env"
load_dotenv(ENV_PATH)


@dataclass(frozen=True)
class Settings:
    """Application settings loaded from environment variables."""

    openweather_api_key: str
    default_city: str = "London"
    units: str = "metric"
    request_timeout_seconds: int = 10
    demo_mode: bool = False


def get_settings() -> Settings:
    """Build a Settings object and fail early if a required value is missing."""

    api_key = os.getenv("OPENWEATHER_API_KEY", "").strip()
    demo_mode = os.getenv("DEMO_MODE", "false").strip().lower() in {"1", "true", "yes", "on"}

    if not api_key and not demo_mode:
        raise ValueError(
            "Missing OPENWEATHER_API_KEY. Add it to a .env file or enable DEMO_MODE."
        )

    return Settings(
        openweather_api_key=api_key,
        default_city=os.getenv("DEFAULT_CITY", "London").strip() or "London",
        units=os.getenv("WEATHER_UNITS", "metric").strip() or "metric",
        demo_mode=demo_mode,
    )
