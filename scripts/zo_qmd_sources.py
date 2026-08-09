"""Discover and fingerprint authority sources for ZO Math QMD operations.

This module describes the sources an agent must read or observe before QMD
production starts. It does not claim that an agent has actually consumed those
sources; acknowledgement is handled by the operations layer.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable

from zo_qmd_config import (
    ProjectConfig,
    ProjectConfigError,
    discover_project_config,
    load_yaml_document,
)


SYSTEM_AUTHORITY_DOCUMENTS = (
    Path("AGENTS.md"),
    Path("quy_trinh_xay_dung/quy_tac_lam_viec_voi_agent.md"),
    Path("quy_trinh_xay_dung/quy_trinh_thuc_hien_nhiem_vu_ky_thuat.md"),
    Path("quy_trinh_xay_dung/he_thong_san_xuat_qmd/README.md"),
)


@dataclass(frozen=True)
class AuthoritySource:
    path: Path
    role: str
    action: str = "read"
    condition: str | None = None


class AuthoritySourceError(RuntimeError):
    """Raised when authority-source discovery cannot be completed safely."""


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def agent_chain(root: Path, relative: Path) -> list[Path]:
    target = root / relative
    start = target if target.is_dir() else target.parent
    try:
        start_relative = start.resolve().relative_to(root.resolve())
    except ValueError as exc:
        raise AuthoritySourceError(
            f"Đường dẫn nằm ngoài repository: {relative.as_posix()}."
        ) from exc

    chain: list[Path] = []
    current = Path()
    root_agents = Path("AGENTS.md")

    if (root / root_agents).is_file():
        chain.append(root_agents)

    for part in start_relative.parts:
        current /= part
        candidate = current / "AGENTS.md"
        if candidate != root_agents and (root / candidate).is_file():
            chain.append(candidate)

    return chain


def reference_paths(config: ProjectConfig, key: str) -> list[Path]:
    references = config.raw.get("references", {})
    values = references.get(key, []) if isinstance(references, dict) else []
    result: list[Path] = []

    for value in values if isinstance(values, list) else []:
        if isinstance(value, str) and value.strip():
            result.append(config.project_root / Path(value))

    return result


def _add(
    mapping: dict[Path, AuthoritySource],
    source: AuthoritySource,
) -> None:
    mapping.setdefault(source.path, source)


def discover_authority_sources(
    root: Path,
    relative: Path,
    *,
    config: ProjectConfig | None = None,
    require_project: bool = True,
) -> dict[str, list[AuthoritySource]]:
    required: dict[Path, AuthoritySource] = {}
    conditional: dict[Path, AuthoritySource] = {}

    for path in SYSTEM_AUTHORITY_DOCUMENTS:
        _add(required, AuthoritySource(path, "system_instruction"))

    for path in agent_chain(root, relative):
        _add(required, AuthoritySource(path, "project_instruction"))

    if config is None:
        try:
            config = discover_project_config(root, relative)
        except ProjectConfigError as exc:
            raise AuthoritySourceError(str(exc)) from exc

    if config is None:
        if require_project:
            raise AuthoritySourceError(
                f"Không tìm thấy cấu hình dự án cho {relative.as_posix()}."
            )
        return {
            "required": [
                required[path]
                for path in sorted(required, key=lambda item: item.as_posix())
            ],
            "conditional": [],
        }

    _add(
        required,
        AuthoritySource(config.config_path, "project_config"),
    )

    article_type = config.article_type_for(relative)
    if article_type is not None:
        profile = config.profile_path_for(relative)
        profile_exists = (root / profile).is_file()
        target_exists = (root / relative).is_file()
        if profile_exists or (config.profile_required and target_exists):
            _add(
                required,
                AuthoritySource(profile, "production_profile"),
            )

    for path in reference_paths(config, "controlling_documents"):
        _add(
            required,
            AuthoritySource(path, "controlling_document"),
        )

    for path in reference_paths(config, "templates"):
        _add(
            required,
            AuthoritySource(path, "template"),
        )

    for path in reference_paths(config, "quality_exemplars"):
        action = "observe" if path.suffix.lower() == ".pdf" else "read"
        _add(
            required,
            AuthoritySource(path, "quality_exemplar", action),
        )

    for path in reference_paths(config, "theory_sources"):
        if path not in required:
            _add(
                conditional,
                AuthoritySource(
                    path,
                    "theory_source",
                    "read",
                    "Đọc khi quy chuẩn nén chưa đủ cho trường hợp đang xét.",
                ),
            )

    return {
        "required": [
            required[path]
            for path in sorted(required, key=lambda item: item.as_posix())
        ],
        "conditional": [
            conditional[path]
            for path in sorted(conditional, key=lambda item: item.as_posix())
        ],
    }


def source_record(root: Path, source: AuthoritySource) -> dict[str, Any]:
    absolute = root / source.path
    exists = absolute.is_file()

    record: dict[str, Any] = {
        "path": source.path.as_posix(),
        "role": source.role,
        "action": source.action,
        "exists": exists,
        "sha256": sha256_file(absolute) if exists else None,
    }

    if source.condition is not None:
        record["condition"] = source.condition

    return record


def authority_manifest(
    root: Path,
    relative: Path,
    *,
    config: ProjectConfig | None = None,
) -> dict[str, Any]:
    discovered = discover_authority_sources(
        root,
        relative,
        config=config,
    )

    required = [
        source_record(root, source)
        for source in discovered["required"]
    ]
    conditional = [
        source_record(root, source)
        for source in discovered["conditional"]
    ]

    fingerprint_payload = [
        {
            "path": record["path"],
            "role": record["role"],
            "action": record["action"],
            "sha256": record["sha256"],
        }
        for record in required
    ]

    canonical = json.dumps(
        fingerprint_payload,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")

    return {
        "required": required,
        "conditional": conditional,
        "fingerprint_algorithm": "sha256",
        "fingerprint": hashlib.sha256(canonical).hexdigest(),
        "missing_required": [
            record["path"]
            for record in required
            if not record["exists"]
        ],
    }


def provenance_manifest(root: Path, profile_path: Path) -> dict[str, Any]:
    """Check expected checksums declared by a production profile."""

    absolute_profile = root / profile_path
    if not absolute_profile.is_file():
        return {
            "profile_path": profile_path.as_posix(),
            "status": "profile_missing",
            "sources": [],
            "blocked": False,
        }

    raw = load_yaml_document(absolute_profile)
    if not isinstance(raw, dict):
        raise AuthoritySourceError("Hồ sơ sản xuất phải là một YAML mapping.")
    controls = raw.get("tai_lieu_dieu_khien", {})
    if controls is None:
        controls = {}
    if not isinstance(controls, dict):
        raise AuthoritySourceError("tai_lieu_dieu_khien phải là một mapping.")

    sources: list[dict[str, Any]] = []
    for source_id, declaration in controls.items():
        if not isinstance(declaration, dict) or "sha256_ki_vong" not in declaration:
            continue
        raw_path = declaration.get("duong_dan")
        expected = declaration.get("sha256_ki_vong")
        if not isinstance(source_id, str) or not isinstance(raw_path, str) or not raw_path.strip():
            raise AuthoritySourceError("Khai báo provenance phải có id và duong_dan hợp lệ.")
        if not isinstance(expected, str) or len(expected.strip()) != 64 or any(
            character not in "0123456789abcdefABCDEF" for character in expected.strip()
        ):
            raise AuthoritySourceError(
                f"sha256_ki_vong của {source_id!r} phải là SHA-256 hợp lệ."
            )

        source_path = Path(raw_path.strip())
        if source_path.is_absolute():
            raise AuthoritySourceError(f"Đường dẫn provenance phải tương đối: {raw_path}")
        resolved = (root / source_path).resolve()
        try:
            relative = resolved.relative_to(root.resolve())
        except ValueError as exc:
            raise AuthoritySourceError(
                f"Đường dẫn provenance nằm ngoài repository: {raw_path}"
            ) from exc

        exists = resolved.is_file()
        actual = sha256_file(resolved) if exists else None
        expected_normalized = expected.strip().lower()
        status = "pass" if actual == expected_normalized else ("mismatch" if exists else "missing")
        used = declaration.get("da_dung") is True
        locations = declaration.get("vi_tri_da_dung", [])
        if locations is None:
            locations = []
        if not isinstance(locations, list):
            raise AuthoritySourceError(
                f"vi_tri_da_dung của {source_id!r} phải là danh sách."
            )
        blocked = status != "pass" and used
        sources.append(
            {
                "id": source_id,
                "path": relative.as_posix(),
                "expected_sha256": expected_normalized,
                "actual_sha256": actual,
                "status": status,
                "da_dung": used,
                "vi_tri_da_dung": locations,
                "blocked": blocked,
            }
        )

    blocked = any(source["blocked"] for source in sources)
    if blocked:
        status = "blocked"
    elif any(source["status"] != "pass" for source in sources):
        status = "recorded"
    else:
        status = "pass"
    return {
        "profile_path": profile_path.as_posix(),
        "status": status,
        "sources": sources,
        "blocked": blocked,
    }


def _write(root: Path, relative: Path, text: str) -> None:
    path = root / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


def self_test() -> int:
    with tempfile.TemporaryDirectory(prefix="zo-qmd-sources-self-test-") as raw:
        root = Path(raw)

        _write(root, Path("AGENTS.md"), "# Root instructions\n")
        _write(
            root,
            Path("quy_trinh_xay_dung/quy_tac_lam_viec_voi_agent.md"),
            "# Rules\n",
        )
        _write(
            root,
            Path("quy_trinh_xay_dung/quy_trinh_thuc_hien_nhiem_vu_ky_thuat.md"),
            "# Workflow\n",
        )
        _write(
            root,
            Path("quy_trinh_xay_dung/he_thong_san_xuat_qmd/README.md"),
            "# QMD operations\n",
        )

        project = Path("content/demo")
        article = project / "core/demo.qmd"
        profile = project / "_quy_trinh/ho_so/demo.yml"
        config_path = project / "_quy_trinh/cau_hinh_san_xuat_qmd.yml"

        _write(root, project / "AGENTS.md", "# Project instructions\n")
        _write(root, article, "---\ntitle: Demo\n---\n")
        _write(root, profile, "production: in_production\n")
        _write(root, project / "_quy_trinh/rules.md", "# Rules\n")
        _write(root, project / "_quy_trinh/template.qmd", "# Template\n")
        _write(root, project / "_quy_trinh/theory.qmd", "# Theory\n")
        _write(root, project / "depth/exemplar.qmd", "# Exemplar\n")
        _write(root, project / "depth/exemplar.pdf", "fake-pdf-for-self-test\n")

        _write(
            root,
            config_path,
            """\
