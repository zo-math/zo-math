"""Explicitly select the independent G04 source review, preserving old receipts."""
from pathlib import Path
import json

def settings_for(path):
    path=Path(path)
    config=path.parent/'_quy_trinh/revision_r01.json'
    if path.parent.name!='r1_g04' or not config.is_file():return None
    data=json.loads(config.read_text(encoding='utf-8'))
    if data.get('adapter')!='g04-source-r01':return None
    if data.get('revision')!='R01-DOT04' or data.get('package')!='r1_g04' or data.get('runtime')!='g04_revision_r01':
        raise ValueError('G04 revision configuration mismatch')
    if data.get('pdf_build') is not False:raise ValueError('G04 R01 is HTML-only')
    return data

def review_for(path,root):
    if settings_for(path) is None:return None
    review_path=Path(path).parent/'_quy_trinh/ho_so/video_editorial_review.json'
    if not review_path.is_file():review_path=Path(path).parent/'_quy_trinh/ho_so/lesson_titles_20261103_review.json'
    if not review_path.is_file():review_path=Path(path).parent/'_quy_trinh/ho_so/r01_editorial_review.json'
    review=json.loads(review_path.read_text(encoding='utf-8'))
    if review.get('revision')!='R01-DOT04' or review.get('package')!='r1_g04':raise ValueError('G04 source review mismatch')
    if review.get('owner_HTML_acceptance') is not False:raise ValueError('Source review is not owner acceptance')
    return review

def graph_inventory_matches(images,source,owned_names):
    """Allow only the exact source-declared occurrences of owned G04 images."""
    if settings_for(source) is None:return None
    import re
    from collections import Counter
    declared=Counter(Path(name).name for name in re.findall(r'!\[[^\]\n]*\]\(([^)]+\.svg)\)',Path(source).read_text(encoding='utf-8')))
    actual=Counter(Path(image['src']).name for image in images)
    return actual==declared and set(declared)==set(owned_names)
