"""Compatibility entrypoint for local development.

This file stays at the repository root for the early scaffold phase so
contributors can start the minimal FastAPI app with a single command:

    uv run python main.py
"""

import sys
from pathlib import Path


def _ensure_src_on_path() -> None:
    src_path = Path(__file__).resolve().parent / "src"
    if str(src_path) not in sys.path:
        sys.path.insert(0, str(src_path))


def main() -> None:
    _ensure_src_on_path()

    from ddd_fast_api.bootstrap import run

    run()



if __name__ == "__main__":
    main()
