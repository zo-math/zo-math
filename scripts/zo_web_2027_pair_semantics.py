"""Check actual answer ownership, not only matching solution headings."""
from pathlib import Path
import copy
import json
from zo_web_2027_pair_check import OUT, PAGES, parse
from zo_web_2027_check import Checks
from zo_web_2027_preview import dump, sha

def main():
    c=Checks(OUT)
    groups={
      1:{'W':'loi-giai-khoi-dong','D':'loi-giai-bai-hoc','L':'loi-giai-luyen-tap','K':'loi-giai-kiem-tra','SL':'loi-giai-sua-loi-sau-luyen-tap','SK':'loi-giai-sua-loi-sau-kiem-tra','O':'loi-giai-on-lai-moi','SO':'loi-giai-sua-loi-sau-on-lai'},
      2:{'W':'loi-giai-khoi-dong','D':'loi-giai-bai-hoc','L':'loi-giai-luyen-tap','K':'loi-giai-kiem-tra','SL':'loi-giai-sua-loi','SK':'loi-giai-sua-loi-sau-kiem-tra','O':'loi-giai-on-lai','SO':'loi-giai-sua-loi-sau-on-lai','P':'loi-giai-chuyen-giao'}}
    expected={
      1:{'W':['lg-khoi-dong','g01-loi-giai-khoi-dong'],'D':[f'lg-d{i:02}' for i in range(1,7)]+['lg-cg01','loi-giai-1','g01-loi-giai-sua-loi-mau'],
        'L':[f'loi-giai-{i}' for i in range(2,10)]+['lg-g01-l08-xn01'],'K':[f'loi-giai-{i}' for i in range(10,15)],
        'SL':['loi-giai-15']+[f'lg-sc{i:02}' for i in range(1,9)],'SK':[f'lg-g01-s-k-e{i:02}' for i in range(1,10)],
        'O':[f'lg-g01-o{i:02}' for i in range(1,4)],'SO':[f'lg-g01-s-o-e{i:02}' for i in range(1,10)]},
      2:{'W':['loi-giai-khoi-dong-01'],'D':[f'loi-giai-bai-hoc-{i:02}' for i in range(1,6)],
        'L':[f'loi-giai-l{i:02}' for i in [1,2,3,4,5,6,9,10,11]]+['loi-giai-l06-cong-thuc'],
        'K':[f'loi-giai-kt{i:02}' for i in range(1,6)],'SL':[f'loi-giai-s{i:02}' for i in range(6)],
        'SK':[f'loi-giai-s-k-e{i:02}' for i in range(1,7)],'O':[f'loi-giai-on-lai-{i:02}' for i in range(1,4)],
        'SO':[f'loi-giai-s-o-e{i:02}' for i in range(1,7)],'P':['loi-giai-l07','loi-giai-l08','loi-giai-thu-lai-chuyen-giao','loi-giai-s-p02']}}
    docs=[parse(p) for p in PAGES]
    for i,doc in enumerate(docs,1):
        inventory=[n.get('id') for n in doc.select('#loi-giai .r1-solution')]
        covered={ident for ids in expected[i].values() for ident in ids}
        c.check(f'G0{i}: all solution disclosures have an explicit category test',sorted(set(inventory)-covered),[])
        for kind,ids in expected[i].items():
            owner=doc.find(id=groups[i][kind])
            c.check(f'G0{i}: category owner {kind}',owner is not None)
            for ident in ids:
                node=doc.find(id=ident)
                c.check(f'G0{i}: answer owned by {kind}: {ident}',node is not None and owner is not None and owner in node.parents)
    journal=lambda d:[[n.get_text(' ',strip=True) for n in row.find_all(['td','th'])] for row in d.select('#r1-table-t13 tr')]
    c.check('Shared blank journal exact cell content',journal(docs[0]),journal(docs[1]))
    broken=copy.deepcopy(docs[1]);answer=broken.find(id='loi-giai-on-lai-01');answer.extract();broken.find(id=groups[2]['K']).append(answer)
    c.check('Negative fixture: answer moved to wrong category rejected',broken.find(id=groups[2]['O']) not in answer.parents)
    failures=[n for n in c.checks if not n['pass']]
    dump(OUT/'answer-ownership-qa.json',{'checks':c.checks,'passed':len(c.checks)-len(failures),'total':len(c.checks),'html_hashes':{str(p):sha(p) for p in PAGES},'checker_sha256':sha(Path(__file__))})
    print(json.dumps({'passed':len(c.checks)-len(failures),'total':len(c.checks),'failures':[n['name'] for n in failures]},ensure_ascii=False))
    return int(bool(failures))
if __name__=='__main__':raise SystemExit(main())
