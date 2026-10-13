"""Run Quarto with repository Python settings."""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
from pathlib import Path
from collections.abc import Mapping, Sequence
from zo_build_boundary import ROOT, require_repository, require_source


def require_arguments(args):
    """CLI metadata/filter/include overrides are compilation inputs as well."""
    inputs = {'--metadata-file', '--include-in-header', '--include-before-body',
              '--include-after-body', '--filter', '--lua-filter', '--template',
              '--defaults', '--reference-doc', '--css'}
    for index, argument in enumerate(args):
        option, separator, value = argument.partition('=')
        if option in inputs:
            if not separator and index + 1 < len(args):
                value = args[index + 1]
            if value:
                require_source(Path(value), ROOT)
        elif not argument.startswith('-') and Path(argument).suffix.lower() in {'.qmd', '.rmd'}:
            require_source(Path(argument), ROOT)


def prepare_quarto(
    args: Sequence[str], environ: Mapping[str, str] | None = None
) -> tuple[list[str], dict[str, str]]:
    """Return a Quarto command and environment using the current Python."""
    env = dict(os.environ if environ is None else environ)
    if not args or args[0] in {'render', 'preview'}:
        require_arguments(args)
        require_repository()
        env['ZO_OFFICIAL_BUILD'] = '1'
        runtime = str(Path(__file__).resolve().parent / 'zo_build_runtime')
        env['PYTHONPATH'] = os.pathsep.join([runtime, *filter(None, [env.get('PYTHONPATH')])])
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
    except ValueError as exc:
        print('Error: official build input boundary: ' + str(exc), file=sys.stderr)
        return 4
    return subprocess.run(command, env=env, check=False).returncode


if __name__ == "__main__":
    raise SystemExit(main())
