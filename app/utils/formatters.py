"""Small formatting helpers used by the GUI."""

from __future__ import annotations

from app.models import WeatherReport


def format_temperature(value: float, units: str) -> str:
    """Format temperature based on the configured units."""

    symbol = "C" if units == "metric" else "F"
    return f"{value:.1f}°{symbol}"


def format_location(report: WeatherReport) -> str:
    """Build a human-readable location label."""

    country = f", {report.country}" if report.country else ""
    return f"{report.city}{country}"
