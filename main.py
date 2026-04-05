"""Entry point for launching the weather desktop application."""

from __future__ import annotations

from app.config import get_settings
from app.services.weather_service import WeatherService
from app.ui.main_window import WeatherApp


def main() -> None:
    """Configure services and start the UI loop."""

    settings = get_settings()
    weather_service = WeatherService(settings)
    app = WeatherApp(settings, weather_service)
    app.mainloop()


if __name__ == "__main__":
    main()
