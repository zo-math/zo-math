#!/usr/bin/env python3
"""Kiểm tra dữ liệu kiến trúc học tập của các gói Ôn thi Toán THPT."""

from __future__ import annotations

import argparse
import copy
import json
import re
import sys
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable

import yaml


REPO_ROOT = Path(__file__).resolve().parents[1]
COMMON_DIR = REPO_ROOT / "content/thpt/on_thi_toan_thpt/_quy_trinh"
COMMON_CATALOG = COMMON_DIR / "danh_muc_kien_truc_hoc_tap.yml"
SCHEMA_PATH = COMMON_DIR / "schema_kien_truc_hoc_tap.json"
DEFAULT_MANIFESTS = (
    REPO_ROOT / "content/thpt/on_thi_toan_thpt/hoc_lieu/r1_g01/_quy_trinh/kien_truc_hoc_tap.yml",
    REPO_ROOT / "content/thpt/on_thi_toan_thpt/hoc_lieu/r1_g02/_quy_trinh/kien_truc_hoc_tap.yml",
)


class UniqueKeyLoader(yaml.SafeLoader):
    """Safe YAML loader that rejects duplicate mapping keys."""


def _construct_mapping(loader: UniqueKeyLoader, node: yaml.MappingNode, deep: bool = False) -> dict[str, Any]:
    mapping: dict[str, Any] = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        if key in mapping:
            raise ValueError(f"khóa YAML bị trùng: {key}")
        mapping[key] = loader.construct_object(value_node, deep=deep)
    return mapping


UniqueKeyLoader.add_constructor(
    yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
    _construct_mapping,
)


@dataclass(frozen=True)
class Issue:
    code: str
    message: str

    def __str__(self) -> str:
        return f"[{self.code}] {self.message}"


def load_yaml(path: Path) -> dict[str, Any]:
    data = yaml.load(path.read_text(encoding="utf-8"), Loader=UniqueKeyLoader)
    if not isinstance(data, dict):
        raise ValueError(f"gốc YAML phải là mapping: {path}")
    return data


def load_common() -> dict[str, Any]:
    common = load_yaml(COMMON_CATALOG)
    json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    return common


def extract_anchors(source: Path) -> set[str]:
    text = source.read_text(encoding="utf-8")
    return set(re.findall(r"\{#([^\s}.]+)", text))


def extract_item_task_anchors(source: Path) -> set[str]:
    text = source.read_text(encoding="utf-8")
    return set(
        re.findall(
            r"\{#([^\s}.]+)[^}\n]*\.zo-learning-task--item[^}\n]*\}",
            text,
        )
    )


def _as_list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def _id_map(
    manifest: dict[str, Any],
    field: str,
    issues: list[Issue],
) -> dict[str, dict[str, Any]]:
    records = manifest.get(field)
    if not isinstance(records, list):
        issues.append(Issue("schema.type", f"{field} phải là danh sách"))
        return {}
    result: dict[str, dict[str, Any]] = {}
    for index, record in enumerate(records):
        if not isinstance(record, dict):
            issues.append(Issue("schema.type", f"{field}[{index}] phải là mapping"))
            continue
        item_id = record.get("id")
        if not isinstance(item_id, str) or not item_id.strip():
            issues.append(Issue("id.missing", f"{field}[{index}] thiếu id"))
            continue
        if item_id in result:
            issues.append(Issue("id.duplicate", f"{field} trùng id {item_id}"))
            continue
        result[item_id] = record
    return result


def _require_keys(record: dict[str, Any], keys: Iterable[str], where: str, issues: list[Issue]) -> None:
    for key in keys:
        if key not in record:
            issues.append(Issue("schema.required", f"{where} thiếu trường {key}"))


def _check_refs(
    values: Any,
    known: set[str],
    where: str,
    issues: list[Issue],
    *,
    allow_empty: bool = True,
) -> None:
    if not isinstance(values, list):
        issues.append(Issue("schema.type", f"{where} phải là danh sách"))
        return
    if not allow_empty and not values:
        issues.append(Issue("link.empty", f"{where} không được rỗng"))
    duplicates = sorted(key for key, count in Counter(values).items() if count > 1)
    if duplicates:
        issues.append(Issue("id.duplicate-reference", f"{where} trùng tham chiếu: {', '.join(duplicates)}"))
    missing = sorted(value for value in values if value not in known)
    if missing:
        issues.append(Issue("link.broken", f"{where} trỏ tới id không tồn tại: {', '.join(missing)}"))


