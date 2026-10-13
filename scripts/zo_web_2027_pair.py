"""Scoped pair refinement: isolated configured renders, never PDF or release."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import yaml

ROOT=Path(__file__).resolve().parents[1]
BASE=Path('content/thpt/on_thi_toan_thpt/hoc_lieu')
def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()
def save(path,data):path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command',choices=['snapshot','raw','render','protect','promote-g01'])
    parser.add_argument('--package',choices=['r1_g01','r1_g02'])
    parser.add_argument('--output',type=Path,default=Path('_audit/zo_web_pair_refinement_2026-10-08'))
    args=parser.parse_args();out=(ROOT/args.output).resolve()
    if not out.is_relative_to(ROOT/'_audit'):raise ValueError('Audit output only')
    out.mkdir(parents=True,exist_ok=True)
    if args.command=='snapshot':
        if (out/'before.json').exists():raise ValueError('Do not overwrite snapshot')
        protected=[ROOT/'.git/index',ROOT/'_quarto.yml']
        for folder in ['docs/content/thpt/on_thi_toan_thpt','content/thpt/on_thi_toan_thpt/hoc_lieu/d0','content/thpt/on_thi_toan_thpt/tot_nghiep_thpt/2027','_design/ngon_ngu_thiet_ke_zo_math_0_4/06_nguon','_design/ngon_ngu_thiet_ke_zo_math_0_4/07_mau_thi_giac']:
            protected.extend(p for p in (ROOT/folder).rglob('*') if p.is_file())
        for package in ['r1_g01','r1_g02']:
            source=ROOT/BASE/package
            protected.extend(source.glob('*.pdf'))
            shutil.copyfile(source/'index.qmd',out/(package+'-before.qmd'))
        shutil.copyfile(ROOT/BASE/'r1_g01/giao_dien/web_2027_layout.json',out/'g01-layout-before.json')
        shutil.copyfile(ROOT/BASE/'r1_g01/giao_dien/web_2027_accepted.json',out/'g01-accepted-before.json')
        save(out/'before.json',{p.relative_to(ROOT).as_posix():sha(p) for p in protected})
        save(out/'worktree-before.json',{'status':subprocess.check_output(['git','status','--short'],cwd=ROOT,text=True,encoding='utf-8')})
        print('Snapshot saved');return
    if args.command=='protect':
        before=json.loads((out/'before.json').read_text(encoding='utf-8'))
        allowed_prefix='docs/'+(BASE/'r1_g01').as_posix()+'/'
        changed=[n for n,h in before.items() if not (ROOT/n).is_file() or sha(ROOT/n)!=h]
        unexpected=[n for n in changed if not n.startswith(allowed_prefix)]
        save(out/'protected-result.json',{'files':len(before),'authorized_g01_output_changes':[n for n in changed if n not in unexpected],'unexpected':unexpected})
        print('Unexpected protected changes:',unexpected);raise SystemExit(bool(unexpected))
    if not args.package and args.command!='promote-g01':parser.error('--package required')
    if args.command=='promote-g01':
        generated=out/'r1_g01-render/docs'
        qa=json.loads((out/'pair-qa.json').read_text(encoding='utf-8'))
        page=generated/BASE/'r1_g01/index.html'
        hashes={Path(name).as_posix():digest for name,digest in qa['html_hashes'].items()}
        if qa['passed']!=qa['total'] or hashes.get(page.relative_to(ROOT).as_posix())!=sha(page):
            raise ValueError('Promotion requires current passing pair QA and matching G01 HTML')
        if any(sha(ROOT/name)!=digest for name,digest in qa['source_hashes'].items()):
            raise ValueError('Canonical source changed after pair QA')
        allowed=[generated/BASE/'r1_g01/index.html']
        allowed.extend(p for p in (generated/'assets/zo_web_2027').rglob('*') if p.is_file())
        # Copy only declared G01 page + its runtime, never unrelated rendered pages.
        records=[]
        for src in allowed:
            rel=src.relative_to(generated);dest=ROOT/'docs'/rel
            if dest.exists() and sha(src)==sha(dest):continue
            dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(src,dest)
            records.append({'path':dest.relative_to(ROOT).as_posix(),'sha256':sha(dest)})
        save(out/'g01-promotion.json',{'files':records,'published':False,'receipt_updated':False})
        print('G01 local HTML synchronized:',len(records));return
    package=BASE/args.package
    dest=out/(args.package+'-'+args.command)
    dest.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='render_',dir=out) as name:
        mirror=Path(name)
        skip=shutil.ignore_patterns('__pycache__','.quarto','_freeze','.git','*.pyc')
        for folder in ['scripts','assets','quy_trinh_xay_dung','projects','_projects','figures','images','content/thpt/on_thi_toan_thpt','content/support','_design/web_2027_mau_dung_chung','_design/ngon_ngu_thiet_ke_zo_math_0_4/07_mau_thi_giac']:
            if (ROOT/folder).is_dir():shutil.copytree(ROOT/folder,mirror/folder,ignore=skip)
        for p in ROOT.iterdir():
            if p.is_file() and (p.suffix in ['.yml','.yaml','.qmd','.md','.scss','.json','.toml'] or p.name in ['CNAME','.gitattributes','.gitignore']):shutil.copyfile(p,mirror/p.name)
        for folder in ['content','content/thpt']:
            for p in (ROOT/folder).glob('_metadata.*'):
                (mirror/folder).mkdir(parents=True,exist_ok=True);shutil.copyfile(p,mirror/folder/p.name)
        for p in (ROOT/'content').glob('*.qmd'):
            shutil.copyfile(p,mirror/'content'/p.name)
        if args.command=='raw':
            config=yaml.safe_load((mirror/'_quarto.yml').read_text(encoding='utf-8'))
            config['project'].pop('post-render',None)
            (mirror/'_quarto.yml').write_text(yaml.safe_dump(config,allow_unicode=True,sort_keys=False),encoding='utf-8')
        shutil.copyfile(ROOT/'.git/index',mirror/'isolated.index')
        env=dict(os.environ,GIT_DIR=str(ROOT/'.git'),GIT_WORK_TREE=str(mirror),GIT_INDEX_FILE=str(mirror/'isolated.index'))
        command=['python','scripts/zo_python.py','scripts/zo_qmd.py','render',str(package/'index.qmd')]
        with (dest/'render.log').open('w',encoding='utf-8') as log:
            result=subprocess.run(command,cwd=mirror,env=env,stdout=log,stderr=subprocess.STDOUT)
        if result.returncode:raise RuntimeError('Render failed: '+str(dest/'render.log'))
        shutil.copytree(mirror/'docs',dest/'docs',dirs_exist_ok=True)
        save(dest/'provenance.json',{'source':str(package/'index.qmd'),'sha256':sha(ROOT/package/'index.qmd'),'raw_without_post_render':args.command=='raw','command':command,'root_output_changed':False,'learning_pdf_built':False})
    print('Isolated render complete:',dest)
if __name__=='__main__':main()
