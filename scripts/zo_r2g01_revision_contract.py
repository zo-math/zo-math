"""Explicitly select the independent R2-G01 source review, preserving old receipts."""
from pathlib import Path
import json

def settings_for(path):
    path=Path(path)
    config=path.parent/'_quy_trinh/revision_r01.json'
    if path.parent.name!='r2_g01' or not config.is_file():return None
    data=json.loads(config.read_text(encoding='utf-8'))
    if data.get('adapter')!='r2-g01-source-r01':return None
    if data.get('revision')!='R01-DOT06' or data.get('package')!='r2_g01' or data.get('runtime')!='r2_g01_revision_r01':
        raise ValueError('R2-G01 revision configuration mismatch')
    if data.get('pdf_build') is not False:raise ValueError('R2-G01 R01 is HTML-only')
    return data

def review_for(path,root):
    if settings_for(path) is None:return None
    review_path=Path(path).parent/'_quy_trinh/ho_so/independent_figures_20261103_review.json'
    if not review_path.is_file():review_path=Path(path).parent/'_quy_trinh/ho_so/course_format_20261103_review.json'
    if not review_path.is_file():review_path=Path(path).parent/'_quy_trinh/ho_so/r01_editorial_review.json'
    review=json.loads(review_path.read_text(encoding='utf-8'))
    if review.get('revision')!='R01-DOT06' or review.get('package')!='r2_g01':raise ValueError('R2-G01 source review mismatch')
    if review.get('owner_HTML_acceptance') is not False:raise ValueError('Source review is not owner acceptance')
    return review