def validate_manifest(
    manifest: dict[str, Any],
    manifest_path: Path,
    common: dict[str, Any] | None = None,
) -> list[Issue]:
    common = common or load_common()
    issues: list[Issue] = []
    package = manifest.get("package")
    package_id = package.get("id") if isinstance(package, dict) else manifest_path.stem

    required_top = (
        "schema_version",
        "architecture_version",
        "matrix_version",
        "package",
        "source",
        "policies",
        "objectives",
        "stages",
        "checkpoints",
        "tasks",
        "errors",
        "foundation_routes",
        "readiness",
    )
    _require_keys(manifest, required_top, str(package_id), issues)
    if manifest.get("schema_version") != 1:
        issues.append(Issue("schema.version", f"{package_id}: schema_version phải bằng 1"))
    if manifest.get("architecture_version") != "0.2":
        issues.append(Issue("architecture.version", f"{package_id}: architecture_version phải bằng 0.2"))
    if manifest.get("matrix_version") != "0.1":
        issues.append(Issue("matrix.version", f"{package_id}: matrix_version phải bằng 0.1"))

    objectives = _id_map(manifest, "objectives", issues)
    stages = _id_map(manifest, "stages", issues)
    checkpoints = _id_map(manifest, "checkpoints", issues)
    tasks = _id_map(manifest, "tasks", issues)
    errors = _id_map(manifest, "errors", issues)
    foundation_routes = _id_map(manifest, "foundation_routes", issues)

    source_data = manifest.get("source")
    source_path: Path | None = None
    anchors: set[str] = set()
    item_task_anchors: set[str] = set()
    if not isinstance(source_data, dict) or not isinstance(source_data.get("qmd"), str):
        issues.append(Issue("source.missing", f"{package_id}: source.qmd không hợp lệ"))
    else:
        source_path = (manifest_path.parent / source_data["qmd"]).resolve()
        if not source_path.is_file():
            issues.append(Issue("source.missing", f"{package_id}: không tồn tại nguồn {source_path}"))
        else:
            anchors = extract_anchors(source_path)
            item_task_anchors = extract_item_task_anchors(source_path)

    objective_ids = set(objectives)
    stage_ids = set(stages)
    checkpoint_ids = set(checkpoints)
    task_ids = set(tasks)
    error_ids = set(errors)
    route_ids = set(foundation_routes)
    unit_ids = {
        item.get("id")
        for item in common.get("foundation_catalog", {}).get("units", [])
        if isinstance(item, dict) and isinstance(item.get("id"), str)
    }
    valid_roles = set(_as_list(common.get("valid_task_roles")))
    valid_statuses = set(_as_list(common.get("valid_task_statuses")))

    for objective_id, objective in objectives.items():
        _require_keys(
            objective,
            ("description", "essential", "prerequisite_ids", "dependent_objective_ids"),
            objective_id,
            issues,
        )
        if not isinstance(objective.get("description"), str) or not objective.get("description", "").strip():
            issues.append(Issue("objective.description", f"{objective_id} thiếu mô tả"))
        if not isinstance(objective.get("essential"), bool):
            issues.append(Issue("objective.essential", f"{objective_id}.essential phải là boolean"))
        _check_refs(objective.get("prerequisite_ids"), objective_ids, f"{objective_id}.prerequisite_ids", issues)
        _check_refs(
            objective.get("dependent_objective_ids"),
            objective_ids,
            f"{objective_id}.dependent_objective_ids",
            issues,
        )

    for stage_id, stage in stages.items():
        _require_keys(
            stage,
            ("description", "objective_ids", "learning_section_anchors", "practice_task_ids", "checkpoint_id"),
            stage_id,
            issues,
        )
        _check_refs(stage.get("objective_ids"), objective_ids, f"{stage_id}.objective_ids", issues, allow_empty=False)
        _check_refs(stage.get("practice_task_ids"), task_ids, f"{stage_id}.practice_task_ids", issues, allow_empty=False)
        checkpoint_id = stage.get("checkpoint_id")
        if not isinstance(checkpoint_id, str) or checkpoint_id not in checkpoints:
            issues.append(Issue("stage.checkpoint", f"{stage_id} thiếu điểm kiểm soát tồn tại"))
        section_anchors = stage.get("learning_section_anchors")
        if not isinstance(section_anchors, list) or not section_anchors:
            issues.append(Issue("stage.learning-sections", f"{stage_id} thiếu learning_section_anchors"))
        else:
            missing = sorted(anchor for anchor in section_anchors if anchor not in anchors)
            if missing:
                issues.append(Issue("anchor.missing", f"{stage_id} thiếu anchor nguồn: {', '.join(missing)}"))

    valid_path_kinds = set(_as_list(common.get("transition_path_kinds")))
    for checkpoint_id, checkpoint in checkpoints.items():
        _require_keys(checkpoint, ("evidence_task_ids", "paths"), checkpoint_id, issues)
        _check_refs(
            checkpoint.get("evidence_task_ids"),
            task_ids,
            f"{checkpoint_id}.evidence_task_ids",
            issues,
            allow_empty=False,
        )
        paths = checkpoint.get("paths")
        if not isinstance(paths, dict):
            issues.append(Issue("checkpoint.paths", f"{checkpoint_id} thiếu paths"))
            continue
        for branch in ("pass", "error", "foundation"):
            path = paths.get(branch)
            if not isinstance(path, dict):
                issues.append(Issue("checkpoint.path", f"{checkpoint_id} thiếu đường {branch}"))
                continue
            kind = path.get("kind")
            targets = path.get("target_ids")
            if kind not in valid_path_kinds:
                issues.append(Issue("checkpoint.path-kind", f"{checkpoint_id}.{branch} có kind không hợp lệ: {kind}"))
                continue
            known: set[str]
            allow_empty = False
            if kind == "stage":
                known = stage_ids
            elif kind == "checkpoint":
                known = checkpoint_ids
            elif kind == "remediation":
                known = error_ids
            elif kind == "foundation":
                known = route_ids
            elif kind == "transfer":
                known = checkpoint_ids | task_ids | stage_ids
            else:
                known = set()
                allow_empty = True
            _check_refs(targets, known, f"{checkpoint_id}.paths.{branch}.target_ids", issues, allow_empty=allow_empty)

    anchors_to_tasks: dict[str, list[dict[str, Any]]] = defaultdict(list)
    content_keys: dict[str, str] = {}
    for task_id, task in tasks.items():
        _require_keys(
            task,
            (
                "role",
                "status",
                "objective_ids",
                "error_ids",
                "checkpoint_ids",
                "source_anchor",
                "source_locator",
                "answer_anchor",
                "content_key",
                "exposure_policy",
                "next_on_pass",
                "next_on_error",
            ),
            task_id,
            issues,
        )
        role = task.get("role")
        status = task.get("status")
        if not isinstance(role, str) or role not in valid_roles:
            issues.append(Issue("task.role", f"{task_id} có role không hợp lệ: {role}"))
        if isinstance(role, list):
            issues.append(Issue("task.dual-role", f"{task_id} không được mang hai vai trò bằng chứng"))
        if status not in valid_statuses:
            issues.append(Issue("task.status", f"{task_id} có status không hợp lệ: {status}"))
        _check_refs(task.get("objective_ids"), objective_ids, f"{task_id}.objective_ids", issues, allow_empty=False)
        _check_refs(task.get("error_ids"), error_ids, f"{task_id}.error_ids", issues)
        _check_refs(task.get("checkpoint_ids"), checkpoint_ids, f"{task_id}.checkpoint_ids", issues, allow_empty=False)
        for field in ("next_on_pass", "next_on_error"):
            target = task.get(field)
            if not isinstance(target, str) or target not in checkpoint_ids:
                issues.append(Issue("task.path", f"{task_id}.{field} không trỏ tới checkpoint tồn tại"))
        source_anchor = task.get("source_anchor")
        answer_anchor = task.get("answer_anchor")
        if status == "current":
            if not isinstance(source_anchor, str) or source_anchor not in anchors:
                issues.append(Issue("anchor.missing", f"{task_id} thiếu source_anchor tồn tại: {source_anchor}"))
            else:
                anchors_to_tasks[source_anchor].append(task)
            if not isinstance(answer_anchor, str) or answer_anchor not in anchors:
                issues.append(Issue("anchor.missing", f"{task_id} thiếu answer_anchor tồn tại: {answer_anchor}"))
        elif status == "planned" and (source_anchor is not None or answer_anchor is not None):
            issues.append(Issue("planned.fake-anchor", f"{task_id} planned không được khai anchor nội dung giả"))
        content_key = task.get("content_key")
        if not isinstance(content_key, str) or not content_key.strip():
            issues.append(Issue("task.content-key", f"{task_id} thiếu content_key"))
        elif content_key in content_keys:
            issues.append(
                Issue(
                    "task.exposure-leak",
                    f"{task_id} dùng lại content_key của {content_keys[content_key]}: {content_key}",
                )
            )
        else:
            content_keys[content_key] = task_id
        policy_by_role = {
            "L": "practice",
            "S-L": "remediation",
            "S-K": "remediation",
            "S-O": "remediation",
            "K": "independent",
            "O": "review-reserved",
            "P": "transfer",
            "H": "guided",
            "N": "foundation",
        }
        expected_policy = policy_by_role.get(role) if isinstance(role, str) else None
        if expected_policy and task.get("exposure_policy") != expected_policy:
            issues.append(
                Issue(
                    "task.exposure-policy",
                    f"{task_id} role {role} phải dùng exposure_policy {expected_policy}",
                )
            )

    for anchor, anchored_tasks in anchors_to_tasks.items():
        if len(anchored_tasks) < 2:
            continue
        locators = [task.get("source_locator") for task in anchored_tasks]
        if any(not isinstance(locator, str) or not locator.strip() for locator in locators) or len(set(locators)) != len(locators):
            issues.append(Issue("anchor.ambiguous", f"anchor dùng chung {anchor} phải có source_locator riêng cho từng nhiệm vụ"))

    mapped_current_anchors = {
        task.get("source_anchor")
        for task in tasks.values()
        if task.get("status") == "current" and isinstance(task.get("source_anchor"), str)
    }
    unmapped_item_anchors = sorted(item_task_anchors - mapped_current_anchors)
    if unmapped_item_anchors:
        issues.append(
            Issue(
                "source.task-unmapped",
                "nhiệm vụ item hiện có chưa được manifest ánh xạ: " + ", ".join(unmapped_item_anchors),
            )
        )

    for objective_id, objective in objectives.items():
        if objective.get("essential") is True:
            evidence = [
                task_id
                for task_id, task in tasks.items()
                if task.get("role") == "K" and objective_id in _as_list(task.get("objective_ids"))
            ]
            if not evidence:
                issues.append(Issue("objective.no-k", f"mục tiêu thiết yếu {objective_id} không có nhiệm vụ K"))

    role_for_remediation = {"S-L": "S-L", "S-K": "S-K", "S-O": "S-O"}
    for error_id, error in errors.items():
        _require_keys(
            error,
            (
                "symptom",
                "classification_rule",
                "objective_ids",
                "detection_checkpoint_ids",
                "review_anchor",
                "foundation_route_ids",
                "remediation",
                "return_anchor",
            ),
            error_id,
            issues,
        )
        _check_refs(error.get("objective_ids"), objective_ids, f"{error_id}.objective_ids", issues, allow_empty=False)
        detection = error.get("detection_checkpoint_ids")
        _check_refs(detection, checkpoint_ids, f"{error_id}.detection_checkpoint_ids", issues, allow_empty=False)
        _check_refs(error.get("foundation_route_ids"), route_ids, f"{error_id}.foundation_route_ids", issues)
        for field in ("review_anchor", "return_anchor"):
            anchor = error.get(field)
            if not isinstance(anchor, str) or anchor not in anchors:
                issues.append(Issue("anchor.missing", f"{error_id}.{field} không tồn tại: {anchor}"))
        remediation = error.get("remediation")
        if not isinstance(remediation, dict):
            issues.append(Issue("error.remediation", f"{error_id} thiếu remediation"))
            continue
        required_layers: set[str] = set()
        for checkpoint_id in _as_list(detection):
            if checkpoint_id.startswith("CP-LT"):
                required_layers.add("S-L")
            elif checkpoint_id == "CP-KT":
                required_layers.add("S-K")
            elif checkpoint_id.startswith("CP-ON"):
                required_layers.add("S-O")
        for layer in ("S-L", "S-K", "S-O"):
            task_id = remediation.get(layer)
            if layer in required_layers and not isinstance(task_id, str):
                issues.append(Issue("error.remediation-missing", f"{error_id} thiếu tuyến {layer}"))
                continue
            if task_id is None:
                continue
            task = tasks.get(task_id)
            if task is None:
                issues.append(Issue("link.broken", f"{error_id}.{layer} trỏ tới task không tồn tại: {task_id}"))
            elif task.get("role") != role_for_remediation[layer] or error_id not in _as_list(task.get("error_ids")):
                issues.append(Issue("error.remediation-role", f"{task_id} không phải tuyến {layer} hợp lệ cho {error_id}"))

    for route_id, route in foundation_routes.items():
        _require_keys(route, ("objective_ids", "symptom", "unit_id", "retest", "return_anchors"), route_id, issues)
        _check_refs(route.get("objective_ids"), objective_ids, f"{route_id}.objective_ids", issues, allow_empty=False)
        if route.get("unit_id") not in unit_ids:
            issues.append(Issue("foundation.unit", f"{route_id} trỏ tới đơn vị N không tồn tại: {route.get('unit_id')}"))
        retest = route.get("retest")
        if not isinstance(retest, dict) or retest.get("status") != "specified" or not isinstance(retest.get("requirement"), str) or not retest.get("requirement", "").strip():
            issues.append(Issue("foundation.retest", f"{route_id} thiếu câu kiểm tra lại được đặc tả"))
        return_anchors = route.get("return_anchors")
        if not isinstance(return_anchors, list) or not return_anchors:
            issues.append(Issue("foundation.return", f"{route_id} thiếu điểm quay về"))
        else:
            missing = sorted(anchor for anchor in return_anchors if anchor not in anchors)
            if missing:
                issues.append(Issue("anchor.missing", f"{route_id} thiếu return_anchor nguồn: {', '.join(missing)}"))

    readiness = manifest.get("readiness")
    expected = readiness.get("expected_planned_task_ids") if isinstance(readiness, dict) else None
    planned = sorted(task_id for task_id, task in tasks.items() if task.get("status") == "planned")
    if not isinstance(expected, list):
        issues.append(Issue("readiness.expected", f"{package_id} thiếu expected_planned_task_ids"))
    elif sorted(expected) != planned:
        issues.append(
            Issue(
                "readiness.mismatch",
                f"{package_id}: planned thực tế không khớp ma trận khai báo",
            )
        )

    return issues


