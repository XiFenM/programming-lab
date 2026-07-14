"""Lightweight TileLang installation probe.

TileLang's kernel API is evolving quickly. This probe deliberately validates
the installed package without freezing an example to one release's DSL API.
"""

from importlib.metadata import version

import tilelang


def main() -> None:
    """Print the installed TileLang package and import location."""
    print(f"TileLang version: {version('tilelang')}")
    print(f"TileLang module: {tilelang.__file__}")


if __name__ == "__main__":
    main()
