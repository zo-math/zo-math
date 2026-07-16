"""Run Quarto with repository Python settings."""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
from collections.abc import Mapping, Sequence


def prepare_quarto(
    args: Sequence[str], environ: Mapping[str, str] | None = None
) -> tuple[list[str], dict[str, str]]:
    """Return a Quarto command and environment using the current Python."""
    env = dict(os.environ if environ is None else environ)
    quarto = shutil.which("quarto", path=env.get("PATH"))
    if quarto is None:
        raise FileNotFoundError("quarto")
    env.setdefault("QUARTO_PYTHON", sys.executable)
    env.setdefault("RETICULATE_PYTHON", sys.executable)
    return [quarto, *args], env


def main(argv: Sequence[str] | None = None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    if not args:
        print("Usage: python scripts/zo_quarto.py <quarto-command> [args...]", file=sys.stderr)
        return 2
    try:
        command, env = prepare_quarto(args)
    except FileNotFoundError:
        print("Error: quarto executable not found in PATH.", file=sys.stderr)
        return 3
    return subprocess.run(command, env=env, check=False).returncode


if __name__ == "__main__":
    raise SystemExit(main())
