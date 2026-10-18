"""Purposeful instructions: required actions visible, optional help declared.

No renderer, no learning prose generator. Historical G01 text is used only
on a detached comparison tree to preserve its immutable accepted fingerprint.
"""
from pathlib import Path
import copy, hashlib, json, re

ROOT = Path(__file__).resolve().parents[1]
RULE = 'INSTRUCTIONS-20261018'
norm = lambda s: re.sub(r'\s+', ' ', s).strip()

def spec(path):
    from zo_course_labels import governed
    path = Path(path)
    if path.name != 'index.qmd' or not governed(path):
        return None
    data = json.loads((path.parent/'giao_dien/he_nhan.json').read_text(encoding='utf-8'))
    return data.get('instructions', {})

def uppercase_start(text):
    # Lists, Markdown emphasis, punctuation and anchor syntax are not letters.
    text = re.sub(r'\[\]\{[^}]*\}', '', text)
    first = next((c for c in text if c.isalpha()), '')
    return bool(first and first.isupper())

def source_checks(path, root=ROOT, text=None):
    path = Path(path); b = spec(path)
    if b is None:
        return {}
    text = path.read_text(encoding='utf-8') if text is None else text
    checks = {'explicit instruction policy': b.get('rule') == RULE}
    declared = b.get('required', []) + b.get('optional', []) + b.get('retired_aliases', [])
    checks['unique instruction declarations'] = len(declared) == len(set(declared))
    actual = re.findall(r'^:{3,} \{#([^ }]+)[^\n]*data-zo-instructions="required"[^\n]*\}', text, re.M)
    checks['visible instruction bindings complete'] = sorted(actual) == sorted(b.get('required', []))
    for ident in b.get('required', []):
        match = re.search(r'^(:{3,}) \{#'+re.escape(ident)+r'[^\n]*data-zo-instructions="required"[^\n]*\}\n(.*?)^\1[ \t]*$', text, re.M|re.S)
        checks[ident+' visible source body'] = bool(match and norm(match[2]) and not re.search(r'<details\b|zo-learning-guidance|Cách thực hiện', match[2]))
        checks[ident+' uppercase opening'] = bool(match and uppercase_start(match[2]))
    # Generic repeated boxes may return only with explicit optional ownership.
    native = list(re.finditer(r'<details\b(?P<attrs>[^>]*)>\s*<summary[^>]*>Cách thực hiện</summary>(?P<body>.*?)</details>', text, re.S))
    found = []
    for m in native:
        ident = re.search(r'\bid="([^"]+)"', m['attrs'])
        ident = ident[1] if ident else None; found.append(ident)
        checks['optional '+str(ident)+' closed and capitalized'] = bool(ident in b.get('optional', []) and 'data-zo-instructions="optional"' in m['attrs'] and not re.search(r'\bopen(?:\s|=|$)', m['attrs']) and uppercase_start(m['body']))
    checks['all optional instructions declared'] = sorted(x or '' for x in found) == sorted(b.get('optional', []))
    checks['no legacy mandatory guidance slot'] = not re.search(r'(?m)^Cách thực hiện\s*$', text)
    for ident in b.get('retired_aliases', []):
        checks[ident+' bookmark only'] = text.count('[]{#'+ident+'}') == 1
    return checks

def html_checks(doc, binding):
    b = binding.get('instructions', {}); root = doc.select_one('.reader-content')
    checks = {'instruction policy declared': b.get('rule') == RULE, 'reader exists': root is not None}
    if root is None:
        return checks
    actual = root.select('[data-zo-instructions="required"]')
    checks['all visible instructions bound'] = sorted(n.get('id','') for n in actual) == sorted(b.get('required', []))
    for ident in b.get('required', []):
        nodes = root.find_all(id=ident); n = nodes[0] if len(nodes)==1 else None
        checks[ident+' visible and capitalized'] = bool(n and n.name=='div' and n.get('data-zo-instructions')=='required' and not n.find_parent('details') and not n.find('details') and not n.has_attr('hidden') and uppercase_start(n.get_text(' ',strip=True)))
    found = []
    for node in root.select('details'):
        summary = node.find('summary', recursive=False)
        if summary and summary.get_text(' ',strip=True) == 'Cách thực hiện':
            ident = node.get('id'); found.append(ident)
            body = copy.deepcopy(node); body.summary.decompose()
            checks['optional '+str(ident)+' declared and closed'] = bool(ident in b.get('optional', []) and node.get('data-zo-instructions')=='optional' and not node.has_attr('open') and uppercase_start(body.get_text(' ',strip=True)))
    checks['optional ownership complete'] = sorted(x or '' for x in found) == sorted(b.get('optional', []))
    for ident in b.get('retired_aliases', []):
        nodes = root.find_all(id=ident)
        checks[ident+' no obsolete box'] = bool(len(nodes)==1 and nodes[0].name=='span' and not nodes[0].get_text(strip=True))
    return checks

def restore_g01_for_comparison(source, plan, qmd):
    """Inverse only the enumerated, source-bound instruction edits on a COPY.

    This never changes learner output or the historical accepted receipt.
    All words, maths, anchors and disclosure states outside these nodes remain
    subject to the original complete fingerprint comparison.
    """
    change = plan.get('instructions_transition')
    if not change:
        return source
    digest = hashlib.sha256(Path(qmd).read_bytes()).hexdigest()
    if change.get('id') != RULE or change.get('source_qmd_sha256') != digest:
        raise ValueError('G01 instruction transition does not match canonical source')
    result = copy.deepcopy(source); seen = set()
    from bs4 import BeautifulSoup
    for edit in change['edits']:
        ident = edit['id']; nodes = result.find_all(id=ident)
        if ident in seen or len(nodes)!=1:
            raise ValueError('Missing/duplicated G01 instruction anchor: '+ident)
        seen.add(ident); node=nodes[0]
        if norm(node.get_text(' ',strip=True)) != edit['after_text']:
            raise ValueError('Unexpected G01 instruction text: '+ident)
        if edit['mode']=='visible':
            if node.name!='div' or node.get('data-zo-instructions')!='required' or node.find_parent('details') or node.find('math') or node.find('details'):
                raise ValueError('G01 required instructions must stay visible: '+ident)
        elif edit['mode']=='remove':
            if node.name!='span' or node.contents:
                raise ValueError('Obsolete G01 guide must remain bookmark-only: '+ident)
        else:
            raise ValueError('Unknown G01 instruction transition mode')
        old=BeautifulSoup('<details></details>','html.parser').details
        old['id']=ident;old.string=edit['before_text'];node.replace_with(old)
    return result
