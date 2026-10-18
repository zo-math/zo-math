"""Package-wide visible type numbering, independent of pedagogical function.

Stable IDs own references; answers reuse their question number. Shared sources
remain neutral and receive package-local numbers only in the projection.
"""
from collections import defaultdict
from pathlib import Path
import re

MODE = 'package-type-v1'
REFERENCE_FUNCTIONS={
    'Luyện tập':{'function.practice','function.confirmation','function.integration','function.transfer'},
    'Kiểm tra':{'function.test'},'Ôn lại':{'function.review'},
    'Sửa lỗi':{'function.remediation'},'Khởi động':{'function.warmup'},
    'Chuyển giao':{'function.transfer'},'Phối hợp':{'function.integration'},
    'Ôn nền':{'function.foundation_confirmation'},
}


def reference_checks(text,data):
    checks={}
    # The shared journal explicitly illustrates G01 in every package. Its
    # sample references belong to that named package, not the host package.
    sample=[]
    if data.get('package')!='R1-G01' and 'Ví dụ dùng một bài của Đơn điệu và cực trị' in text:
        from zo_course_labels import ROOT,binding
        external=binding(ROOT/'content/thpt/on_thi_toan_thpt/hoc_lieu/r1_g01/index.qmd')
        for block in re.finditer(r'(?ms)^::: \{#r1-table-t18[^\n]*\}\n.*?^:::[ \t]*$',text):
            sample.append((block.start(),block.end()))
            checks.update({'G01 journal example '+k:v for k,v in reference_checks(block[0],external).items()})
    for i,m in enumerate(re.finditer(r'[Nn]hiệm vụ\s+(\d+)\s+của\s+('+'|'.join(REFERENCE_FUNCTIONS)+')',text),1):
        if any(start<=m.start()<end for start,end in sample):continue
        allowed={u['number'] for u in data['units'] if u['function'] in REFERENCE_FUNCTIONS[m[2]]}
        checks[f'contextual reference {i}: {m[0]}']=int(m[1]) in allowed
    return checks


def group(unit):
    return 'Gợi mở' if unit['function'] == 'function.guided_thinking' else 'Nhiệm vụ'


def anchor_position(text, ident):
    match = re.search(r'\{#'+re.escape(ident)+r'(?=[\s}])|\bid=["\']'+re.escape(ident)+r'["\']', text)
    if match is None:
        raise ValueError('Numbering owner missing: '+ident)
    return match.start()


def source_checks(text, data):
    if data.get('numbering_scope') != MODE:
        return {'package-wide visible type numbering required': False}
    checks = {}; groups = defaultdict(list)
    for unit in sorted(data['units'], key=lambda u: anchor_position(text, u['question'])):
        groups[group(unit)].append(unit)
    for name, units in groups.items():
        checks[name+' follows source order without reset'] = [u.get('number') for u in units] == list(range(1, len(units)+1))
        for u in units:
            prefix = name+f' {u["number"]:02d}'
            checks[u['id']+' visible title agrees with package number'] = bool(re.match(r'^(?:\d+(?:\.\d+)*\.\s*)?'+re.escape(prefix)+r'(?:\s|$)', u['title']))
            if u.get('answer'):
                checks[u['id']+' answer reuses question number'] = prefix in u.get('answer_title', u['title'])
    positions = sorted(data.get('checkpoint_numbers', {}), key=lambda a: anchor_position(text, a))
    checks['all checkpoints numbered once'] = set(positions) == set(data['checkpoints'])
    checks['checkpoints follow package source order'] = [data['checkpoint_numbers'][a] for a in positions] == list(range(1,len(positions)+1))
    for a in positions:
        line = text[:anchor_position(text,a)].splitlines()[-1]
        checks[a+' source checkpoint title numbered'] = bool(re.search(r'Điểm dừng '+f'{data["checkpoint_numbers"][a]:02d}'+r'(?:\s|$)', line))
    targets={u[k]:(group(u),u['number']) for u in data['units'] for k in ['question','answer'] if u.get(k)}
    targets.update({a:('Điểm dừng',n) for a,n in data['checkpoint_numbers'].items()})
    for i,m in enumerate(re.finditer(r'\[([^\]\n]+)\]\(#([^\s)]+)\)',text),1):
        if m[2] not in targets:continue
        name,number=targets[m[2]]
        match=re.search(r'(?:Nhiệm vụ|nhiệm vụ|Gợi mở|Điểm dừng) (\d+)',m[1])
        if match:checks[f'reference {i}/{m[2]} follows stable target']=int(match[1])==number
    checks.update(reference_checks(text,data))
    return checks


