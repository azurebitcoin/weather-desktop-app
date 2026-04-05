"""Launch the customer demo with automatic city transitions for recording."""

from __future__ import annotations

import os

from demo import launch_demo


def main() -> None:
    """Start the demo in autoplay mode for screencasts."""

    os.environ["DEMO_AUTOPLAY"] = "true"
    launch_demo()


if __name__ == "__main__":
    main()
