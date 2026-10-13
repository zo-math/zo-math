"""ZO Math geometry compiler v0.1."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import subprocess
import sys
from pathlib import Path
from typing import Any

import yaml


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
STYLE_PATH = REPOSITORY_ROOT / "assets/tex/zo-geometry-styles.tex"


class GeometryError(RuntimeError):
    pass


ROLE_STYLE = {
    "visible": "zo geometry visible",
    "hidden": "zo geometry hidden",
    "auxiliary": "zo geometry auxiliary",
    "emphasized": "zo geometry main",
    "emphasized_hidden": "zo geometry main hidden",
}


def load_document(path: Path) -> dict[str, Any]:
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError) as exc:
        raise GeometryError(f"Không đọc được YAML: {exc}") from exc
    if not isinstance(data, dict):
        raise GeometryError("Gốc tài liệu YAML phải là một mapping.")
    return data


def require_keys(item: dict[str, Any], keys: tuple[str, ...], context: str) -> None:
    missing = [key for key in keys if key not in item]
    if missing:
        raise GeometryError(f"{context} thiếu trường: {', '.join(missing)}")


def validate_common(data: dict[str, Any]) -> None:
    require_keys(data, ("id", "dimension", "labels"), "Tài liệu")
    if data["dimension"] not in {"2d", "3d"}:
        raise GeometryError("dimension phải là '2d' hoặc '3d'.")
    expected_backend = "tkz-euclide" if data["dimension"] == "2d" else "tikz-3dplot"
    if data.get("backend") != expected_backend:
        raise GeometryError(f"Backend của {data['dimension']} phải là {expected_backend}.")
    labels = data.get("labels", [])
    if not isinstance(labels, list):
        raise GeometryError("labels phải là một danh sách.")
    label_targets: set[str] = set()
    for index, label in enumerate(labels, 1):
        require_keys(label, ("target", "text", "anchor", "mask"), f"Nhãn {index}")
        if label["target"] in label_targets:
            raise GeometryError(f"Nhãn trùng target: {label['target']}")
        label_targets.add(label["target"])
        if label["mask"] not in {"none", "when_required"}:
            raise GeometryError(f"mask không hợp lệ ở nhãn {label['target']}")


def validate_2d(data: dict[str, Any]) -> None:
    require_keys(data, ("points", "objects"), "Hình phẳng")
    point_ids: set[str] = set()
    for point in data["points"]:
        require_keys(point, ("id",), "Điểm")
        point_id = str(point["id"])
        if point_id in point_ids:
            raise GeometryError(f"Điểm trùng id: {point_id}")
        point_ids.add(point_id)
        if "coordinates" not in point and "construction" not in point:
            raise GeometryError(f"Điểm {point_id} thiếu coordinates hoặc construction.")
    for label in data["labels"]:
        if label["target"] not in point_ids:
            raise GeometryError(f"Nhãn tham chiếu điểm không tồn tại: {label['target']}")
    for index, obj in enumerate(data["objects"], 1):
        references = obj.get("points", obj.get("endpoints", []))
        if obj.get("type") == "circle":
            references = [obj.get("center"), obj.get("through")]
        elif obj.get("type") in {"ellipse", "parabola", "hyperbola"}:
            references = [obj.get("center", obj.get("vertex"))]
        if any(reference not in point_ids for reference in references):
            raise GeometryError(f"Đối tượng 2D số {index} tham chiếu điểm không tồn tại.")
    validate_relations_2d(data)


def validate_relations_2d(data: dict[str, Any]) -> None:
    coords = {
        str(point["id"]): tuple(map(float, point["coordinates"]))
        for point in data["points"]
        if "coordinates" in point
    }
    tolerance = 1e-5
    for relation in data.get("relations", []):
        kind = relation["type"]
        required = [relation.get("point"), *relation.get("line", [])]
        center_id = relation.get("center", relation.get("vertex"))
        if center_id:
            required.append(center_id)
        if any(item not in coords for item in required):
            raise GeometryError(f"Quan hệ {kind} chỉ hỗ trợ điểm có tọa độ tường minh trong v0.1.")
        point = coords[relation["point"]]
        line_a, line_b = (coords[item] for item in relation["line"])
        direction = (line_b[0] - line_a[0], line_b[1] - line_a[1])
        origin = coords[center_id]
        x, y = point[0] - origin[0], point[1] - origin[1]
        if kind == "circle_tangent":
            radius = float(relation["radius"])
            residuals = (x * x + y * y - radius * radius, x * direction[0] + y * direction[1])
        elif kind == "ellipse_tangent":
            a, b = float(relation["x_radius"]), float(relation["y_radius"])
            residuals = (x * x / (a * a) + y * y / (b * b) - 1, x * direction[0] / (a * a) + y * direction[1] / (b * b))
        elif kind == "parabola_tangent":
            p = float(relation["p"])
            residuals = (y * y - 4 * p * x, -4 * p * direction[0] + 2 * y * direction[1])
        elif kind == "hyperbola_tangent":
            a, b = float(relation["x_radius"]), float(relation["y_radius"])
            residuals = (x * x / (a * a) - y * y / (b * b) - 1, x * direction[0] / (a * a) - y * direction[1] / (b * b))
        else:
            raise GeometryError(f"Quan hệ 2D chưa hỗ trợ: {kind}")
        if any(abs(value) > tolerance for value in residuals):
            raise GeometryError(f"Quan hệ {kind} không đúng trong sai số {tolerance}.")


def vector_sub(a: list[float], b: list[float]) -> list[float]:
    return [float(x) - float(y) for x, y in zip(a, b)]


def dot(a: list[float], b: list[float]) -> float:
    return sum(float(x) * float(y) for x, y in zip(a, b))


def cross(a: list[float], b: list[float]) -> list[float]:
    return [
        a[1] * b[2] - a[2] * b[1],
        a[2] * b[0] - a[0] * b[2],
        a[0] * b[1] - a[1] * b[0],
    ]


def centroid(points: list[list[float]]) -> list[float]:
    return [sum(float(point[axis]) for point in points) / len(points) for axis in range(3)]


def camera_view_direction(camera: dict[str, Any]) -> list[float]:
    """Return the object-to-viewer vector used by tdplot_main_coords."""
    require_keys(camera, ("elevation", "azimuth"), "Camera")
    theta = math.radians(float(camera["elevation"]))
    phi = math.radians(float(camera["azimuth"]))
    return [
        math.sin(theta) * math.sin(phi),
        -math.sin(theta) * math.cos(phi),
        math.cos(theta),
    ]


def trig_visibility_intervals(a: float, b: float, c: float) -> tuple[list[tuple[float, float]], list[tuple[float, float]]]:
    """Split 0..360 where a*cos(t)+b*sin(t)+c is front/back facing."""
    radius = math.hypot(a, b)
    if radius < 1e-12:
        return ([(0.0, 360.0)], []) if c >= 0 else ([], [(0.0, 360.0)])
    ratio = -c / radius
    if ratio <= -1:
        return [(0.0, 360.0)], []
    if ratio >= 1:
        return [], [(0.0, 360.0)]
    phase = math.degrees(math.atan2(b, a))
    half = math.degrees(math.acos(ratio))
    roots = sorted(((phase - half) % 360.0, (phase + half) % 360.0))
    bounds = [roots[0], roots[1], roots[0] + 360.0]
    visible: list[tuple[float, float]] = []
    hidden: list[tuple[float, float]] = []
    for start, end in zip(bounds, bounds[1:]):
        middle = math.radians((start + end) / 2.0)
        target = visible if a * math.cos(middle) + b * math.sin(middle) + c >= 0 else hidden
        target.append((start, end))
    return visible, hidden


def classify_faces(data: dict[str, Any]) -> tuple[dict[str, str], dict[str, set[str]]]:
    vertices = {str(v["id"]): list(map(float, v["coordinates"])) for v in data["vertices"]}
    direction = camera_view_direction(data["camera"])
    if dot(direction, direction) < 1e-12:
        raise GeometryError("camera.view_direction không được là vector không.")
    solid_vertex_ids = {str(item) for face in data.get("faces", []) for item in face["points"]}
    solid_center = centroid([vertices[item] for item in solid_vertex_ids])
    face_states: dict[str, str] = {}
    face_vertices: dict[str, set[str]] = {}
    for face in data.get("faces", []):
        face_id = str(face["id"])
        ids = [str(item) for item in face["points"]]
        coords = [vertices[item] for item in ids]
        normal: list[float] | None = None
        for index in range(1, len(coords) - 1):
            candidate = cross(vector_sub(coords[index], coords[0]), vector_sub(coords[index + 1], coords[0]))
            if dot(candidate, candidate) > 1e-12:
                normal = candidate
                break
        if normal is None:
            raise GeometryError(f"Mặt {face_id} suy biến, không xác định được pháp tuyến.")
        outward_hint = vector_sub(centroid(coords), solid_center)
        if dot(normal, outward_hint) < 0:
            normal = [-value for value in normal]
        facing = dot(normal, direction)
        face_states[face_id] = "front" if facing > 1e-9 else "back" if facing < -1e-9 else "silhouette"
        face_vertices[face_id] = set(ids)
    return face_states, face_vertices


def auto_face_visibility(data: dict[str, Any]) -> dict[str, str]:
    face_states, face_vertices = classify_faces(data)
    result: dict[str, str] = {}
    for edge in data["edges"]:
        require_keys(edge, ("id", "endpoints", "visibility"), "Cạnh")
        visibility = edge["visibility"]
        if visibility == "auto":
            endpoints = set(map(str, edge["endpoints"]))
            adjacent = [face_id for face_id, ids in face_vertices.items() if endpoints <= ids]
            if len(adjacent) != 2:
                raise GeometryError(
                    f"Cạnh {edge['id']} phải thuộc đúng hai mặt để suy ra visibility; nhận {len(adjacent)}."
                )
            visibility = "visible" if any(face_states[face_id] == "front" for face_id in adjacent) else "hidden"
        if visibility not in {"visible", "hidden"}:
            raise GeometryError(f"visibility không hợp lệ ở cạnh {edge['id']}")
        result[str(edge["id"])] = visibility
    for override in data.get("visibility_overrides", []):
        require_keys(override, ("target", "value", "reason"), "Visibility override")
        if not str(override["reason"]).strip():
            raise GeometryError(f"Override {override['target']} thiếu lý do.")
        if override["target"] not in result:
            raise GeometryError(f"Override tham chiếu cạnh không tồn tại: {override['target']}")
        if override["value"] not in {"visible", "hidden"}:
            raise GeometryError(f"Override {override['target']} có value không hợp lệ.")
        result[override["target"]] = override["value"]
    return result


def compute_section(data: dict[str, Any]) -> tuple[dict[str, list[float]], list[dict[str, Any]]]:
    section = data.get("section")
    if not section:
        return {}, []
    require_keys(section, ("id", "plane", "edges", "point_ids"), "Thiết diện")
    require_keys(section["plane"], ("normal", "offset"), "Mặt phẳng thiết diện")
    normal = list(map(float, section["plane"]["normal"]))
    if len(normal) != 3 or dot(normal, normal) < 1e-12:
        raise GeometryError("Pháp tuyến thiết diện phải là vector 3D khác 0.")
    source_edges = list(map(str, section["edges"]))
    point_ids = list(map(str, section["point_ids"]))
    if len(source_edges) < 3 or len(source_edges) != len(point_ids):
        raise GeometryError("Thiết diện cần ít nhất ba cạnh cắt và số point_ids tương ứng.")
    if len(set(point_ids)) != len(point_ids):
        raise GeometryError("point_ids của thiết diện không được trùng nhau.")
    vertices = {str(v["id"]): list(map(float, v["coordinates"])) for v in data["vertices"]}
    edges = {str(edge["id"]): list(map(str, edge["endpoints"])) for edge in data["edges"]}
    points: dict[str, list[float]] = {}
    offset = float(section["plane"]["offset"])
    for edge_id, point_id in zip(source_edges, point_ids):
        if edge_id not in edges:
            raise GeometryError(f"Thiết diện tham chiếu cạnh không tồn tại: {edge_id}")
        a_id, b_id = edges[edge_id]
        a, b = vertices[a_id], vertices[b_id]
        direction = vector_sub(b, a)
        denominator = dot(normal, direction)
        if abs(denominator) < 1e-12:
            raise GeometryError(f"Mặt phẳng thiết diện không cắt duy nhất cạnh {edge_id}.")
        parameter = -(dot(normal, a) + offset) / denominator
        if not 1e-9 < parameter < 1.0 - 1e-9:
            raise GeometryError(f"Giao điểm thiết diện không nằm trong lòng cạnh {edge_id}.")
        points[point_id] = [a[i] + parameter * direction[i] for i in range(3)]
    face_states, face_vertices = classify_faces(data)
    segments: list[dict[str, Any]] = []
    for index, left_edge in enumerate(source_edges):
        right_edge = source_edges[(index + 1) % len(source_edges)]
        endpoints = set(edges[left_edge] + edges[right_edge])
        containing = [face_id for face_id, ids in face_vertices.items() if endpoints <= ids]
        if len(containing) != 1:
            raise GeometryError(
                f"Hai cạnh liên tiếp {left_edge}, {right_edge} phải cùng thuộc đúng một mặt; nhận {len(containing)}."
            )
        segments.append({
            "id": f"{section['id']}-{index + 1}",
            "endpoints": [point_ids[index], point_ids[(index + 1) % len(point_ids)]],
            "visibility": "hidden" if face_states[containing[0]] == "back" else "visible",
            "emphasized": bool(section.get("emphasized", True)),
            "face": containing[0],
        })
    return points, segments


def validate_3d(data: dict[str, Any]) -> dict[str, str]:
    require_keys(data, ("vertices", "camera", "solid_type"), "Hình không gian")
    vertex_ids: set[str] = set()
    for vertex in data["vertices"]:
        require_keys(vertex, ("id", "coordinates"), "Đỉnh")
        vertex_id = str(vertex["id"])
        if vertex_id in vertex_ids:
            raise GeometryError(f"Đỉnh trùng id: {vertex_id}")
        if len(vertex["coordinates"]) != 3:
            raise GeometryError(f"Đỉnh {vertex_id} phải có ba tọa độ.")
        vertex_ids.add(vertex_id)
    coordinate_keys = [tuple(map(float, vertex["coordinates"])) for vertex in data["vertices"]]
    if len(set(coordinate_keys)) != len(coordinate_keys):
        raise GeometryError("Các đỉnh của hình không gian phải có tọa độ phân biệt.")
    section_ids = set(map(str, data.get("section", {}).get("point_ids", [])))
    for label in data["labels"]:
        if label["target"] not in vertex_ids | section_ids:
            raise GeometryError(f"Nhãn tham chiếu đỉnh không tồn tại: {label['target']}")
    for item in data.get("segments", []):
        if any(reference not in vertex_ids for reference in item.get("endpoints", [])):
            raise GeometryError(f"segments tham chiếu đỉnh không tồn tại: {item.get('id', '?')}")
    if data["solid_type"] in {"cylinder", "cone", "frustum", "sphere"}:
        shape_key = data["solid_type"]
        shape_name = {"cylinder": "Khối trụ", "cone": "Khối nón", "frustum": "Khối nón cụt", "sphere": "Khối cầu"}[shape_key]
        require_keys(data, (shape_key,), shape_name)
        shape = data[shape_key]
        if shape_key == "sphere":
            require_keys(shape, ("center", "radius"), shape_name)
            if shape["center"] not in vertex_ids:
                raise GeometryError("Tâm khối cầu phải tham chiếu đỉnh đã khai báo.")
            if float(shape["radius"]) <= 0:
                raise GeometryError("Bán kính khối cầu phải dương.")
            section = data.get("curve_section")
            if section:
                require_keys(section, ("type", "z"), "Đường tròn trên mặt cầu")
                if section["type"] != "horizontal_circle":
                    raise GeometryError("Khối cầu prototype chỉ hỗ trợ đường tròn ngang.")
                if abs(float(section["z"])) >= float(shape["radius"]):
                    raise GeometryError("Mặt phẳng đường tròn phải cắt trong lòng khối cầu.")
            return {}
        upper_key = "apex" if shape_key == "cone" else "top_center"
        radius_keys = ("radius",) if shape_key != "frustum" else ("bottom_radius", "top_radius")
        require_keys(shape, ("bottom_center", upper_key, *radius_keys), shape_name)
        if shape["bottom_center"] not in vertex_ids or shape[upper_key] not in vertex_ids:
            raise GeometryError(f"Trục {shape_name.lower()} phải tham chiếu đỉnh đã khai báo.")
        if any(float(shape[key]) <= 0 for key in radius_keys):
            raise GeometryError(f"Bán kính {shape_name.lower()} phải dương.")
        if shape_key == "frustum" and float(shape["top_radius"]) >= float(shape["bottom_radius"]):
            raise GeometryError("C04 yêu cầu bán kính đáy trên nhỏ hơn bán kính đáy dưới.")
        bottom = next(v["coordinates"] for v in data["vertices"] if v["id"] == shape["bottom_center"])
        top = next(v["coordinates"] for v in data["vertices"] if v["id"] == shape[upper_key])
        if float(bottom[0]) != float(top[0]) or float(bottom[1]) != float(top[1]) or float(bottom[2]) == float(top[2]):
            raise GeometryError(f"Prototype yêu cầu trục {shape_name.lower()} song song Oz và hai đầu khác cao độ.")
        direction = camera_view_direction(data["camera"])
        if math.hypot(direction[0], direction[1]) < 1e-9:
            raise GeometryError(f"{shape_name} cần camera có thành phần nhìn ngang khác 0.")
        if shape_key == "cone":
            cone_tangent_angles(data)
        elif shape_key == "frustum":
            frustum_tangent_angles(data)
        section = data.get("curve_section")
        if section:
            require_keys(section, ("type",), "Thiết diện mặt cong")
            if shape_key == "cylinder":
                require_keys(section, ("z_center", "x_slope", "y_slope"), "Thiết diện khối trụ")
                z_center = float(section["z_center"])
                amplitude = float(shape["radius"]) * math.hypot(float(section["x_slope"]), float(section["y_slope"]))
                low, high = sorted((float(bottom[2]), float(top[2])))
                if z_center - amplitude <= low or z_center + amplitude >= high:
                    raise GeometryError("Thiết diện xiên phải nằm trong hai đáy khối trụ.")
            elif shape_key == "cone":
                require_keys(section, ("z",), "Thiết diện khối nón")
                z = float(section["z"])
                low, high = sorted((float(bottom[2]), float(top[2])))
                if not low < z < high:
                    raise GeometryError("Thiết diện ngang phải nằm giữa đáy và đỉnh nón.")
        return {}
    require_keys(data, ("edges",), "Đa diện")
    edge_ids: set[str] = set()
    for edge in data["edges"]:
        endpoints = edge.get("endpoints", [])
        if len(endpoints) != 2 or any(item not in vertex_ids for item in endpoints):
            raise GeometryError(f"Cạnh {edge.get('id', '?')} có đầu mút không hợp lệ.")
        if edge["id"] in edge_ids:
            raise GeometryError(f"Cạnh trùng id: {edge['id']}")
        edge_ids.add(edge["id"])
    for collection, key in (("faces", "points"), ("dimensions", "endpoints"), ("angles", "points")):
        for item in data.get(collection, []):
            if any(reference not in vertex_ids for reference in item.get(key, [])):
                raise GeometryError(f"{collection} tham chiếu đỉnh không tồn tại: {item.get('id', '?')}")
    if data.get("solid_type") not in {"convex_box", "convex_polyhedron"}:
        raise GeometryError("Auto visibility v0.1 chỉ hỗ trợ đa diện lồi.")
    if len(data.get("faces", [])) < 4:
        raise GeometryError("Đa diện lồi phải khai báo đầy đủ các mặt.")
    for face in data["faces"]:
        require_keys(face, ("id", "points"), "Mặt")
        if len(face["points"]) < 3:
            raise GeometryError(f"Mặt {face['id']} phải có ít nhất ba đỉnh.")
    compute_section(data)
    return auto_face_visibility(data)


def validate(data: dict[str, Any]) -> dict[str, str] | None:
    validate_common(data)
    if data["dimension"] == "2d":
        validate_2d(data)
        return None
    return validate_3d(data)


def tex_header(packages: list[str], libraries: list[str] | None = None) -> list[str]:
    lines = [
        "% Generated by scripts/zo_geometry.py v0.1.",
        "\\documentclass[tikz,border=3pt]{standalone}",
        "\\usepackage{fontspec}",
        "\\usepackage{unicode-math}",
    ]
    lines.extend(f"\\usepackage{{{package}}}" for package in packages)
    if libraries:
        lines.append(f"\\usetikzlibrary{{{','.join(libraries)}}}")
    lines.extend(["\\input{assets/tex/zo-geometry-styles.tex}", "", "\\begin{document}"])
    return lines


def style_for(role: str, visibility: str | None = None, emphasized: bool = False) -> str:
    if emphasized:
        key = "emphasized_hidden" if visibility == "hidden" else "emphasized"
    else:
        key = visibility or role
    try:
        return ROLE_STYLE[key]
    except KeyError as exc:
        raise GeometryError(f"Vai trò kiểu nét chưa được hỗ trợ: {key}") from exc


def render_2d(data: dict[str, Any]) -> str:
    lines = tex_header(["tkz-euclide"])
    lines.append("\\begin{tikzpicture}")
    for point in data["points"]:
        point_id = point["id"]
        if "coordinates" in point:
            x, y = point["coordinates"]
            lines.append(f"  \\tkzDefPoint({x},{y}){{{point_id}}}")
            continue
        construction = point["construction"]
        kind = construction["type"]
        if kind == "projection":
            source = construction["source"]
            a, b = construction["onto"]
            lines.append(f"  \\tkzDefPointBy[projection=onto {a}--{b}]({source})\\tkzGetPoint{{{point_id}}}")
        elif kind == "circumcenter":
            a, b, c = construction["points"]
            lines.append(f"  \\tkzDefTriangleCenter[circum]({a},{b},{c})\\tkzGetPoint{{{point_id}}}")
        else:
            raise GeometryError(f"Phép dựng 2D chưa hỗ trợ: {kind}")
    lines.append("")
    marks: list[dict[str, Any]] = []
    for obj in data["objects"]:
        kind = obj["type"]
        if kind == "right_angle_mark":
            marks.append(obj)
            continue
        style = style_for(obj["role"])
        if kind == "circle":
            lines.append(f"  \\tkzDrawCircle[{style}]({obj['center']},{obj['through']})")
        elif kind == "polygon":
            lines.append(f"  \\tkzDrawPolygon[{style}]({','.join(obj['points'])})")
        elif kind == "segment":
            lines.append(f"  \\tkzDrawSegment[{style}]({obj['endpoints'][0]},{obj['endpoints'][1]})")
        elif kind == "ellipse":
            lines.append(
                f"  \\draw[{style}] ({obj['center']}) ellipse "
                f"[x radius={obj['x_radius']}cm,y radius={obj['y_radius']}cm];"
            )
        elif kind == "parabola":
            vertex = obj["vertex"]
            vx, vy = next(point["coordinates"] for point in data["points"] if point["id"] == vertex)
            lines.append(
                f"  \\draw[{style}] plot[domain={obj['domain'][0]}:{obj['domain'][1]},samples=100,variable=\\t] "
                f"({{{vx}+\\t*\\t/(4*{obj['p']})}},{{{vy}+\\t}});"
            )
        elif kind == "hyperbola":
            center = obj["center"]
            cx, cy = next(point["coordinates"] for point in data["points"] if point["id"] == center)
            a, b = obj["x_radius"], obj["y_radius"]
            lo, hi = obj["domain"]
            for sign in ("", "-"):
                lines.append(
                    f"  \\draw[{style}] plot[domain={lo}:{hi},samples=100,variable=\\t] "
                    f"({{{cx}{'+' if not sign else '-'}{a}*sqrt(1+\\t*\\t/({b}*{b}))}},{{{cy}+\\t}});"
                )
        elif kind == "angle_mark":
            marks.append(obj)
        else:
            raise GeometryError(f"Đối tượng 2D chưa hỗ trợ: {kind}")
    point_ids = ",".join(str(point["id"]) for point in data["points"] if point.get("draw", True))
    if point_ids:
        lines.append(f"  \\tkzDrawPoints[zo geometry point]({point_ids})")
    for mark in marks:
        command = "tkzMarkRightAngle" if mark["type"] == "right_angle_mark" else "tkzMarkAngle"
        lines.append(f"  \\{command}[zo geometry angle,size={mark.get('size', '.25')}]({','.join(mark['points'])})")
    lines.append("")
    for label in data["labels"]:
        style = "zo geometry label masked" if label["mask"] == "when_required" else "zo geometry label"
        lines.append(
            f"  \\tkzLabelPoint[{style},{label['anchor']}]({label['target']}){{{label['text']}}}"
        )
    # The production PDF/SVG contract requires both STIX text and math fonts.
    # Purely mathematical figures otherwise contain no text glyph to embed.
    lines.append(f"  \\node[opacity=0] at ({data['points'][0]['id']}) {{x}};")
    lines.extend(["\\end{tikzpicture}", "\\end{document}", ""])
    return "\n".join(lines)


def coord_text(values: list[Any]) -> str:
    return ",".join(str(value) for value in values)


def render_3d(data: dict[str, Any], visibility: dict[str, str]) -> str:
    lines = tex_header(["tikz-3dplot"], ["angles", "quotes", "positioning"])
    camera = data["camera"]
    lines.append(f"\\tdplotsetmaincoords{{{camera['elevation']}}}{{{camera['azimuth']}}}")
    lines.append(f"\\begin{{tikzpicture}}[tdplot_main_coords,scale={camera.get('scale', 1)}]")
    for vertex in data["vertices"]:
        lines.append(f"  \\coordinate ({vertex['id']}) at ({coord_text(vertex['coordinates'])});")
    section_points, section_segments = compute_section(data)
    for point_id, coordinates in section_points.items():
        lines.append(f"  \\coordinate ({point_id}) at ({coord_text(coordinates)});")
    lines.append("")
    for face in data.get("faces", []):
        if not face.get("render", False):
            continue
        points = "--".join(f"({point})" for point in face["points"])
        lines.append(f"  \\fill[zo geometry surface] {points}--cycle;")
    # Occluded structure is painted first so visible edges remain in front at
    # projected crossings. This is semantic z-order, not YAML list order.
    for edge in data["edges"]:
        if visibility[edge["id"]] != "hidden":
            continue
        style = style_for("visible", "hidden", bool(edge.get("emphasized")))
        a, b = edge["endpoints"]
        lines.append(f"  % {edge['id']}: hidden")
        lines.append(f"  \\draw[{style}] ({a})--({b});")
    for segment in section_segments:
        if segment["visibility"] != "hidden":
            continue
        a, b = segment["endpoints"]
        lines.append(f"  % {segment['id']}: hidden section on {segment['face']}")
        lines.append(f"  \\draw[{style_for('visible', 'hidden', segment['emphasized'])}] ({a})--({b});")
    for segment in data.get("segments", []):
        style = style_for(segment.get("role", "auxiliary"), segment.get("visibility"), bool(segment.get("emphasized")))
        a, b = segment["endpoints"]
        lines.append(f"  \\draw[{style}] ({a})--({b});")
    for edge in data["edges"]:
        if visibility[edge["id"]] != "visible":
            continue
        style = style_for("visible", "visible", bool(edge.get("emphasized")))
        a, b = edge["endpoints"]
        lines.append(f"  % {edge['id']}: visible")
        lines.append(f"  \\draw[{style}] ({a})--({b});")
    for segment in section_segments:
        if segment["visibility"] != "visible":
            continue
        a, b = segment["endpoints"]
        lines.append(f"  % {segment['id']}: visible section on {segment['face']}")
        lines.append(f"  \\draw[{style_for('visible', 'visible', segment['emphasized'])}] ({a})--({b});")
    vertex_ids = ",".join([*(str(vertex["id"]) for vertex in data["vertices"]), *section_points])
    lines.append(f"  \\foreach \\P in {{{vertex_ids}}} \\node[zo geometry point] at (\\P) {{}};")
    for label in data["labels"]:
        style = "zo geometry label masked" if label["mask"] == "when_required" else "zo geometry label"
        lines.append(f"  \\node[{style},{label['anchor']}] at ({label['target']}) {{{label['text']}}};")
    for dimension in data.get("dimensions", []):
        a, b = dimension["endpoints"]
        lines.append(
            f"  \\path ({a})--({b}) node[pos={dimension['position']},zo geometry label masked,{dimension['anchor']}] {{{dimension['text']}}};"
        )
    for angle in data.get("angles", []):
        c, a, b = angle["points"]
        lines.append(
            f"  \\pic[zo geometry angle,angle radius={angle.get('radius', '8mm')},\"{angle['text']}\"{{zo geometry label masked}}] "
            f"{{angle={c}--{a}--{b}}};"
        )
    lines.append(f"  \\node[opacity=0] at ({data['vertices'][0]['id']}) {{x}};")
    lines.extend(["\\end{tikzpicture}", "\\end{document}", ""])
    return "\n".join(lines)


def render_cylinder(data: dict[str, Any]) -> str:
    lines = tex_header(["tikz-3dplot"], ["positioning"])
    camera = data["camera"]
    lines.append(f"\\tdplotsetmaincoords{{{camera['elevation']}}}{{{camera['azimuth']}}}")
    lines.append(f"\\begin{{tikzpicture}}[tdplot_main_coords,scale={camera.get('scale', 1)}]")
    vertices = {str(vertex["id"]): vertex["coordinates"] for vertex in data["vertices"]}
    for vertex_id, coords in vertices.items():
        lines.append(f"  \\coordinate ({vertex_id}) at ({coord_text(coords)});")
    cylinder = data["cylinder"]
    bottom_id, top_id = cylinder["bottom_center"], cylinder["top_center"]
    bx, by, bz = map(float, vertices[bottom_id])
    tx, ty, tz = map(float, vertices[top_id])
    radius = float(cylinder["radius"])
    view = camera_view_direction(camera)
    view_angle = math.degrees(math.atan2(view[1], view[0]))
    tangent_a = view_angle + 90.0
    tangent_b = view_angle - 90.0
    front_start, front_end = tangent_b, tangent_a
    back_start, back_end = tangent_a, tangent_b + 360.0
    number = lambda value: f"{value:.8g}"
    def curve(z: float, start: float, end: float, style: str) -> str:
        return (
            f"  \\draw[{style}] plot[domain={number(start)}:{number(end)},samples=72,variable=\\t] "
            f"({{{number(bx)}+{number(radius)}*cos(\\t)}},{{{number(by)}+{number(radius)}*sin(\\t)}},{number(z)});"
        )
    def rim_point(name: str, angle: float, z: float) -> str:
        return (
            f"  \\coordinate ({name}) at "
            f"({{{number(bx)}+{number(radius)}*cos({number(angle)})}},"
            f"{{{number(by)}+{number(radius)}*sin({number(angle)})}},{number(z)});"
        )
    lines.append(
        f"  \\fill[zo geometry surface] plot[domain=0:360,samples=72,variable=\\t] "
        f"({{{number(tx)}+{number(radius)}*cos(\\t)}},{{{number(ty)}+{number(radius)}*sin(\\t)}},{number(tz)})--cycle;"
    )
    lines.append(curve(bz, back_start, back_end, "zo geometry hidden"))
    section = data.get("curve_section")
    section_visible: list[tuple[float, float]] = []
    if section:
        section_visible, section_hidden = trig_visibility_intervals(view[0], view[1], 0.0)
        z_center = float(section["z_center"])
        x_slope, y_slope = float(section["x_slope"]), float(section["y_slope"])
        def section_curve(start: float, end: float, style: str) -> str:
            return (
                f"  \\draw[{style}] plot[domain={number(start)}:{number(end)},samples=72,variable=\\t] "
                f"({{{number(bx)}+{number(radius)}*cos(\\t)}},{{{number(by)}+{number(radius)}*sin(\\t)}},"
                f"{{{number(z_center)}+{number(x_slope * radius)}*cos(\\t)+{number(y_slope * radius)}*sin(\\t)}});"
            )
        for start, end in section_hidden:
            lines.append(section_curve(start, end, "zo geometry main hidden"))
    for segment in data.get("segments", []):
        style = style_for(segment.get("role", "auxiliary"), segment.get("visibility"), bool(segment.get("emphasized")))
        a, b = segment["endpoints"]
        lines.append(f"  \\draw[{style}] ({a})--({b});")
    lines.append(rim_point("zoCylAB", tangent_a, bz))
    lines.append(rim_point("zoCylAT", tangent_a, tz))
    lines.append(rim_point("zoCylBB", tangent_b, bz))
    lines.append(rim_point("zoCylBT", tangent_b, tz))
    lines.append(curve(bz, front_start, front_end, "zo geometry visible"))
    lines.append("  \\draw[zo geometry visible] (zoCylAB)--(zoCylAT) (zoCylBB)--(zoCylBT);")
    lines.append(curve(tz, 0.0, 360.0, "zo geometry visible"))
    if section:
        for start, end in section_visible:
            lines.append(section_curve(start, end, "zo geometry main"))
    vertex_ids = ",".join(vertices)
    lines.append(f"  \\foreach \\P in {{{vertex_ids}}} \\node[zo geometry point] at (\\P) {{}};")
    for label in data["labels"]:
        style = "zo geometry label masked" if label["mask"] == "when_required" else "zo geometry label"
        lines.append(f"  \\node[{style},{label['anchor']}] at ({label['target']}) {{{label['text']}}};")
    lines.append(f"  \\node[opacity=0] at ({data['vertices'][0]['id']}) {{x}};")
    lines.extend(["\\end{tikzpicture}", "\\end{document}", ""])
    return "\n".join(lines)


def render_sphere(data: dict[str, Any]) -> str:
    lines = tex_header(["tikz-3dplot"], ["positioning"])
    camera = data["camera"]
    lines.append(f"\\tdplotsetmaincoords{{{camera['elevation']}}}{{{camera['azimuth']}}}")
    lines.append(f"\\begin{{tikzpicture}}[tdplot_main_coords,scale={camera.get('scale', 1)}]")
    vertices = {str(vertex["id"]): vertex["coordinates"] for vertex in data["vertices"]}
    for vertex_id, coords in vertices.items():
        lines.append(f"  \\coordinate ({vertex_id}) at ({coord_text(coords)});")
    sphere = data["sphere"]
    center_id = str(sphere["center"])
    cx, cy, cz = map(float, vertices[center_id])
    radius = float(sphere["radius"])
    view = camera_view_direction(camera)
    view_angle = math.degrees(math.atan2(view[1], view[0]))
    tangent_a, tangent_b = view_angle + 90.0, view_angle - 90.0
    number = lambda value: f"{value:.8g}"
    def equator(start: float, end: float, style: str) -> str:
        return (
            f"  \\draw[{style}] plot[domain={number(start)}:{number(end)},samples=72,variable=\\t] "
            f"({{{number(cx)}+{number(radius)}*cos(\\t)}},{{{number(cy)}+{number(radius)}*sin(\\t)}},{number(cz)});"
        )
    lines.append("  \\begin{scope}[tdplot_screen_coords]")
    lines.append(f"    \\fill[zo geometry surface] ({center_id}) circle ({number(radius)}cm);")
    lines.append("  \\end{scope}")
    lines.append(equator(tangent_a, tangent_b + 360.0, "zo geometry hidden"))
    section = data.get("curve_section")
    section_visible: list[tuple[float, float]] = []
    if section:
        section_z = float(section["z"])
        section_radius = math.sqrt(radius * radius - section_z * section_z)
        section_visible, section_hidden = trig_visibility_intervals(
            section_radius * view[0], section_radius * view[1], section_z * view[2]
        )
        def sphere_section(start: float, end: float, style: str) -> str:
            return (
                f"  \\draw[{style}] plot[domain={number(start)}:{number(end)},samples=72,variable=\\t] "
                f"({{{number(cx)}+{number(section_radius)}*cos(\\t)}},"
                f"{{{number(cy)}+{number(section_radius)}*sin(\\t)}},{number(cz + section_z)});"
            )
        for start, end in section_hidden:
            lines.append(sphere_section(start, end, "zo geometry main hidden"))
    for segment in data.get("segments", []):
        style = style_for(segment.get("role", "auxiliary"), segment.get("visibility"), bool(segment.get("emphasized")))
        a, b = segment["endpoints"]
        lines.append(f"  \\draw[{style}] ({a})--({b});")
    lines.append(equator(tangent_b, tangent_a, "zo geometry visible"))
    if section:
        for start, end in section_visible:
            lines.append(sphere_section(start, end, "zo geometry main"))
    lines.append("  \\begin{scope}[tdplot_screen_coords]")
    lines.append(f"    \\draw[zo geometry visible] ({center_id}) circle ({number(radius)}cm);")
    lines.append("  \\end{scope}")
    vertex_ids = ",".join(vertices)
    lines.append(f"  \\foreach \\P in {{{vertex_ids}}} \\node[zo geometry point] at (\\P) {{}};")
    for label in data["labels"]:
        style = "zo geometry label masked" if label["mask"] == "when_required" else "zo geometry label"
        lines.append(f"  \\node[{style},{label['anchor']}] at ({label['target']}) {{{label['text']}}};")
    lines.append(f"  \\node[opacity=0] at ({center_id}) {{x}};")
    lines.extend(["\\end{tikzpicture}", "\\end{document}", ""])
    return "\n".join(lines)


def cone_tangent_angles(data: dict[str, Any]) -> tuple[float, float]:
    camera = data["camera"]
    view = camera_view_direction(camera)
    cone = data["cone"]
    vertices = {str(vertex["id"]): list(map(float, vertex["coordinates"])) for vertex in data["vertices"]}
    bottom = vertices[cone["bottom_center"]]
    apex = vertices[cone["apex"]]
    height = apex[2] - bottom[2]
    if height <= 0:
        raise GeometryError("C03 yêu cầu đỉnh nón nằm phía trên tâm đáy.")
    horizontal = math.hypot(view[0], view[1])
    ratio = -view[2] * float(cone["radius"]) / (height * horizontal)
    if abs(ratio) >= 1:
        raise GeometryError("Camera hiện tại không cho hai đường sinh biên thực phân biệt của khối nón.")
    view_angle = math.degrees(math.atan2(view[1], view[0]))
    half_span = math.degrees(math.acos(ratio))
    return view_angle - half_span, view_angle + half_span


def render_cone(data: dict[str, Any]) -> str:
    lines = tex_header(["tikz-3dplot"], ["positioning"])
    camera = data["camera"]
    lines.append(f"\\tdplotsetmaincoords{{{camera['elevation']}}}{{{camera['azimuth']}}}")
    lines.append(f"\\begin{{tikzpicture}}[tdplot_main_coords,scale={camera.get('scale', 1)}]")
    vertices = {str(vertex["id"]): vertex["coordinates"] for vertex in data["vertices"]}
    for vertex_id, coords in vertices.items():
        lines.append(f"  \\coordinate ({vertex_id}) at ({coord_text(coords)});")
    cone = data["cone"]
    bottom_id, apex_id = cone["bottom_center"], cone["apex"]
    bx, by, bz = map(float, vertices[bottom_id])
    radius = float(cone["radius"])
    visible_start, visible_end = cone_tangent_angles(data)
    hidden_start, hidden_end = visible_end, visible_start + 360.0
    number = lambda value: f"{value:.8g}"
    def curve(start: float, end: float, style: str) -> str:
        return (
            f"  \\draw[{style}] plot[domain={number(start)}:{number(end)},samples=72,variable=\\t] "
            f"({{{number(bx)}+{number(radius)}*cos(\\t)}},{{{number(by)}+{number(radius)}*sin(\\t)}},{number(bz)});"
        )
    def base_point(name: str, angle: float) -> str:
        return (
            f"  \\coordinate ({name}) at "
            f"({{{number(bx)}+{number(radius)}*cos({number(angle)})}},"
            f"{{{number(by)}+{number(radius)}*sin({number(angle)})}},{number(bz)});"
        )
    lines.append(curve(hidden_start, hidden_end, "zo geometry hidden"))
    section = data.get("curve_section")
    section_visible: list[tuple[float, float]] = []
    if section:
        apex_z = float(vertices[apex_id][2])
        section_z = float(section["z"])
        section_radius = radius * (apex_z - section_z) / (apex_z - bz)
        section_visible, section_hidden = trig_visibility_intervals(
            camera_view_direction(camera)[0], camera_view_direction(camera)[1],
            camera_view_direction(camera)[2] * radius / (apex_z - bz),
        )
        def cone_section(start: float, end: float, style: str) -> str:
            return (
                f"  \\draw[{style}] plot[domain={number(start)}:{number(end)},samples=72,variable=\\t] "
                f"({{{number(bx)}+{number(section_radius)}*cos(\\t)}},"
                f"{{{number(by)}+{number(section_radius)}*sin(\\t)}},{number(section_z)});"
            )
        for start, end in section_hidden:
            lines.append(cone_section(start, end, "zo geometry main hidden"))
    for segment in data.get("segments", []):
        style = style_for(segment.get("role", "auxiliary"), segment.get("visibility"), bool(segment.get("emphasized")))
        a, b = segment["endpoints"]
        lines.append(f"  \\draw[{style}] ({a})--({b});")
    lines.append(base_point("zoConeA", visible_start))
    lines.append(base_point("zoConeB", visible_end))
    lines.append(curve(visible_start, visible_end, "zo geometry visible"))
    lines.append(f"  \\draw[zo geometry visible] ({apex_id})--(zoConeA) ({apex_id})--(zoConeB);")
    if section:
        for start, end in section_visible:
            lines.append(cone_section(start, end, "zo geometry main"))
    vertex_ids = ",".join(vertices)
    lines.append(f"  \\foreach \\P in {{{vertex_ids}}} \\node[zo geometry point] at (\\P) {{}};")
    for label in data["labels"]:
        style = "zo geometry label masked" if label["mask"] == "when_required" else "zo geometry label"
        lines.append(f"  \\node[{style},{label['anchor']}] at ({label['target']}) {{{label['text']}}};")
    lines.append(f"  \\node[opacity=0] at ({data['vertices'][0]['id']}) {{x}};")
    lines.extend(["\\end{tikzpicture}", "\\end{document}", ""])
    return "\n".join(lines)


def frustum_tangent_angles(data: dict[str, Any]) -> tuple[float, float]:
    camera = data["camera"]
    view = camera_view_direction(camera)
    shape = data["frustum"]
    vertices = {str(vertex["id"]): list(map(float, vertex["coordinates"])) for vertex in data["vertices"]}
    bottom = vertices[shape["bottom_center"]]
    top = vertices[shape["top_center"]]
    height = top[2] - bottom[2]
    if height <= 0:
        raise GeometryError("C04 yêu cầu tâm đáy trên nằm phía trên tâm đáy dưới.")
    slope = (float(shape["bottom_radius"]) - float(shape["top_radius"])) / height
    horizontal = math.hypot(view[0], view[1])
    ratio = -view[2] * slope / horizontal
    if abs(ratio) >= 1:
        raise GeometryError("Camera hiện tại không cho hai đường sinh biên thực phân biệt của khối nón cụt.")
    view_angle = math.degrees(math.atan2(view[1], view[0]))
    half_span = math.degrees(math.acos(ratio))
    return view_angle - half_span, view_angle + half_span


def render_frustum(data: dict[str, Any]) -> str:
    lines = tex_header(["tikz-3dplot"], ["positioning"])
    camera = data["camera"]
    lines.append(f"\\tdplotsetmaincoords{{{camera['elevation']}}}{{{camera['azimuth']}}}")
    lines.append(f"\\begin{{tikzpicture}}[tdplot_main_coords,scale={camera.get('scale', 1)}]")
    vertices = {str(vertex["id"]): vertex["coordinates"] for vertex in data["vertices"]}
    for vertex_id, coords in vertices.items():
        lines.append(f"  \\coordinate ({vertex_id}) at ({coord_text(coords)});")
    shape = data["frustum"]
    bottom_id, top_id = shape["bottom_center"], shape["top_center"]
    bx, by, bz = map(float, vertices[bottom_id])
    tx, ty, tz = map(float, vertices[top_id])
    bottom_radius = float(shape["bottom_radius"])
    top_radius = float(shape["top_radius"])
    visible_start, visible_end = frustum_tangent_angles(data)
    hidden_start, hidden_end = visible_end, visible_start + 360.0
    number = lambda value: f"{value:.8g}"
    def curve(cx: float, cy: float, z: float, radius: float, start: float, end: float, style: str) -> str:
        return (
            f"  \\draw[{style}] plot[domain={number(start)}:{number(end)},samples=72,variable=\\t] "
            f"({{{number(cx)}+{number(radius)}*cos(\\t)}},{{{number(cy)}+{number(radius)}*sin(\\t)}},{number(z)});"
        )
    def rim_point(name: str, cx: float, cy: float, z: float, radius: float, angle: float) -> str:
        return (
            f"  \\coordinate ({name}) at "
            f"({{{number(cx)}+{number(radius)}*cos({number(angle)})}},"
            f"{{{number(cy)}+{number(radius)}*sin({number(angle)})}},{number(z)});"
        )
    lines.append(
        f"  \\fill[zo geometry surface] plot[domain=0:360,samples=72,variable=\\t] "
        f"({{{number(tx)}+{number(top_radius)}*cos(\\t)}},{{{number(ty)}+{number(top_radius)}*sin(\\t)}},{number(tz)})--cycle;"
    )
    lines.append(curve(bx, by, bz, bottom_radius, hidden_start, hidden_end, "zo geometry hidden"))
    for segment in data.get("segments", []):
        style = style_for(segment.get("role", "auxiliary"), segment.get("visibility"), bool(segment.get("emphasized")))
        a, b = segment["endpoints"]
        lines.append(f"  \\draw[{style}] ({a})--({b});")
    lines.append(rim_point("zoFrustumAB", bx, by, bz, bottom_radius, visible_start))
    lines.append(rim_point("zoFrustumAT", tx, ty, tz, top_radius, visible_start))
    lines.append(rim_point("zoFrustumBB", bx, by, bz, bottom_radius, visible_end))
    lines.append(rim_point("zoFrustumBT", tx, ty, tz, top_radius, visible_end))
    lines.append(curve(bx, by, bz, bottom_radius, visible_start, visible_end, "zo geometry visible"))
    lines.append("  \\draw[zo geometry visible] (zoFrustumAB)--(zoFrustumAT) (zoFrustumBB)--(zoFrustumBT);")
    lines.append(curve(tx, ty, tz, top_radius, 0.0, 360.0, "zo geometry visible"))
    vertex_ids = ",".join(vertices)
    lines.append(f"  \\foreach \\P in {{{vertex_ids}}} \\node[zo geometry point] at (\\P) {{}};")
    for label in data["labels"]:
        style = "zo geometry label masked" if label["mask"] == "when_required" else "zo geometry label"
        lines.append(f"  \\node[{style},{label['anchor']}] at ({label['target']}) {{{label['text']}}};")
    lines.append(f"  \\node[opacity=0] at ({data['vertices'][0]['id']}) {{x}};")
    lines.extend(["\\end{tikzpicture}", "\\end{document}", ""])
    return "\n".join(lines)


def compile_document(source: Path, output: Path) -> None:
    data = load_document(source)
    visibility = validate(data)
    if data["dimension"] == "2d":
        rendered = render_2d(data)
    elif data.get("solid_type") == "cylinder":
        rendered = render_cylinder(data)
    elif data.get("solid_type") == "cone":
        rendered = render_cone(data)
    elif data.get("solid_type") == "frustum":
        rendered = render_frustum(data)
    elif data.get("solid_type") == "sphere":
        rendered = render_sphere(data)
    else:
        assert visibility is not None
        rendered = render_3d(data, visibility)
    output.write_text(rendered, encoding="utf-8", newline="\n")
    print(f"ĐÃ SINH: {output}")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def build_document(source: Path, output_prefix: Path, dpi: int = 180) -> None:
    """Compile YAML to TeX, vector PDF/SVG and a PNG review image."""
    output_prefix.parent.mkdir(parents=True, exist_ok=True)
    tex_path = output_prefix.with_suffix(".tex")
    pdf_path = output_prefix.with_suffix(".pdf")
    svg_path = output_prefix.with_suffix(".svg")
    preview_prefix = output_prefix
    compile_document(source, tex_path)
    subprocess.run(
        ["lualatex", "-interaction=batchmode", "-halt-on-error", f"-output-directory={output_prefix.parent}", str(tex_path)],
        check=True,
    )
    subprocess.run(["pdftocairo", "-svg", str(pdf_path), str(svg_path)], check=True)
    subprocess.run(["pdftoppm", "-png", "-singlefile", "-r", str(dpi), str(pdf_path), str(preview_prefix)], check=True)
    outputs = {
        suffix: sha256(output_prefix.with_suffix(suffix))
        for suffix in (".tex", ".pdf", ".svg", ".png")
    }
    receipt_path = output_prefix.with_suffix(".geometry.json")
    receipt = {
        "schema_version": 1,
        "source_sha256": sha256(source),
        "compiler_sha256": sha256(Path(__file__).resolve()),
        "style_sha256": sha256(STYLE_PATH),
        "dpi": dpi,
        "outputs": outputs,
    }
    receipt_path.write_text(
        json.dumps(receipt, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    for suffix in (".aux", ".log"):
        temporary = output_prefix.with_suffix(suffix)
        if temporary.is_file():
            temporary.unlink()
    print(f"ĐÃ DỰNG: {pdf_path} | {svg_path} | {preview_prefix}.png | {receipt_path}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Compiler hình học ZO Math v0.1")
    subparsers = parser.add_subparsers(dest="command", required=True)
    check_parser = subparsers.add_parser("check", help="Kiểm tra YAML và quan hệ tham chiếu")
    check_parser.add_argument("source", type=Path)
    compile_parser = subparsers.add_parser("compile", help="Kiểm tra rồi sinh nguồn TikZ")
    compile_parser.add_argument("source", type=Path)
    compile_parser.add_argument("output", type=Path)
    build_parser = subparsers.add_parser("build", help="Sinh TeX, PDF, SVG và PNG kiểm tra")
    build_parser.add_argument("source", type=Path)
    build_parser.add_argument("output_prefix", type=Path)
    build_parser.add_argument("--dpi", type=int, default=180)
    args = parser.parse_args()
    try:
        if args.command == "check":
            validate(load_document(args.source))
            print(f"ĐẠT: {args.source}")
        elif args.command == "compile":
            compile_document(args.source, args.output)
        else:
            build_document(args.source, args.output_prefix, args.dpi)
    except (GeometryError, OSError, subprocess.CalledProcessError) as exc:
        print(f"LỖI: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
