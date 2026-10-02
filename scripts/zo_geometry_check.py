"""Semantic-layout and SVG checker for ZO Geometry v0.1."""

from __future__ import annotations

import argparse
import json
import math
import re
import sys
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

from zo_geometry import compute_section


class CheckError(RuntimeError):
    pass


@dataclass(frozen=True)
class Box:
    left: float
    bottom: float
    right: float
    top: float

    def expanded(self, margin: float) -> "Box":
        return Box(self.left - margin, self.bottom - margin, self.right + margin, self.top + margin)

    def overlaps(self, other: "Box", margin: float = 0.0) -> bool:
        return not (
            self.right + margin <= other.left
            or other.right + margin <= self.left
            or self.top + margin <= other.bottom
            or other.top + margin <= self.bottom
        )


def load_yaml(path: Path) -> dict[str, Any]:
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError) as exc:
        raise CheckError(f"Không đọc được YAML: {exc}") from exc
    if not isinstance(data, dict):
        raise CheckError("Gốc YAML phải là mapping.")
    return data


def point_projection(source: tuple[float, float], a: tuple[float, float], b: tuple[float, float]) -> tuple[float, float]:
    vx, vy = b[0] - a[0], b[1] - a[1]
    denominator = vx * vx + vy * vy
    if denominator == 0:
        raise CheckError("Không thể chiếu lên đoạn có hai đầu mút trùng nhau.")
    t = ((source[0] - a[0]) * vx + (source[1] - a[1]) * vy) / denominator
    return a[0] + t * vx, a[1] + t * vy


def circumcenter(a: tuple[float, float], b: tuple[float, float], c: tuple[float, float]) -> tuple[float, float]:
    d = 2 * (a[0] * (b[1] - c[1]) + b[0] * (c[1] - a[1]) + c[0] * (a[1] - b[1]))
    if abs(d) < 1e-9:
        raise CheckError("Không xác định tâm ngoại tiếp của ba điểm thẳng hàng.")
    ux = (
        (a[0] ** 2 + a[1] ** 2) * (b[1] - c[1])
        + (b[0] ** 2 + b[1] ** 2) * (c[1] - a[1])
        + (c[0] ** 2 + c[1] ** 2) * (a[1] - b[1])
    ) / d
    uy = (
        (a[0] ** 2 + a[1] ** 2) * (c[0] - b[0])
        + (b[0] ** 2 + b[1] ** 2) * (a[0] - c[0])
        + (c[0] ** 2 + c[1] ** 2) * (b[0] - a[0])
    ) / d
    return ux, uy


def points_2d(data: dict[str, Any]) -> dict[str, tuple[float, float]]:
    result: dict[str, tuple[float, float]] = {}
    pending = list(data["points"])
    while pending:
        progressed = False
        for point in pending[:]:
            point_id = str(point["id"])
            if "coordinates" in point:
                result[point_id] = tuple(map(float, point["coordinates"]))
            else:
                construction = point["construction"]
                refs = construction.get("onto", construction.get("points", []))
                refs = [construction.get("source"), *refs] if construction["type"] == "projection" else refs
                if any(ref not in result for ref in refs):
                    continue
                if construction["type"] == "projection":
                    result[point_id] = point_projection(
                        result[construction["source"]], result[construction["onto"][0]], result[construction["onto"][1]]
                    )
                elif construction["type"] == "circumcenter":
                    p, q, r = (result[item] for item in construction["points"])
                    result[point_id] = circumcenter(p, q, r)
                else:
                    raise CheckError(f"Phép dựng chưa hỗ trợ: {construction['type']}")
            pending.remove(point)
            progressed = True
        if not progressed:
            raise CheckError("Không giải được thứ tự phụ thuộc giữa các điểm 2D.")
    return result


def points_3d(data: dict[str, Any]) -> dict[str, tuple[float, float]]:
    theta = math.radians(float(data["camera"]["elevation"]))
    phi = math.radians(float(data["camera"]["azimuth"]))
    result: dict[str, tuple[float, float]] = {}
    source_points = {str(vertex["id"]): vertex["coordinates"] for vertex in data["vertices"]}
    section_points, _ = compute_section(data)
    source_points.update(section_points)
    for point_id, coordinates in source_points.items():
        x, y, z = map(float, coordinates)
        screen_x = math.cos(phi) * x + math.sin(phi) * y
        screen_y = -math.cos(theta) * math.sin(phi) * x + math.cos(theta) * math.cos(phi) * y + math.sin(theta) * z
        result[point_id] = screen_x, screen_y
    return result


