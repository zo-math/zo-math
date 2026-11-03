"""Project explicitly declared review rounds into native, exclusive disclosures."""
from pathlib import Path
import os

ASSETS=Path(__file__).resolve().parent/'assets'

def project(root,document):
    from zo_web_2027_g02 import inv
    before=inv(root)
    originals=list(root.select("details"))
    rounds=root.select('#on-lai > section[data-zo-review-disclosure="closed"]')
    if not rounds:return False
    for section in rounds:
        heading=section.find(['h3','h4'],recursive=False)
        if heading is None:raise ValueError('Review round lacks its source heading')
        panel=document.new_tag('details',attrs={'name':'r01-review-rounds','class':'zo-learning-guidance r01-review-round'})
        summary=document.new_tag('summary')
        summary.append(heading.extract());panel.append(summary)
        for child in list(section.contents):panel.append(child.extract())
        section.append(panel)
    after=inv(root)
    assert all(before[k]==after[k] for k in before if k!="disclosures"), "Review disclosure changed content, formula, link or ID"
    assert all(node in root.descendants for node in originals), "Existing disclosure lost"
    return True

def install(document,page,runtime):
    if not document.select('details.r01-review-round'):return
    for filename,kind in [('revision-review-rounds.js','script'),('revision-review-rounds.css','style')]:
        dest=Path(runtime)/filename;dest.write_bytes((ASSETS/filename).read_bytes())
        url=os.path.relpath(dest,Path(page).parent).replace('\\','/')
        node=document.new_tag('script',src=url) if kind=='script' else document.new_tag('link',rel='stylesheet',href=url)
        (document.body if kind=='script' else document.head).append(node)
