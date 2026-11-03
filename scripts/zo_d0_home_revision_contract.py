"""Explicit source-only review for independent D0 and Home revisions."""
from pathlib import Path
import json,hashlib

def review_for(path,root):
    root=Path(root).resolve();path=Path(path).resolve()
    allowed={root/'content/thpt/on_thi_toan_thpt/hoc_lieu/d0/index.qmd':'d0',root/'content/thpt/on_thi_toan_thpt/tot_nghiep_thpt/2027/index.qmd':'home'}
    if path not in allowed:return None
    current=path.parent/'_quy_trinh/ho_so/integration_r01_r20_editorial_review.json'
    if allowed[path]=='home' and current.is_file():
        review=json.loads(current.read_text(encoding='utf-8'))
        if review.get('revision')!='INTEGRATION-R01-R20-20261103' or review.get('package')!='home' or review.get('owner_HTML_acceptance') is not False:
            raise ValueError('Home integration review is not the declared source review')
        return review
    p=path.parent/'_quy_trinh/ho_so/course_format_20261103_review.json'
    if not p.is_file():p=path.parent/'_quy_trinh/ho_so/r01_editorial_review.json'
    if not p.is_file():return None
    review=json.loads(p.read_text(encoding='utf-8'))
    if review.get('revision')!='R01-DOT08' or review.get('package')!=allowed[path] or review.get('owner_HTML_acceptance') is not False:
        raise ValueError('D0/Home R01 source review mismatch; not owner acceptance')
    return review

def restore_d0_source(text,root):
    text=restore_format_source(text,root)
    p=Path(root)/'content/thpt/on_thi_toan_thpt/hoc_lieu/d0/_quy_trinh/revision_r01_delta.json'
    if not p.is_file():return text
    d=json.loads(p.read_text(encoding='utf-8'))
    sha=lambda value:hashlib.sha256(value.encode('utf-8')).hexdigest()
    if d.get('revision')!='R01-DOT08' or d.get('status')!='pending_owner_review' or d.get('owner_acceptance') is not False:raise ValueError('Invalid D0 R01 review state')
    if sha(text)!=d['after_sha256']:raise ValueError('D0 current source differs from bounded R01 delta')
    for key in ['before','after']:
        block=d[key]
        if not block.startswith('::: d0-live-materials\n') or not block.endswith('\n:::') or block.count(':::')!=2:raise ValueError('D0 delta escapes live materials')
    if text.count(d['after'])!=1:raise ValueError('D0 live-materials delta missing or repeated')
    restored=text.replace(d['after'],d['before'],1)
    if sha(restored)!=d['before_sha256']:raise ValueError('D0 historical source not restored exactly')
    return restored


def d0_runtime_source(name,default,root):
    root=Path(root)
    p=root/'content/thpt/on_thi_toan_thpt/hoc_lieu/d0/_quy_trinh/r01_preserved_runtime.json'
    if not p.is_file():return default
    config=json.loads(p.read_text(encoding='utf-8'))
    if config.get('revision')!='R01-DOT08':raise ValueError('Unexpected D0 runtime preservation revision')
    if name not in config['assets']:return default
    record=config['assets'][name];source=root/record['source']
    allowed=root/'content/thpt/on_thi_toan_thpt/hoc_lieu/d0/giao_dien/r01_preserved_runtime'/name
    if source.resolve()!=allowed.resolve() or name not in {'web-shell.css','site-ui.js'}:raise ValueError('D0 UI preservation escapes exact two-file scope')
    if hashlib.sha256(source.read_bytes()).hexdigest()!=record['sha256']:raise ValueError('Preserved D0 UI bytes changed')
    return source


def format_delta(root):
    p=Path(root)/'content/thpt/on_thi_toan_thpt/hoc_lieu/d0/_quy_trinh/course_format_20261103_delta.json'
    if not p.is_file():return None
    d=json.loads(p.read_text(encoding='utf-8'))
    if d.get('id')!='R2-FORMAT-D0-20261103':raise ValueError('Unknown D0 format delta')
    return d

def restore_format_source(text,root):
    d=format_delta(root)
    if d is None:return text
    sha=lambda s:hashlib.sha256(s.encode('utf-8')).hexdigest()
    if sha(text)!=d['source_after_sha256']:raise ValueError('D0 format source differs from explicit delta')
    for item in d['source_math_changes']:
        if item['after'] not in text:raise ValueError('Missing D0 format fraction')
        text=text.replace(item['after'],item['before'],1)
    if sha(text)!=d['source_before_sha256']:raise ValueError('D0 inverse format changed other source bytes')
    return text

def restore_format_projection(root,repo):
    # Comparison-only copy. The displayed DOM keeps the new fraction notation.
    d=format_delta(repo)
    if d is None:return root
    from bs4 import BeautifulSoup
    copy=BeautifulSoup(str(root),'html.parser')
    nodes=copy.select('annotation[encoding="application/x-tex"]')
    sha=lambda values:hashlib.sha256(json.dumps(values,ensure_ascii=False).encode('utf-8')).hexdigest()
    if sha([n.get_text() for n in nodes])!=d['html_after_math_sha256']:raise AssertionError('D0 math differs outside declared format')
    for item in d['html_math_changes']:
        node=nodes[item['index']]
        if node.get_text()!=item['after']:raise AssertionError('D0 format index mismatch')
        node.string=item['before']
    if sha([n.get_text() for n in nodes])!=d['html_before_math_sha256']:raise AssertionError('D0 historical math sequence not restored')
    return copy.select_one('.d0-package')