def project_3d(coordinates: tuple[float, float, float] | list[float], camera: dict[str, Any]) -> tuple[float, float]:
    theta = math.radians(float(camera["elevation"]))
    phi = math.radians(float(camera["azimuth"]))
    x, y, z = map(float, coordinates)
    return (
        math.cos(phi) * x + math.sin(phi) * y,
        -math.cos(theta) * math.sin(phi) * x + math.cos(theta) * math.cos(phi) * y + math.sin(theta) * z,
    )


def curved_segments(data: dict[str, Any]) -> list[tuple[str, tuple[float, float], tuple[float, float]]]:
    if data["dimension"] != "3d" or data.get("solid_type") not in {"cylinder", "cone", "frustum", "sphere"}:
        return []
    vertices = {str(vertex["id"]): list(map(float, vertex["coordinates"])) for vertex in data["vertices"]}
    camera = data["camera"]
    curves: list[tuple[str, list[tuple[float, float]]]] = []

    def circle(name: str, cx: float, cy: float, z: float, radius: float) -> None:
        curves.append((name, [project_3d([cx + radius * math.cos(math.radians(t)), cy + radius * math.sin(math.radians(t)), z], camera) for t in range(0, 361, 5)]))

    solid_type = data["solid_type"]
    if solid_type == "cylinder":
        shape = data["cylinder"]
        bottom, top = vertices[shape["bottom_center"]], vertices[shape["top_center"]]
        radius = float(shape["radius"])
        circle("bottom-rim", bottom[0], bottom[1], bottom[2], radius)
        circle("top-rim", top[0], top[1], top[2], radius)
        section = data.get("curve_section")
        if section:
            coords = []
            for t in range(0, 361, 5):
                angle = math.radians(t)
                x, y = bottom[0] + radius * math.cos(angle), bottom[1] + radius * math.sin(angle)
                z = float(section["z_center"]) + float(section["x_slope"]) * (x - bottom[0]) + float(section["y_slope"]) * (y - bottom[1])
                coords.append(project_3d([x, y, z], camera))
            curves.append(("curve-section", coords))
    elif solid_type == "cone":
        shape = data["cone"]
        bottom, apex = vertices[shape["bottom_center"]], vertices[shape["apex"]]
        radius = float(shape["radius"])
        circle("bottom-rim", bottom[0], bottom[1], bottom[2], radius)
        section = data.get("curve_section")
        if section:
            z = float(section["z"])
            section_radius = radius * (apex[2] - z) / (apex[2] - bottom[2])
            circle("curve-section", bottom[0], bottom[1], z, section_radius)
    elif solid_type == "frustum":
        shape = data["frustum"]
        bottom, top = vertices[shape["bottom_center"]], vertices[shape["top_center"]]
        circle("bottom-rim", bottom[0], bottom[1], bottom[2], float(shape["bottom_radius"]))
        circle("top-rim", top[0], top[1], top[2], float(shape["top_radius"]))
    else:
        shape = data["sphere"]
        center = vertices[shape["center"]]
        radius = float(shape["radius"])
        center_screen = project_3d(center, camera)
        silhouette = [(center_screen[0] + radius * math.cos(math.radians(t)), center_screen[1] + radius * math.sin(math.radians(t))) for t in range(0, 361, 5)]
        curves.append(("silhouette", silhouette))
        circle("great-circle", center[0], center[1], center[2], radius)
        section = data.get("curve_section")
        if section:
            z_offset = float(section["z"])
            circle("curve-section", center[0], center[1], center[2] + z_offset, math.sqrt(radius * radius - z_offset * z_offset))

    return [(f"{name}-{index}", coords[index], coords[index + 1]) for name, coords in curves for index in range(len(coords) - 1)]


def visible_text_length(text: str) -> int:
    text = re.sub(r"\\[A-Za-z]+", "x", text)
    text = re.sub(r"[${}_\\,]", "", text)
    return max(1, len(text))


def anchor_direction(anchor: str) -> tuple[float, float]:
    words = anchor.split("=", 1)[0]
    dx = (-1.0 if "left" in words else 1.0 if "right" in words else 0.0)
    dy = (1.0 if "above" in words else -1.0 if "below" in words else 0.0)
    length = math.hypot(dx, dy) or 1.0
    return dx / length, dy / length


