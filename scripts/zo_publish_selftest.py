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
GOVERNANCE = SECTION + "/_quy_trinh"


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
        with target.open("w", encoding="utf-8", newline="\n") as stream:
            stream.write(text)

    def validation(self):
        manifest = publish.build_manifest(self.public, self.config)
        return publish.validate_public(self.public, manifest, self.config)["issues"]

    def candidate_dirs(self) -> tuple[Path, Path, Path]:
        raw = self.public / "raw"
        target = self.public / "target"
        candidate = self.public / "candidate"
        raw.mkdir()
        target.mkdir()
        return raw, target, candidate

    @staticmethod
    def write_at(root: Path, relative: str, text: str) -> None:
        path = root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("w", encoding="utf-8", newline="\n") as stream:
            stream.write(text)

    def test_private_governance_denies_all_asset_types(self) -> None:
        paths = [f"{GOVERNANCE}/sample{suffix}" for suffix in
                 (".html", ".pdf", ".svg", ".png", ".jpg", ".css", ".js", ".json", ".woff2")]
        for path in paths:
            self.write(path, "fixture")
        manifest = publish.build_manifest(self.public, self.config)
        self.assertEqual(set(manifest["files"]), {"CNAME"})
        self.assertEqual({item["path"] for item in manifest["issues"]}, set(paths))

    def test_normalized_deny_paths(self) -> None:
        deny = self.config["denylist"]
        variants = (
            GOVERNANCE + "/a.pdf", "/" + GOVERNANCE + "/a.pdf",
            GOVERNANCE.upper() + "/a.pdf", GOVERNANCE.replace("/", "\\") + "\\a.pdf",
            SECTION + "/temp/../_quy_trinh/a.pdf",
            SECTION + "//./_quy_trinh/a.pdf?download=1#page=2",
            SECTION + "%2F_quy_trinh%2Fa.pdf",
            SECTION + "%252F_quy_trinh%252Fa.pdf",
            "https://zomath.vn/" + GOVERNANCE + "/a.pdf",
            SECTION + "/&#95;quy_trinh/a.pdf",
        )
        for path in variants:
            with self.subTest(path=path):
                self.assertTrue(publish.path_denied(path, deny["paths"], deny["globs"]))
        self.assertFalse(publish.path_denied(SECTION + "/index.html", deny["paths"], deny["globs"]))

    def test_private_governance_survives_section_opening(self) -> None:
        deny = self.config["denylist"]
        self.assertFalse(publish.path_denied(SECTION + "/index.html", deny["paths"], deny["globs"]))
        for path in ("_quy_trinh/a.pdf", SECTION + "/_quy_trinh/a.pdf",
                     SECTION + "/hoc_lieu/r1_g01/_quy_trinh/lich_su/v1_1/a.html"):
            with self.subTest(path=path):
                self.assertTrue(publish.path_denied(path, deny["paths"], deny["globs"]))

    def test_injected_manifest_is_rejected(self) -> None:
        path = "content%2fthpt%2fon_thi_toan_thpt%2f_quy_trinh%2fsecret.pdf"
        result = publish.validate_public(self.public, {"files": {"CNAME": {}, path: {}}}, self.config)
        self.assertIn({"type": "forbidden-manifest", "path": path}, result["issues"])

    def test_html_links_and_literal_paths(self) -> None:
        variants = (
            f'<a href="/{GOVERNANCE}/index.html">test</a>',
            f'<img src="/{GOVERNANCE}/image.png">',
            f'<img srcset="/{GOVERNANCE}/image.png 2x">',
            f'<p>{GOVERNANCE}/secret.pdf</p>',
            '<script>const p="content\\/thpt\\/on_thi_toan_thpt\\/_quy_trinh\\/secret.pdf";</script>',
            '<a href="content%252fthpt%252fon_thi_toan_thpt%252f_quy_trinh%252fsecret.pdf">x</a>',
            '<p>content/thpt/&#111;n_thi_toan_thpt/&#95;quy_trinh/secret.pdf</p>',
            '<a href="scripts/zo_publish.py">not one of the first three denies</a>',
        )
        for html in variants:
            with self.subTest(html=html):
                self.write("index.html", html)
                self.assertTrue(any(i["type"] == "private-reference" for i in self.validation()))

    def test_relative_private_link(self) -> None:
        self.write(f"{SECTION}/public/index.html", '<a href="../%5fquy_trinh/a.pdf">x</a>')
        self.assertTrue(any(i["type"] == "private-link" for i in self.validation()))

    def test_search_private_navigation_but_not_snippet_is_rejected(self) -> None:
        self.write("index.html", "public")
        for sample in (
            json.dumps([{"href": f"{GOVERNANCE}/index.html#intro"}]),
            '[{"href":"content\\u002fthpt\\u002fon_thi_toan_thpt\\u002f_quy_trinh\\u002findex.html"}]',
        ):
            with self.subTest(sample=sample):
                self.write("search.json", sample)
                self.assertTrue(any(i["type"] == "private-reference" for i in self.validation()))
        self.write("search.json", json.dumps([
            {"href": "index.html", "text": f"Internal {GOVERNANCE}/secret.pdf"},
        ]))
        self.assertEqual(self.validation(), [])

    def test_search_normalization_uses_manifest_targets_and_is_deterministic(self) -> None:
        self.write("index.html", "public")
        self.write("content/thpt/index.html", "public")
        records = [
            {"href": "index.html#intro", "text": f"Literal {GOVERNANCE}/secret.pdf"},
            {"href": "https://zomath.vn/content/thpt/index.html?x=1#intro"},
            {"href": "content/thpt/"},
            {"href": "/content%2Fthpt%2Findex.html#encoded"},
            {"href": f"{GOVERNANCE}/index.html"},
            {"href": "content/thpt/missing.html"},
        ]
        self.write("search.json", json.dumps(records))
        manifest = publish.build_manifest(self.public, self.config)
        report = publish.normalize_public_indexes(self.public, manifest, self.config)
        normalized = json.loads((self.public / "search.json").read_text(encoding="utf-8"))
        self.assertEqual(normalized, records[:4])
        self.assertEqual(report["indexes"]["search.json"]["before"], 6)
        self.assertEqual(report["indexes"]["search.json"]["after"], 4)
        self.assertEqual(report["indexes"]["search.json"]["removed_by_reason"], {
            "denied-target": 1, "missing-target": 1,
        })
        first = (self.public / "search.json").read_bytes()
        self.assertNotIn(b"\r\n", first)
        publish.normalize_public_indexes(self.public, manifest, self.config)
        self.assertEqual((self.public / "search.json").read_bytes(), first)
        self.assertEqual(self.validation(), [])

    def test_sitemap_url_and_sitemap_index(self) -> None:
        for root_tag, entry_tag in (("urlset", "url"), ("sitemapindex", "sitemap")):
            with self.subTest(tag=root_tag):
                self.write("sitemap.xml", f'<{root_tag} xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
                           f'<{entry_tag}><loc>https://zomath.vn/{GOVERNANCE}/index.html?x=1&amp;y=2</loc>'
                           f'</{entry_tag}></{root_tag}>')
                self.assertTrue(any(i["type"] == "private-reference" for i in self.validation()))

    def test_sitemap_normalization_filters_denied_and_missing_targets(self) -> None:
        self.write("index.html", "public")
        self.write("content/thpt/index.html", "public")
        self.write("sitemap.xml", '''<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url><loc>https://zomath.vn/index.html#top</loc></url>
  <url><loc>content/thpt/?x=1</loc></url>
  <url><loc>https://zomath.vn/content%2Fthpt%2Findex.html</loc></url>
  <url><loc>https://zomath.vn/''' + GOVERNANCE + '''/index.html</loc></url>
  <url><loc>https://zomath.vn/content/thpt/missing.html</loc></url>
</urlset>''')
        manifest = publish.build_manifest(self.public, self.config)
        report = publish.normalize_public_indexes(self.public, manifest, self.config)
        root = publish.ElementTree.parse(self.public / "sitemap.xml").getroot()
        entries = [node for node in list(root) if node.tag.rsplit("}", 1)[-1] == "url"]
        self.assertEqual(len(entries), 3)
        self.assertEqual(report["indexes"]["sitemap.xml"]["removed_by_reason"], {
            "denied-target": 1, "missing-target": 1,
        })
        first = (self.public / "sitemap.xml").read_bytes()
        self.assertNotIn(b"\r\n", first)
        publish.normalize_public_indexes(self.public, manifest, self.config)
        self.assertEqual((self.public / "sitemap.xml").read_bytes(), first)
        self.assertEqual(self.validation(), [])

    def test_missing_search_target_is_rejected_before_normalization(self) -> None:
        self.write("search.json", json.dumps([{"href": "missing.html"}]))
        self.assertTrue(any(i["type"] == "missing-index-target" for i in self.validation()))

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

    def test_check_normalizes_indexes_before_validation(self) -> None:
        self.write("search.json", json.dumps([{"href": f"{GOVERNANCE}/index.html"}]))
        self.config["output_dir"] = self.public.relative_to(ROOT).as_posix()
        state = {"issues": [], "branch": "test", "commit": "test", "status": []}
        with patch.dict(os.environ, {"QUARTO_PROFILE": ""}), \
                patch.object(publish, "repo_root", return_value=ROOT), \
                patch.object(publish, "load_config", return_value=(ROOT / "publish_public.yml", self.config)), \
                patch.object(publish, "find_publish_worktree", return_value=self.public), \
                patch.object(publish, "git_state", return_value=state), \
                redirect_stdout(io.StringIO()) as output:
            self.assertEqual(publish.main(["check"]), publish.EXIT_OK)
            self.assertNotIn("private-reference", output.getvalue())

    def test_candidate_filters_raw_private_files_and_normalizes_indexes(self) -> None:
        raw, target, candidate = self.candidate_dirs()
        config = copy.deepcopy(self.config)
        config["required_files"] = ["CNAME", ".nojekyll"]
        self.write_at(raw, "CNAME", config["custom_domain"]["cname"])
        self.write_at(raw, "index.html", '<a href="index.html">public</a>')
        self.write_at(raw, f"{GOVERNANCE}/secret.html", "private")
        self.write_at(raw, "search.json", json.dumps([
            {"href": "index.html"}, {"href": f"{GOVERNANCE}/secret.html"},
        ]))
        self.write_at(raw, "sitemap.xml", '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
                      '<url><loc>https://zomath.vn/index.html</loc></url>'
                      f'<url><loc>https://zomath.vn/{GOVERNANCE}/secret.html</loc></url></urlset>')
        before = publish.tree_manifest(raw)
        result = publish.build_public_candidate(raw, candidate, target, config)
        self.assertEqual(result["issues"], [])
        self.assertNotIn(f"{GOVERNANCE}/secret.html", result["manifest"]["files"])
        self.assertEqual(len(json.loads((candidate / "search.json").read_text(encoding="utf-8"))), 1)
        sitemap = publish.ElementTree.parse(candidate / "sitemap.xml").getroot()
        self.assertEqual(len(list(sitemap)), 1)
        self.assertTrue((candidate / ".nojekyll").is_file())
        self.assertFalse((raw / ".nojekyll").exists())
        self.assertEqual(publish.tree_manifest(raw), before)

    def test_candidate_still_rejects_private_html_and_missing_resource(self) -> None:
        for html, issue_type in (
            (f'<p>{GOVERNANCE}/secret.pdf</p>', "private-reference"),
            ('<img src="missing.png">', "missing-resource"),
        ):
            with self.subTest(issue=issue_type):
                raw = self.public / f"raw-{issue_type}"
                target = self.public / f"target-{issue_type}"
                candidate = self.public / f"candidate-{issue_type}"
                raw.mkdir()
                target.mkdir()
                self.write_at(raw, "CNAME", self.config["custom_domain"]["cname"])
                self.write_at(raw, "index.html", html)
                result = publish.build_public_candidate(raw, candidate, target, self.config)
                self.assertTrue(any(item["type"] == issue_type for item in result["issues"]))

    def test_candidate_requires_non_generated_required_files(self) -> None:
        raw, target, candidate = self.candidate_dirs()
        config = copy.deepcopy(self.config)
        config["required_files"] = ["CNAME", "index.html", ".nojekyll"]
        self.write_at(raw, "CNAME", config["custom_domain"]["cname"])
        result = publish.build_public_candidate(raw, candidate, target, config)
        self.assertTrue((candidate / ".nojekyll").is_file())
        self.assertFalse(any(item.get("path") == ".nojekyll" for item in result["issues"]))
        self.assertTrue(any(item["type"] == "missing-required" and item["path"] == "index.html"
                            for item in result["issues"]))

    def test_candidate_keeps_symlink_sensitive_and_size_guards(self) -> None:
        for issue_type in ("symlink", "sensitive-content", "oversize"):
            with self.subTest(issue=issue_type):
                raw = self.public / f"guard-raw-{issue_type}"
                target = self.public / f"guard-target-{issue_type}"
                candidate = self.public / f"guard-candidate-{issue_type}"
                raw.mkdir()
                target.mkdir()
                config = copy.deepcopy(self.config)
                self.write_at(raw, "CNAME", config["custom_domain"]["cname"])
                if issue_type == "sensitive-content":
                    self.write_at(raw, "index.html", "C:/Users/example/private")
                elif issue_type == "oversize":
                    config["default_max_file_size"] = 3
                    self.write_at(raw, "index.html", "public")
                scanner = patch.object(publish, "scan_symlinks", return_value=["link"])
                context = scanner if issue_type == "symlink" else patch.object(
                    publish, "scan_symlinks", wraps=publish.scan_symlinks)
                with context:
                    result = publish.build_public_candidate(raw, candidate, target, config)
                self.assertTrue(any(item["type"] == issue_type for item in result["issues"]))

    def test_candidate_builder_is_deterministic_and_preserves_inputs(self) -> None:
        raw, target, first = self.candidate_dirs()
        second = self.public / "candidate-second"
        self.write_at(raw, "CNAME", self.config["custom_domain"]["cname"])
        self.write_at(raw, "index.html", "public")
        raw_before = publish.tree_manifest(raw)
        target_before = publish.tree_manifest(target, True)
        one = publish.build_public_candidate(raw, first, target, self.config)
        two = publish.build_public_candidate(raw, second, target, self.config)
        for key in ("manifest", "manifest_sha256", "diff", "validation"):
            self.assertEqual(one[key], two[key])
        self.assertEqual(publish.tree_manifest(raw), raw_before)
        self.assertEqual(publish.tree_manifest(target, True), target_before)

    def test_candidate_builder_refuses_existing_directory_without_deleting_it(self) -> None:
        raw, target, candidate = self.candidate_dirs()
        self.write_at(raw, "CNAME", self.config["custom_domain"]["cname"])
        candidate.mkdir()
        marker = candidate / "keep.txt"
        marker.write_text("keep", encoding="utf-8")
        with self.assertRaises(publish.ConfigError):
            publish.build_public_candidate(raw, candidate, target, self.config)
        self.assertEqual(marker.read_text(encoding="utf-8"), "keep")

    def test_scoped_candidate_preserves_published_bytes_for_unchanged_source_output(self) -> None:
        baseline = self.public / "scope-baseline"
        rendered = self.public / "scope-rendered"
        target = self.public / "scope-target"
        candidate = self.public / "scope-candidate"
        for root in (baseline, rendered, target):
            root.mkdir()
            self.write_at(root, "CNAME", self.config["custom_domain"]["cname"])
        outside = "content/thpt/scope/unchanged.html"
        inside = "content/thpt/scope/changed.html"
        self.write_at(target, outside, "published bytes\n")
        self.write_at(baseline, outside, "baseline render drift\n")
        self.write_at(rendered, outside, "current render drift\n")
        self.write_at(target, inside, "published old\n")
        self.write_at(baseline, inside, "baseline old\n")
        self.write_at(rendered, inside, "source-derived new\n")

        result = publish.build_scoped_candidate(
            baseline, rendered, candidate, target, self.config,
            allowed_outputs={inside},
        )

        self.assertEqual(result["issues"], [])
        self.assertEqual((candidate / outside).read_bytes(), (target / outside).read_bytes())
        self.assertEqual((candidate / inside).read_bytes(), (rendered / inside).read_bytes())
        self.assertIn(outside, result["preserved_render_drift"])
        self.assertIn(outside, result["raw_source_output_diff"]["update"])
        self.assertNotIn(outside, result["source_output_diff"]["update"])
        self.assertEqual(result["diff"]["update"], [inside])

    def test_candidate_normalization_passes_git_diff_check(self) -> None:
        raw, target, candidate = self.candidate_dirs()
        self.write_at(target, "CNAME", self.config["custom_domain"]["cname"])
        self.write_at(target, "index.html", "<main>old</main>\n")
        self.write_at(target, "search.json", '[{"href":"index.html"}]\n')
        self.write_at(target, "sitemap.xml",
                      "<urlset><url><loc>https://zomath.vn/index.html</loc></url></urlset>\n")
        self.write_at(raw, "CNAME", self.config["custom_domain"]["cname"])
        self.write_at(raw, "index.html",
                      '<main>\n<div class="sidebar-item-container"> \n</main>\n')
        (raw / "search.json").write_bytes(b'[\r\n  {"href":"index.html"}\r\n]\r\n')
        (raw / "sitemap.xml").write_bytes(
            b'<urlset>\r\n<url><loc>https://zomath.vn/index.html</loc></url>\r\n</urlset>\r\n'
        )

        result = publish.build_public_candidate(raw, candidate, target, self.config)
        self.assertEqual(result["issues"], [])
        self.assertNotIn(b"\r\n", (candidate / "search.json").read_bytes())
        self.assertNotIn(b"\r\n", (candidate / "sitemap.xml").read_bytes())
        self.assertNotIn(b"> \n", (candidate / "index.html").read_bytes())

        repository = self.public / "diff-check-repository"
        repository.mkdir()
        publish.copy_manifest(target, repository, publish.tree_manifest(target))
        self.assertEqual(publish.run(["git", "init"], repository).returncode, 0)
        self.assertEqual(publish.run(["git", "add", "."], repository).returncode, 0)
        committed = publish.run([
            "git", "-c", "user.name=ZO Math Test", "-c", "user.email=test@example.invalid",
            "commit", "-m", "baseline",
        ], repository)
        self.assertEqual(committed.returncode, 0, committed.stderr)
        before = publish.tree_manifest(repository, True)
        publish.sync_exact(candidate, repository, result["public_manifest"],
                           publish.exact_diff(before, result["public_manifest"]))
        checked = publish.run(["git", "diff", "--check"], repository)
        self.assertEqual(checked.returncode, 0, checked.stdout + checked.stderr)

    def test_candidate_does_not_strip_meaningful_preformatted_whitespace(self) -> None:
        raw, target, candidate = self.candidate_dirs()
        self.write_at(raw, "CNAME", self.config["custom_domain"]["cname"])
        self.write_at(raw, "index.html", "<pre>\nmeaningful  \n</pre>\n")

        result = publish.build_public_candidate(raw, candidate, target, self.config)

        self.assertIn(b"meaningful  \n", (candidate / "index.html").read_bytes())
        self.assertTrue(any(item["type"] == "trailing-whitespace"
                            and item["path"] == "index.html" for item in result["issues"]))

    def test_check_temporary_candidate_is_cleaned_on_pass_and_failure(self) -> None:
        state = {"issues": [], "branch": "test", "commit": "test", "status": []}
        real_temporary = tempfile.TemporaryDirectory
        created: list[Path] = []

        class RecordingTemporaryDirectory(real_temporary):
            def __enter__(self):
                name = super().__enter__()
                created.append(Path(name))
                return name

        self.config["output_dir"] = self.public.relative_to(ROOT).as_posix()
        for mode in ("pass", "validation", "exception"):
            created.clear()
            if mode == "validation":
                self.write("index.html", f"<p>{GOVERNANCE}/secret.pdf</p>")
            side_effect = RuntimeError("fixture failure") if mode == "exception" else None
            builder = patch.object(publish, "build_public_candidate", side_effect=side_effect) if mode == "exception" else patch.object(
                publish, "build_public_candidate", wraps=publish.build_public_candidate)
            with patch.dict(os.environ, {"QUARTO_PROFILE": ""}), \
                    patch.object(publish, "repo_root", return_value=ROOT), \
                    patch.object(publish, "load_config", return_value=(ROOT / "publish_public.yml", self.config)), \
                    patch.object(publish, "find_publish_worktree", return_value=self.public), \
                    patch.object(publish, "git_state", return_value=state), \
                    patch.object(publish.tempfile, "TemporaryDirectory", RecordingTemporaryDirectory), \
                    builder, redirect_stdout(io.StringIO()), redirect_stderr(io.StringIO()):
                result = publish.main(["check"])
            self.assertEqual(result, publish.EXIT_OK if mode == "pass" else publish.EXIT_UNSAFE)
            self.assertTrue(created)
            self.assertTrue(all(not path.exists() for path in created))


if __name__ == "__main__":
    unittest.main(verbosity=2)
