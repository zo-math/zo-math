"""Scoped G02 completion evidence; no publication or PDF build operations."""
from __future__ import annotations
import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import sys
sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[1]
PACKAGE = Path('content/thpt/on_thi_toan_thpt/hoc_lieu/r1_g02')

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def save(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')

def protected():
    folders = ['content/thpt/on_thi_toan_thpt/hoc_lieu/r1_g01',
        'content/thpt/on_thi_toan_thpt/hoc_lieu/d0', 'docs/content/thpt/on_thi_toan_thpt',
        '_design/ngon_ngu_thiet_ke_zo_math_0_4/06_nguon',
        '_design/ngon_ngu_thiet_ke_zo_math_0_4/07_mau_thi_giac']
    paths = [ROOT/'.git/index', ROOT/'_quarto.yml']
    paths += [p for folder in folders for p in (ROOT/folder).rglob('*') if p.is_file()]
    paths += list((ROOT/PACKAGE).glob('*.pdf'))
    return {p.relative_to(ROOT).as_posix(): sha(p) for p in paths}

def run(mode, output):
    output = (ROOT/output).resolve()
    if not output.is_relative_to(ROOT/'_audit'): raise ValueError('Output must be inside _audit')
    output.mkdir(parents=True, exist_ok=True)
    if mode == 'snapshot':
        if (output/'protected-before.json').exists(): raise ValueError('Do not overwrite baseline')
        save(output/'protected-before.json', protected())
        shutil.copyfile(ROOT/PACKAGE/'index.qmd', output/'source-before.qmd')
        save(output/'worktree-before.json', {'status': subprocess.check_output(
            ['git','status','--short'], cwd=ROOT, text=True, encoding='utf-8')})
        print('Protected snapshot saved')
        return
    if mode == 'render':
        skip = shutil.ignore_patterns('__pycache__','.quarto','_freeze','.git','*.pyc')
        with tempfile.TemporaryDirectory(prefix='source_render_', dir=output) as temp:
            mirror = Path(temp)
            for name in ['scripts','assets','quy_trinh_xay_dung','projects','_projects','figures','images',
                'content/thpt/on_thi_toan_thpt','_design/web_2027_mau_dung_chung',
                '_design/ngon_ngu_thiet_ke_zo_math_0_4/07_mau_thi_giac']:
                if (ROOT/name).is_dir(): shutil.copytree(ROOT/name, mirror/name, ignore=skip)
            for p in ROOT.iterdir():
                if p.is_file() and (p.suffix in {'.yml','.yaml','.qmd','.md','.scss','.json','.toml'} or p.name in {'CNAME','.gitattributes','.gitignore'}):
                    shutil.copyfile(p, mirror/p.name)
            for folder in ['content','content/thpt']:
                for p in (ROOT/folder).glob('_metadata.*'):
                    (mirror/folder).mkdir(parents=True, exist_ok=True); shutil.copyfile(p, mirror/folder/p.name)
            shutil.copyfile(ROOT/'.git/index', mirror/'isolated.index')
            env = dict(os.environ, GIT_DIR=str(ROOT/'.git'), GIT_WORK_TREE=str(mirror), GIT_INDEX_FILE=str(mirror/'isolated.index'))
            command = ['python','scripts/zo_python.py','scripts/zo_qmd.py','render',str(PACKAGE/'index.qmd')]
            with (output/'render.log').open('w',encoding='utf-8') as log:
                result = subprocess.run(command,cwd=mirror,env=env,stdout=log,stderr=subprocess.STDOUT)
            if result.returncode: raise RuntimeError('Configured render failed: render.log')
            # Keep a fresh raw render and its own assets, never use stale root docs.
            shutil.copytree(mirror/'docs', output/'raw', dirs_exist_ok=True)
            save(output/'render-provenance.json', {'source':str(PACKAGE/'index.qmd'),
                'source_sha256':sha(ROOT/PACKAGE/'index.qmd'), 'command':command,
                'include_hashes':{p.relative_to(ROOT).as_posix():sha(p) for p in (ROOT/'content/thpt/on_thi_toan_thpt/hoc_lieu/_dung_chung/nen').glob('*.qmd')},
                'source_only':True,'production_output_changed':False,'pdf_build':False})
        print('Fresh isolated HTML rendered; mirror cleaned')
    elif mode == 'preview':
        from zo_web_2027_g02 import build
        from zo_web_2027_g02_payloads import apply
        print(build(output,output/'raw'/PACKAGE/'index.html'))
        save(output/'payloads.json',apply(output/'g02-reading.html',output))
    elif mode == 'pdf-status':
        records=[]
        for variant in ['full','student','bai_hoc','luyen_tap','kiem_tra','sua_loi','on_lai','loi_giai']:
            result=subprocess.run(['python','scripts/zo_python.py','scripts/zo_pdf.py','status',str(PACKAGE/'index.qmd'),'--variant',variant],cwd=ROOT,capture_output=True,text=True,encoding='utf-8')
            records.append({'variant':variant,'exit_code':result.returncode,'output':result.stdout+result.stderr})
        save(output/'pdf-status.json',records)
        print('\n'.join(f"{r['variant']}: {r['output'].split(':',1)[0]}" for r in records))
    elif mode == 'protected':
        before = json.loads((output/'protected-before.json').read_text(encoding='utf-8'))
        changed = [name for name,digest in before.items() if not (ROOT/name).is_file() or sha(ROOT/name)!=digest]
        save(output/'protected-result.json', {'files':len(before),'changed':changed})
        if changed: raise ValueError('Protected files changed: '+repr(changed))
        print(f'Protected {len(before)} files unchanged')

if __name__ == '__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('mode',choices=['snapshot','render','preview','protected','pdf-status'])
    parser.add_argument('--output',default='_audit/zo_g02_completion_2026-10-08')
    args=parser.parse_args();run(args.mode,args.output)
