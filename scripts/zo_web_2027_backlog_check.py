"""Owned local actions, full-text hierarchy and repair routing: QD_031."""
import copy,json,re
from pathlib import Path
from zo_r1_g01_labels import local_answer_pair

ORDER=['bat-dau','bai-hoc','phieu-luyen','tu-kiem-tra','on-lai','on-nen','sua-loi','nhat-ky','loi-giai','nguon','tai-tai-lieu']

def source_checks(path,binding):
    text=Path(path).read_text(encoding='utf-8');result={}
    result['source peer order before JavaScript']=re.findall(r'^## [^\n]*\{#([^ }]+)',text,re.M)==ORDER
    result['source journal included once']=text.count('include ../_dung_chung/nhat_ki_hoc_tap.qmd')==1
    positions=[]
    for u in binding['units']:
        if u['function']!='function.remediation':continue
        for key in ['question','answer']:
            anchor=re.search(r'\{#'+re.escape(u[key])+r'(?=[\s}])',text)
            if not anchor:result[u['id']+'/'+key+' source anchor']=False;continue
            line=text.rfind('\n',0,anchor.start())+1
            if not re.match(r'#{3,4} Nhiệm vụ',text[line:]):line=text.index('\n',anchor.start())+1
            heading=re.search(r'(?m)^(?:#{3,4} )?(Nhiệm vụ \d\d[^\n{]*)(?: \{#.*)?$',text[line:])
            result[u['id']+'/'+key+' canonical title matches binding']=bool(heading and heading.start()<300 and heading[1].strip()==u['title'])
            if key=='question':positions.append((anchor.start(),u['number']))
        for label,target in re.findall(r'\[([^\]]+)\]\(#([^\)]+)\)',text):
            number=re.search(r'nhiệm vụ (\d\d)',label,re.I)
            if target==u['question'] and number:result[u['id']+'/source link number '+label]=int(number[1])==u['number']
    numbers=[n for _,n in sorted(positions)]
    result['source repair order has continuous numbers']=bool(numbers) and numbers==sorted(set(numbers))
    return result

def require_source(path,binding):
    result=source_checks(path,binding);fail=[k for k,v in result.items() if not v]
    if fail:raise ValueError('QD_031 canonical source guard: '+str(fail))
    return result

def checks(doc,binding):
    root=doc.select_one('.reader-content');result={}
    sections=root.select(':scope > section.level2')
    result['full-text canonical peer order']=[n.get('id') for n in sections]==ORDER
    result['journal is independent peer']=root.find(id='nhat-ky').parent is root
    result['journal has 14 shared fields']=len(root.select('#r1-table-t13 tbody tr'))==14
    result['review does not contain journal or repair']=not root.find(id='on-lai').select('#nhat-ky,#sua-loi-sau-on-lai')
    groups=['sua-loi-sau-luyen-tap','sua-loi-sau-kiem-tra','sua-loi-sau-on-lai']
    actual=[n.get('id') for n in root.find(id='sua-loi').select(':scope > section') if n.get('id') in groups]
    result['repair groups follow caller order']=actual==groups
    tasks=[]
    for node in root.find(id='sua-loi').select('[data-zo-type=task][data-zo-function="function.remediation"]'):
        tasks.append(int(node['data-zo-number']))
        result[node['id']+' has a repair group owner']=any(node.find_parent(id=g) for g in groups)
    result['repair numbering follows actual reading order']=bool(tasks) and tasks==sorted(set(tasks))
    for group in binding.get('group_ownership',[]):
        selected=[u for u in binding['units'] if u['function']==group['function'] and u['number'] in group['numbers']]
        for unit in selected:
            q,a=root.find(id=unit['question']),root.find(id=unit['answer'])
            result[unit['id']+' exact question group owner']=bool(q and q.find_parent(id=group['question_owner']))
            result[unit['id']+' exact answer group owner']=bool(a and a.find_parent(id=group['answer_owner']))
    for unit in binding['units']:
        if not unit.get('answer'):continue
        q,a=root.find(id=unit['question']),root.find(id=unit['answer'])
        if q is None or a is None:result[unit['id']+' task and answer exist']=False;continue
        local=local_answer_pair(q,a)
        for node,target,direction in [(q,unit['answer'],'forward'),(a,unit['question'],'return')]:
            links=node.select('.answer-link a[href="#'+target+'"]')
            result[unit['id']+'/'+direction+' appropriate action']=len(links)==(0 if local else 1)
    tid='r1-table-t12' if binding['package']=='R1-G01' else 'r1-g02-table-t04'
    table=root.find(id=tid).find('table')
    result['routing is four common columns']=[n.get_text(' ',strip=True) for n in table.select('thead th')]==['Dấu hiệu cần sửa','Sau Luyện tập','Sau Kiểm tra','Sau Ôn lại']
    result['routing retains package row count']=len(table.select('tbody tr'))==(9 if binding['package']=='R1-G01' else 8)
    result['routing symptoms do not mix in directions']='Cách sửa:' not in table.get_text()
    by_id={u['question']:u for u in binding['units']}
    for link in table.select('a[href]'):
        target=link['href'].removeprefix('#');unit=by_id.get(target)
        if unit and unit['function']=='function.remediation':result[target+' routing exact task title']=link.get_text(' ',strip=True)==unit['title']
    result['sentence initial task cells capitalized']=not any(re.match(r'^nhiệm vụ\s',cell.get_text(' ',strip=True)) for cell in root.select('td'))
    result['all disclosures closed']=not root.select('details[open]')
    return result

def require(doc,binding):
    result=checks(doc,binding);fail=[k for k,v in result.items() if not v]
    if fail:raise ValueError('QD_031 structural guard: '+str(fail))
    return result

def fixtures(doc,binding):
    """Negative tests run the actual predicates, rather than a surrogate count."""
    results={};root=doc.select_one('.reader-content')
    unit=next(u for u in binding['units'] if u.get('answer') and local_answer_pair(root.find(id=u['question']),root.find(id=u['answer'])))
    broken=copy.deepcopy(doc);q=broken.find(id=unit['question'])
    from bs4 import BeautifulSoup
    q.append(BeautifulSoup('<div class="answer-link"><a href="#'+unit['answer']+'">Xem lời giải</a></div>','html.parser'))
    results['negative redundant local action']=not all(checks(broken,binding).values())
    broken=copy.deepcopy(doc);broken.find(id='on-lai').append(broken.find(id='nhat-ky').extract())
    results['negative journal nested in review']=not all(checks(broken,binding).values())
    broken=copy.deepcopy(doc);broken.find(id='sua-loi').insert(0,broken.find(id='sua-loi-sau-on-lai').extract())
    results['negative after-review placed first']=not all(checks(broken,binding).values())
    broken=copy.deepcopy(doc);tid='r1-table-t12' if binding['package']=='R1-G01' else 'r1-g02-table-t04'
    broken.find(id=tid).select_one('tbody a').string='Nhiệm vụ 99'
    results['negative routing mismatched title']=not all(checks(broken,binding).values())
    broken=copy.deepcopy(doc)
    unit=next(u for u in binding['units'] if u['function']=='function.remediation' and u['number']==1)
    broken.find(id='loi-giai-kiem-tra').append(broken.find(id=unit['answer']).extract())
    results['negative answer moved to wrong group']=not all(checks(broken,binding).values())
    return results