def label_box(point: tuple[float, float], label: dict[str, Any]) -> Box:
    width = 0.18 * visible_text_length(str(label["text"])) + 0.12
    height = 0.34
    anchor = str(label["anchor"])
    dx, dy = anchor_direction(anchor)
    gap = 0.055
    offsets = [float(value) * 0.03514598 for value in re.findall(r"([\d.]+)pt", anchor)]
    extra_x = offsets[1] if dx and dy and len(offsets) > 1 else offsets[0] if dx and offsets else 0.0
    extra_y = offsets[0] if dy and offsets else 0.0
    cx = point[0] + (math.copysign(width / 2 + gap + extra_x, dx) if dx else 0.0)
    cy = point[1] + (math.copysign(height / 2 + gap + extra_y, dy) if dy else 0.0)
    return Box(cx - width / 2, cy - height / 2, cx + width / 2, cy + height / 2)


def point_box(point: tuple[float, float], radius: float = 0.045) -> Box:
    return Box(point[0] - radius, point[1] - radius, point[0] + radius, point[1] + radius)


def segment_intersects_box(a: tuple[float, float], b: tuple[float, float], box: Box) -> bool:
    if box.left <= a[0] <= box.right and box.bottom <= a[1] <= box.top:
        return True
    if box.left <= b[0] <= box.right and box.bottom <= b[1] <= box.top:
        return True
    dx, dy = b[0] - a[0], b[1] - a[1]
    p = (-dx, dx, -dy, dy)
    q = (a[0] - box.left, box.right - a[0], a[1] - box.bottom, box.top - a[1])
    low, high = 0.0, 1.0
    for pi, qi in zip(p, q):
        if abs(pi) < 1e-12:
            if qi < 0:
                return False
            continue
        ratio = qi / pi
        if pi < 0:
            low = max(low, ratio)
        else:
            high = min(high, ratio)
        if low > high:
            return False
    return True


def trim_incident_endpoint(
    a: tuple[float, float],
    b: tuple[float, float],
    target_is_a: bool,
    clearance: float = 0.09,
) -> tuple[tuple[float, float], tuple[float, float]]:
    """Ignore only the point-marker neighbourhood of an incident segment."""
    start, end = (a, b) if target_is_a else (b, a)
    dx, dy = end[0] - start[0], end[1] - start[1]
    length = math.hypot(dx, dy)
    if length <= clearance:
        return end, end
    clipped = (start[0] + clearance * dx / length, start[1] + clearance * dy / length)
    return (clipped, end) if target_is_a else (end, clipped)


def segments(data: dict[str, Any]) -> list[tuple[str, str, str]]:
    result: list[tuple[str, str, str]] = []
    if data["dimension"] == "2d":
        for index, obj in enumerate(data["objects"], 1):
            if obj["type"] == "segment":
                result.append((f"object-{index}", *obj["endpoints"]))
            elif obj["type"] == "polygon":
                pts = obj["points"]
                result.extend((f"object-{index}-{i}", pts[i], pts[(i + 1) % len(pts)]) for i in range(len(pts)))
    else:
        result.extend((str(edge["id"]), *edge["endpoints"]) for edge in data.get("edges", []))
        result.extend((str(item["id"]), *item["endpoints"]) for item in data.get("segments", []))
        _, section_segments = compute_section(data)
        result.extend((str(item["id"]), *item["endpoints"]) for item in section_segments)
    return result


