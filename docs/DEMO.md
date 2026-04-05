# Demo Build Notes

This project now includes a customer-facing demo build.

## Demo Entry Points

- `python demo.py`
- double-click `launch_demo.bat` on Windows
- `python demo_autoplay.py` for automated screencasts

## Demo Restrictions

- No real OpenWeatherMap API key is required
- The interface clearly displays `Demo Version`
- Search requests return preview data suitable for presentations and client review
- The full version keeps the live API integration in `main.py` and unlocks production data

## Suggested Client Handoff

Share only the demo launcher and screenshot/video materials before payment. Keep the production `.env` and the standard `main.py` launch instructions for the paid delivery package.
