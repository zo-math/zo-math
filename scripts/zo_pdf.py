from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from zo_artifact_freshness import FreshnessError, evaluate_artifact_freshness
from zo_qmd_config import discover_project_config
from zo_pdf_contract import (
    canonical_pdf_provenance_enabled,
    canonical_variant_input_state,
    pdf_build_receipt_path,
    pdf_output_path,
    pdf_variant,
    update_canonical_pdf_provenance,
    validate_canonical_pdf_provenance,
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


def output_path(source: Path, variant: str = "full") -> Path:
    return pdf_output_path(ROOT, source, variant)


def validate_rendered_pdf(path: Path) -> None:
    """Reject an incomplete renderer output before it can replace a canonical PDF."""
    if not path.is_file() or path.stat().st_size < 1024:
        raise ValueError("PDF vừa render bị thiếu hoặc có kích thước không hợp lệ")
    with path.open("rb") as stream:
        if stream.read(5) != b"%PDF-":
            raise ValueError("Đầu ra vừa render không có PDF header hợp lệ")
        stream.seek(max(0, path.stat().st_size - 2048))
        if b"%%EOF" not in stream.read():
            raise ValueError("Đầu ra vừa render không có PDF EOF marker")


def isolated_project(source: Path, directory: Path) -> Path:
    """Variant builds must never let Quarto's intermediate PDF touch production."""
    config = discover_project_config(ROOT, source.relative_to(ROOT))
    if config is None:
        raise ValueError("Isolated variant build requires project configuration")
    mirror = directory / "project"
    mirror.mkdir()
    # Keep root configuration/theme and shared assets byte-identical. No .git,
    # docs, caches or audit trees are copied into the disposable build context.
    for path in ROOT.iterdir():
        if path.is_file():
            shutil.copy2(path, mirror / path.name)
    for relative in (Path("assets"), Path("scripts"), config.project_root):
        shutil.copytree(ROOT / relative, mirror / relative, dirs_exist_ok=True,
                        ignore=shutil.ignore_patterns("__pycache__", ".quarto", "*_files"))
    for parent in source.parent.parents:
        if parent == ROOT:
            break
        for name in ("_metadata.yml", "_metadata.yaml"):
            path = parent / name
            if path.is_file():
                target = mirror / path.relative_to(ROOT)
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(path, target)
    return mirror


def build(source: Path, variant: str = "full") -> int:
    definition = pdf_variant(ROOT, source, variant)
    destination = output_path(source, variant)
    canonical_provenance = canonical_pdf_provenance_enabled(ROOT, source)
    input_state = canonical_variant_input_state(ROOT, source, variant) if canonical_provenance else None
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
        build_root = ROOT
        if definition:
            build_root = isolated_project(source, temp_dir)
            command[1] = str(build_root / "scripts" / "zo_quarto.py")
            command[-1] = "_audit/pdf_output"
            if definition.get("include_support", True) is False:
                support = build_root / "assets" / "tex" / "zo-pdf-support.tex"
                support.write_text(
                    "% Intentionally omitted for this isolated PDF variant.\n",
                    encoding="utf-8",
                )
        if definition:
            metadata = dict(definition.get("metadata", {}))
            metadata["zo-pdf-variant"] = variant
            metadata["zo-pdf-output"] = definition["output"]
            metadata_file = temp_dir / "variant.json"
            metadata_file.write_text(json.dumps(metadata, ensure_ascii=False), encoding="utf-8")
            command.extend(["--metadata-file", str(metadata_file)])
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
            cwd=build_root,
            check=False,
            env=environment,
        )
        if completed.returncode != 0:
            return completed.returncode

        output_root = build_root / "_audit/pdf_output" if definition else temp_dir
        expected = output_root / source.relative_to(ROOT).with_suffix(".pdf")
        if not expected.is_file():
            matches = list(output_root.rglob(f"{source.stem}.pdf"))
            if len(matches) != 1:
                print("Không xác định được duy nhất tệp PDF vừa render.", file=sys.stderr)
                return 1
            expected = matches[0]

        validate_rendered_pdf(expected)
        if input_state is not None and canonical_variant_input_state(ROOT, source, variant) != input_state:
            print("PDF inputs changed during render; canonical output was not replaced.", file=sys.stderr)
            return 1
        replacement = destination.with_name(f".{destination.name}.zo-pdf-replacement")
        shutil.copy2(expected, replacement)
        validate_rendered_pdf(replacement)
        replacement.replace(destination)
        receipt = write_pdf_build_receipt(ROOT, source, destination, variant=variant)
        manifest = None
        if input_state is not None:
            manifest = update_canonical_pdf_provenance(
                ROOT,
                source,
                destination,
                variant=variant,
                expected_input_state=input_state,
            )
        print(f"PDF created: {relative_to_root(destination)}")
        print(f"PDF build receipt: {relative_to_root(receipt)}")
        if manifest is not None:
            print(f"Canonical PDF provenance: {relative_to_root(manifest)}")
        return 0
    finally:
        replacement = destination.with_name(f".{destination.name}.zo-pdf-replacement")
        if replacement.is_file():
            replacement.unlink()
        shutil.rmtree(temp_dir, ignore_errors=True)


def status(source: Path, variant: str = "full") -> int:
    destination = output_path(source, variant)
    if not destination.is_file():
        print(f"MISSING: {relative_to_root(destination)}")
        return 1
    if canonical_pdf_provenance_enabled(ROOT, source):
        errors = validate_canonical_pdf_provenance(ROOT, source, variant=variant)
        label = "CURRENT" if not errors else "STALE"
        detail = "Canonical Git-tracked provenance manifest; mtime and local audit receipts are not used."
        if errors:
            detail += " " + "; ".join(errors) + "."
        print(f"{label}: {relative_to_root(destination)} | {detail}")
        return 0 if not errors else 2
    try:
        freshness = evaluate_artifact_freshness(ROOT, source, destination)
    except (FreshnessError, OSError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    receipt_errors = validate_pdf_build_receipt(ROOT, source, destination, variant=variant)
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
        command.add_argument("--variant", default="full")
    subparsers.add_parser("self-test")
    return result


def main() -> int:
    args = parser().parse_args()
    if args.command == "self-test":
        return self_test()
    try:
        if args.command == "build":
            return build(args.source, args.variant)
        return status(args.source, args.variant)
    except (ValueError, OSError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
