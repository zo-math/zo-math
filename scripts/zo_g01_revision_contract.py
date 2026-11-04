"""Select the new G01 review only for its explicit source-owned R01 adapter."""
from pathlib import Path
import json
def review_for(path, root):
    path=Path(path);root=Path(root)
    if path.parent.name!='r1_g01':return None
    config=path.parent/'giao_dien/html.json'
    if not config.is_file():return None
    settings=json.loads(config.read_text(encoding='utf-8'))
    if settings.get('adapter')!='g01-revision-source-v1':return None
    if settings.get('package')!='r1_g01':raise ValueError('Revision package mismatch')
    review_path=path.parent/'_quy_trinh/ho_so/videos_20261105_review.json'
    if not review_path.is_file():review_path=path.parent/'_quy_trinh/ho_so/videos_20261104_review.json'
    if not review_path.is_file():review_path=path.parent/'_quy_trinh/ho_so/independent_figures_20261103_review.json'
    if not review_path.is_file():review_path=path.parent/'_quy_trinh/ho_so/course_format_20261103_review.json'
    if not review_path.is_file():review_path=path.parent/'_quy_trinh/ho_so/lesson_titles_20261103_review.json'
    if not review_path.is_file():review_path=path.parent/'_quy_trinh/ho_so/r01_editorial_review.json'
    review=json.loads(review_path.read_text(encoding='utf-8'))
    if review.get('revision')!='R01-DOT01' or review.get('package')!='r1_g01':raise ValueError('Revision review mismatch')
    if review.get('owner_HTML_acceptance') is not False:raise ValueError('R01 source review is not owner acceptance')
    return review
