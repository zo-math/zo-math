"""Canonical PDF build provenance contract for ZO Math."""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from typing import Any

from pypdf import PdfReader

from zo_qmd_config import discover_project_config

PDF_BUILD_RECEIPT_VERSION = 1
PDF_BUILD_GENERATOR = "scripts/zo_pdf.py"
PDF_BUILD_COMMAND = "build"
PDF_BUILD_PROFILE = "pdf"
PDF_VARIANT_NAME = re.compile(r"^[a-z][a-z0-9_]*$")
PDF_PROVENANCE_SCHEMA_VERSION = 1
PDF_PROVENANCE_CONFIG_KEY = "pdf_provenance_manifest"
ARTIFACT_ROOT_INPUTS_CONFIG_KEY = "artifact_root_inputs"

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


def _safe_relative_path(raw: Any, field: str) -> Path:
    if not isinstance(raw, str) or not raw or "\\" in raw:
        raise ValueError(f"{field} must be a normalized relative path")
    relative = Path(raw)
    if (
        relative.is_absolute()
        or raw != relative.as_posix()
        or any(part in ("", ".", "..") for part in relative.parts)
    ):
        raise ValueError(f"Unsafe path in {field}: {raw}")
    return relative


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
    if not isinstance(variants, dict) or not {"full", "student"}.issubset(variants):
        raise ValueError("pdf_variants must declare at least full and student")
    outputs = []
    for name, definition in variants.items():
        if not isinstance(name, str) or not PDF_VARIANT_NAME.fullmatch(name):
            raise ValueError(f"Invalid PDF variant name: {name}")
        if not isinstance(definition, dict):
            raise ValueError(f"Invalid PDF variant: {name}")
        output = definition.get("output", "")
        if not isinstance(output, str) or not output or Path(output).name != output or "\\" in output or "/" in output or Path(output).suffix != ".pdf":
            raise ValueError(f"Unsafe PDF output: {output}")
        if not isinstance(definition.get("metadata", {}), dict):
            raise ValueError(f"Invalid PDF variant metadata: {name}")
        if "include_support" in definition and not isinstance(definition["include_support"], bool):
            raise ValueError(f"Invalid include_support flag: {name}")
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
    root_declared = config.raw.get("extensions", {}).get(ARTIFACT_ROOT_INPUTS_CONFIG_KEY, [])
    if not isinstance(root_declared, list) or not all(isinstance(p, str) for p in root_declared):
        raise ValueError(f"extensions.{ARTIFACT_ROOT_INPUTS_CONFIG_KEY} must be a list of repository-relative paths")
    for raw in root_declared:
        relative = _safe_relative_path(raw, f"extensions.{ARTIFACT_ROOT_INPUTS_CONFIG_KEY}")
        absolute = (root / relative).resolve()
        absolute.relative_to(root.resolve())
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


def canonical_pdf_provenance_path(root: Path, source: Path) -> Path | None:
    """Return the tracked manifest path for projects that explicitly opt in."""
    root = root.resolve()
    source = source.resolve()
    config = discover_project_config(root, _relative(root, source))
    raw = config.raw.get("extensions", {}).get(PDF_PROVENANCE_CONFIG_KEY) if config else None
    if raw is None:
        return None
    relative = _safe_relative_path(raw, f"extensions.{PDF_PROVENANCE_CONFIG_KEY}")
    candidate = (root / config.project_root / relative).resolve()
    candidate.relative_to((root / config.project_root).resolve())
    return candidate


def canonical_pdf_provenance_enabled(root: Path, source: Path) -> bool:
    return canonical_pdf_provenance_path(root, source) is not None


def _variant_registry(root: Path, source: Path) -> dict[str, dict[str, Any]]:
    config = discover_project_config(root, _relative(root, source))
    variants = config.raw.get("extensions", {}).get("pdf_variants") if config else None
    if not isinstance(variants, dict):
        raise ValueError("Canonical PDF provenance requires pdf_variants")
    # pdf_variant performs all name, definition, and output collision checks.
    for name in variants:
        pdf_variant(root, source, name)
    return variants


