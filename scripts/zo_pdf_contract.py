"""Canonical PDF build provenance contract for ZO Math."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

PDF_BUILD_RECEIPT_VERSION = 1
PDF_BUILD_GENERATOR = "scripts/zo_pdf.py"
PDF_BUILD_COMMAND = "build"
PDF_BUILD_PROFILE = "pdf"

CANONICAL_PDF_PIPELINE_INPUTS = (
    Path("_quarto-pdf.yml"),
    Path("assets/lua/zo_pdf_branding.lua"),
    Path("assets/lua/zo_pdf_content.lua"),
    Path("assets/tex/zo-pdf.tex"),
    Path("assets/tex/zo-pdf-rights.tex"),
    Path("assets/tex/zo-pdf-support.tex"),
    Path("scripts/zo_pdf.py"),
    Path("scripts/zo_quarto.py"),
)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _relative(root: Path, path: Path) -> Path:
    return path.resolve().relative_to(root.resolve())


def pdf_build_receipt_path(root: Path, source: Path) -> Path:
    return root / "_audit" / f"{source.stem}_pdf_build.json"


def _pipeline_records(root: Path) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for relative in CANONICAL_PDF_PIPELINE_INPUTS:
        absolute = root / relative
        if not absolute.is_file():
            raise FileNotFoundError(f"Thiếu đầu vào PDF canonical: {relative.as_posix()}")
        records.append(
            {
                "path": relative.as_posix(),
                "sha256": sha256_file(absolute),
            }
        )
    return records


def build_pdf_receipt_payload(root: Path, source: Path, output: Path) -> dict[str, Any]:
    root = root.resolve()
    source = source.resolve()
    output = output.resolve()
    source_rel = _relative(root, source)
    output_rel = _relative(root, output)
    if not source.is_file():
        raise FileNotFoundError(f"Thiếu QMD nguồn: {source_rel.as_posix()}")
    if not output.is_file():
        raise FileNotFoundError(f"Thiếu PDF đầu ra: {output_rel.as_posix()}")
    return {
        "pdf_build_receipt_version": PDF_BUILD_RECEIPT_VERSION,
        "generator": PDF_BUILD_GENERATOR,
        "command": PDF_BUILD_COMMAND,
        "profile": PDF_BUILD_PROFILE,
        "source": {
            "path": source_rel.as_posix(),
            "sha256": sha256_file(source),
        },
        "output": {
            "path": output_rel.as_posix(),
            "sha256": sha256_file(output),
        },
        "pipeline_inputs": _pipeline_records(root),
    }


def write_pdf_build_receipt(
    root: Path,
    source: Path,
    output: Path,
    receipt_path: Path | None = None,
) -> Path:
    receipt = receipt_path or pdf_build_receipt_path(root, source)
    receipt.parent.mkdir(parents=True, exist_ok=True)
    payload = build_pdf_receipt_payload(root, source, output)
    receipt.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return receipt


def validate_pdf_build_receipt(
    root: Path,
    source: Path,
    output: Path,
    receipt_path: Path | None = None,
) -> list[str]:
    root = root.resolve()
    source = source.resolve()
    output = output.resolve()
    receipt = receipt_path or pdf_build_receipt_path(root, source)
    errors: list[str] = []

    if not receipt.is_file():
        return [f"thiếu PDF build receipt: {_relative(root, receipt).as_posix()}"]

    try:
        payload = json.loads(receipt.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        return [f"không đọc được PDF build receipt: {exc}"]
    if not isinstance(payload, dict):
        return ["PDF build receipt phải là JSON object"]

    if payload.get("pdf_build_receipt_version") != PDF_BUILD_RECEIPT_VERSION:
        errors.append(
            f"pdf_build_receipt_version phải bằng {PDF_BUILD_RECEIPT_VERSION}"
        )
    if payload.get("generator") != PDF_BUILD_GENERATOR:
        errors.append(f"generator phải là {PDF_BUILD_GENERATOR}")
    if payload.get("command") != PDF_BUILD_COMMAND:
        errors.append(f"command phải là {PDF_BUILD_COMMAND}")
    if payload.get("profile") != PDF_BUILD_PROFILE:
        errors.append(f"profile phải là {PDF_BUILD_PROFILE}")

    try:
        source_rel = _relative(root, source).as_posix()
        output_rel = _relative(root, output).as_posix()
    except ValueError:
        return ["QMD/PDF nằm ngoài repository"]

    source_record = payload.get("source")
    output_record = payload.get("output")
    if not isinstance(source_record, dict):
        errors.append("thiếu source record")
    else:
        if source_record.get("path") != source_rel:
            errors.append("source.path không khớp QMD hiện hành")
        if not source.is_file() or source_record.get("sha256") != sha256_file(source):
            errors.append("source.sha256 không khớp QMD hiện hành")

    if not isinstance(output_record, dict):
        errors.append("thiếu output record")
    else:
        if output_record.get("path") != output_rel:
            errors.append("output.path không khớp PDF hiện hành")
        if not output.is_file() or output_record.get("sha256") != sha256_file(output):
            errors.append("output.sha256 không khớp PDF hiện hành")

    expected_paths = [path.as_posix() for path in CANONICAL_PDF_PIPELINE_INPUTS]
    raw_pipeline = payload.get("pipeline_inputs")
    if not isinstance(raw_pipeline, list):
        errors.append("thiếu pipeline_inputs")
        raw_pipeline = []
    actual_map: dict[str, Any] = {}
    for item in raw_pipeline:
        if isinstance(item, dict) and isinstance(item.get("path"), str):
            actual_map[str(item["path"])] = item.get("sha256")

    if set(actual_map) != set(expected_paths):
        missing = sorted(set(expected_paths) - set(actual_map))
        extra = sorted(set(actual_map) - set(expected_paths))
        if missing:
            errors.append("pipeline_inputs thiếu: " + ", ".join(missing))
        if extra:
            errors.append("pipeline_inputs thừa: " + ", ".join(extra))

    for relative in CANONICAL_PDF_PIPELINE_INPUTS:
        absolute = root / relative
        if not absolute.is_file():
            errors.append(f"đầu vào PDF canonical đã mất: {relative.as_posix()}")
            continue
        expected_hash = actual_map.get(relative.as_posix())
        current_hash = sha256_file(absolute)
        if expected_hash != current_hash:
            errors.append(f"pipeline input drift: {relative.as_posix()}")

    return errors
