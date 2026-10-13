"""Explicit maintenance of G01 bindings after an approved QMD edit.

Fresh before/after raw renders are evidence for this command only. Normal
production uses canonical QMD/layout; it never reads this audit directory.
Keeps the approved shell and unaffected reading-region geometry.
"""
import argparse
import copy
import difflib
import json
import re
from pathlib import Path
from bs4 import BeautifulSoup, Comment, NavigableString, Tag
from zo_web_2027_production import ROOT, PACKAGE, PLAN, pools, norm, sha, content_fingerprint


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--audit', type=Path, required=True)
    ap.add_argument('--write', action='store_true');ap.add_argument('--fresh',type=Path); args = ap.parse_args()
    audit = args.audit.resolve()
    if not audit.is_relative_to(ROOT / '_audit'):
        raise ValueError('Maintenance evidence must stay under audit')
    if args.fresh and not args.fresh.resolve().is_relative_to(ROOT/'_audit'):raise ValueError('Fresh evidence must stay under audit')
    raw = lambda phase: BeautifulSoup((args.fresh if phase=='after' and args.fresh else audit / phase / 'r1_g01-raw/docs' / PACKAGE / 'index.html').read_text(encoding='utf-8'), 'html.parser')
    old, fresh = raw('before'), raw('after')
    oldroot, source = old.select_one('.zo-on-thi-package'), fresh.select_one('.zo-on-thi-package')
    oldtexts, oldmaths = pools(oldroot); texts, maths = pools(source)
    plan = json.loads((audit / 'g01-layout-before.json').read_text(encoding='utf-8'))
    result = BeautifulSoup('', 'html.parser')
    def decode(n):
        if 'literal' in n: return NavigableString(n['literal'])
        if 'text' in n: return NavigableString(n.get('leading','') + norm(oldtexts[n['text']]) + n.get('trailing',''))
        if 'math' in n: return copy.deepcopy(oldmaths[n['math']])
        tag = result.new_tag(n['tag'], attrs=copy.deepcopy(n['attrs']))
        for c in n['children']: tag.append(decode(c))
        return tag
    result.append(decode(plan['layout']))
    reader = result.select_one('.reader-content')
    def paper(nodes, role=None):
        wrapper = result.new_tag('div', attrs={'class':'reading-region'})
        if nodes and nodes[0].parent: nodes[0].insert_before(wrapper)
        if role:
            label = result.new_tag('span', attrs={'class':'role','data-reading-label':''});label.string=role;wrapper.append(label)
        for node in nodes: wrapper.append(node.extract())
        return wrapper
    def update(target):
        current = reader.find(id=target); newer = source.find(id=target)
        if not current or not newer: raise ValueError('Missing replacement ' + target)
        current.replace_with(copy.deepcopy(newer))
    # Replace whole policy payloads when paragraph cardinality changes; never
    # retain deleted permission gates through leaf-only binding maintenance.
    for target in ['cp-lt1','cp-lt2','cp-lt3','cp-kt']:
        oldnode=reader.find(id=target);newnode=copy.deepcopy(source.find(id=target))
        if 'reading-region' in oldnode.get('class',[]):newnode['class']=newnode.get('class',[])+['reading-region']
        oldnode.replace_with(newnode)
    # Three approved beats: no nested boxes and no loose headings.
    guide = copy.deepcopy(source.find(id='cách-học-với-tài-liệu-này'))
    existing = reader.find(id='cách-học-với-tài-liệu-này')
    for ident in ['g01-ho-tro-khi-can','g01-chuyen-goi']:
        prior=reader.find(id=ident)
        if prior:prior.decompose()
    for child in list(guide.find_all(recursive=False)):
        if child.name == 'section' and child.get('id') in ('g01-ho-tro-khi-can','g01-chuyen-goi'):
            child['class'] = child.get('class',[]) + ['reading-region']
            existing.insert_before(child.extract())
    guide['class'] = guide.get('class',[]) + ['reading-region']
    existing.insert_before(guide);existing.decompose()
    # Put guide first, then its two following beats (same source owner).
    support = reader.find(id='g01-ho-tro-khi-can'); finish = reader.find(id='g01-chuyen-goi')
    guide.insert_after(support.extract());support.insert_after(finish.extract())
    # Warmup receives atomic IDs/answers without changing its reading beat.
    for target in ['bốn-câu-thử-nền-tn01-đến-tn04','từ-đi-lên-đến-định-nghĩa','định-nghĩa-theo-so-sánh-trong-một-lân-cận',
                   'đồ-thị-của-f-khác-đồ-thị-của-fprime','cùng-bảng-tóm-tắt-không-có-nghĩa-cùng-công-thức','vì-sao-không-tự-gộp-các-khoảng-rời-nhau']:
        oldnode=reader.find(id=target);newnode=copy.deepcopy(source.find(id=target))
        if 'reading-region' in oldnode.get('class',[]): newnode['class']=newnode.get('class',[])+['reading-region']
        oldnode.replace_with(newnode)
    for target in ['thử-nghĩ-trước'] + [f'thử-nghĩ-trước-{n}' for n in range(1,7)]:
        update(target)
    # Rebuild each canonical task payload, including inserted secondary
    # paragraphs (test points). Rebinding only old text leaves cannot project
    # newly inserted prose, even when the mathematics is unchanged.
    from zo_learning_architecture import load_yaml
    manifest=load_yaml(ROOT/PACKAGE/'_quy_trinh/kien_truc_hoc_tap.yml')
    for task in manifest['tasks']:
        target=task['source_anchor'];oldnode=reader.find(id=target)
        newnode=copy.deepcopy(source.find(id=target))
        if 'reading-region' in oldnode.get('class',[]):
            newnode['class']=newnode.get('class',[])+['reading-region']
        oldnode.replace_with(newnode)
    for number,first in [(1,'lt01'),(2,'lt05'),(3,'lt07')]:
        prior_header=reader.find(id=f'g01-c{number}')
        if prior_header:
            if prior_header.select('.zo-learning-task,table,details'):
                raise ValueError('Stage header unexpectedly owns task content')
            prior_header.decompose()
        stage=source.find(id=f'g01-c{number}')
        opening=[copy.deepcopy(n) for n in stage.find_all(recursive=False) if n.name!='section']
        for prior in list(reader.select('p')):
            if prior.get_text(' ',strip=True).startswith(f'Chặng {number} —'):
                parent=prior.find_parent(class_='reading-region');prior.decompose()
                if parent and not parent.get_text(' ',strip=True):parent.decompose()
        target=reader.find(id=first)
        region=target if 'reading-region' in target.get('class',[]) else target.find_parent(class_='reading-region')
        header=paper(opening);header['id']=f'g01-c{number}';region.insert_before(header)
    test = reader.find(id='tu-kiem-tra')
    opening=[]
    for node in source.find(id='tu-kiem-tra').find_all(recursive=False):
        if node.get('id') == 'kt01': break
        opening.append(copy.deepcopy(node))
    test.find(class_='reading-region',recursive=False).replace_with(paper(opening))
    # The result guide belongs to the ended test, not to the solution bank.
    prior=reader.find(id='đọc-kết-quả-tự-kiểm-tra')
    if prior:prior.decompose()
    result_guide=copy.deepcopy(source.find(id='đọc-kết-quả-tự-kiểm-tra'))
    result_guide['class']=result_guide.get('class',[])+['reading-region']
    test.append(result_guide)
    # Rebuild the review opening from source to include its shared calendar
    # pattern; do not flatten new table links into old positional text leaves.
    review=reader.find(id='on-lai')
    opening=[]
    for node in source.find(id='on-lai').find_all(recursive=False):
        if node.name=='section':break
        opening.append(copy.deepcopy(node))
    review.find(class_='reading-region',recursive=False).replace_with(paper(opening))
    # Independent support area, seven includes kept once; answers stay inside.
    foundation = copy.deepcopy(source.find(id='on-nen'))
    oldfoundation = reader.find(id='on-nen');oldfoundation.decompose()
    header = [n for n in foundation.find_all(recursive=False) if n.name != 'details']
    if header: foundation.insert(0,paper(header))
    for details in list(foundation.find_all('details', recursive=False)):
        paper([details])
    repair=reader.find(id='sua-loi');review=reader.find(id='on-lai')
    review.insert_after(foundation);foundation.insert_after(repair.extract())
    # Move the existing after-review papers, not copies, to their true owner.
    start=reader.find(id='sua-loi-sau-on-lai')
    move=[start] + [reader.find(id=f'g01-s-o-e{n:02}') for n in range(1,10)]
    for node in move: repair.append(node.extract())
    # Solutions mirror source hierarchy; exact QMD task payloads retained.
    solution=copy.deepcopy(source.find(id='loi-giai'))
    def wrap(section):
        pending=[]
        def flush():
            if pending:
                paper(pending);pending.clear()
        for node in list(section.find_all(recursive=False)):
            if node.name=='section' or (node.name=='div' and node.select('details.r1-solution')): flush();wrap(node)
            elif node.name=='details': pending.append(node);flush()
            else: pending.append(node)
        flush()
    wrap(solution);reader.find(id='loi-giai').replace_with(solution)
    for region in list(solution.select('.reading-region')):
        meaningful=bool(region.select('li,table,figure,details')) or any(
            p.get_text(' ',strip=True) and not (p.find('strong') and p.get_text(' ',strip=True)==p.find('strong').get_text(' ',strip=True))
            for p in region.find_all('p'))
        if meaningful:continue
        following=region.find_next(class_='reading-region')
        if following and following.find_parent(id='loi-giai'):
            for child in reversed(list(region.contents)):following.insert(0,child.extract())
            region.decompose()
    # Match unchanged leaf text, and explicit one-to-one editorial replacements
    # from fresh canonical renders. Refuse every unresolved binding.
    def strings(node): return [s for s in node.find_all(string=True) if norm(str(s)) and not s.find_parent('math') and not isinstance(s,Comment)]
    before, after = strings(oldroot), strings(source)
    replacements={}
    matcher=difflib.SequenceMatcher(None,[norm(str(s)) for s in before],[norm(str(s)) for s in after],autojunk=False)
    for kind,a,b,c,d in matcher.get_opcodes():
        if kind=='replace' and b-a==d-c:
            for left,right in zip(before[a:b],after[c:d]): replacements[sha(norm(str(left)))]=norm(str(right))
    bindings=json.loads((ROOT/PACKAGE/'giao_dien/he_nhan.json').read_text(encoding='utf-8'))
    # Source-ID bindings are stronger than positional replacements after relocation.
    for original in oldroot.select('[id]'):
        new=source.find(id=original['id'])
        if not new:continue
        left,right=strings(original),strings(new)
        if len(left)==len(right):
            for l,r in zip(left,right):replacements[sha(norm(str(l)))]=norm(str(r))
    unresolved=[]
    for text in strings(reader):
        key=sha(norm(str(text)))
        if key not in texts:
            value=replacements.get(key)
            mechanical=norm(str(text)).replace('Câu hỏi khởi động','nhiệm vụ Khởi động')
            mechanical=re.sub(r'Bài kiểm tra (\d\d)',r'nhiệm vụ \1 của Kiểm tra',mechanical)
            if sha(mechanical) in texts:value=mechanical
            if value and sha(norm(value)) in texts:
                previous = str(text)
                text.replace_with(NavigableString(
                    re.match(r'^\s*', previous).group() + norm(value) +
                    re.search(r'\s*$', previous).group()))
            elif 'data-reading-label' not in text.parent.attrs:
                # Only old presentation labels are literals; never allow an
                # unresolved canonical wording to be silently retained.
                if key in oldtexts:unresolved.append(norm(str(text)))
    # Headings/summary titles come from the new canonical node, not heuristics.
    for oldnode in reader.select('[id]'):
        new=source.find(id=oldnode['id'])
        if not new:continue
        oh=oldnode.find(['h2','h3','h4','h5','h6','summary'],recursive=False)
        nh=new.find(['h2','h3','h4','h5','h6','summary'],recursive=False)
        if oh and nh:oh.replace_with(copy.deepcopy(nh))
    # Re-evaluate after explicit title replacement.
    unresolved=[norm(str(t)) for t in strings(reader) if sha(norm(str(t))) in oldtexts and sha(norm(str(t))) not in texts and 'data-reading-label' not in t.parent.attrs]
    if unresolved:
        print(json.dumps({'unresolved':sorted(set(unresolved))},ensure_ascii=False,indent=2));return 1
    # Table identity binds its entire DOM (including href), not cell text alone.
    # This prevents M37: canonical resource links disappearing on projection.
    for table in source.select('[id].table-scroll'):
        ident=table['id'];current=reader.find(id=ident)
        if current:current.replace_with(copy.deepcopy(table))
    # Existing mathematical figures keep their approved viewport behavior.
    for image in reader.select('figure img'):
        if not image.find_parent(class_='figure-viewport'):
            viewport=result.new_tag('div',attrs={'class':'figure-viewport','tabindex':'0','role':'region','aria-label':image.get('alt','Hình toán học')+' — có thể cuộn ngang'})
            image.wrap(viewport)
    for details in reader.select('details'):details.attrs.pop('open',None)
    def encode(node):
        if isinstance(node,Comment):return None
        if isinstance(node,NavigableString):
            value=str(node);key=sha(norm(value))
            if node.find_parent(class_='zo-on-thi-package') and key in texts:
                return {'text':key,'leading':re.match(r'^\s*',value).group(),'trailing':re.search(r'\s*$',value).group()}
            return {'literal':value}
        if not isinstance(node,Tag):return None
        if node.name=='math':return {'math':sha(norm(node.select_one('annotation').get_text()))}
        attrs=copy.deepcopy(node.attrs)
        if node.name=='img' and isinstance(attrs.get('src'),str):attrs['src']={'package_asset':attrs['src']}
        return {'tag':node.name,'attrs':attrs,'children':[v for c in node.children if (v:=encode(c)) is not None]}
    plan['layout']=encode(result.html);plan['source_fingerprint']=content_fingerprint(source)
    for name,digest in plan['source_asset_hashes'].items():
        current=sha((ROOT/name).read_bytes())
        if current==digest:continue
        if name!=(PACKAGE/'du_lieu/bang_bien_thien.json').as_posix():
            raise ValueError('Unapproved canonical figure change: '+name)
        # Existing 13 tables must retain their exact rows. The only addition
        # in this maintenance pass is BBT14, present in the new O03 answer.
        records=json.loads((ROOT/name).read_text(encoding='utf-8'))
        if isinstance(records,dict):records=records.get('tables',records.get('records'))
        assert len(records)==14 and records[-1]['id']=='BBT14'
        for record in records[:-1]:
            original=oldroot.select_one(f'figure[data-bbt="{record["id"]}"] table.variation')
            rows=[[c.get_text(' ',strip=True) for c in row.find_all(['th','td'],recursive=False)] for row in original.find_all('tr')]
            expected=copy.deepcopy(record['rows'])
            for r in range(1,len(expected)):
                for c in record.get('excluded_columns',[]):expected[r][c]='∥'
            assert rows==expected,record['id']
        plan['source_asset_hashes'][name]=current
    for digest,spec in list(plan['assets'].items()):
        current=sha((ROOT/spec['source']).read_bytes())
        if current!=spec['sha256']:
            if spec['name']!='r1-controller.js':raise ValueError('Unapproved asset change '+spec['name'])
            spec['sha256']=current;plan['assets'][current]=plan['assets'].pop(digest)
            def rekey(n):
                for v in n.get('attrs',{}).values():
                    if isinstance(v,dict) and v.get('asset')==digest:v['asset']=current
                for child in n.get('children',[]):rekey(child)
            rekey(plan['layout'])
    plan['refinement']={'decision':'QD_028','status':'candidate_pending_owner_review','historical_acceptance_retained':True}
    destination=PLAN if args.write else audit/'layout-candidate.json'
    destination.write_text(json.dumps(plan,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'layout':str(destination),'canonical_written':args.write,'regions':len(reader.select('.reading-region'))},ensure_ascii=False))
    return 0

if __name__=='__main__':raise SystemExit(main())
