"""Run Quarto with repository Python settings."""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
from pathlib import Path
from collections.abc import Mapping, Sequence
from zo_build_boundary import ROOT, require_repository, require_source


class QuartoNotFoundError(FileNotFoundError):
    """The Quarto executable itself could not be resolved."""


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
            from zo_course_labels import source_checks as course_label_source_checks, require as require_labels
            require_labels(course_label_source_checks(ROOT/argument,ROOT),"source before Quarto")
            from zo_course_remediation import source_checks as remediation_source_checks
            require_labels(remediation_source_checks(ROOT/argument,ROOT),'remediation source before Quarto')
            from zo_course_math_assets import require_source as require_math_assets
            require_math_assets(ROOT/argument,ROOT)


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
    configured = env.get("ZO_QUARTO_EXECUTABLE")
    if configured:
        candidate = Path(configured)
        if not candidate.is_file():
            raise QuartoNotFoundError("quarto")
        quarto = str(candidate)
    else:
        quarto = shutil.which("quarto", path=env.get("PATH"))
    if quarto is None:
        raise QuartoNotFoundError("quarto")
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
    except QuartoNotFoundError as exc:
        detail = str(exc)
        if detail and detail != "quarto":
            print("Error: quarto executable is unavailable: " + detail, file=sys.stderr)
        else:
            print("Error: quarto executable not found in PATH or ZO_QUARTO_EXECUTABLE.", file=sys.stderr)
        return 3
    except ValueError as exc:
        print('Error: official build input boundary: ' + str(exc), file=sys.stderr)
        return 4
    return subprocess.run(command, env=env, check=False).returncode


if __name__ == "__main__":
    raise SystemExit(main())
