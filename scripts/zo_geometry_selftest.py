from __future__ import annotations

import copy
import math
import sys
import unittest
from pathlib import Path

from zo_geometry_check import check_layout, check_svg, load_yaml
from zo_geometry import (
    GeometryError,
    camera_view_direction,
    compute_section,
    cone_tangent_angles,
    frustum_tangent_angles,
    render_3d,
    render_cone,
    render_cylinder,
    render_sphere,
    validate,
)
REPO_ROOT = Path(__file__).resolve().parents[1]
FIXTURE_ROOT = REPO_ROOT / "_audit" / "zo_geometry_spike"
sys.path.insert(0, str(FIXTURE_ROOT))

from zo_geometry_stress_v01 import FAMILIES, VIEWS, adapt_labels, camera_readability, negative_cases, render_case, resolved_camera


HERE = FIXTURE_ROOT


class GeometryPrototypeTests(unittest.TestCase):
    def test_p01_layout_passes(self) -> None:
        errors, warnings = check_layout(load_yaml(HERE / "p01_triangle.yaml"))
        self.assertEqual(errors, [])
        self.assertEqual(warnings, [])

    def test_s01_layout_and_svg_pass(self) -> None:
        errors, warnings = check_layout(load_yaml(HERE / "s01_box.yaml"))
        self.assertEqual(errors, [])
        self.assertEqual(warnings, [])
        svg_errors, info = check_svg(HERE / "generated_s01.svg")
        self.assertEqual(svg_errors, [])
        self.assertGreater(info["vector_elements"], 0)

    def test_label_covering_its_point_is_rejected(self) -> None:
        data = copy.deepcopy(load_yaml(HERE / "p01_triangle.yaml"))
        data["labels"][0]["anchor"] = "center"
        errors, _ = check_layout(data)
        self.assertIn("Nhãn A che điểm đích.", errors)

    def test_strict_labels_check_incident_edges_beyond_point_marker(self) -> None:
        data = load_yaml(HERE / "s01_box.yaml")
        compatibility_errors, _ = check_layout(data)
        strict_errors, _ = check_layout(data, strict_labels=True)
        self.assertEqual(compatibility_errors, [])
        self.assertIn("Nhãn A cắt đường AB.", strict_errors)

    def test_s01_auto_visibility_matches_approved_baseline(self) -> None:
        visibility = validate(load_yaml(HERE / "s01_box.yaml"))
        self.assertIsNotNone(visibility)
        assert visibility is not None
        self.assertEqual({edge for edge, state in visibility.items() if state == "hidden"}, {"AB", "DA", "AA1"})
        self.assertEqual(visibility["CD"], "visible")
        self.assertEqual(visibility["DD1"], "visible")

    def test_reversing_camera_changes_hidden_edges_geometrically(self) -> None:
        data = copy.deepcopy(load_yaml(HERE / "s01_box.yaml"))
        data["camera"]["elevation"] = 112
        data["camera"]["azimuth"] = 298
        visibility = validate(data)
        self.assertIsNotNone(visibility)
        assert visibility is not None
        self.assertEqual(
            {edge for edge, state in visibility.items() if state == "hidden"},
            {"CC1", "B1C1", "C1D1"},
        )

    def test_visibility_override_requires_reason(self) -> None:
        data = copy.deepcopy(load_yaml(HERE / "s01_box.yaml"))
        data["visibility_overrides"] = [{"target": "CD", "value": "hidden", "reason": ""}]
        with self.assertRaises(GeometryError):
            validate(data)

    def test_s02_pyramid_visibility_layout_and_svg(self) -> None:
        data = load_yaml(HERE / "s02_pyramid.yaml")
        visibility = validate(data)
        self.assertIsNotNone(visibility)
        assert visibility is not None
        self.assertEqual(
            {edge for edge, state in visibility.items() if state == "hidden"},
            {"AB", "DA", "SA"},
        )
        layout_errors, layout_warnings = check_layout(data)
        self.assertEqual(layout_errors, [])
        self.assertEqual(layout_warnings, [])
        svg_errors, info = check_svg(HERE / "generated_s02.svg")
        self.assertEqual(svg_errors, [])
        self.assertGreater(info["vector_elements"], 0)

    def test_visible_edge_is_painted_after_internal_segment(self) -> None:
        data = load_yaml(HERE / "s02_pyramid.yaml")
        visibility = validate(data)
        assert visibility is not None
        tex = render_3d(data, visibility)
        self.assertLess(tex.index("\\draw[zo geometry main hidden] (S)--(O);"), tex.index("% SD: visible"))

    def test_c02_cylinder_layout_svg_and_arc_split(self) -> None:
        data = load_yaml(HERE / "c02_cylinder.yaml")
        self.assertEqual(validate(data), {})
        layout_errors, layout_warnings = check_layout(data)
        self.assertEqual(layout_errors, [])
        self.assertEqual(layout_warnings, [])
        svg_errors, info = check_svg(HERE / "generated_c02.svg")
        self.assertEqual(svg_errors, [])
        self.assertGreater(info["vector_elements"], 0)
        tex = render_cylinder(data)
        self.assertIn("domain=118:298", tex)
        self.assertIn("domain=-62:118", tex)

    def test_cylinder_arc_split_follows_camera_azimuth(self) -> None:
        data = copy.deepcopy(load_yaml(HERE / "c02_cylinder.yaml"))
        data["camera"]["azimuth"] = 90
        tex = render_cylinder(data)
        self.assertIn("domain=90:270", tex)
        self.assertIn("domain=-90:90", tex)

    def test_c03_cone_tangency_layout_and_svg(self) -> None:
        data = load_yaml(HERE / "c03_cone.yaml")
        self.assertEqual(validate(data), {})
        start, end = cone_tangent_angles(data)
        view = camera_view_direction(data["camera"])
        radius = float(data["cone"]["radius"])
        height = 3.0
        for angle in (start, end):
            radians = math.radians(angle)
            normal = [math.cos(radians), math.sin(radians), radius / height]
            self.assertAlmostEqual(sum(a * b for a, b in zip(normal, view)), 0.0, places=9)
        layout_errors, layout_warnings = check_layout(data)
        self.assertEqual(layout_errors, [])
        self.assertEqual(layout_warnings, [])
        svg_errors, info = check_svg(HERE / "generated_c03.svg")
        self.assertEqual(svg_errors, [])
        self.assertGreater(info["vector_elements"], 0)

    def test_cone_rejects_camera_without_two_distinct_generators(self) -> None:
        data = copy.deepcopy(load_yaml(HERE / "c03_cone.yaml"))
        data["camera"]["elevation"] = 10
        with self.assertRaises(GeometryError):
            validate(data)

    def test_c04_frustum_tangency_layout_and_svg(self) -> None:
        data = load_yaml(HERE / "c04_frustum.yaml")
        self.assertEqual(validate(data), {})
        start, end = frustum_tangent_angles(data)
        view = camera_view_direction(data["camera"])
        shape = data["frustum"]
        slope = (float(shape["bottom_radius"]) - float(shape["top_radius"])) / 3.0
        for angle in (start, end):
            radians = math.radians(angle)
            normal = [math.cos(radians), math.sin(radians), slope]
            self.assertAlmostEqual(sum(a * b for a, b in zip(normal, view)), 0.0, places=9)
        layout_errors, layout_warnings = check_layout(data)
        self.assertEqual(layout_errors, [])
        self.assertEqual(layout_warnings, [])
        svg_errors, info = check_svg(HERE / "generated_c04.svg")
        self.assertEqual(svg_errors, [])
        self.assertGreater(info["vector_elements"], 0)

    def test_frustum_rejects_non_decreasing_radius(self) -> None:
        data = copy.deepcopy(load_yaml(HERE / "c04_frustum.yaml"))
        data["frustum"]["top_radius"] = data["frustum"]["bottom_radius"]
        with self.assertRaises(GeometryError):
            validate(data)

    def test_batch_1_planar_cases_layout_svg_and_relations(self) -> None:
        cases = (
            "p02_circle_tangent",
            "p03_intersection_angle",
            "p04_ellipse",
            "p05_parabola",
            "p06_hyperbola",
        )
        for case in cases:
            with self.subTest(case=case):
                data = load_yaml(HERE / f"{case}.yaml")
                self.assertIsNone(validate(data))
                layout_errors, layout_warnings = check_layout(data)
                self.assertEqual(layout_errors, [])
                self.assertEqual(layout_warnings, [])
                svg_errors, info = check_svg(HERE / f"generated_{case}.svg")
                self.assertEqual(svg_errors, [])
                self.assertGreater(info["vector_elements"], 0)

    def test_incorrect_conic_tangent_is_rejected(self) -> None:
        data = copy.deepcopy(load_yaml(HERE / "p04_ellipse.yaml"))
        data["points"][-1]["coordinates"][1] += 0.25
        with self.assertRaises(GeometryError):
            validate(data)

    def test_p06_asymptotes_share_branch_x_extent_and_avoid_tangent_endpoints(self) -> None:
        data = load_yaml(HERE / "p06_hyperbola.yaml")
        coords = {point["id"]: point["coordinates"] for point in data["points"]}
        branch_extent = 2 * math.sqrt(1 + 3**2 / 1.2**2)
        self.assertAlmostEqual(abs(float(coords["A2"][0])), branch_extent, places=7)
        self.assertAlmostEqual(abs(float(coords["B2"][0])), branch_extent, places=7)
        for endpoint in ("U", "V"):
            x, y = map(float, coords[endpoint])
            self.assertGreater(min(abs(y - 0.6 * x), abs(y + 0.6 * x)), 0.05)

    def test_batch_2_polyhedra_visibility_layout_and_svg(self) -> None:
        cases = {
            "s03_truncated_pyramid": {"AB", "DA", "AA1"},
            "s04_oblique_triangular_prism": {"AB", "CA", "AA1"},
        }
        for case, expected_hidden in cases.items():
            with self.subTest(case=case):
                data = load_yaml(HERE / f"{case}.yaml")
                visibility = validate(data)
                assert visibility is not None
                self.assertEqual({edge for edge, state in visibility.items() if state == "hidden"}, expected_hidden)
                self.assertEqual(check_layout(data), ([], []))
                svg_errors, info = check_svg(HERE / f"generated_{case}.svg")
                self.assertEqual(svg_errors, [])
                self.assertGreater(info["vector_elements"], 0)

    def test_s05_section_is_computed_and_layered(self) -> None:
        data = load_yaml(HERE / "s05_polyhedron_section.yaml")
        visibility = validate(data)
        assert visibility is not None
        points, segments = compute_section(data)
        self.assertEqual(set(points), {"M", "N", "P", "Q"})
        for point in points.values():
            self.assertAlmostEqual(point[2], 1.35, places=9)
        self.assertEqual(
            {segment["id"] for segment in segments if segment["visibility"] == "hidden"},
            {"sigma-1", "sigma-4"},
        )
        layout_errors, layout_warnings = check_layout(data)
        self.assertEqual(layout_errors, [])
        self.assertEqual(len(layout_warnings), 2)
        self.assertTrue(all("Được phép che nền" in warning for warning in layout_warnings))
        tex = render_3d(data, visibility)
        self.assertLess(tex.index("% sigma-1: hidden section"), tex.index("% BC: visible"))
        self.assertLess(tex.index("% SD: visible"), tex.index("% sigma-2: visible section"))
        svg_errors, info = check_svg(HERE / "generated_s05_polyhedron_section.svg")
        self.assertEqual(svg_errors, [])
        self.assertGreater(info["vector_elements"], 0)

    def test_section_rejects_plane_missing_an_edge(self) -> None:
        data = copy.deepcopy(load_yaml(HERE / "s05_polyhedron_section.yaml"))
        data["section"]["plane"]["offset"] = -3.2
        with self.assertRaises(GeometryError):
            validate(data)

    def test_c05_sphere_layout_svg_and_arc_split(self) -> None:
        data = load_yaml(HERE / "c05_sphere.yaml")
        self.assertEqual(validate(data), {})
        tex = render_sphere(data)
        self.assertIn("circle (2cm)", tex)
        self.assertIn("domain=118:298", tex)
        self.assertIn("domain=-62:118", tex)
        self.assertEqual(check_layout(data), ([], []))
        svg_errors, info = check_svg(HERE / "generated_c05_sphere.svg")
        self.assertEqual(svg_errors, [])
        self.assertGreater(info["vector_elements"], 0)

    def test_sphere_rejects_non_positive_radius(self) -> None:
        data = copy.deepcopy(load_yaml(HERE / "c05_sphere.yaml"))
        data["sphere"]["radius"] = 0
        with self.assertRaises(GeometryError):
            validate(data)

    def test_s06_oblique_hexagonal_section(self) -> None:
        data = load_yaml(HERE / "s06_oblique_hexagonal_section.yaml")
        visibility = validate(data)
        assert visibility is not None
        points, segments = compute_section(data)
        self.assertEqual(set(points), {"M", "N", "P", "Q", "R", "T"})
        for point in points.values():
            self.assertAlmostEqual(sum(point), 4.5, places=9)
        self.assertEqual(
            {segment["id"] for segment in segments if segment["visibility"] == "hidden"},
            {"sigma-1", "sigma-3", "sigma-5"},
        )
        self.assertEqual(check_layout(data), ([], []))
        svg_errors, info = check_svg(HERE / "generated_s06_oblique_hexagonal_section.svg")
        self.assertEqual(svg_errors, [])
        self.assertGreater(info["vector_elements"], 0)

    def test_c01_preserves_approved_sphere_render(self) -> None:
        data = load_yaml(HERE / "c01_sphere.yaml")
        self.assertEqual(validate(data), {})
        self.assertEqual(check_layout(data), ([], []))
        self.assertEqual(
            (HERE / "generated_c01_sphere_preview.png").read_bytes(),
            (HERE / "generated_c05_sphere_preview.png").read_bytes(),
        )

    def test_batch_3_curved_sections_layout_and_svg(self) -> None:
        for case in ("c05_cylinder_section", "c06_cone_section", "c07_sphere_circle"):
            with self.subTest(case=case):
                data = load_yaml(HERE / f"{case}.yaml")
                self.assertEqual(validate(data), {})
                self.assertEqual(check_layout(data), ([], []))
                svg_errors, info = check_svg(HERE / f"generated_{case}.svg")
                self.assertEqual(svg_errors, [])
                self.assertGreater(info["vector_elements"], 0)

    def test_batch_3_curves_have_visible_and_hidden_parts(self) -> None:
        renderers = {
            "c05_cylinder_section": render_cylinder,
            "c06_cone_section": render_cone,
            "c07_sphere_circle": render_sphere,
        }
        for case, renderer in renderers.items():
            with self.subTest(case=case):
                tex = renderer(load_yaml(HERE / f"{case}.yaml"))
                self.assertIn("zo geometry main hidden", tex)
                self.assertIn("zo geometry main] plot", tex)

    def test_curved_sections_reject_planes_outside_solids(self) -> None:
        cylinder = copy.deepcopy(load_yaml(HERE / "c05_cylinder_section.yaml"))
        cylinder["curve_section"]["z_center"] = 0.1
        with self.assertRaises(GeometryError):
            validate(cylinder)
        cone = copy.deepcopy(load_yaml(HERE / "c06_cone_section.yaml"))
        cone["curve_section"]["z"] = 3.0
        with self.assertRaises(GeometryError):
            validate(cone)
        sphere = copy.deepcopy(load_yaml(HERE / "c07_sphere_circle.yaml"))
        sphere["curve_section"]["z"] = 2.0
        with self.assertRaises(GeometryError):
            validate(sphere)

    def test_c05_projected_section_is_not_visually_flat(self) -> None:
        data = load_yaml(HERE / "c05_cylinder_section.yaml")
        camera = data["camera"]
        theta = math.radians(float(camera["elevation"]))
        phi = math.radians(float(camera["azimuth"]))
        radius = float(data["cylinder"]["radius"])
        section = data["curve_section"]
        projected = []
        for angle in range(360):
            t = math.radians(angle)
            x, y = radius * math.cos(t), radius * math.sin(t)
            z = float(section["z_center"]) + float(section["x_slope"]) * x + float(section["y_slope"]) * y
            screen_x = math.cos(phi) * x + math.sin(phi) * y
            screen_y = -math.cos(theta) * math.sin(phi) * x + math.cos(theta) * math.cos(phi) * y + math.sin(theta) * z
            projected.append((screen_x, screen_y))
        width = max(x for x, _ in projected) - min(x for x, _ in projected)
        height = max(y for _, y in projected) - min(y for _, y in projected)
        self.assertGreater(height / width, 0.35)

    def test_stress_matrix_sources_and_negative_cases(self) -> None:
        camera_cases = 0
        for family, source_name in FAMILIES.items():
            source = load_yaml(HERE / source_name)
            for view_name in VIEWS:
                data = copy.deepcopy(source)
                data["camera"].update(resolved_camera(family, view_name))
                adapt_labels(data)
                self.assertTrue(render_case(data).startswith("% Generated"))
                self.assertEqual(check_layout(data)[0], [])
                camera_cases += 1
        self.assertEqual(camera_cases, 20)
        for _, data in negative_cases():
            with self.assertRaises(GeometryError):
                validate(data)

    def test_stress_matrix_includes_dense_labels_and_emphasis(self) -> None:
        dense = load_yaml(HERE / FAMILIES["polyhedron"])
        self.assertGreaterEqual(len(dense["labels"]), 12)
        emphasized_families = 0
        for source_name in FAMILIES.values():
            data = load_yaml(HERE / source_name)
            if data.get("section", {}).get("emphasized") or data.get("curve_section"):
                emphasized_families += 1
        self.assertGreaterEqual(emphasized_families, 4)

    def test_stress_cameras_meet_readability_floor(self) -> None:
        for view, camera in VIEWS.items():
            with self.subTest(view=view):
                self.assertGreaterEqual(camera_readability(camera)["horizontal_circle_minor_ratio"], 0.20)

    def test_visual_tokens_are_centralized(self) -> None:
        style = (HERE / "zo_geometry_spike_style.tex").read_text(encoding="utf-8")
        for token in (
            "\\zoGeometryVisibleWidth",
            "\\zoGeometryHiddenWidth",
            "\\zoGeometryMainWidth",
            "\\zoGeometryPointSize",
            "\\zoGeometryLabelPadding",
            "\\zoGeometryMaskPadding",
        ):
            self.assertIn(f"\\newcommand{{{token}}}", style)
        angle_style = style.split("zo geometry angle/.style={", 1)[1].split("}", 1)[0]
        self.assertIn("fill=none", angle_style)
        self.assertNotIn("fill opacity", angle_style)


if __name__ == "__main__":
    unittest.main()
