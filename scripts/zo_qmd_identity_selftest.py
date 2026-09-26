"""Opt-in artifact identities and dependency receipts; fixtures stay in _audit."""
from __future__ import annotations

import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from pypdf import PdfWriter
import yaml

from zo_pdf_contract import (
    canonical_pdf_provenance_path, canonical_variant_input_state,
    update_canonical_pdf_provenance, validate_canonical_pdf_provenance,
    pdf_build_receipt_path, qmd_artifact_key, validate_pdf_build_receipt,
    write_pdf_build_receipt,
    pdf_output_path, pdf_variant,
)
from zo_qmd_config import discover_project_config


ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT/'content/thpt/on_thi_toan_thpt/hoc_lieu/r1_g01/_quy_trinh/cau_hinh_san_xuat_qmd.yml'


class IdentityTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix='qmd_identity_', dir=ROOT/'_audit')
        self.addCleanup(self.tmp.cleanup)
        self.base = Path(self.tmp.name)
        self.base.resolve().relative_to((ROOT/'_audit').resolve())
        self.pages = []
        for name in ['one', 'two']:
            package = self.base/name
            (package/'_quy_trinh/ho_so').mkdir(parents=True)
            config = yaml.safe_load(CONFIG.read_text(encoding='utf-8'))
            config['project']['id'] = 'fixture_'+name
            config['project']['root'] = package.relative_to(ROOT).as_posix()
            config['extensions']['artifact_inputs'] = ['table.json', 'figure.png', 'filter.lua']
            (package/'_quy_trinh/cau_hinh_san_xuat_qmd.yml').write_text(yaml.safe_dump(config), encoding='utf-8')
            (package/'_quy_trinh/ho_so/index.yml').write_text('publication: pending\n', encoding='utf-8')
            for filename in ['index.qmd', 'index.pdf', 'table.json', 'figure.png', 'filter.lua']:
                (package/filename).write_bytes(b'fixture\n')
            self.pages.append(package/'index.qmd')

    def make_pdf(self, path, pages=1):
        writer = PdfWriter()
        for _ in range(pages):
            writer.add_blank_page(width=595, height=842)
        with path.open('wb') as handle:
            writer.write(handle)

    def make_canonical_provenance(self, source):
        cfg = yaml.safe_load((source.parent/'_quy_trinh/cau_hinh_san_xuat_qmd.yml').read_text(encoding='utf-8'))
        for index, name in enumerate(cfg['extensions']['pdf_variants'], start=1):
            output = pdf_output_path(ROOT, source, name)
            self.make_pdf(output, 1 + (index % 2))
            state = canonical_variant_input_state(ROOT, source, name)
            update_canonical_pdf_provenance(
                ROOT, source, output, variant=name, expected_input_state=state,
            )
        return canonical_pdf_provenance_path(ROOT, source)

    def test_index_identity_and_profile_isolation(self):
        a, b = self.pages
        self.assertNotEqual(qmd_artifact_key(ROOT, a), qmd_artifact_key(ROOT, b))
        self.assertNotEqual(pdf_build_receipt_path(ROOT, a), pdf_build_receipt_path(ROOT, b))
        configs = [discover_project_config(ROOT, p.relative_to(ROOT)) for p in self.pages]
        self.assertNotEqual(configs[0].profile_path_for(a.relative_to(ROOT)), configs[1].profile_path_for(b.relative_to(ROOT)))

    def test_receipt_tracks_all_dependencies(self):
        source = self.pages[0]
        output = source.with_suffix('.pdf')
        receipt = self.base/'receipt.json'
        write_pdf_build_receipt(ROOT, source, output, receipt)
        self.assertEqual(validate_pdf_build_receipt(ROOT, source, output, receipt), [])
        for filename in ['table.json', 'figure.png', 'filter.lua', 'index.qmd', 'index.pdf']:
            path = source.parent/filename
            old = path.read_bytes()
            path.write_bytes(old+b'drift')
            self.assertTrue(validate_pdf_build_receipt(ROOT, source, output, receipt), filename)
            path.write_bytes(old)

    def test_config_drift_and_missing_dependency_fail(self):
        source = self.pages[0]
        receipt = self.base/'receipt.json'
        write_pdf_build_receipt(ROOT, source, source.with_suffix('.pdf'), receipt)
        config_path = source.parent/'_quy_trinh/cau_hinh_san_xuat_qmd.yml'
        config = yaml.safe_load(config_path.read_text(encoding='utf-8'))
        config['extensions']['artifact_inputs'].pop()
        config_path.write_text(yaml.safe_dump(config), encoding='utf-8')
        self.assertTrue(validate_pdf_build_receipt(ROOT, source, source.with_suffix('.pdf'), receipt))

    def test_legacy_project_keys_unchanged(self):
        for relative in [
            'content/thpt/zo_math_100/100_ham_so_su_bien_thien_va_do_thi/core/ham_ln_x.qmd',
            'content/thpt/zo_math_100/100_bai_toan_thuc_te/core/chi_phi_di_taxi.qmd',
        ]:
            source = Path(relative)
            self.assertEqual(qmd_artifact_key(ROOT, source), source.stem)
            self.assertEqual(pdf_build_receipt_path(ROOT, source).name, source.stem+'_pdf_build.json')

    def test_unsafe_dependency_rejected(self):
        source = self.pages[0]
        config_path = source.parent/'_quy_trinh/cau_hinh_san_xuat_qmd.yml'
        config = yaml.safe_load(config_path.read_text(encoding='utf-8'))
        config['extensions']['artifact_inputs'] = ['../outside']
        config_path.write_text(yaml.safe_dump(config), encoding='utf-8')
        with self.assertRaises(ValueError):
            write_pdf_build_receipt(ROOT, source, source.with_suffix('.pdf'), self.base/'receipt.json')

    def test_variant_outputs_receipts_and_cross_use(self):
        source = self.pages[0]
        full = pdf_output_path(ROOT, source)
        student = pdf_output_path(ROOT, source, 'student')
        self.assertNotEqual(full, student)
        self.assertNotEqual(pdf_build_receipt_path(ROOT, source), pdf_build_receipt_path(ROOT, source, 'student'))
        student.write_bytes(b'%PDF-student')
        rf, rs = self.base/'full.json', self.base/'student.json'
        write_pdf_build_receipt(ROOT, source, full, rf)
        write_pdf_build_receipt(ROOT, source, student, rs, variant='student')
        self.assertEqual(validate_pdf_build_receipt(ROOT, source, full, rf), [])
        self.assertEqual(validate_pdf_build_receipt(ROOT, source, student, rs, variant='student'), [])
        self.assertTrue(validate_pdf_build_receipt(ROOT, source, full, rs))
        self.assertTrue(validate_pdf_build_receipt(ROOT, source, student, rf, variant='student'))
        for filename in ['index.qmd', 'table.json', 'figure.png', 'filter.lua']:
            p = source.parent/filename
            old = p.read_bytes()
            p.write_bytes(old+b'drift')
            self.assertTrue(validate_pdf_build_receipt(ROOT, source, full, rf))
            self.assertTrue(validate_pdf_build_receipt(ROOT, source, student, rs, variant='student'))
            p.write_bytes(old)

    def test_variant_config_drift_and_output_collision(self):
        source = self.pages[0]
        receipt = self.base/'full.json'
        write_pdf_build_receipt(ROOT, source, source.with_suffix('.pdf'), receipt)
        path = source.parent/'_quy_trinh/cau_hinh_san_xuat_qmd.yml'
        cfg = yaml.safe_load(path.read_text(encoding='utf-8'))
        cfg['extensions']['pdf_variants']['student']['metadata']['subtitle'] = 'changed'
        path.write_text(yaml.safe_dump(cfg), encoding='utf-8')
        self.assertTrue(validate_pdf_build_receipt(ROOT, source, source.with_suffix('.pdf'), receipt))
        cfg['extensions']['pdf_variants']['student']['output'] = 'index.pdf'
        path.write_text(yaml.safe_dump(cfg), encoding='utf-8')
        with self.assertRaises(ValueError):
            pdf_output_path(ROOT, source, 'student')

    def test_additional_variant_and_registry_validation(self):
        source = self.pages[0]
        path = source.parent/'_quy_trinh/cau_hinh_san_xuat_qmd.yml'
        original = yaml.safe_load(path.read_text(encoding='utf-8'))
        cfg = yaml.safe_load(path.read_text(encoding='utf-8'))
        cfg['extensions']['pdf_variants']['part_one'] = {
            'output': 'index_part_one.pdf',
            'include_support': False,
            'metadata': {'subtitle': 'Part one'},
        }
        path.write_text(yaml.safe_dump(cfg), encoding='utf-8')
        self.assertEqual(pdf_output_path(ROOT, source, 'part_one'), source.with_name('index_part_one.pdf'))
        self.assertEqual(pdf_variant(ROOT, source, 'part_one')['metadata']['subtitle'], 'Part one')
        self.assertFalse(pdf_variant(ROOT, source, 'part_one')['include_support'])
        with self.assertRaises(ValueError):
            pdf_output_path(ROOT, source, 'missing')

        for invalid_name in ('BadName', 'two-parts', '../escape'):
            cfg = yaml.safe_load(yaml.safe_dump(original))
            cfg['extensions']['pdf_variants'][invalid_name] = {
                'output': 'safe.pdf', 'metadata': {},
            }
            path.write_text(yaml.safe_dump(cfg), encoding='utf-8')
            with self.assertRaises(ValueError):
                pdf_variant(ROOT, source)

        for unsafe_output in ('../escape.pdf', 'nested/escape.pdf', r'nested\\escape.pdf'):
            cfg = yaml.safe_load(yaml.safe_dump(original))
            cfg['extensions']['pdf_variants']['extra'] = {
                'output': unsafe_output, 'metadata': {},
            }
            path.write_text(yaml.safe_dump(cfg), encoding='utf-8')
            with self.assertRaises(ValueError):
                pdf_variant(ROOT, source)

        cfg = yaml.safe_load(yaml.safe_dump(original))
        cfg['extensions']['pdf_variants']['extra'] = {
            'output': cfg['extensions']['pdf_variants']['full']['output'],
            'metadata': {},
        }
        path.write_text(yaml.safe_dump(cfg), encoding='utf-8')
        with self.assertRaises(ValueError):
            pdf_variant(ROOT, source)

        cfg = yaml.safe_load(yaml.safe_dump(original))
        cfg['extensions']['pdf_variants']['full']['include_support'] = 'no'
        path.write_text(yaml.safe_dump(cfg), encoding='utf-8')
        with self.assertRaises(ValueError):
            pdf_variant(ROOT, source)

    def test_legacy_default_output_and_student_rejected(self):
        source = ROOT/'content/thpt/zo_math_100/100_ham_so_su_bien_thien_va_do_thi/core/ham_ln_x.qmd'
        self.assertEqual(pdf_output_path(ROOT, source), source.with_suffix('.pdf'))
        with self.assertRaises(ValueError):
            pdf_output_path(ROOT, source, 'student')

    def test_failed_isolated_build_preserves_existing_outputs(self):
        import zo_pdf
        source = self.pages[0]
        full = source.with_suffix('.pdf')
        student = pdf_output_path(ROOT, source, 'student')
        student.write_bytes(b'old-student')
        before = [full.read_bytes(), student.read_bytes()]
        def fake_run(command, **kwargs):
            mirror = kwargs['cwd']
            self.assertNotEqual(mirror, ROOT)
            # Simulate Quarto deleting its intermediate, then failing.
            (mirror/source.relative_to(ROOT)).with_suffix('.pdf').unlink()
            return type('Result', (), {'returncode': 1})()
        with patch.object(zo_pdf.subprocess, 'run', side_effect=fake_run):
            self.assertEqual(zo_pdf.build(source, 'student'), 1)
        self.assertEqual([full.read_bytes(), student.read_bytes()], before)

    def test_canonical_provenance_valid_and_manifest_failures(self):
        source = self.pages[0]
        manifest = self.make_canonical_provenance(source)
        registry = yaml.safe_load((source.parent/'_quy_trinh/cau_hinh_san_xuat_qmd.yml').read_text(encoding='utf-8'))['extensions']['pdf_variants']
        self.assertTrue(all(validate_canonical_pdf_provenance(ROOT, source, variant=name) == [] for name in registry))
        original = manifest.read_bytes()
        manifest.unlink()
        self.assertTrue(validate_canonical_pdf_provenance(ROOT, source))
        manifest.write_bytes(original)

        payload = json.loads(original)
        payload['pdf_provenance_schema_version'] = 999
        manifest.write_text(json.dumps(payload), encoding='utf-8')
        self.assertTrue(validate_canonical_pdf_provenance(ROOT, source))
        for unsafe in ('C:/outside.pdf', '../outside.pdf'):
            payload = json.loads(original)
            payload['variants'][0]['output']['path'] = unsafe
            manifest.write_text(json.dumps(payload), encoding='utf-8')
            self.assertTrue(any('path' in error.lower() for error in validate_canonical_pdf_provenance(ROOT, source)))

    def test_canonical_provenance_variant_registry_contract(self):
        source = self.pages[0]
        manifest = self.make_canonical_provenance(source)
        original = manifest.read_bytes()
        payload = json.loads(original)
        payload['variants'].pop()
        manifest.write_text(json.dumps(payload), encoding='utf-8')
        self.assertTrue(any('variant' in error for error in validate_canonical_pdf_provenance(ROOT, source)))
        payload = json.loads(original)
        payload['variants'].append(payload['variants'][0])
        manifest.write_text(json.dumps(payload), encoding='utf-8')
        self.assertTrue(any('duplicate variant' in error for error in validate_canonical_pdf_provenance(ROOT, source)))

        manifest.write_bytes(original)
        config_path = source.parent/'_quy_trinh/cau_hinh_san_xuat_qmd.yml'
        config = yaml.safe_load(config_path.read_text(encoding='utf-8'))
        config['extensions']['pdf_variants']['student']['metadata']['subtitle'] = 'registry drift'
        config_path.write_text(yaml.safe_dump(config), encoding='utf-8')
        self.assertTrue(validate_canonical_pdf_provenance(ROOT, source, variant='student'))

    def test_canonical_provenance_detects_every_input_and_pdf_drift(self):
        mutations = ('index.qmd', 'filter.lua', 'figure.png')
        for filename in mutations:
            source = self.pages[0]
            self.make_canonical_provenance(source)
            path = source.parent/filename
            original = path.read_bytes()
            path.write_bytes(original+b'drift')
            self.assertTrue(validate_canonical_pdf_provenance(ROOT, source), filename)
            path.write_bytes(original)

        source = self.pages[0]
        self.make_canonical_provenance(source)
        output = pdf_output_path(ROOT, source)
        output.write_bytes(output.read_bytes()+b'drift')
        self.assertTrue(any('PDF hash drift' in error for error in validate_canonical_pdf_provenance(ROOT, source)))

    def test_canonical_provenance_detects_config_and_input_set_drift(self):
        source = self.pages[0]
        self.make_canonical_provenance(source)
        config_path = source.parent/'_quy_trinh/cau_hinh_san_xuat_qmd.yml'
        original = config_path.read_bytes()
        config = yaml.safe_load(original)
        config['extensions']['artifact_inputs'].pop()
        config_path.write_text(yaml.safe_dump(config), encoding='utf-8')
        self.assertTrue(validate_canonical_pdf_provenance(ROOT, source))
        config_path.write_bytes(original)

        self.make_canonical_provenance(source)
        config = yaml.safe_load(original)
        (source.parent/'extra.asset').write_bytes(b'extra')
        config['extensions']['artifact_inputs'].append('extra.asset')
        config_path.write_text(yaml.safe_dump(config), encoding='utf-8')
        self.assertTrue(validate_canonical_pdf_provenance(ROOT, source))

    def test_audit_receipt_cannot_rescue_manifest_and_mtime_is_irrelevant(self):
        source = self.pages[0]
        manifest = self.make_canonical_provenance(source)
        output = pdf_output_path(ROOT, source)
        receipt = self.base/'valid-audit-receipt.json'
        write_pdf_build_receipt(ROOT, source, output, receipt)
        manifest.unlink()
        self.assertEqual(validate_pdf_build_receipt(ROOT, source, output, receipt), [])
        self.assertTrue(validate_canonical_pdf_provenance(ROOT, source))

        manifest = self.make_canonical_provenance(source)
        os.utime(source, (1, 1))
        os.utime(output, (2, 2))
        self.assertEqual(validate_canonical_pdf_provenance(ROOT, source), [])

    def test_single_variant_update_does_not_revalidate_other_variants(self):
        source = self.pages[0]
        self.make_canonical_provenance(source)
        filter_path = source.parent/'filter.lua'
        filter_path.write_bytes(filter_path.read_bytes()+b'new pipeline')
        state = canonical_variant_input_state(ROOT, source, 'full')
        update_canonical_pdf_provenance(
            ROOT, source, pdf_output_path(ROOT, source),
            variant='full', expected_input_state=state,
        )
        self.assertEqual(validate_canonical_pdf_provenance(ROOT, source, variant='full'), [])
        self.assertTrue(any('fingerprint' in error for error in validate_canonical_pdf_provenance(ROOT, source, variant='student')))

    def test_mid_build_input_drift_cannot_be_certified(self):
        source = self.pages[0]
        manifest = self.make_canonical_provenance(source)
        before_manifest = manifest.read_bytes()
        state = canonical_variant_input_state(ROOT, source, 'full')
        filter_path = source.parent/'filter.lua'
        filter_path.write_bytes(filter_path.read_bytes()+b'mid-build drift')
        with self.assertRaises(RuntimeError):
            update_canonical_pdf_provenance(
                ROOT, source, pdf_output_path(ROOT, source),
                variant='full', expected_input_state=state,
            )
        self.assertEqual(manifest.read_bytes(), before_manifest)

    def test_legacy_project_does_not_opt_in_to_canonical_manifest(self):
        source = ROOT/'content/thpt/zo_math_100/100_ham_so_su_bien_thien_va_do_thi/core/ham_ln_x.qmd'
        self.assertIsNone(canonical_pdf_provenance_path(ROOT, source))


if __name__ == '__main__':
    unittest.main()