def retired_self_check_absent(reader, data):
    """The approved routing column is not the retired numbered activity name."""
    import copy
    from zo_course_remediation import CONTRACT, HEADERS
    visible=copy.deepcopy(reader)
    binding=data.get('remediation',{})
    frames=visible.find_all(id=binding.get('table',''))
    if binding.get('contract')==CONTRACT and len(frames)==1:
        frame=frames[0]
        heads=frame.select('thead th')
        if frame.get('data-zo-remediation')==CONTRACT and [h.get_text(' ',strip=True) for h in heads]==HEADERS:
            heads[-1].decompose()
    return 'Tự kiểm tra' not in visible.get_text(' ',strip=True)


def html_checks(doc, data):
    reader=doc.select_one('.reader-content'); checks={}; groups=defaultdict(list)
    for u in data['units']:
        node=reader.find(id=u['question'])
        if node is not None: groups[group(u)].append((node,u))
    order={id(n):i for i,n in enumerate(reader.find_all(True))}
    for name, pairs in groups.items():
        pairs.sort(key=lambda p:order[id(p[0])])
        checks[name+' HTML order and package numbers']=[u['number'] for _,u in pairs]==list(range(1,len(pairs)+1))
    for a,n in data['checkpoint_numbers'].items():
        node=reader.find(id=a); title=node.find(['h2','h3','h4','h5','h6']) if node else None
        checks[a+' HTML checkpoint number']=bool(title and re.search(r'Điểm dừng '+f'{n:02d}'+r'(?:\s|$)',title.get_text(' ',strip=True)))
    checks['retired self-check name absent outside approved routing column']=retired_self_check_absent(reader,data)
    examples=data.get('editorial_examples') or [u for u in data.get('knowledge_units',[]) if u['type']=='type.example'] or data.get('examples',[])
    for number,example in enumerate(examples,1):
        if not isinstance(example,dict):continue
        node=reader.find(id=example['anchor'])
        match=re.search(r'Ví dụ\s+(\d+)',node.get_text(' ',strip=True)) if node else None
        checks[example['anchor']+' example package number']=bool(match and int(match[1])==number)
    targets={u[k]:u['number'] for u in data['units'] for k in ['question','answer'] if u.get(k)}
    targets.update(data['checkpoint_numbers'])
    for i,link in enumerate(reader.select('a[href^="#"]'),1):
        target=link['href'][1:]
        match=re.search(r'(?:[Nn]hiệm vụ|Gợi mở|Điểm dừng) (\d+)',link.get_text(' ',strip=True))
        if target in targets and match:checks[f'HTML reference {i}/{target} follows stable target']=int(match[1])==targets[target]
    accessible='\n'.join(str(n.get(a,'')) for n in reader.find_all(True) for a in ['aria-label','title'])
    checks.update({'accessible '+k:v for k,v in reference_checks(accessible,data).items()})
    return checks


def restore_g01_for_comparison(source, plan, qmd):
    """Reuse the bounded block inverse; the accepted receipt stays immutable."""
    from zo_course_editorial import restore_g01_for_comparison as restore, RULE
    import copy
    change=plan.get('numbering_transition')
    if not change:return source
    if change.get('id')!='NUMBERING-20261018':raise ValueError('Unknown numbering transition')
    # source_qmd_sha256 already binds the complete current QMD.  Older
    # transitions also copied that same QMD into `sources`; retaining its
    # historical digest there would reject every later, separately reviewed
    # bounded transition before its own inverse can run.  Keep independent
    # includes protected, and let the complete current-source binding guard
    # the QMD exactly once.
    qmd_path=Path(qmd).resolve()
    sources={path:digest for path,digest in change.get('sources',{}).items()
             if (Path(__file__).resolve().parents[1]/path).resolve()!=qmd_path}
    proxy=copy.deepcopy(plan);proxy['editorial_transition']=dict(change,id=RULE,sources=sources)
    return restore(source,proxy,qmd)