schema_version: 1
project:
  id: demo
  name: Demo
  root: content/demo
discovery:
  article_types:
    - id: demo_article
      include:
        - core/*.qmd
      exclude: []
profiles:
  directory: _quy_trinh/ho_so
  naming: by_article_stem
  required: true
modules:
  required:
    - qmd-core
  optional: []
metadata:
  core_required: []
  project_required: []
  body_classes_required: []
  placeholders: []
publication:
  production_states:
    - draft
    - in_production
    - validated
    - accepted
  publication_states:
    - pending
    - published
  user_confirmation_required: true
references:
  controlling_documents:
    - _quy_trinh/rules.md
  templates:
    - _quy_trinh/template.qmd
  theory_sources:
    - _quy_trinh/theory.qmd
  quality_exemplars:
    - depth/exemplar.qmd
    - depth/exemplar.pdf
regression:
  articles: []
  expected_checker_version: null
  preserve_cli: true
extensions: {}
""",
        )

        manifest = authority_manifest(root, article)

        required = {
            item["path"]: item
            for item in manifest["required"]
        }
        conditional = {
            item["path"]: item
            for item in manifest["conditional"]
        }

        expected_required = {
            "AGENTS.md",
            "quy_trinh_xay_dung/quy_tac_lam_viec_voi_agent.md",
            "quy_trinh_xay_dung/quy_trinh_thuc_hien_nhiem_vu_ky_thuat.md",
            "quy_trinh_xay_dung/he_thong_san_xuat_qmd/README.md",
            "content/demo/AGENTS.md",
            "content/demo/_quy_trinh/cau_hinh_san_xuat_qmd.yml",
            "content/demo/_quy_trinh/ho_so/demo.yml",
            "content/demo/_quy_trinh/rules.md",
            "content/demo/_quy_trinh/template.qmd",
            "content/demo/depth/exemplar.qmd",
            "content/demo/depth/exemplar.pdf",
        }

        if set(required) != expected_required:
            raise AuthoritySourceError(
                "Self-test: tập nguồn bắt buộc không đúng."
            )

        theory = "content/demo/_quy_trinh/theory.qmd"
        if set(conditional) != {theory}:
            raise AuthoritySourceError(
                "Self-test: theory source phải là conditional."
            )

        exemplar_pdf = required["content/demo/depth/exemplar.pdf"]
        if exemplar_pdf["action"] != "observe":
            raise AuthoritySourceError(
                "Self-test: quality exemplar PDF phải yêu cầu observe."
            )

        if manifest["missing_required"]:
            raise AuthoritySourceError(
                "Self-test: không được báo thiếu nguồn trong fixture đầy đủ."
            )

        first_fingerprint = manifest["fingerprint"]
        _write(root, project / "_quy_trinh/rules.md", "# Changed rules\n")
        second_fingerprint = authority_manifest(root, article)["fingerprint"]

        if first_fingerprint == second_fingerprint:
            raise AuthoritySourceError(
                "Self-test: fingerprint không đổi khi nguồn bắt buộc thay đổi."
            )

        template = project / "_quy_trinh/template.qmd"
        (root / template).unlink()
        missing = authority_manifest(root, article)["missing_required"]
        if template.as_posix() not in missing:
            raise AuthoritySourceError(
                "Self-test: không phát hiện nguồn bắt buộc bị thiếu."
            )

        _write(root, template, "# Template restored\n")

        (root / profile).unlink()
        missing_profile = authority_manifest(root, article)["missing_required"]
        if profile.as_posix() not in missing_profile:
            raise AuthoritySourceError(
                "Self-test: bài đã tồn tại phải báo thiếu production profile bắt buộc."
            )

        new_article = project / "core/new_demo.qmd"
        new_profile = project / "_quy_trinh/ho_so/new_demo.yml"
        new_manifest = authority_manifest(root, new_article)
        new_required = {
            item["path"]
            for item in new_manifest["required"]
        }

        if new_profile.as_posix() in new_manifest["missing_required"]:
            raise AuthoritySourceError(
                "Self-test: bài mới không được bị chặn vì profile chưa được tạo."
            )

        if new_profile.as_posix() in new_required:
            raise AuthoritySourceError(
                "Self-test: profile chưa tồn tại của bài mới chưa phải authority source."
            )

        provenance_source = project / "_quy_trinh/theory-provenance.qmd"
        _write(root, provenance_source, "# Provenance source\n")
        actual = sha256_file(root / provenance_source)

        def write_provenance(expected: str, used: bool, *, missing: bool = False) -> dict[str, Any]:
            declared = project / "_quy_trinh/missing.qmd" if missing else provenance_source
            _write(
                root,
                profile,
                "tai_lieu_dieu_khien:\n"
                "  nguon_li_thuyet_day_du:\n"
                f"    duong_dan: {declared.as_posix()}\n"
                f"    sha256_ki_vong: '{expected}'\n"
                f"    da_dung: {'true' if used else 'false'}\n"
                "    vi_tri_da_dung:\n"
                "      - Mệnh đề fixture\n",
            )
            return provenance_manifest(root, profile)

        matching = write_provenance(actual, True)
        if matching["status"] != "pass" or matching["blocked"]:
            raise AuthoritySourceError("Self-test: SHA khớp + đã dùng phải PASS.")

        wrong = "0" * 64 if actual != "0" * 64 else "1" * 64
        unused_mismatch = write_provenance(wrong, False)
        if unused_mismatch["status"] != "recorded" or unused_mismatch["blocked"]:
            raise AuthoritySourceError("Self-test: SHA sai + chưa dùng phải record, không BLOCK.")

        used_mismatch = write_provenance(wrong, True)
        if used_mismatch["status"] != "blocked" or not used_mismatch["blocked"]:
            raise AuthoritySourceError("Self-test: SHA sai + đã dùng phải BLOCK.")
        evidence = used_mismatch["sources"][0]
        if evidence["vi_tri_da_dung"] != ["Mệnh đề fixture"]:
            raise AuthoritySourceError("Self-test: provenance không giữ vi_tri_da_dung.")

        missing_used = write_provenance(actual, True, missing=True)
        if missing_used["sources"][0]["status"] != "missing" or not missing_used["blocked"]:
            raise AuthoritySourceError("Self-test: nguồn thiếu + đã dùng phải BLOCK.")

    print("PASS: zo_qmd_sources self-test")
    return 0


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(description=__doc__)
    subparsers = result.add_subparsers(dest="command", required=True)
    subparsers.add_parser("self-test", help="Chạy kiểm tra nội bộ.")
    return result


def main() -> int:
    args = parser().parse_args()
    if args.command == "self-test":
        try:
            return self_test()
        except (
            AuthoritySourceError,
            ProjectConfigError,
            OSError,
            ValueError,
        ) as exc:
            print(f"Authority source self-test thất bại: {exc}")
            return 1
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
