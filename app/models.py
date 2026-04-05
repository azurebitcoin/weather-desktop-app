"""Shared data models used across the application."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class WeatherReport:
    """Normalized weather data shown inside the GUI."""

    city: str
    country: str
    latitude: float
    longitude: float
    temperature: float
    feels_like: float
    humidity: int
    condition: str
    description: str
