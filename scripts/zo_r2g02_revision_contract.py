"""Explicitly select the independent R2-G02 source review, preserving old receipts."""
from pathlib import Path
import json

def settings_for(path):
    path=Path(path)
    config=path.parent/'_quy_trinh/revision_r01.json'
    if path.parent.name!='r2_g02' or not config.is_file():return None
    data=json.loads(config.read_text(encoding='utf-8'))
    if data.get('adapter')!='r2-g02-source-r01':return None
    if data.get('revision')!='R01-DOT07' or data.get('package')!='r2_g02' or data.get('runtime')!='r2_g02_revision_r01':
        raise ValueError('R2-G02 revision configuration mismatch')
    if data.get('pdf_build') is not False:raise ValueError('R2-G02 R01 is HTML-only')
    return data

def review_for(path,root):
    if settings_for(path) is None:return None
    review=json.loads((Path(path).parent/'_quy_trinh/ho_so/r01_editorial_review.json').read_text(encoding='utf-8'))
    if review.get('revision')!='R01-DOT07' or review.get('package')!='r2_g02':raise ValueError('R2-G02 source review mismatch')
    if review.get('owner_HTML_acceptance') is not False:raise ValueError('Source review is not owner acceptance')
    return review
