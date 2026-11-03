"""Explicitly select the independent G05 source review, preserving old receipts."""
from pathlib import Path
import json

def settings_for(path):
    path=Path(path)
    config=path.parent/'_quy_trinh/revision_r01.json'
    if path.parent.name!='r1_g05' or not config.is_file():return None
    data=json.loads(config.read_text(encoding='utf-8'))
    if data.get('adapter')!='g05-source-r01':return None
    if data.get('revision')!='R01-DOT05' or data.get('package')!='r1_g05' or data.get('runtime')!='g05_revision_r01':
        raise ValueError('G05 revision configuration mismatch')
    if data.get('pdf_build') is not False:raise ValueError('G05 R01 is HTML-only')
    return data

def review_for(path,root):
    if settings_for(path) is None:return None
    review_path=Path(path).parent/'_quy_trinh/ho_so/independent_figures_20261103_review.json'
    if not review_path.is_file():review_path=Path(path).parent/'_quy_trinh/ho_so/course_format_20261103_review.json'
    if not review_path.is_file():review_path=Path(path).parent/'_quy_trinh/ho_so/lesson_titles_20261103_review.json'
    if not review_path.is_file():review_path=Path(path).parent/'_quy_trinh/ho_so/r01_editorial_review.json'
    review=json.loads(review_path.read_text(encoding='utf-8'))
    if review.get('revision')!='R01-DOT05' or review.get('package')!='r1_g05':raise ValueError('G05 source review mismatch')
    if review.get('owner_HTML_acceptance') is not False:raise ValueError('Source review is not owner acceptance')
    return review

def extend_tables(data,root):
    config=settings_for(Path(root)/'content/thpt/on_thi_toan_thpt/hoc_lieu/r1_g05/index.qmd')
    if config is None:return data
    entries=data['pages']['r1_g05']
    for extra in config.get('table_bindings',[]):
        if not extra['selector'].startswith('#g05-table-r01-') or extra['kind']!='values':
            raise ValueError('G05 R01 table binding outside permitted scope')
        if any(e['selector']==extra['selector'] for e in entries):raise ValueError('Duplicate G05 R01 table')
        entries.append(extra)
    return data
