"""Rebuild the four course pages in a disposable source tree without audit history."""
from __future__ import annotations
import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

from zo_build_boundary import ROOT, require_repository

BASE = Path('content/thpt/on_thi_toan_thpt')
PAGES = {
    'home': BASE/'tot_nghiep_thpt/2027/index.qmd',
    'd0': BASE/'hoc_lieu/d0/index.qmd',
    'g01': BASE/'hoc_lieu/r1_g01/index.qmd',
    'g02': BASE/'hoc_lieu/r1_g02/index.qmd',
}


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    output = args.output.resolve()
    if not output.is_relative_to(ROOT/'_audit') or output == ROOT/'_audit' or output.exists():
        parser.error('Use a new named report directory under _audit')
    output.mkdir(parents=True)
    result = {'source_boundary': require_repository(), 'pages': {}, 'passed': False,
              'audit_history_copied': False, 'published': False}
    result['tool_hashes'] = {name: sha(ROOT/name) for name in [
        'scripts/zo_build_boundary.py', 'scripts/zo_build_runtime/sitecustomize.py',
        'scripts/zo_quarto.py', 'scripts/zo_build_boundary_verify.py',
        'scripts/zo_web_2027_production.py', 'scripts/zo_web_2027_figures.py',
        'scripts/zo_pdf.py']}
    protected = list(PAGES.values()) + [BASE/'tot_nghiep_thpt/2027/giao_dien/trang_nha.html.tpl']
    protected += [p.relative_to(ROOT) for p in (ROOT/'docs').rglob('*') if p.is_file()]
    before = {str(p): sha(ROOT/p) for p in protected}
    try:
        with tempfile.TemporaryDirectory(prefix='source_', dir=output) as temporary:
            mirror = Path(temporary)
            ignored = shutil.ignore_patterns('_audit', '__pycache__', '.quarto',
                                             '.ipynb_checkpoints', '*_cache', '*_files')
            for name in ['scripts', 'assets', 'quy_trinh_xay_dung', 'figures', 'images',
                         '_projects', 'projects', 'content/thpt/on_thi_toan_thpt',
                         'content/support', '_design/web_2027_mau_dung_chung',
                         '_design/ngon_ngu_thiet_ke_zo_math_0_4/07_mau_thi_giac']:
                source = ROOT/name
                if source.is_dir():
                    shutil.copytree(source, mirror/name, ignore=ignored)
            for source in ROOT.iterdir():
                if source.is_file() and source.suffix in {'.yml', '.yaml', '.qmd', '.md', '.scss', '.json', '.toml'}:
                    shutil.copyfile(source, mirror/source.name)
            for folder in ['content', 'content/thpt']:
                for source in (ROOT/folder).iterdir():
                    if not source.is_file() or (folder != 'content' and not source.name.startswith('_metadata')):
                        continue
                    destination = mirror/source.relative_to(ROOT)
                    destination.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copyfile(source, destination)
            shutil.copyfile(ROOT/'CNAME', mirror/'CNAME')
            result['clean_source_boundary'] = require_repository(mirror)
            result['audit_absent_before_render'] = not (mirror/'_audit').exists()
            for key, source in PAGES.items():
                print('Building without audit history:', key, flush=True)
                command = ['python', 'scripts/zo_python.py', 'scripts/zo_quarto.py',
                           'render', source.as_posix(), '--profile', 'on-thi-preview', '--to', 'html']
                with (output/(key+'.log')).open('w', encoding='utf-8') as log:
                    code = subprocess.run(command, cwd=mirror, env=os.environ.copy(),
                                          stdout=log, stderr=subprocess.STDOUT).returncode
                page = mirror/'docs'/source.with_suffix('.html')
                result['pages'][key] = {'returncode': code, 'html_exists': page.is_file()}
                if code:
                    raise RuntimeError(key + ' failed; see ' + str(output/(key+'.log')))
                result['pages'][key]['html_sha256'] = sha(page)
                from bs4 import BeautifulSoup
                doc = BeautifulSoup(page.read_text(encoding='utf-8'), 'html.parser')
                result['pages'][key]['adapter'] = doc.body.get('data-zo-web-production')
                if not result['pages'][key]['adapter']:
                    raise RuntimeError(key + ': canonical adapter did not run')
            result['audit_absent_after_render'] = not (mirror/'_audit').exists()
            result['passed'] = result['audit_absent_before_render'] and result['audit_absent_after_render']
    except Exception as exc:
        result['error'] = str(exc)
    finally:
        result['source_and_docs_unchanged'] = before == {str(p): sha(ROOT/p) for p in protected}
        result['passed'] = result['passed'] and result['source_and_docs_unchanged']
        (output/'result.json').write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return int(not result['passed'])


if __name__ == '__main__':
    raise SystemExit(main())
