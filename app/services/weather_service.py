"""Service layer that talks to OpenWeatherMap and normalizes responses."""

from __future__ import annotations

import hashlib
from typing import Any

import requests

from app.config import Settings
from app.models import WeatherReport


DEMO_REPORTS: dict[str, WeatherReport] = {
    "chicago": WeatherReport(
        city="Chicago",
        country="US",
        latitude=41.88,
        longitude=-87.63,
        temperature=18.4,
        feels_like=17.8,
        humidity=63,
        condition="Clouds",
        description="scattered clouds",
    ),
    "kyiv": WeatherReport(
        city="Kyiv",
        country="UA",
        latitude=50.45,
        longitude=30.52,
        temperature=15.1,
        feels_like=14.2,
        humidity=58,
        condition="Clear",
        description="clear sky",
    ),
    "london": WeatherReport(
        city="London",
        country="GB",
        latitude=51.51,
        longitude=-0.13,
        temperature=12.6,
        feels_like=11.9,
        humidity=72,
        condition="Rain",
        description="light rain",
    ),
    "new york": WeatherReport(
        city="New York",
        country="US",
        latitude=40.71,
        longitude=-74.01,
        temperature=20.3,
        feels_like=19.4,
        humidity=54,
        condition="Mist",
        description="light mist",
    ),
    "tokyo": WeatherReport(
        city="Tokyo",
        country="JP",
        latitude=35.68,
        longitude=139.69,
        temperature=22.8,
        feels_like=23.1,
        humidity=68,
        condition="Clouds",
        description="broken clouds",
    ),
}


class WeatherService:
    """Fetch current weather details for a city."""

    BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

    def __init__(self, settings: Settings) -> None:
        self.settings = settings

    def get_current_weather(self, city: str) -> WeatherReport:
        """Fetch and validate the latest weather snapshot for the provided city."""

        cleaned_city = city.strip()
        if not cleaned_city:
            raise ValueError("Please enter a city name.")

        if self.settings.demo_mode:
            return self._build_demo_report(cleaned_city)

        response = requests.get(
            self.BASE_URL,
            params={
                "q": cleaned_city,
                "appid": self.settings.openweather_api_key,
                "units": self.settings.units,
            },
            timeout=self.settings.request_timeout_seconds,
        )

        try:
            payload: dict[str, Any] = response.json()
        except ValueError as exc:
            raise RuntimeError("Weather service returned an invalid response.") from exc

        if response.status_code != 200:
            message = payload.get("message", "Unable to fetch weather data.")
            raise RuntimeError(message.capitalize())

        weather_items = payload.get("weather", [])
        main_block = payload.get("main", {})
        coord_block = payload.get("coord", {})
        sys_block = payload.get("sys", {})
        primary_condition = weather_items[0] if weather_items else {}

        return WeatherReport(
            city=payload.get("name", cleaned_city),
            country=sys_block.get("country", ""),
            latitude=float(coord_block.get("lat", 0.0)),
            longitude=float(coord_block.get("lon", 0.0)),
            temperature=float(main_block.get("temp", 0.0)),
            feels_like=float(main_block.get("feels_like", 0.0)),
            humidity=int(main_block.get("humidity", 0)),
            condition=primary_condition.get("main", "Unknown"),
            description=primary_condition.get("description", "No description available"),
        )

    def _build_demo_report(self, city: str) -> WeatherReport:
        """Return a predictable sample record when the app is launched in demo mode."""

        known_report = DEMO_REPORTS.get(city.lower())
        if known_report:
            return known_report

        # Produce stable but fake data for any city typed during a client demo.
        digest = hashlib.sha256(city.lower().encode("utf-8")).digest()
        humidity = 35 + digest[0] % 55
        temperature = round(-2 + (digest[1] / 255) * 34, 1)
        feels_like = round(temperature + ((digest[2] % 7) - 3) * 0.4, 1)
        latitude = round(-60 + (digest[3] / 255) * 120, 2)
        longitude = round(-170 + (digest[4] / 255) * 340, 2)
        conditions = [
            ("Clear", "clear sky"),
            ("Clouds", "few clouds"),
            ("Rain", "light rain"),
            ("Mist", "morning mist"),
            ("Snow", "light snow"),
        ]
        condition, description = conditions[digest[5] % len(conditions)]

        return WeatherReport(
            city=city.title(),
            country="DEMO",
            latitude=latitude,
            longitude=longitude,
            temperature=temperature,
            feels_like=feels_like,
            humidity=humidity,
            condition=condition,
            description=description,
        )