def planned_tasks(manifest: dict[str, Any]) -> list[dict[str, Any]]:
    return sorted(
        (copy.deepcopy(task) for task in _as_list(manifest.get("tasks")) if isinstance(task, dict) and task.get("status") == "planned"),
        key=lambda task: task.get("id", ""),
    )


def _resolve_manifest_paths(values: list[str] | None) -> list[Path]:
    if not values:
        return list(DEFAULT_MANIFESTS)
    return [(REPO_ROOT / value).resolve() if not Path(value).is_absolute() else Path(value).resolve() for value in values]


def run(mode: str, paths: list[Path]) -> int:
    common = load_common()
    loaded: list[tuple[Path, dict[str, Any]]] = []
    all_issues: list[tuple[Path, Issue]] = []
    for path in paths:
        try:
            manifest = load_yaml(path)
        except (OSError, ValueError, yaml.YAMLError) as exc:
            all_issues.append((path, Issue("manifest.load", str(exc))))
            continue
        loaded.append((path, manifest))
        all_issues.extend((path, issue) for issue in validate_manifest(manifest, path, common))

    if all_issues:
        for path, issue in all_issues:
            print(f"FAIL {path.relative_to(REPO_ROOT) if path.is_relative_to(REPO_ROOT) else path}: {issue}")
        print(f"RESULT: FAIL | issues={len(all_issues)}")
        return 1

    if mode == "schema":
        for path, manifest in loaded:
            package_id = manifest["package"]["id"]
            print(
                f"PASS {package_id}: objectives={len(manifest['objectives'])} "
                f"stages={len(manifest['stages'])} checkpoints={len(manifest['checkpoints'])} "
                f"tasks={len(manifest['tasks'])} errors={len(manifest['errors'])} "
                f"foundation_routes={len(manifest['foundation_routes'])}"
            )
        print("RESULT: PASS")
        return 0

    missing_count = 0
    for _path, manifest in loaded:
        package_id = manifest["package"]["id"]
        missing = planned_tasks(manifest)
        missing_count += len(missing)
        print(f"{package_id}: planned={len(missing)}")
        for task in missing:
            print(f"  - {task['id']} | role={task['role']}" + (f" | subtype={task['subtype']}" if task.get("subtype") else ""))
    if missing_count:
        print(f"RESULT: NOT READY | planned={missing_count}")
        return 2
    print("RESULT: PASS | planned=0")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=("schema", "readiness"))
    parser.add_argument(
        "manifests",
        nargs="*",
        help="Đường dẫn manifest; bỏ trống để kiểm cả R1-G01 và R1-G02.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        return run(args.mode, _resolve_manifest_paths(args.manifests))
    except (OSError, ValueError, json.JSONDecodeError, yaml.YAMLError) as exc:
        print(f"RESULT: FAIL | {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