def check_layout(data: dict[str, Any], *, strict_labels: bool = False) -> tuple[list[str], list[str]]:
    points = points_2d(data) if data["dimension"] == "2d" else points_3d(data)
    visible_points = {
        str(point["id"])
        for point in (data["points"] if data["dimension"] == "2d" else data["vertices"])
        if point.get("draw", True)
    }
    if data["dimension"] == "3d":
        visible_points.update(map(str, data.get("section", {}).get("point_ids", [])))
    errors: list[str] = []
    warnings: list[str] = []
    boxes: dict[str, Box] = {}
    labels = data.get("labels", [])
    for label in labels:
        target = str(label["target"])
        box = label_box(points[target], label)
        clearance_box = box.expanded(0.04) if strict_labels else box
        boxes[target] = box
        if box.overlaps(point_box(points[target])):
            errors.append(f"Nhãn {target} che điểm đích.")
        for other_id, other_point in points.items():
            if other_id in visible_points and other_id != target and box.overlaps(point_box(other_point)):
                errors.append(f"Nhãn {target} che điểm {other_id}.")
        for segment_id, a_id, b_id in segments(data):
            segment_a, segment_b = points[a_id], points[b_id]
            if target == a_id:
                if not strict_labels:
                    continue
                segment_a, segment_b = trim_incident_endpoint(segment_a, segment_b, True)
            elif target == b_id:
                if not strict_labels:
                    continue
                segment_a, segment_b = trim_incident_endpoint(segment_a, segment_b, False)
            intersects_text = segment_intersects_box(segment_a, segment_b, box)
            intersects_clearance = segment_intersects_box(segment_a, segment_b, clearance_box)
            if intersects_text:
                message = f"Nhãn {target} cắt đường {segment_id}."
                if label["mask"] == "when_required":
                    warnings.append(message + " Được phép che nền.")
                else:
                    errors.append(message)
            elif strict_labels and intersects_clearance:
                errors.append(f"Nhãn {target} quá sát đường {segment_id}.")
        for curve_id, a, b in curved_segments(data):
            intersects_text = segment_intersects_box(a, b, box)
            intersects_clearance = segment_intersects_box(a, b, clearance_box)
            if intersects_text:
                message = f"Nhãn {target} cắt đường cong {curve_id}."
                if label["mask"] == "when_required":
                    warnings.append(message + " Được phép che nền.")
                else:
                    errors.append(message)
            elif strict_labels and intersects_clearance:
                errors.append(f"Nhãn {target} quá sát đường cong {curve_id}.")
    targets = list(boxes)
    for index, left in enumerate(targets):
        for right in targets[index + 1 :]:
            if boxes[left].overlaps(boxes[right], margin=0.02):
                errors.append(f"Nhãn {left} chồng nhãn {right}.")
    return errors, warnings


def local_name(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def check_svg(path: Path) -> tuple[list[str], dict[str, Any]]:
    try:
        root = ET.parse(path).getroot()
    except (OSError, ET.ParseError) as exc:
        raise CheckError(f"Không đọc được SVG: {exc}") from exc
    errors: list[str] = []
    view_box = root.attrib.get("viewBox")
    if not view_box or len(view_box.split()) != 4:
        errors.append("SVG thiếu viewBox hợp lệ.")
    elements = list(root.iter())
    raster_count = sum(local_name(item.tag) == "image" for item in elements)
    if raster_count:
        errors.append(f"SVG chứa {raster_count} phần tử raster image.")
    external_refs = []
    for item in elements:
        for key, value in item.attrib.items():
            if local_name(key) == "href" and re.match(r"^(?:https?:|file:)", value):
                external_refs.append(value)
    if external_refs:
        errors.append("SVG chứa tham chiếu ngoài.")
    vector_count = sum(local_name(item.tag) in {"path", "line", "polyline", "polygon", "circle", "ellipse"} for item in elements)
    if vector_count == 0:
        errors.append("SVG không chứa phần tử vector có thể nhận diện.")
    return errors, {"viewBox": view_box, "vector_elements": vector_count, "raster_elements": raster_count}


def main() -> int:
    parser = argparse.ArgumentParser(description="Checker layout/SVG prototype cho hình học ZO Math")
    parser.add_argument("source", type=Path)
    parser.add_argument("svg", type=Path)
    parser.add_argument("--report", type=Path)
    parser.add_argument("--strict-labels", action="store_true")
    args = parser.parse_args()
    try:
        data = load_yaml(args.source)
        layout_errors, layout_warnings = check_layout(data, strict_labels=args.strict_labels)
        svg_errors, svg_info = check_svg(args.svg)
    except (CheckError, KeyError, TypeError, ValueError) as exc:
        print(f"LỖI: {exc}", file=sys.stderr)
        return 1
    report = {
        "source": str(args.source),
        "svg": str(args.svg),
        "layout": {"errors": layout_errors, "warnings": layout_warnings},
        "svg_structure": {"errors": svg_errors, **svg_info},
        "status": "pass" if not layout_errors and not svg_errors else "fail",
        "limitation": "Va chạm được ước lượng từ mô hình nguồn; SVG từ PDF không giữ ID ngữ nghĩa TikZ.",
    }
    rendered = json.dumps(report, ensure_ascii=False, indent=2)
    if args.report:
        args.report.write_text(rendered + "\n", encoding="utf-8", newline="\n")
    print(rendered)
    return 0 if report["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
