"""One live PDF-state label shared by the two course HTML adapters."""
from pathlib import Path
import yaml
from zo_pdf_contract import validate_canonical_pdf_provenance

def apply(doc,root,package):
    for generated_note in doc.select('.prototype-note'):generated_note.decompose()
    package=Path(package);source=root/package/'index.qmd'
    config=yaml.safe_load((source.parent/'_quy_trinh/cau_hinh_san_xuat_qmd.yml').read_text(encoding='utf-8'))
    by_output={v['output']:k for k,v in config['extensions']['pdf_variants'].items()}
    cards=doc.select('#tai-tai-lieu .zo-pdf-card')
    names=[Path(card.select_one('a[download]')['href']).name for card in cards]
    if len(names)!=len(by_output) or set(names)!=set(by_output):
        raise ValueError('PDF cards must match every registered variant exactly once.')
    current=[]
    for card in cards:
        link=card.select_one('a[download]');name=Path(link['href']).name
        variant=by_output[name]
        fresh=not validate_canonical_pdf_provenance(root,source,variant=variant)
        card['data-pdf-current']=str(fresh).lower()
        label=card.select_one('.zo-pdf-version-note')
        label.string='PDF đã cập nhật.' if fresh else 'PDF đang chờ cập nhật.'
        current.append(fresh)
    note=doc.select_one('#tai-tai-lieu .zo-pdf-current-note')
    if note is None:
        note=doc.new_tag('p',attrs={'class':'zo-pdf-current-note'})
        heading=doc.select_one('#tai-tai-lieu h2');heading.insert_after(note)
    note.string='Các bản PDF đã cập nhật từ cùng nguồn học liệu.' if all(current) else 'Bản có nhãn “đang chờ cập nhật” chưa dùng để xuất bản. Số trang được đọc từ từng tệp PDF.'
    old='Số trang được đọc từ các tệp PDF đang có; các bản PDF này chưa được đồng bộ với HTML mới.'
    for node in doc.select_one('#tai-tai-lieu').find_all(string=True):
        if old in str(node):
            node.replace_with(str(node).replace(old,'Số trang được đọc trực tiếp từ từng tệp PDF.'))
    return current
