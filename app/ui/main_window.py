"""Tkinter UI for the desktop weather application."""

from __future__ import annotations

import threading
import tkinter as tk
from tkinter import messagebox, ttk

from app.config import Settings
from app.models import WeatherReport
from app.services.weather_service import WeatherService
from app.utils.formatters import format_location, format_temperature


class WeatherApp(tk.Tk):
    """Main application window."""

    def __init__(self, settings: Settings, weather_service: WeatherService) -> None:
        super().__init__()
        self.settings = settings
        self.weather_service = weather_service

        self.title("Weather Desk")
        self.geometry("520x420")
        self.minsize(520, 420)
        self.configure(bg="#edf2f7")

        # Tk variables make it easy to update labels after a search.
        self.city_var = tk.StringVar(value=self.settings.default_city)
        self.status_var = tk.StringVar(value="Enter a city and click Search.")
        self.location_var = tk.StringVar(value="Location will appear here")
        self.temperature_var = tk.StringVar(value="--")
        self.feels_like_var = tk.StringVar(value="Feels like: --")
        self.humidity_var = tk.StringVar(value="Humidity: --")
        self.condition_var = tk.StringVar(value="Condition: --")
        self.coordinates_var = tk.StringVar(value="Coordinates: --")
        self._is_loading = False

        self._configure_styles()
        self._build_layout()
        self.fetch_weather()

    def _configure_styles(self) -> None:
        """Define a small visual system so the interface looks consistent."""

        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure("App.TFrame", background="#edf2f7")
        style.configure("Card.TFrame", background="#ffffff")
        style.configure(
            "Header.TLabel",
            background="#edf2f7",
            foreground="#1a202c",
            font=("Segoe UI Semibold", 18),
        )
        style.configure(
            "Body.TLabel",
            background="#ffffff",
            foreground="#2d3748",
            font=("Segoe UI", 11),
        )
        style.configure(
            "Value.TLabel",
            background="#ffffff",
            foreground="#0f172a",
            font=("Segoe UI Semibold", 24),
        )
        style.configure(
            "Search.TButton",
            font=("Segoe UI Semibold", 10),
            padding=(14, 8),
        )
        style.configure(
            "DemoBanner.TLabel",
            background="#fff7d6",
            foreground="#7a5200",
            font=("Segoe UI Semibold", 10),
            padding=10,
        )

    def _build_layout(self) -> None:
        """Create the visible controls."""

        root = ttk.Frame(self, style="App.TFrame", padding=20)
        root.pack(fill="both", expand=True)

        ttk.Label(root, text="Current Weather", style="Header.TLabel").pack(
            anchor="w", pady=(0, 12)
        )

        if self.settings.demo_mode:
            ttk.Label(
                root,
                text=(
                    "Demo Version: showing preview data only. "
                    "Live OpenWeatherMap API access is included in the full version."
                ),
                style="DemoBanner.TLabel",
                wraplength=460,
                justify="left",
            ).pack(fill="x", pady=(0, 14))

        search_row = ttk.Frame(root, style="App.TFrame")
        search_row.pack(fill="x", pady=(0, 16))

        self.city_entry = ttk.Entry(
            search_row, textvariable=self.city_var, font=("Segoe UI", 11)
        )
        self.city_entry.pack(side="left", fill="x", expand=True)
        self.city_entry.bind("<Return>", lambda _event: self.fetch_weather())

        self.search_button = ttk.Button(
            search_row,
            text="Search",
            style="Search.TButton",
            command=self.fetch_weather,
        )
        self.search_button.pack(side="left", padx=(10, 0))

        card = ttk.Frame(root, style="Card.TFrame", padding=24)
        card.pack(fill="both", expand=True)

        ttk.Label(card, textvariable=self.location_var, style="Body.TLabel").pack(anchor="w")
        ttk.Label(card, textvariable=self.temperature_var, style="Value.TLabel").pack(
            anchor="w", pady=(12, 4)
        )
        ttk.Label(card, textvariable=self.feels_like_var, style="Body.TLabel").pack(anchor="w")
        ttk.Label(card, textvariable=self.humidity_var, style="Body.TLabel").pack(
            anchor="w", pady=(8, 0)
        )
        ttk.Label(card, textvariable=self.condition_var, style="Body.TLabel").pack(
            anchor="w", pady=(8, 0)
        )
        ttk.Label(card, textvariable=self.coordinates_var, style="Body.TLabel").pack(
            anchor="w", pady=(8, 0)
        )

        ttk.Separator(card, orient="horizontal").pack(fill="x", pady=18)

        status_label = ttk.Label(
            card,
            textvariable=self.status_var,
            style="Body.TLabel",
            wraplength=430,
            justify="left",
        )
        status_label.pack(anchor="w")

    def fetch_weather(self) -> None:
        """Load data from the service and refresh the labels."""

        if self._is_loading:
            return

        city = self.city_var.get()
        if not city.strip():
            messagebox.showwarning("Weather Desk", "Please enter a city name.")
            return

        self._set_loading_state(True)
        self.status_var.set("Loading weather data...")
        worker = threading.Thread(target=self._fetch_weather_worker, args=(city,), daemon=True)
        worker.start()

    def _fetch_weather_worker(self, city: str) -> None:
        """Perform the API request away from the Tk event loop."""

        try:
            report = self.weather_service.get_current_weather(city)
        except Exception as exc:  # Broad by design to keep the UI friendly.
            self.after(0, lambda: self._handle_error(str(exc)))
            return

        self.after(0, lambda: self._handle_success(report))

    def _handle_success(self, report: WeatherReport) -> None:
        """Apply a successful response on the main Tk thread."""

        self._render_report(report)
        if self.settings.demo_mode:
            self.status_var.set(
                "Demo data loaded successfully. Full version unlocks live weather API calls."
            )
        else:
            self.status_var.set("Weather updated successfully.")
        self._set_loading_state(False)

    def _handle_error(self, message: str) -> None:
        """Show a user-friendly error on the main Tk thread."""

        self.status_var.set("Unable to load weather information.")
        self._set_loading_state(False)
        messagebox.showerror("Weather Desk", message)

    def _render_report(self, report: WeatherReport) -> None:
        """Push a WeatherReport into the visible fields."""

        self.location_var.set(format_location(report))
        self.temperature_var.set(format_temperature(report.temperature, self.settings.units))
        self.feels_like_var.set(
            f"Feels like: {format_temperature(report.feels_like, self.settings.units)}"
        )
        self.humidity_var.set(f"Humidity: {report.humidity}%")
        self.condition_var.set(
            f"Condition: {report.condition} ({report.description.capitalize()})"
        )
        self.coordinates_var.set(
            f"Coordinates: {report.latitude:.2f}, {report.longitude:.2f}"
        )

    def _set_loading_state(self, is_loading: bool) -> None:
        """Disable input while a request is in flight."""

        self._is_loading = is_loading
        entry_state = "disabled" if is_loading else "normal"
        button_state = "disabled" if is_loading else "normal"
        self.city_entry.configure(state=entry_state)
        self.search_button.configure(state=button_state)