def _canonical_json_hash(value: Any) -> str:
    encoded = json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def canonical_variant_input_state(
    root: Path,
    source: Path,
    variant: str = "full",
) -> dict[str, Any]:
    """Capture the deterministic inputs whose equality permits certification."""
    root = root.resolve()
    source = source.resolve()
    definition = pdf_variant(root, source, variant)
    if definition is None:
        raise ValueError("Canonical PDF provenance is available only to registered variants")
    if canonical_pdf_provenance_path(root, source) is None:
        raise ValueError("Project has not enabled canonical PDF provenance")
    source_record = {
        "path": _relative(root, source).as_posix(),
        "sha256": sha256_file(source),
    }
    pipeline = _pipeline_records(root, source)
    fingerprint_payload = {
        "generator": PDF_BUILD_GENERATOR,
        "profile": PDF_BUILD_PROFILE,
        "source": source_record,
        "pipeline_inputs": pipeline,
        "variant": variant,
        "variant_definition": definition,
    }
    return {
        "source": source_record,
        "pipeline_inputs": pipeline,
        "variant": variant,
        "variant_definition": definition,
        "input_fingerprint": _canonical_json_hash(fingerprint_payload),
    }


def pdf_inventory(path: Path) -> dict[str, int]:
    if not path.is_file():
        raise FileNotFoundError(path)
    return {"pages": len(PdfReader(str(path)).pages)}


def _load_manifest(path: Path) -> dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise ValueError(f"Cannot read canonical PDF provenance manifest: {exc}") from exc
    if not isinstance(payload, dict):
        raise ValueError("Canonical PDF provenance manifest must be a JSON object")
    return payload


def _record_map(payload: dict[str, Any]) -> tuple[dict[str, dict[str, Any]], list[str]]:
    errors: list[str] = []
    raw_records = payload.get("variants")
    if not isinstance(raw_records, list):
        return {}, ["variants must be a list"]
    records: dict[str, dict[str, Any]] = {}
    for index, record in enumerate(raw_records):
        if not isinstance(record, dict) or not isinstance(record.get("name"), str):
            errors.append(f"variants[{index}] is invalid")
            continue
        name = record["name"]
        if name in records:
            errors.append(f"duplicate variant: {name}")
            continue
        records[name] = record
    return records, errors


def update_canonical_pdf_provenance(
    root: Path,
    source: Path,
    output: Path,
    *,
    variant: str = "full",
    expected_input_state: dict[str, Any] | None = None,
) -> Path:
    """Atomically update only the just-built variant in the tracked manifest."""
    root = root.resolve()
    source = source.resolve()
    output = output.resolve()
    manifest = canonical_pdf_provenance_path(root, source)
    if manifest is None:
        raise ValueError("Project has not enabled canonical PDF provenance")
    state = canonical_variant_input_state(root, source, variant)
    if expected_input_state is not None and state != expected_input_state:
        raise RuntimeError("PDF inputs changed during the build; provenance was not updated")
    expected_output = pdf_output_path(root, source, variant).resolve()
    if output != expected_output:
        raise ValueError("PDF output does not match its registered variant")
    output_record = {
        "path": _relative(root, output).as_posix(),
        "sha256": sha256_file(output),
    }
    record = {
        "name": variant,
        "definition": state["variant_definition"],
        "output": output_record,
        "input_fingerprint": state["input_fingerprint"],
        "inventory": pdf_inventory(output),
    }

    existing: dict[str, dict[str, Any]] = {}
    if manifest.is_file():
        try:
            existing, _ = _record_map(_load_manifest(manifest))
        except ValueError:
            existing = {}
    existing[variant] = record
    registry = _variant_registry(root, source)
    payload = {
        "pdf_provenance_schema_version": PDF_PROVENANCE_SCHEMA_VERSION,
        "generator": PDF_BUILD_GENERATOR,
        "profile": PDF_BUILD_PROFILE,
        "source": state["source"],
        "pipeline_inputs": state["pipeline_inputs"],
        "variants": [existing[name] for name in registry if name in existing],
    }
    manifest_relative = _relative(root, manifest)
    input_paths = set(pipeline_input_paths(root, source))
    if manifest_relative in input_paths:
        raise ValueError("The provenance manifest must not hash itself")
    manifest.parent.mkdir(parents=True, exist_ok=True)
    replacement = manifest.with_name(f".{manifest.name}.zo-provenance-replacement")
    try:
        with replacement.open("w", encoding="utf-8", newline="\n") as handle:
            handle.write(json.dumps(payload, ensure_ascii=False, indent=2) + "\n")
        replacement.replace(manifest)
    finally:
        if replacement.is_file():
            replacement.unlink()
    return manifest


