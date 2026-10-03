#!/usr/bin/env python3
"""Self-test hồi quy cho checker kiến trúc học tập Ôn thi Toán THPT."""

from __future__ import annotations

import copy
import json
import unittest

import zo_learning_architecture as checker


class LearningArchitectureCheckerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.common = checker.load_common()
        cls.g01_path, cls.g02_path = checker.DEFAULT_MANIFESTS
        cls.g01 = checker.load_yaml(cls.g01_path)
        cls.g02 = checker.load_yaml(cls.g02_path)

    def issue_codes(self, manifest, path):
        return {issue.code for issue in checker.validate_manifest(manifest, path, self.common)}

    def test_canonical_manifests_pass_schema(self):
        self.assertEqual(checker.validate_manifest(self.g01, self.g01_path, self.common), [])
        self.assertEqual(checker.validate_manifest(self.g02, self.g02_path, self.common), [])

    def test_duplicate_id_is_rejected(self):
        manifest = copy.deepcopy(self.g01)
        duplicate = copy.deepcopy(manifest["tasks"][0])
        duplicate["role"] = "K"
        duplicate["content_key"] = "fixture-duplicate-id"
        manifest["tasks"].append(duplicate)
        self.assertIn("id.duplicate", self.issue_codes(manifest, self.g01_path))

    def test_missing_anchor_is_rejected(self):
        manifest = copy.deepcopy(self.g01)
        manifest["tasks"][0]["source_anchor"] = "anchor-khong-ton-tai"
        self.assertIn("anchor.missing", self.issue_codes(manifest, self.g01_path))

    def test_existing_source_task_cannot_be_dropped_from_manifest(self):
        manifest = copy.deepcopy(self.g01)
        manifest["tasks"] = [task for task in manifest["tasks"] if task["id"] != "G01-L01"]
        self.assertIn("source.task-unmapped", self.issue_codes(manifest, self.g01_path))

    def test_task_cannot_carry_two_evidence_roles(self):
        manifest = copy.deepcopy(self.g01)
        manifest["tasks"][0]["role"] = ["L", "K"]
        self.assertIn("task.dual-role", self.issue_codes(manifest, self.g01_path))

    def test_stage_without_cp_lt_is_rejected(self):
        manifest = copy.deepcopy(self.g01)
        manifest["stages"][0]["checkpoint_id"] = "CP-MISSING"
        self.assertIn("stage.checkpoint", self.issue_codes(manifest, self.g01_path))

    def test_foundation_route_without_return_anchor_is_rejected(self):
        manifest = copy.deepcopy(self.g01)
        manifest["foundation_routes"][0]["return_anchors"] = []
        self.assertIn("foundation.return", self.issue_codes(manifest, self.g01_path))

    def test_exposed_k_or_o_content_is_rejected(self):
        manifest = copy.deepcopy(self.g01)
        practice = next(task for task in manifest["tasks"] if task["role"] == "L")
        independent = next(task for task in manifest["tasks"] if task["role"] == "K")
        independent["content_key"] = practice["content_key"]
        self.assertIn("task.exposure-leak", self.issue_codes(manifest, self.g01_path))

    def test_readiness_reports_exact_planned_cells(self):
        g01_planned = {task["id"] for task in checker.planned_tasks(self.g01)}
        g02_planned = {task["id"] for task in checker.planned_tasks(self.g02)}
        self.assertEqual(g01_planned, set(self.g01["readiness"]["expected_planned_task_ids"]))
        self.assertEqual(g02_planned, set(self.g02["readiness"]["expected_planned_task_ids"]))
        self.assertEqual(len(g01_planned), 21)
        self.assertEqual(len(g02_planned), 14)

    def test_r1_g02_lessons_07_and_08_are_transfer_tasks(self):
        tasks = {task["id"]: task for task in self.g02["tasks"]}
        self.assertEqual(tasks["G02-P01"]["role"], "P")
        self.assertEqual(tasks["G02-P01"]["source_anchor"], "l07")
        self.assertEqual(tasks["G02-P02"]["role"], "P")
        self.assertEqual(tasks["G02-P02"]["source_anchor"], "l08")

    def test_schema_document_is_valid_json(self):
        data = json.loads(checker.SCHEMA_PATH.read_text(encoding="utf-8"))
        self.assertEqual(data["properties"]["schema_version"]["const"], 1)
        self.assertEqual(
            set(data["$defs"]["task"]["properties"]["role"]["enum"]),
            set(self.common["valid_task_roles"]),
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
