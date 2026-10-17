"""Regression tests for accidental cross-package/default covers."""
import json
from pathlib import Path
import tempfile
import unittest
from zo_course_cover import BASE, digest, load_cover, check_html

class CoverTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.folder = self.root / BASE / "r1_g04"
        (self.folder / "giao_dien").mkdir(parents=True)
        self.image = self.folder / "giao_dien/cover.svg"
        self.image.write_text('<svg>own illustration</svg>', encoding="utf-8")
        self.record = dict(schema_version=1,package="r1_g04",image="giao_dien/cover.svg",sha256=digest(self.image),approval="approved",selection_reason="Represents the lesson",approval_evidence="Owner approved this proposal")
        self.save()
    def save(self):
        (self.folder / "giao_dien/anh_bia.json").write_text(json.dumps(self.record),encoding="utf-8")
    def test_approved_owned_cover(self):
        self.assertEqual(load_cover(self.root,"r1_g04"),self.image)
    def test_missing_declaration_blocks(self):
        (self.folder / "giao_dien/anh_bia.json").unlink()
        with self.assertRaises(FileNotFoundError):load_cover(self.root,"r1_g04")
    def test_unapproved_blocks(self):
        self.record["approval"]="pending";self.save()
        with self.assertRaises(ValueError):load_cover(self.root,"r1_g04")
    def test_wrong_package_blocks(self):
        self.record["package"]="r1_g01";self.save()
        with self.assertRaises(ValueError):load_cover(self.root,"r1_g04")
    def test_borrowed_path_blocks(self):
        self.record["image"]="../r1_g01/cover.svg";self.save()
        with self.assertRaises(ValueError):load_cover(self.root,"r1_g04")
    def test_modified_image_blocks(self):
        self.image.write_text("changed",encoding="utf-8")
        with self.assertRaises(ValueError):load_cover(self.root,"r1_g04")
    def test_renamed_copy_blocks(self):
        other=self.root/BASE/"r1_g01/giao_dien";other.mkdir(parents=True)
        (other/"anh_bia.json").write_text(json.dumps(dict(self.record,package="r1_g01")),encoding="utf-8")
        with self.assertRaises(ValueError):load_cover(self.root,"r1_g04")
    def test_rendered_wrong_cover_blocks(self):
        page=self.folder/"index.html"
        page.write_text('<figure class="hero-art"><img src="giao_dien/cover.svg"></figure>',encoding="utf-8")
        self.assertTrue(check_html(self.root,"r1_g04",page))
        wrong=self.folder/"wrong.svg";wrong.write_text("other",encoding="utf-8")
        page.write_text('<figure class="hero-art"><img src="wrong.svg"></figure>',encoding="utf-8")
        with self.assertRaises(ValueError):check_html(self.root,"r1_g04",page)

if __name__ == "__main__":unittest.main()
