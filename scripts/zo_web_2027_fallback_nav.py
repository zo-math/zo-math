"""Full progressive-enhancement navigation for both learning packages."""
SECTIONS=[('bat-dau','Bắt đầu'),('bai-hoc','Bài học'),('phieu-luyen','Luyện tập'),
 ('tu-kiem-tra','Kiểm tra'),('on-lai','Ôn lại'),('on-nen','Ôn nền'),
 ('sua-loi','Sửa lỗi'),('nhat-ky','Nhật kí'),('loi-giai','Lời giải'),
 ('tai-tai-lieu','Tải PDF'),('nguon','Nguồn')]
def apply(doc):
    mount=doc.find(id='rail-content')
    for prior in list(mount.select('noscript')):prior.decompose()
    fallback=doc.new_tag('noscript');nav=doc.new_tag('nav',attrs={'aria-label':'Các phần của học liệu — không cần JavaScript'})
    for anchor,title in SECTIONS:
        if doc.find(id=anchor) is None:raise ValueError('Missing fallback navigation target '+anchor)
        p=doc.new_tag('p');a=doc.new_tag('a',href='#'+anchor);a.string=title;p.append(a);nav.append(p)
    fallback.append(nav);mount.append(fallback)
