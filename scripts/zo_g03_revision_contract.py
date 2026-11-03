"""Explicitly select the independent G03 source review, preserving old receipts."""
from pathlib import Path
import json

def settings_for(path):
    path=Path(path)
    config=path.parent/'_quy_trinh/revision_r01.json'
    if path.parent.name!='r1_g03' or not config.is_file():return None
    data=json.loads(config.read_text(encoding='utf-8'))
    if data.get('adapter')!='g03-source-r01':return None
    if data.get('revision')!='R01-DOT03' or data.get('package')!='r1_g03' or data.get('runtime')!='g03_revision_r01':
        raise ValueError('G03 revision configuration mismatch')
    if data.get('pdf_build') is not False:raise ValueError('G03 R01 is HTML-only')
    return data

def review_for(path,root):
    if settings_for(path) is None:return None
    review_path=Path(path).parent/'_quy_trinh/ho_so/course_format_20261103_review.json'
    if not review_path.is_file():review_path=Path(path).parent/'_quy_trinh/ho_so/lesson_titles_20261103_review.json'
    if not review_path.is_file():review_path=Path(path).parent/'_quy_trinh/ho_so/r01_editorial_review.json'
    review=json.loads(review_path.read_text(encoding='utf-8'))
    if review.get('revision')!='R01-DOT03' or review.get('package')!='r1_g03':raise ValueError('G03 source review mismatch')
    if review.get('owner_HTML_acceptance') is not False:raise ValueError('Source review is not owner acceptance')
    return review
