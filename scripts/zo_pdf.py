from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from zo_artifact_freshness import FreshnessError, evaluate_artifact_freshness
from zo_qmd_config import discover_project_config
from zo_graphics import graph_path
from zo_pdf_contract import (
    canonical_pdf_provenance_enabled,
    canonical_variant_input_state,
    pdf_build_receipt_path,
    pdf_output_path,
    pipeline_input_paths,
    pdf_variant,
    update_canonical_pdf_provenance,
    validate_canonical_pdf_provenance,
    validate_pdf_build_receipt,
    write_pdf_build_receipt,
)


ROOT = Path(__file__).resolve().parents[1]
AUDIT_DIR = ROOT / "_audit"
BUILD_DIR = ROOT / '.quarto' / 'zo_pdf_build'
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
                        ignore=shutil.ignore_patterns("__pycache__", ".quarto", "_audit", "*_files"))
    for parent in source.parent.parents:
        if parent == ROOT:
            break
        for name in ("_metadata.yml", "_metadata.yaml"):
            path = parent / name
            if path.is_file():
                target = mirror / path.relative_to(ROOT)
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(path, target)
    # Includes outside the package are declared canonical dependencies too.
    # Copy them explicitly; the mirror must never resolve them from old HTML.
    for relative in pipeline_input_paths(ROOT, source):
        if graph_path(ROOT / relative, ROOT) != (ROOT / relative).resolve():
            # External tools stay external, including inside isolated builds.
            # The launcher propagates ZO_MATH_GRAPHICS_ROOT to the child.
            continue
        target = mirror / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(ROOT / relative, target)
    return mirror


def verify_course_graph_paths(source: Path, text: str | None = None) -> None:
    if source.parent.name != 'r1_g02':
        return
    text = source.read_text(encoding='utf-8') if text is None else text
    references = re.findall(r'\]\(([^)\s]+\.(?:svg|pdf))\)', text)
    graphs = [p for p in references if re.fullmatch(r'(?:nen_)?do_thi_\d{2}\.(?:svg|pdf)', Path(p).name)]
    expected = {'giao_dien/assets/figures_0_4/'+n+'.svg' for n in ['do_thi_01','do_thi_02','nen_do_thi_01','nen_do_thi_02']}
    if len(graphs) != 4 or set(graphs) != expected:
        raise ValueError('G02 QMD must select exactly the four current shared graph SVG/PDF pairs.')


def build(source: Path, variant: str = "full", preflight: bool = False,
          output_directory: Path | None = None) -> int:
    verify_course_graph_paths(source)
    # Fail before the expensive Quarto render if any current graph pair drifts.
    if source.parent.name == 'r1_g01':
        from zo_web_2027_figures import verify_print
        verify_print()
    if source.parent.name == 'r1_g02':
        from zo_web_2027_g02_payloads import verify_print
        verify_print()
    definition = pdf_variant(ROOT, source, variant)
    destination = output_path(source, variant)
    if output_directory is not None:
        output_directory = output_directory.resolve()
        if not output_directory.is_relative_to(ROOT / '.quarto'):
            raise ValueError('Candidate PDF output directory must be inside .quarto')
        output_directory.mkdir(parents=True, exist_ok=True)
        destination = output_directory / destination.name
        if destination.exists():
            raise ValueError('Candidate PDF already exists: ' + str(destination))
    canonical_provenance = canonical_pdf_provenance_enabled(ROOT, source)
    input_state = canonical_variant_input_state(ROOT, source, variant) if canonical_provenance else None
    BUILD_DIR.mkdir(parents=True, exist_ok=True)
    temp_dir = Path(tempfile.mkdtemp(prefix="zo_pdf_", dir=BUILD_DIR))
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
    if preflight:
        command[command.index('--to')+1]='latex'

    try:
        build_root = ROOT
        if definition:
            build_root = isolated_project(source, temp_dir)
            command[1] = str(build_root / "scripts" / "zo_quarto.py")
            command[-1] = ".quarto/pdf_output"
            if definition.get("include_support", True) is False:
                support = build_root / "assets" / "tex" / "zo-pdf-support.tex"
                support.write_text(
                    "% Intentionally omitted for this isolated PDF variant.\n",
                    encoding="utf-8",
                )
        if definition:
            metadata = dict(definition.get("metadata", {}))
            from zo_pdf_course_shell import prepare as prepare_course_shell
            course_shell = prepare_course_shell(ROOT, build_root, source, definition)
            if course_shell:
                metadata["zo-course-pdf-shell"] = True
                metadata["geometry"] = ["top=22mm", "bottom=22mm", "left=21mm", "right=21mm"]
            metadata["zo-pdf-variant"] = variant
            metadata["zo-pdf-output"] = definition["output"]
            metadata_file = temp_dir / "variant.json"
            metadata_file.write_text(json.dumps(metadata, ensure_ascii=False), encoding="utf-8")
            command.extend(["--metadata-file", str(metadata_file)])
        environment = os.environ.copy()
        quarto = shutil.which("quarto", path=environment.get("PATH"))
        if quarto is not None:
            environment["ZO_QUARTO_EXECUTABLE"] = quarto
        tex_resource_dirs = [
            str((ROOT / "assets" / "logo").resolve()),
            str((ROOT / "assets" / "images").resolve()),
        ]
        if definition and course_shell:
            tex_resource_dirs.insert(0, str(course_shell['runtime']))
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

        if preflight:
            candidates=list((build_root/'.quarto/pdf_output').rglob(source.stem+'.tex'))
            if len(candidates)!=1:raise ValueError('Preflight TeX output is missing or ambiguous')
            shutil.copyfile(candidates[0],AUDIT_DIR/(source.parent.name+'_'+variant+'_preflight.tex'))
            print('PREFLIGHT PASS: source, projection, current figures and TeX emitted without compiling the book.')
            return 0

        output_root = build_root / '.quarto/pdf_output' if definition else temp_dir
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
        if output_directory is not None:
            from zo_pdf_contract import sha256_file
            receipt = destination.with_suffix('.pdf.build.json')
            receipt.write_text(json.dumps({
                'candidate_build_schema_version': 1,
                'generator': 'scripts/zo_pdf.py', 'variant': variant,
                'input_state': input_state,
                'output': {'path': relative_to_root(destination), 'sha256': sha256_file(destination)},
                'canonical_output_replaced': False,
            }, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
        else:
            receipt = write_pdf_build_receipt(ROOT, source, destination, variant=variant)
        manifest = None
        if input_state is not None and output_directory is None:
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
    for name in ("build", "status", "preflight"):
        command = subparsers.add_parser(name)
        command.add_argument("source", type=source_path)
        command.add_argument("--variant", default="full")
        if name == 'build':
            command.add_argument('--out-dir', type=Path, help='Build a candidate under .quarto without replacing registered PDFs or provenance')
    subparsers.add_parser("self-test")
    return result


def main() -> int:
    args = parser().parse_args()
    if args.command == "self-test":
        return self_test()
    try:
        if args.command in ("build", "preflight"):
            return build(args.source, args.variant, args.command=='preflight', getattr(args, 'out_dir', None))
        return status(args.source, args.variant)
    except (ValueError, OSError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
