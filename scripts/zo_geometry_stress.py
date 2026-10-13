"""Reproducible stress matrix for the isolated ZO Geometry prototype."""

from __future__ import annotations

import copy
import json
import math
from pathlib import Path
from typing import Any

from zo_geometry_check import check_layout, check_svg, load_yaml
from zo_geometry import (
    GeometryError,
    render_3d,
    render_cone,
    render_cylinder,
    render_frustum,
    render_sphere,
    validate,
)


HERE = Path(__file__).resolve().parent / "fixtures" / "geometry"


FAMILIES = {
    "polyhedron": "s06_oblique_hexagonal_section.yaml",
    "cylinder": "c05_cylinder_section.yaml",
    "cone": "c06_cone_section.yaml",
    "frustum": "c04_frustum.yaml",
    "sphere": "c07_sphere_circle.yaml",
}

VIEWS = {
    "normal": {"elevation": 68, "azimuth": 118},
    "near_frontal": {"elevation": 76, "azimuth": 118},
    "near_top": {"elevation": 48, "azimuth": 118},
    "reversed": {"elevation": 68, "azimuth": 298},
}

FAMILY_VIEW_OVERRIDES = {
    ("polyhedron", "near_top"): {"elevation": 30, "azimuth": 118},
}


def resolved_camera(family: str, view_name: str) -> dict[str, float]:
    return dict(FAMILY_VIEW_OVERRIDES.get((family, view_name), VIEWS[view_name]))


def camera_readability(camera: dict[str, Any]) -> dict[str, float]:
    """Cheap projection guard: horizontal circles must retain visible depth."""
    elevation = float(camera["elevation"])
    circle_minor_ratio = abs(math.cos(math.radians(elevation)))
    return {"horizontal_circle_minor_ratio": circle_minor_ratio}

ANCHORS = [
    "above=4pt", "below=4pt", "left=4pt", "right=4pt",
    "above left=4pt and 4pt", "above right=4pt and 4pt",
    "below left=4pt and 4pt", "below right=4pt and 4pt",
    "above=9pt", "below=9pt", "left=9pt", "right=9pt",
    "above left=8pt and 8pt", "above right=8pt and 8pt",
    "below left=8pt and 8pt", "below right=8pt and 8pt",
]


def adapt_labels(data: dict[str, Any]) -> list[dict[str, str]]:
    """Camera-local coordinate descent over approved anchor and mask choices."""
    original = {str(label["target"]): (str(label["anchor"]), str(label["mask"])) for label in data["labels"]}
    for _ in range(6):
        changed = False
        for label in data["labels"]:
            current = (str(label["anchor"]), str(label["mask"]))
            best = current
            errors, warnings = check_layout(data, strict_labels=True)
            best_score = (len(errors), len(warnings), 0)
            candidates = [current, *((anchor, mask) for anchor in ANCHORS for mask in ("none", "when_required"))]
            for rank, (anchor, mask) in enumerate(candidates):
                label["anchor"], label["mask"] = anchor, mask
                candidate_errors, candidate_warnings = check_layout(data, strict_labels=True)
                score = (len(candidate_errors), len(candidate_warnings), rank)
                if score < best_score:
                    best_score, best = score, (anchor, mask)
            label["anchor"], label["mask"] = best
            changed = changed or best != current
        if not changed or not check_layout(data, strict_labels=True)[0]:
            break
    return [
        {"target": target, "from": f"{before[0]} | {before[1]}", "to": f"{label['anchor']} | {label['mask']}"}
        for target, before in original.items()
        for label in data["labels"]
        if str(label["target"]) == target and (str(label["anchor"]), str(label["mask"])) != before
    ]


def render_case(data: dict[str, Any]) -> str:
    visibility = validate(data)
    solid_type = data["solid_type"]
    if solid_type == "cylinder":
        return render_cylinder(data)
    if solid_type == "cone":
        return render_cone(data)
    if solid_type == "frustum":
        return render_frustum(data)
    if solid_type == "sphere":
        return render_sphere(data)
    assert visibility is not None
    return render_3d(data, visibility)


def negative_cases() -> list[tuple[str, dict[str, Any]]]:
    cases: list[tuple[str, dict[str, Any]]] = []
    sphere = copy.deepcopy(load_yaml(HERE / "c07_sphere_circle.yaml"))
    sphere["sphere"]["radius"] = 0
    cases.append(("sphere_zero_radius", sphere))
    cone = copy.deepcopy(load_yaml(HERE / "c06_cone_section.yaml"))
    cone["curve_section"]["z"] = 3
    cases.append(("cone_section_at_apex", cone))
    cylinder = copy.deepcopy(load_yaml(HERE / "c05_cylinder_section.yaml"))
    cylinder["curve_section"]["z_center"] = 0
    cases.append(("cylinder_section_crosses_base", cylinder))
    polyhedron = copy.deepcopy(load_yaml(HERE / "s05_polyhedron_section.yaml"))
    polyhedron["section"]["plane"]["offset"] = -3
    cases.append(("section_through_apex", polyhedron))
    collapsed = copy.deepcopy(load_yaml(HERE / "s01_box.yaml"))
    collapsed["vertices"][2]["coordinates"] = collapsed["vertices"][1]["coordinates"]
    cases.append(("degenerate_face", collapsed))
    return cases
