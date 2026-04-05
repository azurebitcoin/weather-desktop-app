"""Launch the application in restricted customer demo mode."""

from __future__ import annotations

import os

from main import main


def launch_demo() -> None:
    """Force demo settings so the customer sees a safe preview build."""

    os.environ["DEMO_MODE"] = "true"
    os.environ.setdefault("DEFAULT_CITY", "Chicago")
    main()


if __name__ == "__main__":
    launch_demo()
