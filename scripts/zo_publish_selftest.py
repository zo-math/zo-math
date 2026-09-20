"""Targeted publication-boundary tests; fixtures live only in _audit and are removed."""

from __future__ import annotations

import copy
import io
import json
import os
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path
from unittest.mock import patch

import zo_publish as publish


ROOT = Path(__file__).resolve().parents[1]
SECTION = "content/thpt/on_thi_toan_thpt"


class PublicBoundaryTests(unittest.TestCase):
    def setUp(self) -> None:
        audit = ROOT / "_audit"
        audit.mkdir(exist_ok=True)
        self.temporary = tempfile.TemporaryDirectory(prefix="on_thi_public_test_", dir=audit)
        self.public = Path(self.temporary.name).resolve()
        self.public.relative_to(audit.resolve())
        self.addCleanup(self.temporary.cleanup)
        self.config = copy.deepcopy(publish.load_config(ROOT, "publish_public.yml")[1])
        self.config["required_files"] = ["CNAME"]
        self.write("CNAME", self.config["custom_domain"]["cname"])

    def write(self, relative: str, text: str) -> None:
        target = self.public / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text, encoding="utf-8")

    def validation(self):
        manifest = publish.build_manifest(self.public, self.config)
        return publish.validate_public(self.public, manifest, self.config)["issues"]

    def test_section_denies_all_asset_types(self) -> None:
        paths = [f"{SECTION}/sample{suffix}" for suffix in
                 (".html", ".pdf", ".svg", ".png", ".jpg", ".css", ".js", ".json", ".woff2")]
        for path in paths:
            self.write(path, "fixture")
        manifest = publish.build_manifest(self.public, self.config)
        self.assertEqual(set(manifest["files"]), {"CNAME"})
        self.assertEqual({item["path"] for item in manifest["issues"]}, set(paths))

    def test_normalized_deny_paths(self) -> None:
        deny = self.config["denylist"]
        variants = (
            SECTION + "/a.pdf", "/" + SECTION + "/a.pdf",
            SECTION.upper() + "/a.pdf", SECTION.replace("/", "\\") + "\\a.pdf",
            "content/thpt/temp/../on_thi_toan_thpt/a.pdf",
            "content//thpt/./on_thi_toan_thpt/a.pdf?download=1#page=2",
            "content%2Fthpt%2Fon_thi_toan_thpt%2Fa.pdf",
            "content%252Fthpt%252Fon_thi_toan_thpt%252Fa.pdf",
            "https://zomath.vn/" + SECTION + "/a.pdf",
            "content/thpt/&#111;n_thi_toan_thpt/a.pdf",
        )
        for path in variants:
            with self.subTest(path=path):
                self.assertTrue(publish.path_denied(path, deny["paths"], deny["globs"]))
        self.assertFalse(publish.path_denied(SECTION + "_other/a.pdf", deny["paths"], deny["globs"]))

    def test_private_governance_survives_future_section_opening(self) -> None:
        self.config["denylist"]["paths"].remove(SECTION)
        deny = self.config["denylist"]
        self.assertFalse(publish.path_denied(SECTION + "/index.html", deny["paths"], deny["globs"]))
        for path in ("_quy_trinh/a.pdf", SECTION + "/_quy_trinh/a.pdf",
                     SECTION + "/hoc_lieu/r1_g01/_quy_trinh/lich_su/v1_1/a.html"):
            with self.subTest(path=path):
                self.assertTrue(publish.path_denied(path, deny["paths"], deny["globs"]))

    def test_injected_manifest_is_rejected(self) -> None:
        path = "content%2fthpt%2fon_thi_toan_thpt%2fsecret.pdf"
        result = publish.validate_public(self.public, {"files": {"CNAME": {}, path: {}}}, self.config)
        self.assertIn({"type": "forbidden-manifest", "path": path}, result["issues"])

    def test_html_links_and_literal_paths(self) -> None:
        variants = (
            f'<a href="/{SECTION}/index.html">test</a>',
            f'<img src="/{SECTION}/image.png">',
            f'<img srcset="/{SECTION}/image.png 2x">',
            f'<p>{SECTION}/secret.pdf</p>',
            '<script>const p="content\\/thpt\\/on_thi_toan_thpt\\/secret.pdf";</script>',
            '<a href="content%252fthpt%252fon_thi_toan_thpt%252fsecret.pdf">x</a>',
            '<p>content/thpt/&#111;n_thi_toan_thpt/secret.pdf</p>',
            '<a href="scripts/zo_publish.py">not one of the first three denies</a>',
        )
        for html in variants:
            with self.subTest(html=html):
                self.write("index.html", html)
                self.assertTrue(any(i["type"] == "private-reference" for i in self.validation()))

    def test_relative_private_link(self) -> None:
        self.config["denylist"]["paths"].remove(SECTION)
        self.write(f"{SECTION}/public/index.html", '<a href="../%5fquy_trinh/a.pdf">x</a>')
        self.assertTrue(any(i["type"] == "private-link" for i in self.validation()))

    def test_search_url_snippet_and_escaped_json(self) -> None:
        samples = (
            json.dumps([{"href": f"{SECTION}/index.html#intro"}]),
            json.dumps([{"href": "index.html", "text": f"Internal {SECTION}/secret.pdf"}]),
            '[{"href":"content\\u002fthpt\\u002fon_thi_toan_thpt\\u002findex.html"}]',
        )
        for sample in samples:
            with self.subTest(sample=sample):
                self.write("search.json", sample)
                self.assertTrue(any(i["type"] == "private-reference" for i in self.validation()))

    def test_sitemap_url_and_sitemap_index(self) -> None:
        for tag in ("urlset", "sitemapindex"):
            with self.subTest(tag=tag):
                self.write("sitemap.xml", f'<{tag} xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
                           f'<url><loc>https://zomath.vn/{SECTION}/index.html?x=1&amp;y=2</loc></url></{tag}>')
                self.assertTrue(any(i["type"] == "private-reference" for i in self.validation()))

    def test_invalid_indexes_fail_closed(self) -> None:
        for name, text in (("search.json", "{"), ("sitemap.xml", "<urlset>")):
            with self.subTest(name=name):
                self.write(name, text)
                self.assertTrue(any(i["type"] == "invalid-public-index" and i["path"] == name
                                    for i in self.validation()))

    def test_safe_public_content_passes(self) -> None:
        self.write("index.html", '<a href="index.html#intro">public</a>')
        self.write("search.json", json.dumps([{"href": "index.html", "text": "Nội dung công khai."}]))
        self.write("sitemap.xml", '<urlset><url><loc>https://zomath.vn/index.html</loc></url></urlset>')
        self.assertEqual(self.validation(), [])

    def test_preview_environment_is_blocked(self) -> None:
        for profiles in ("on-thi-preview", "pdf,on-thi-preview", " ON-THI-PREVIEW "):
            with self.subTest(profiles=profiles), patch.dict(os.environ, {"QUARTO_PROFILE": profiles}):
                with self.assertRaises(publish.ConfigError):
                    publish.require_public_profile(ROOT)
                with patch.object(publish, "run") as runner:
                    with self.assertRaises(publish.ConfigError):
                        publish.render_to_staging(ROOT, self.public)
                    runner.assert_not_called()

    def test_preview_default_is_blocked(self) -> None:
        self.write("_quarto.yml", "profile:\n  default: on-thi-preview\n")
        with patch.dict(os.environ, {"QUARTO_PROFILE": ""}):
            with self.assertRaises(publish.ConfigError):
                publish.require_public_profile(self.public)

    def test_check_rejects_preview_before_worktree_access(self) -> None:
        with patch.dict(os.environ, {"QUARTO_PROFILE": "on-thi-preview"}), \
                patch.object(publish, "repo_root", return_value=ROOT), \
                patch.object(publish, "find_publish_worktree") as worktree, redirect_stderr(io.StringIO()):
            self.assertEqual(publish.main(["check"]), publish.EXIT_USAGE)
            worktree.assert_not_called()

    def test_check_invokes_content_validator(self) -> None:
        self.write("search.json", json.dumps([{"href": f"{SECTION}/index.html"}]))
        self.config["output_dir"] = self.public.relative_to(ROOT).as_posix()
        state = {"issues": [], "branch": "test", "commit": "test", "status": []}
        with patch.dict(os.environ, {"QUARTO_PROFILE": ""}), \
                patch.object(publish, "repo_root", return_value=ROOT), \
                patch.object(publish, "load_config", return_value=(ROOT / "publish_public.yml", self.config)), \
                patch.object(publish, "find_publish_worktree", return_value=self.public), \
                patch.object(publish, "git_state", return_value=state), \
                patch.object(publish, "publish_diff", return_value={}), redirect_stdout(io.StringIO()) as output:
            self.assertEqual(publish.main(["check"]), publish.EXIT_UNSAFE)
            self.assertIn("private-reference", output.getvalue())


if __name__ == "__main__":
    unittest.main(verbosity=2)
