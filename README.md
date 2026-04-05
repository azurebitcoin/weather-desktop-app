# Weather Desk

Weather Desk is a Windows-friendly desktop application written in Python. It uses the OpenWeatherMap API to fetch live weather data and displays it in a simple Tkinter interface that is easy to extend.

## Features

- Live weather lookup by city
- Temperature, feels-like temperature, humidity, condition, and coordinates
- Clean GUI built with Tkinter and `ttk`
- Environment-based API key configuration
- Modular folder structure for easier maintenance

## Project Structure

```text
weather-desktop-app/
├── app/
│   ├── config.py
│   ├── models.py
│   ├── services/
│   │   └── weather_service.py
│   ├── ui/
│   │   └── main_window.py
│   └── utils/
│       └── formatters.py
├── assets/
├── docs/
│   └── ARCHITECTURE.md
├── .env.example
├── main.py
└── requirements.txt
```

## Setup on Windows

1. Register for a free API key at [OpenWeatherMap](https://openweathermap.org/api).
2. Open PowerShell in the project folder:

   ```powershell
   cd D:\weather-desktop-app
   ```

3. Create and activate a virtual environment:

   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

4. Install dependencies:

   ```powershell
   pip install -r requirements.txt
   ```

5. Create a local environment file:

   ```powershell
   Copy-Item .env.example .env
   ```

6. Open `.env` and paste your `OPENWEATHER_API_KEY`.
7. Start the application:

   ```powershell
   python main.py
   ```

## Optional Demo Mode

If you want to preview the interface before creating an API key, set `DEMO_MODE=true` in `.env`. The app will load sample weather data instead of calling OpenWeatherMap.

## Screenshot

A sample interface capture created in demo mode is available at `assets/weather-desk-demo-window.png`.

## Demo Build For Clients

If you want to show the app before handing over the production version:

```powershell
python demo.py
```

Or on Windows:

```powershell
.\launch_demo.bat
```

The demo build displays a visible notice and uses preview data instead of live API responses. See `docs/DEMO.md` for the handoff approach.

## How It Works

- `main.py` wires the application together.
- `app/config.py` loads the API key and app settings.
- `app/services/weather_service.py` calls OpenWeatherMap and converts the raw JSON into a Python dataclass.
- `app/ui/main_window.py` renders the desktop interface and refreshes it when the user searches for a city.
- `docs/ARCHITECTURE.md` provides a short explanation of how the modules fit together.

## Notes

- Tkinter ships with standard Python on Windows, so no extra GUI package install is required.
- If a city cannot be found, the app shows a friendly error dialog.
- You can switch between metric and imperial units through the `.env` file.
- `DEMO_MODE=true` is helpful for screenshots, training, or offline previews.
