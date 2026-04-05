# Architecture Notes

This project is intentionally small, but the modules are separated so you can grow it without rewriting the whole app.

## Flow

1. `main.py` loads settings and creates shared services.
2. `WeatherApp` in `app/ui/main_window.py` handles user interaction.
3. When the user searches for a city, `WeatherService` sends a request to OpenWeatherMap.
4. The JSON response is normalized into a `WeatherReport` dataclass.
5. The GUI renders the formatted report in labels.

When `DEMO_MODE=true`, the same UI renders sample data from the service layer so the application can still be demonstrated without external connectivity.

## Why This Structure

- `config.py` keeps environment and setup details in one place.
- `models.py` defines a stable internal shape for weather data.
- `services/` is the right place for API calls and business logic.
- `ui/` contains all Tkinter layout code, keeping it separate from networking.
- `utils/` holds tiny helpers that keep the UI module easier to read.

## Easy Extension Ideas

- Add a forecast view using another OpenWeatherMap endpoint.
- Save recent searches to a local JSON or SQLite database.
- Add icons for weather conditions.
- Package the app into a Windows executable with `pyinstaller`.
