"""Opt-in artifact identities and dependency receipts; fixtures stay in _audit."""
from __future__ import annotations

import json
from pathlib import Path
import tempfile
import unittest

import yaml

from zo_pdf_contract import (
    pdf_build_receipt_path, qmd_artifact_key, validate_pdf_build_receipt,
    write_pdf_build_receipt,
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


if __name__ == '__main__':
    unittest.main()
