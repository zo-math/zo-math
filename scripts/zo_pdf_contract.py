"""Canonical PDF build provenance contract for ZO Math."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

from zo_qmd_config import discover_project_config

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


def qmd_artifact_key(root: Path, source: Path) -> str:
    """Opt-in path identity; existing projects retain their historical filenames."""
    relative = _relative(root, root / source)
    config = discover_project_config(root, relative)
    if config and config.raw.get("extensions", {}).get("artifact_identity") == "path":
        digest = hashlib.sha256(relative.as_posix().encode("utf-8")).hexdigest()[:16]
        return f"{relative.stem}_{digest}"
    return source.stem


def pdf_variant(root: Path, source: Path, variant: str = "full") -> dict[str, Any] | None:
    """Explicit project opt-in; legacy articles retain the full-only contract."""
    config = discover_project_config(root, _relative(root, root / source))
    variants = config.raw.get("extensions", {}).get("pdf_variants") if config else None
    if variants is None:
        if variant != "full":
            raise ValueError("This project has not enabled PDF variants")
        return None
    if not isinstance(variants, dict) or set(variants) != {"full", "student"}:
        raise ValueError("pdf_variants must declare full and student")
    outputs = []
    for name, definition in variants.items():
        if not isinstance(definition, dict):
            raise ValueError(f"Invalid PDF variant: {name}")
        output = definition.get("output", "")
        if not isinstance(output, str) or not output or Path(output).name != output or "\\" in output or "/" in output or Path(output).suffix != ".pdf":
            raise ValueError(f"Unsafe PDF output: {output}")
        if not isinstance(definition.get("metadata", {}), dict):
            raise ValueError(f"Invalid PDF variant metadata: {name}")
        outputs.append(output.casefold())
    if len(set(outputs)) != len(outputs):
        raise ValueError("PDF variants must not share an output")
    if variant not in variants:
        raise ValueError(f"Unknown PDF variant: {variant}")
    return variants[variant]


def pdf_output_path(root: Path, source: Path, variant: str = "full") -> Path:
    definition = pdf_variant(root, source, variant)
    return source.with_name(definition["output"]) if definition else source.with_suffix(".pdf")


def pdf_build_receipt_path(root: Path, source: Path, variant: str = "full") -> Path:
    suffix = f"_{variant}" if pdf_variant(root, source, variant) else ""
    return root / "_audit" / f"{qmd_artifact_key(root, source)}{suffix}_pdf_build.json"


def pipeline_input_paths(root: Path, source: Path | None = None) -> tuple[Path, ...]:
    paths = list(CANONICAL_PDF_PIPELINE_INPUTS)
    if source is None:
        return tuple(paths)
    config = discover_project_config(root, _relative(root, root / source))
    if config is None:
        return tuple(paths)
    if config.raw.get("extensions", {}).get("pdf_variants") is not None:
        paths.extend([config.config_path, Path("scripts/zo_pdf_contract.py")])
    declared = config.raw.get("extensions", {}).get("artifact_inputs", [])
    if not isinstance(declared, list) or not all(isinstance(p, str) for p in declared):
        raise ValueError("extensions.artifact_inputs must be a list of project-relative paths")
    if declared:
        paths.append(config.config_path)
    for raw in declared:
        relative = Path(raw)
        if relative.is_absolute() or ".." in relative.parts:
            raise ValueError(f"Unsafe artifact input: {raw}")
        absolute = (root / config.project_root / relative).resolve()
        absolute.relative_to((root / config.project_root).resolve())
        paths.append(absolute.relative_to(root.resolve()))
    return tuple(dict.fromkeys(paths))


def _pipeline_records(root: Path, source: Path | None = None) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for relative in pipeline_input_paths(root, source):
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


def build_pdf_receipt_payload(root: Path, source: Path, output: Path, variant: str = "full") -> dict[str, Any]:
    root = root.resolve()
    source = source.resolve()
    output = output.resolve()
    source_rel = _relative(root, source)
    output_rel = _relative(root, output)
    if not source.is_file():
        raise FileNotFoundError(f"Thiếu QMD nguồn: {source_rel.as_posix()}")
    if not output.is_file():
        raise FileNotFoundError(f"Thiếu PDF đầu ra: {output_rel.as_posix()}")
    definition = pdf_variant(root, source, variant)
    if definition and output != pdf_output_path(root, source, variant):
        raise ValueError("PDF output does not match its variant")
    payload = {
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
        "pipeline_inputs": _pipeline_records(root, source),
    }
    if definition:
        payload["variant"] = variant
        payload["variant_definition"] = definition
    return payload


def write_pdf_build_receipt(
    root: Path,
    source: Path,
    output: Path,
    receipt_path: Path | None = None,
    *, variant: str = "full",
) -> Path:
    receipt = receipt_path or pdf_build_receipt_path(root, source, variant)
    receipt.parent.mkdir(parents=True, exist_ok=True)
    payload = build_pdf_receipt_payload(root, source, output, variant)
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
    *, variant: str = "full",
) -> list[str]:
    root = root.resolve()
    source = source.resolve()
    output = output.resolve()
    definition = pdf_variant(root, source, variant)
    receipt = receipt_path or pdf_build_receipt_path(root, source, variant)
    errors: list[str] = []

    if not receipt.is_file():
        return [f"thiếu PDF build receipt: {_relative(root, receipt).as_posix()}"]

    try:
        payload = json.loads(receipt.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        return [f"không đọc được PDF build receipt: {exc}"]
    if not isinstance(payload, dict):
        return ["PDF build receipt phải là JSON object"]
    if definition:
        if payload.get("variant") != variant or payload.get("variant_definition") != definition:
            errors.append("PDF variant/definition mismatch")
        if output != pdf_output_path(root, source, variant):
            errors.append("PDF output does not match variant")
    elif payload.get("variant", "full") != "full":
        errors.append("Legacy PDF must use full variant")

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

    try:
        inputs = pipeline_input_paths(root, source)
    except (ValueError, OSError) as exc:
        return [f"invalid artifact inputs: {exc}"]
    expected_paths = [path.as_posix() for path in inputs]
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

    for relative in inputs:
        absolute = root / relative
        if not absolute.is_file():
            errors.append(f"đầu vào PDF canonical đã mất: {relative.as_posix()}")
            continue
        expected_hash = actual_map.get(relative.as_posix())
        current_hash = sha256_file(absolute)
        if expected_hash != current_hash:
            errors.append(f"pipeline input drift: {relative.as_posix()}")

    return errors
