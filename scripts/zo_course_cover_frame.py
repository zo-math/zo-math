"""Apply the existing authored cover presets; no new learner controls."""
from pathlib import Path
import json,os,shutil
ROOT=Path(__file__).resolve().parents[1]
KIT=ROOT/'_design/web_2027_mau_dung_chung'
def apply(doc,spec,page,runtime):
 data=json.loads((KIT/'figure-profile-candidate/frame-tokens.json').read_text('utf-8'))
 if spec['shape'] not in data['sizes_px'] or spec['size'] not in data['sizes_px'][spec['shape']] or spec['background'] not in data['backgrounds']:raise ValueError('Unknown cover preset')
 width,height=data['sizes_px'][spec['shape']][spec['size']]
 frame=doc.select_one('.hero-art');frame['data-zo-cover-shape']=spec['shape'];frame['data-zo-cover-size']=spec['size'];frame['data-zo-cover-background']=spec['background']
 frame['style']=f'--cover-width:{width}px;--cover-height:{height}px'
 target=runtime/'course-cover-frame.css';shutil.copyfile(KIT/'course-cover-frame.css',target)
 doc.head.append(doc.new_tag('link',rel='stylesheet',href=os.path.relpath(target,page.parent).replace(chr(92),'/')))
