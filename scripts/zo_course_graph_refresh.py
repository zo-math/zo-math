"""Refresh source-owned graph pairs from their manifest through the official tool."""
import argparse,hashlib,json,re,shutil,tempfile
from pathlib import Path
from zo_graphics import load_graph,graphics_root
ROOT=Path(__file__).resolve().parents[1]
def digest(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def inputs(root=ROOT):
    tool=graphics_root(root)
    values={str(p.relative_to(tool)).replace('\\','/'):digest(p) for p in [tool/'zo_graph.py',tool/'graph/zo_graph_build.py',tool/'graph/axis_ticks.py',tool/'graph/tex/zo_graph_v02.tex',tool/'graph/tex/zo_graph_v04.tex',tool/'graph/profiles/lesson-g03.json',*sorted((tool/'assets/fonts').glob('STIXTwo*.otf'))]}
    values['project/scripts/zo_course_graph_refresh.py']=digest(Path(root)/'scripts/zo_course_graph_refresh.py')
    return values
def refresh(package, reviewed_sources=()):
    package=Path(package).resolve();package.relative_to(ROOT/'content/thpt/on_thi_toan_thpt/hoc_lieu')
    path=package/'giao_dien/hinh_manifest.json';manifest=json.loads(path.read_text('utf-8'));before=inputs();engine=load_graph('refresh_owned_graphs')
    with tempfile.TemporaryDirectory(prefix='owned_graphs_',dir=ROOT/'.quarto') as temp:
        for figure in manifest['figures']:
            source=package/figure['input'];text=source.read_text('utf-8')
            if digest(source)!=figure['input_sha256'] and source.name not in reviewed_sources:
                raise ValueError('Canonical source changed without review: '+str(source))
            height='8' if re.search(r'height\s*=\s*8cm',text) else '7'
            args=[str(source),'--style','0.4','--surface','paper','--layout','lesson-g03','--frame-height-cm',height,'--check','--out-dir',temp]
            pdf,svg=engine.build(engine.parse_args(args))
            for key,generated in [('pdf',pdf),('svg',svg)]:
                target=package/figure[key];shutil.copyfile(generated,target);figure[key+'_sha256']=digest(target)
            figure['input_sha256']=digest(source)
            print('Refreshed '+figure['name'],flush=True)
        if before!=inputs():raise ValueError('Graph tool inputs changed during refresh')
    manifest['source_hashes']=before;manifest['tool']='scripts/zo_course_graph_refresh.py via zo_graphics graph --style 0.4 --layout lesson-g03 --check'
    path.write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n','utf-8')
if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('package',type=Path);parser.add_argument('--reviewed-source',action='append',default=[]);args=parser.parse_args();refresh(args.package,args.reviewed_source)
