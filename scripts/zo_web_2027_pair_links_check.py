"""M37: ordinary routing tables preserve fresh canonical links.

Journal sample table T18 is package-bound deliberately, not a routing table.
Reads isolated evidence only; no render, learner-source or Git writes.
"""
import argparse,copy,json,sys,hashlib
from pathlib import Path
sys.dont_write_bytecode=True
from bs4 import BeautifulSoup
ROOT=Path(__file__).resolve().parents[1]
BASE=Path('content/thpt/on_thi_toan_thpt/hoc_lieu')
def predicates(raw,rendered):
    checks={}
    for n in raw.select('.table-scroll[id]'):
        if n['id']=='r1-table-t18':continue
        links={a['href'] for a in n.select('a[href]')}
        if not links:continue
        target=rendered.find(id=n['id'])
        checks[n['id']]=bool(target) and links<={a['href'] for a in target.select('a[href]')}
    return checks
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--audit',type=Path,required=True);args=ap.parse_args();out=args.audit.resolve()
    if not out.is_relative_to(ROOT/'_audit'):raise ValueError('Audit only')
    checks={};inputs={Path(__file__).resolve()}
    for pkg in ['r1_g01','r1_g02']:
        parse=lambda p:BeautifulSoup(p.read_text(encoding='utf-8'),'html.parser')
        rawpath=out/'raw-final'/(pkg+'-raw/docs')/BASE/pkg/'index.html'
        renderedpath=out/'after'/(pkg+'-render/docs')/BASE/pkg/'index.html'
        raw=parse(rawpath);rendered=parse(renderedpath)
        inputs.update([rawpath,renderedpath,ROOT/BASE/pkg/'index.qmd',ROOT/BASE/pkg/f'cong_cu/{pkg}.lua'])
        actual=predicates(raw,rendered)
        checks[pkg+' nonempty routing inventory']=bool(actual)
        checks.update({pkg+'/'+k:v for k,v in actual.items()})
        broken=copy.deepcopy(rendered)
        table=next(iter(actual));a=broken.find(id=table).select_one('a[href]')
        # Remove every occurrence of the selected link, not just its first copy.
        href=a['href']
        for link in list(broken.find(id=table).select('a[href]')):
            if link['href']==href:link.decompose()
        checks[pkg+' negative missing href rejected']=not predicates(raw,broken)[table]
    report={'checks':checks,'passed':sum(checks.values()),'total':len(checks),'scope':'Fresh raw to final ordinary routing tables; journal example adaptation excluded explicitly.','failures':[k for k,v in checks.items() if not v],'input_hashes':{p.relative_to(ROOT).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(inputs)}}
    (out/'table-link-review.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(report,ensure_ascii=False));return int(not all(checks.values()))
if __name__=='__main__':raise SystemExit(main())
