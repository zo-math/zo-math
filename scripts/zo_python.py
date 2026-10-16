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
    # Keep the external tool discoverable by children running in source mirrors.
    from zo_graphics import graphics_root
    try:
        env.setdefault("ZO_MATH_GRAPHICS_ROOT", str(graphics_root()))
    except FileNotFoundError:
        pass  # Tasks that do not use graphics do not require that installation.
    # Preserve the variation engine's source/hash while binding moved graph TeX.
    from pathlib import Path
    repo = Path(__file__).resolve().parents[1]
    variation = repo / "quy_trinh_xay_dung/cong_cu_bang_bien_thien_zo_math/zo_variation_build.py"
    for index, argument in enumerate(args):
        if argument.startswith("-"):
            continue
        if argument.endswith("zo_variation_build.py") and Path(argument).resolve() == variation:
            args = [*args[:index], str(repo / "scripts/zo_graphics.py"), "variation", *args[index + 1:]]
        break
    return subprocess.run([sys.executable, *args], env=env, check=False).returncode


if __name__ == "__main__":
    raise SystemExit(main())
