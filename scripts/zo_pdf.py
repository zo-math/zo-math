from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from zo_artifact_freshness import FreshnessError, evaluate_artifact_freshness
from zo_pdf_contract import (
    pdf_build_receipt_path,
    validate_pdf_build_receipt,
    write_pdf_build_receipt,
)


ROOT = Path(__file__).resolve().parents[1]
AUDIT_DIR = ROOT / "_audit"
QUARTO_LAUNCHER = ROOT / "scripts" / "zo_quarto.py"


def source_path(value: str) -> Path:
    candidate = (ROOT / value).resolve()
    try:
        candidate.relative_to(ROOT)
    except ValueError as exc:
        raise argparse.ArgumentTypeError("Tệp nguồn phải nằm trong repository.") from exc
    if not candidate.is_file():
        raise argparse.ArgumentTypeError(f"Không tìm thấy tệp nguồn: {value}")
    if candidate.suffix.lower() != ".qmd":
        raise argparse.ArgumentTypeError("Cơ chế PDF hiện chỉ nhận tệp .qmd.")
    return candidate


def relative_to_root(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def output_path(source: Path) -> Path:
    return source.with_suffix(".pdf")


def build(source: Path) -> int:
    AUDIT_DIR.mkdir(parents=True, exist_ok=True)
    temp_dir = Path(tempfile.mkdtemp(prefix="zo_pdf_", dir=AUDIT_DIR))
    temp_relative = relative_to_root(temp_dir)
    command = [
        sys.executable,
        str(QUARTO_LAUNCHER),
        "render",
        relative_to_root(source),
        "--profile",
        "pdf",
        "--to",
        "pdf",
        "--output-dir",
        temp_relative,
    ]

    try:
        environment = os.environ.copy()
        tex_resource_dirs = [
            str((ROOT / "assets" / "logo").resolve()),
            str((ROOT / "assets" / "images").resolve()),
        ]
        current_texinputs = environment.get("TEXINPUTS", "")
        environment["TEXINPUTS"] = os.pathsep.join(
            [*tex_resource_dirs, current_texinputs]
        )

        completed = subprocess.run(
            command,
            cwd=ROOT,
            check=False,
            env=environment,
        )
        if completed.returncode != 0:
            return completed.returncode

        expected = temp_dir / source.relative_to(ROOT).with_suffix(".pdf")
        if not expected.is_file():
            matches = list(temp_dir.rglob(f"{source.stem}.pdf"))
            if len(matches) != 1:
                print("Không xác định được duy nhất tệp PDF vừa render.", file=sys.stderr)
                return 1
            expected = matches[0]

        destination = output_path(source)
        shutil.copy2(expected, destination)
        receipt = write_pdf_build_receipt(ROOT, source, destination)
        print(f"PDF created: {relative_to_root(destination)}")
        print(f"PDF build receipt: {relative_to_root(receipt)}")
        return 0
    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)


def status(source: Path) -> int:
    destination = output_path(source)
    if not destination.is_file():
        print(f"MISSING: {relative_to_root(destination)}")
        return 1
    try:
        freshness = evaluate_artifact_freshness(ROOT, source, destination)
    except (FreshnessError, OSError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    receipt_errors = validate_pdf_build_receipt(ROOT, source, destination)
    current = freshness.current and not receipt_errors
    label = "CURRENT" if current else "STALE"
    detail = f"{freshness.message} Cơ sở={freshness.basis}."
    if receipt_errors:
        detail += " PDF provenance: " + "; ".join(receipt_errors) + "."
    print(f"{label}: {relative_to_root(destination)} | {detail}")
    return 0 if current else 2


def self_test() -> int:
    AUDIT_DIR.mkdir(parents=True, exist_ok=True)
    temp_dir = Path(tempfile.mkdtemp(prefix="zo_pdf_contract_self_test_", dir=AUDIT_DIR))
    try:
        source = temp_dir / "test.qmd"
        output = temp_dir / "test.pdf"
        source.write_text("---\ntitle: Test\n---\n\nTest.\n", encoding="utf-8")
        output.write_bytes(b"%PDF-1.4\nself-test\n")
        receipt = write_pdf_build_receipt(
            ROOT,
            source,
            output,
            temp_dir / "receipt.json",
        )
        errors = validate_pdf_build_receipt(ROOT, source, output, receipt)
        if errors:
            raise RuntimeError("receipt baseline failed: " + "; ".join(errors))
        output.write_bytes(b"%PDF-1.4\nself-test-drift\n")
        drift = validate_pdf_build_receipt(ROOT, source, output, receipt)
        if not any("output.sha256" in item for item in drift):
            raise RuntimeError("PDF drift was not detected")
        print("SELF-TEST PASS: zo_pdf")
        return 0
    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(
        description="Dựng PDF opt-in cho một trang QMD mà không render lại HTML."
    )
    subparsers = result.add_subparsers(dest="command", required=True)
    for name in ("build", "status"):
        command = subparsers.add_parser(name)
        command.add_argument("source", type=source_path)
    subparsers.add_parser("self-test")
    return result


def main() -> int:
    args = parser().parse_args()
    if args.command == "self-test":
        return self_test()
    if args.command == "build":
        return build(args.source)
    return status(args.source)


if __name__ == "__main__":
    raise SystemExit(main())
