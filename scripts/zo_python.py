"""Run repository Python commands in UTF-8 mode without writing bytecode."""

from __future__ import annotations

import os
import subprocess
import sys
from collections.abc import Sequence


def main(argv: Sequence[str] | None = None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    if not args:
        print(
            "Usage: python scripts/zo_python.py <script.py | -m module> [args...]",
            file=sys.stderr,
        )
        return 2

    env = os.environ.copy()
    env["PYTHONUTF8"] = "1"
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    return subprocess.run([sys.executable, *args], env=env, check=False).returncode


if __name__ == "__main__":
    raise SystemExit(main())
