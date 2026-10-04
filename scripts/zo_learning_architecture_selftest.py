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
        self.assertEqual(len(g01_planned), 0)
        self.assertEqual(len(g02_planned), 0)

    def test_r1_g01_phase3_tasks_are_current_with_real_links(self):
        tasks = {task["id"]: task for task in self.g01["tasks"]}
        self.assertEqual(len(checker.G01_PHASE3_TASK_IDS), 21)
        for task_id in checker.G01_PHASE3_TASK_IDS:
            task = tasks[task_id]
            self.assertEqual(task["status"], "current")
            self.assertIsInstance(task["source_anchor"], str)
            self.assertIsInstance(task["answer_anchor"], str)

    def test_r1_g01_review_remediation_returns_to_activation_checkpoint(self):
        tasks = {task["id"]: task for task in self.g01["tasks"]}
        expected = ["CP-ON1", "CP-ON2", "CP-ON3"]
        for index in range(1, 10):
            task = tasks[f"G01-S-O-E{index:02d}"]
            self.assertEqual(task["checkpoint_ids"], expected)
            for field in ("next_on_pass", "next_on_error"):
                self.assertEqual(task[field], {"kind": "activation_checkpoint", "checkpoint_ids": expected})

    def test_r1_g01_phase3_figures_are_real_and_referenced(self):
        source = self.g01_path.parent / self.g01["source"]["qmd"]
        text = source.read_text(encoding="utf-8")
        for task_id, figure in checker.G01_PHASE3_FIGURES.items():
            self.assertEqual(text.count(f"]({figure})"), 1, task_id)
            for suffix in (".tex", ".pdf", ".svg"):
                self.assertTrue((source.parent / figure).with_suffix(suffix).is_file(), task_id)

    def test_r1_g02_phase2_tasks_are_current_with_real_anchors(self):
        expected = {
            "G02-L11",
            *(f"G02-S-K-E{index:02d}" for index in range(1, 7)),
            *(f"G02-S-O-E{index:02d}" for index in range(1, 7)),
            "G02-S-P02",
        }
        tasks = {task["id"]: task for task in self.g02["tasks"]}
        self.assertEqual(len(expected), 14)
        for task_id in expected:
            self.assertEqual(tasks[task_id]["status"], "current")
            self.assertIsInstance(tasks[task_id]["source_anchor"], str)
            self.assertIsInstance(tasks[task_id]["answer_anchor"], str)

    def test_r1_g02_lessons_07_and_08_are_transfer_tasks(self):
        tasks = {task["id"]: task for task in self.g02["tasks"]}
        self.assertEqual(tasks["G02-P01"]["role"], "P")
        self.assertEqual(tasks["G02-P01"]["source_anchor"], "l07")
        self.assertEqual(tasks["G02-P02"]["role"], "P")
        self.assertEqual(tasks["G02-P02"]["source_anchor"], "l08")

    def test_r1_g02_review_remediation_returns_to_activation_checkpoint(self):
        tasks = {task["id"]: task for task in self.g02["tasks"]}
        expected = ["CP-ON1", "CP-ON2", "CP-ON3"]
        for index in range(1, 7):
            task = tasks[f"G02-S-O-E{index:02d}"]
            self.assertEqual(task["checkpoint_ids"], expected)
            for field in ("next_on_pass", "next_on_error"):
                self.assertEqual(
                    task[field],
                    {"kind": "activation_checkpoint", "checkpoint_ids": expected},
                )

    def test_multi_review_checkpoint_task_rejects_static_return(self):
        for field in ("next_on_pass", "next_on_error"):
            with self.subTest(field=field):
                manifest = copy.deepcopy(self.g02)
                task = next(task for task in manifest["tasks"] if task["id"] == "G02-S-O-E01")
                task[field] = "CP-ON1"
                self.assertIn("task.path-static-activation", self.issue_codes(manifest, self.g02_path))

    def test_activation_checkpoint_requires_full_trigger_scope(self):
        manifest = copy.deepcopy(self.g02)
        task = next(task for task in manifest["tasks"] if task["id"] == "G02-S-O-E01")
        task["next_on_error"]["checkpoint_ids"] = ["CP-ON1", "CP-ON2"]
        self.assertIn("task.path-activation-scope", self.issue_codes(manifest, self.g02_path))

    def test_schema_document_is_valid_json(self):
        data = json.loads(checker.SCHEMA_PATH.read_text(encoding="utf-8"))
        self.assertEqual(data["properties"]["schema_version"]["const"], 1)
        self.assertEqual(
            set(data["$defs"]["task"]["properties"]["role"]["enum"]),
            set(self.common["valid_task_roles"]),
        )
        dynamic_target = data["$defs"]["task_transition"]["oneOf"][1]
        self.assertEqual(dynamic_target["properties"]["kind"]["const"], "activation_checkpoint")


if __name__ == "__main__":
    unittest.main(verbosity=2)