def validate_canonical_pdf_provenance(
    root: Path,
    source: Path,
    *,
    variant: str = "full",
) -> list[str]:
    """Validate CURRENT without mtime or local audit receipts."""
    root = root.resolve()
    source = source.resolve()
    errors: list[str] = []
    try:
        manifest = canonical_pdf_provenance_path(root, source)
        registry = _variant_registry(root, source)
    except (ValueError, OSError) as exc:
        return [f"invalid canonical PDF provenance configuration: {exc}"]
    if manifest is None:
        return ["canonical PDF provenance is not enabled"]
    if not manifest.is_file():
        return [f"missing canonical PDF provenance manifest: {_relative(root, manifest).as_posix()}"]
    try:
        payload = _load_manifest(manifest)
    except ValueError as exc:
        return [str(exc)]
    if payload.get("pdf_provenance_schema_version") != PDF_PROVENANCE_SCHEMA_VERSION:
        errors.append(f"pdf_provenance_schema_version must equal {PDF_PROVENANCE_SCHEMA_VERSION}")
    if payload.get("generator") != PDF_BUILD_GENERATOR:
        errors.append(f"generator must equal {PDF_BUILD_GENERATOR}")
    if payload.get("profile") != PDF_BUILD_PROFILE:
        errors.append(f"profile must equal {PDF_BUILD_PROFILE}")

    try:
        expected_state = canonical_variant_input_state(root, source, variant)
    except (ValueError, OSError) as exc:
        return errors + [f"cannot capture current PDF inputs: {exc}"]
    source_record = payload.get("source")
    if source_record != expected_state["source"]:
        errors.append("source record does not match the current QMD")

    raw_pipeline = payload.get("pipeline_inputs")
    expected_pipeline = expected_state["pipeline_inputs"]
    if not isinstance(raw_pipeline, list):
        errors.append("pipeline_inputs must be a list")
    else:
        actual_paths: list[str] = []
        for index, item in enumerate(raw_pipeline):
            if not isinstance(item, dict) or not isinstance(item.get("path"), str):
                errors.append(f"pipeline_inputs[{index}] is invalid")
                continue
            try:
                _safe_relative_path(item["path"], f"pipeline_inputs[{index}].path")
            except ValueError as exc:
                errors.append(str(exc))
            actual_paths.append(item["path"])
        if len(actual_paths) != len(set(actual_paths)):
            errors.append("pipeline_inputs contains duplicate paths")
        if raw_pipeline != expected_pipeline:
            errors.append("pipeline_inputs do not match the current dependency set and hashes")
    try:
        if _relative(root, manifest) in set(pipeline_input_paths(root, source)):
            errors.append("the provenance manifest hashes itself")
    except (ValueError, OSError) as exc:
        errors.append(f"cannot validate pipeline input paths: {exc}")

    records, record_errors = _record_map(payload)
    errors.extend(record_errors)
    expected_names = list(registry)
    raw_names = [item.get("name") for item in payload.get("variants", []) if isinstance(item, dict)] if isinstance(payload.get("variants"), list) else []
    if raw_names != expected_names:
        errors.append("variant list does not exactly match registry order")
    for name, definition in registry.items():
        record = records.get(name)
        if record is None:
            errors.append(f"missing variant: {name}")
            continue
        if record.get("definition") != definition:
            errors.append(f"variant definition drift: {name}")
        output = pdf_output_path(root, source, name).resolve()
        expected_output_path = _relative(root, output).as_posix()
        output_record = record.get("output")
        if not isinstance(output_record, dict):
            errors.append(f"missing output record: {name}")
        else:
            raw_path = output_record.get("path")
            try:
                _safe_relative_path(raw_path, f"variants[{name}].output.path")
            except ValueError as exc:
                errors.append(str(exc))
            if raw_path != expected_output_path:
                errors.append(f"output path drift: {name}")

    requested = records.get(variant)
    if variant not in registry:
        errors.append(f"unknown variant: {variant}")
    elif requested is not None:
        if requested.get("input_fingerprint") != expected_state["input_fingerprint"]:
            errors.append(f"input fingerprint drift: {variant}")
        output = pdf_output_path(root, source, variant).resolve()
        output_record = requested.get("output")
        if not output.is_file():
            errors.append(f"missing PDF output: {_relative(root, output).as_posix()}")
        elif not isinstance(output_record, dict) or output_record.get("sha256") != sha256_file(output):
            errors.append(f"PDF hash drift: {variant}")
        else:
            try:
                if requested.get("inventory") != pdf_inventory(output):
                    errors.append(f"PDF inventory drift: {variant}")
            except (OSError, ValueError) as exc:
                errors.append(f"cannot read PDF inventory for {variant}: {exc}")
    return errors
