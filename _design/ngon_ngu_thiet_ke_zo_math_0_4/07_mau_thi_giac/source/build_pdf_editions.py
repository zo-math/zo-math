#!/usr/bin/env python3
"""Build new 0.4 covers/end pages around unchanged supplied R1-G01 PDF bodies.
Dependencies: Python 3, reportlab, PyMuPDF, Pillow. Run from any directory.
The body page numbering remains the source edition's numbering, explicitly stated
on new covers and end pages. No learning-content page is removed or re-typeset.
"""
from __future__ import annotations
from pathlib import Path
from io import BytesIO
import hashlib,json,shutil
import fitz
from PIL import Image,ImageOps,ImageDraw,ImageFont
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.colors import HexColor
from reportlab.lib.utils import ImageReader
from reportlab.graphics.barcode import qr
from reportlab.graphics.shapes import Drawing
from reportlab.graphics import renderPDF

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'pdf/r1_editions';OUT.mkdir(parents=True,exist_ok=True)
QA=ROOT/'qa/pdf_editions';QA.mkdir(parents=True,exist_ok=True)
AS=ROOT/'assets'
QR=AS/'qr_bao_tro_zo_math_vietcombank.jpg'
if not QR.exists():
    donor=ROOT.parent/'evidence/r1_g01/assets/images/qr_bao_tro_zo_math_vietcombank.jpg'
    shutil.copy2(donor,QR)
for name,file in [('ZO','BeVietnamPro_Regular.ttf'),('ZOB','BeVietnamPro_SemiBold.ttf')]:
    pdfmetrics.registerFont(TTFont(name,str(AS/file)))
MM=72/25.4;W,H=210*MM,297*MM
INK='#3E3A35';RED='#EF5350';YELLOW='#FFCA28';BG='#DFD7CA';MUTED='#766F66';DARKRED='#BF4240'
CANON='https://zomath.vn/content/thpt/on_thi_toan_thpt/hoc_lieu/r1_g01/index.html'
SUPPORT='https://zomath.vn/content/support/donate.html'
SPECS=[
 dict(file='index.pdf',label='Bản đầy đủ',note='Bài học, bài tập, lời giải và hướng dẫn chấm.',replace_end=True,next='Chọn phần cần học. Tự làm trước, rồi dùng lời giải để đối chiếu điều kiện và lập luận.'),
 dict(file='index_hoc_sinh.pdf',label='Bản học và bài tập',note='Dành cho tự học và làm bài. Không kèm lời giải.',replace_end=True,next='Giữ lại bài làm và câu hỏi của bạn. Khi đã tự giải, mở bản đầy đủ để đối chiếu.'),
 dict(file='index_bai_hoc.pdf',label='Bài học',note='Kiến thức nền, ví dụ và câu hỏi tự kiểm tra.',replace_end=False,next='Tự nói lại năm điều ở phần khép lại bài học, rồi chuyển sang luyện tập khi đã giải thích được.'),
 dict(file='index_luyen_tap.pdf',label='Luyện tập',note='Tám bài luyện tập. Tự làm trước khi xem lời giải.',replace_end=True,next='Đối chiếu từng bài sau khi tự làm. Ghi lỗi còn lặp trước khi chuyển sang phần kiểm tra.'),
 dict(file='index_kiem_tra.pdf',label='Kiểm tra',note='Năm bài tự kiểm tra. Thời gian đề xuất: 45 phút.',replace_end=False,next='Giữ bài làm ban đầu. Mở hướng dẫn chấm, xác định lỗi rồi chọn nhiệm vụ sửa lỗi tương ứng.'),
 dict(file='index_sua_loi.pdf',label='Sửa lỗi',note='Nhận diện lỗi, sửa lập luận và kiểm tra lại.',replace_end=False,next='Kết thúc việc sửa lỗi bằng một câu mới tự làm. Ghi kết quả vào nhật kí và lên lịch ôn lại.'),
 dict(file='index_on_lai.pdf',label='Ôn lại',note='Tự nhớ lại, làm nhiệm vụ mới và ghi nhận tiến bộ.',replace_end=True,next='Ghi ngày ôn, mức hỗ trợ và kết quả. Dùng bằng chứng từ bài làm để quyết định buổi học tiếp theo.'),
 dict(file='index_loi_giai.pdf',label='Lời giải và hướng dẫn chấm',note='Đối chiếu điều kiện, lập luận và cách cho điểm.',replace_end=False,next='Trở lại bài đã tự làm. Ghi rõ điều cần sửa, rồi làm một câu mới để kiểm tra cách hiểu của mình.'),
]

def sha(data):return hashlib.sha256(data).hexdigest()
def text(c,s,x,y,size=11,font='ZO',color=INK):
    c.setFont(font,size);c.setFillColor(HexColor(color));c.drawString(x*MM,H-y*MM,s)
def wrap(s,size,maxw,font='ZO'):
    lines=[];line=''
    for word in s.split():
        proposed=(line+' '+word).strip()
        if pdfmetrics.stringWidth(proposed,font,size)>maxw*MM and line:
            lines.append(line);line=word
        else:line=proposed
    if line:lines.append(line)
    return lines

def paragraph(c,s,x,y,w,size=11,leading=5.5,font='ZO',color=INK):
    lines=wrap(s,size,w,font)
    for i,line in enumerate(lines):text(c,line,x,y+i*leading,size,font,color)
    return y+len(lines)*leading

def rect(c,x,y,w,h,fill,r=0):
    c.setFillColor(HexColor(fill));c.setStrokeColor(HexColor(fill))
    if r:c.roundRect(x*MM,H-(y+h)*MM,w*MM,h*MM,r*MM,fill=1,stroke=0)
    else:c.rect(x*MM,H-(y+h)*MM,w*MM,h*MM,fill=1,stroke=0)
def img(c,path,x,y,w):
    im=Image.open(path);h=w*im.height/im.width
    c.drawImage(ImageReader(im),x*MM,H-(y+h)*MM,w*MM,h*MM,mask='auto')
    return h

def link(c,label,url,x,y,w,size=10,color=DARKRED):
    text(c,label,x,y,size,'ZOB',color)
    c.linkURL(url,(x*MM,H-(y+1)*MM,(x+w)*MM,H-(y-4)*MM),relative=0,thickness=0)
def base(c):
    rect(c,0,0,210,297,BG);rect(c,14,14,182,269,'#FFFFFF',4)

def make_cover(spec,n):
    buf=BytesIO();c=canvas.Canvas(buf,pagesize=(W,H));base(c)
    text(c,'ZO MATH / ÔN THI TOÁN THPT 2027',30,29,8.8,'ZOB',MUTED)
    img(c,ROOT/'logos/horizontal_color.png',30,39,49)
    text(c,'Đơn điệu',30,88,38,'ZOB')
    text(c,'và cực trị',30,105,38,'ZOB')
    text(c,spec['label'],30,123,15,'ZOB',DARKRED)
    paragraph(c,spec['note'],30,134,149,10.5,5.4)
    # The diagram is inserted as a vector PDF after the ReportLab page is built.
    text(c,'Đọc dấu. Hiểu chiều biến thiên. Xét đúng điều kiện.',30,220,8.6,'ZO',MUTED)
    text(c,'R1-G01',30,237,10.5,'ZOB')
    paragraph(c,'Mở học liệu trực tuyến để đi đúng phần đang học và lưu lại tiến trình của bạn.',30,246,113,9.7,4.9)
    text(c,'Nội dung v1.3 · Bìa và trang kết 0.4',30,263,8.5,'ZOB',MUTED)
    text(c,'Ruột giữ số trang bản nguồn; trang kết mới không đánh số.',30,270,7.0,'ZO',MUTED)
    text(c,'Bản nguồn: '+str(n)+' trang · Bản thảo 06/10/2026',30,276,7.0,'ZO',MUTED)
    q=qr.QrCodeWidget(CANON);bounds=q.getBounds();size=28*MM
    d=Drawing(size,size,transform=[size/(bounds[2]-bounds[0]),0,0,size/(bounds[3]-bounds[1]),0,0]);d.add(q)
    renderPDF.draw(d,c,151*MM,H-259*MM)
    c.linkURL(CANON,(151*MM,H-259*MM,179*MM,H-231*MM),relative=0,thickness=0)
    link(c,'Mở R1-G01',CANON,151,264,30,7.8)
    c.save();doc=fitz.open(stream=buf.getvalue(),filetype='pdf')
    figure=fitz.open(ROOT/'graphics/cubic.pdf')
    doc[0].show_pdf_page(fitz.Rect(30*MM,145*MM,180*MM,213*MM),figure,0,keep_proportion=True)
    return doc

def make_end(spec):
    buf=BytesIO();c=canvas.Canvas(buf,pagesize=(W,H));base(c)
    img(c,ROOT/'logos/horizontal_color.png',30,30,45)
    text(c,'SAU KHI KHÉP LẠI TÀI LIỆU',30,61,8.6,'ZOB',MUTED)
    text(c,'Một bước tiếp theo.',30,76,24,'ZOB')
    paragraph(c,spec['next'],30,87,150,10.2,5.3)
    rect(c,25,111,160,130,INK,3)
    text(c,'Ủng hộ ZO Math',35,127,21,'ZOB',YELLOW)
    paragraph(c,'ZO Math hiện chưa có tài trợ. Sự ủng hộ của bạn giúp duy trì việc biên soạn học liệu và phát triển các công cụ học Toán.',35,139,140,10.2,5.3,color='#FFFFFF')
    rect(c,32,157,50,50,'#FFFFFF',1)
    img(c,QR,36,161,42)
    text(c,'NGÂN HÀNG',85,164,7.4,'ZO','#DFD7CA')
    text(c,'Vietcombank',85,171,11,'ZOB','#FFFFFF')
    text(c,'SỐ TÀI KHOẢN',85,181,7.4,'ZO','#DFD7CA')
    text(c,'0601000137768',85,188,12,'ZOB',YELLOW)
    text(c,'CHỦ TÀI KHOẢN',85,198,7.4,'ZO','#DFD7CA')
    text(c,'Nguyễn Tấn Nhựt',85,205,11,'ZOB','#FFFFFF')
    text(c,'NỘI DUNG CHUYỂN KHOẢN',35,215,7.4,'ZO','#DFD7CA')
    text(c,'BAO TRO ZO MATH',35,222,11,'ZOB','#FFFFFF')
    rect(c,35,228,140,8.5,YELLOW,1.3)
    link(c,'Xem thông tin ủng hộ tại zomath.vn',SUPPORT,40,234,128,9.2,INK)
    text(c,'Việc ủng hộ là tự nguyện. Cảm ơn bạn đã đồng hành.',30,251,8.5,'ZO',MUTED)
    link(c,'Trở lại gói học liệu R1-G01',CANON,30,263,148,10)
    text(c,'Bìa và trang kết 0.4 · Ruột giữ bản nguồn v1.3',30,273,7.6,'ZO',MUTED)
    text(c,'Trang kết này nằm ngoài hệ đánh số trang của bản nguồn.',30,279,7,'ZO',MUTED)
    c.save();return fitz.open(stream=buf.getvalue(),filetype='pdf')

def body_proof(doc,start,end):
    txt=hashlib.sha256();pixels=hashlib.sha256();individual=[]
    for i in range(start,end):
        p=doc[i];raw=p.get_text().encode();pix=p.get_pixmap(matrix=fitz.Matrix(.4,.4),alpha=False)
        txt.update(raw);pixels.update(pix.samples)
        individual.append({'page':i+1,'text_sha256':sha(raw),'raster_sha256':sha(pix.samples)})
    return {'text_sha256':txt.hexdigest(),'raster_sha256':pixels.hexdigest(),'pages':individual}

entries=[];thumbs=[]
for spec in SPECS:
    src=ROOT/'reference/r1_pdf'/spec['file'];original=fitz.open(src);n=len(original)
    stop=n-1 if spec['replace_end'] else n
    cover=make_cover(spec,n);end=make_end(spec)
    doc=fitz.open();doc.insert_pdf(cover);doc.insert_pdf(original,from_page=1,to_page=stop-1);doc.insert_pdf(end)
    source_toc=original.get_toc()
    toc=[entry[:] for entry in source_toc]
    if not any('Bảo trợ' in entry[1] or 'Ủng hộ' in entry[1] for entry in toc):
        toc.append([1,'Ủng hộ ZO Math',len(doc)])
    doc.set_toc(toc)
    doc.set_metadata({'title':'ZO Math · '+spec['label']+' · Đơn điệu và cực trị','author':'ZO Math','subject':'Bìa và trang kết 0.4; ruột nguồn R1-G01 v1.3','keywords':'ZO Math, R1-G01, Đơn điệu, Cực trị, 0.4','creator':'ZO Math PDF edition builder 0.4'})
    target=OUT/spec['file'];doc.save(target,garbage=4,deflate=True)
    output=fitz.open(target)
    proof_src=body_proof(original,1,stop);proof_out=body_proof(output,1,stop)
    assert proof_src['text_sha256']==proof_out['text_sha256'],spec['file']+' body text mismatch'
    assert proof_src['raster_sha256']==proof_out['raster_sha256'],spec['file']+' body render mismatch'
    expected=n if spec['replace_end'] else n+1
    assert len(output)==expected
    for i in [0,len(output)-1]:
        p=output[i];ss=p.get_text()
        assert '\ufffd' not in ss
        if i:assert all(x in ss for x in ['Vietcombank','0601000137768','Nguyễn Tấn Nhựt','BAO TRO ZO MATH'])
        label='cover' if i==0 else 'end';png=QA/(src.stem+'_'+label+'.png');p.get_pixmap(matrix=fitz.Matrix(1.2,1.2),alpha=False).save(png)
        thumbs.append((spec['label']+' / '+('Bìa' if i==0 else 'Kết'),png))
    assert output.get_toc()[:len(source_toc)]==source_toc
    source_uri=sum(l.get('kind')==2 for i in range(1,stop) for l in original[i].get_links())
    output_uri=sum(l.get('kind')==2 for i in range(1,stop) for l in output[i].get_links())
    assert source_uri==output_uri
    entries.append({'file':str(target.relative_to(ROOT)),'source_file':spec['file'],'display_name':spec['label'],'page_count':len(output),'body_status':'Giữ nguyên trang ruột nguồn v1.3; văn bản, hình và liên kết URI đã đối chiếu.','source_bookmarks_preserved':len(source_toc),'label':spec['label'],'original':str(src.relative_to(ROOT)),'source_sha256':sha(src.read_bytes()),'pdf_sha256':sha(target.read_bytes()),'original_pages':n,'pages':len(output),'body_source_pages_inclusive':[2,stop],'end_action':'replace' if spec['replace_end'] else 'append','body_unchanged_text':True,'body_unchanged_render':True,'body_text_sha256':proof_src['text_sha256'],'body_raster_sha256':proof_src['raster_sha256'],'body_uri_links_preserved':source_uri,'numbering':'Ruột giữ hệ số trang nguồn; trang kết mới không đánh số.','source_page_proofs':proof_src['pages']})

font=ImageFont.truetype(str(AS/'BeVietnamPro_SemiBold.ttf'),14)
contact=Image.new('RGB',(1280,1920),'#DFD7CA');draw=ImageDraw.Draw(contact)
for idx,(label,path) in enumerate(thumbs):
    col=idx%4;row=idx//4;im=Image.open(path);im.thumbnail((295,424));x=col*320+(320-im.width)//2;y=row*480+37
    contact.paste(im,(x,y));draw.text((col*320+13,row*480+12),label,font=font,fill=INK)
contact.save(QA/'contact_all.png')
(ROOT/'design/pdf_editions.json').write_text(json.dumps({'edition':'0.4','scope':'Bìa và trang kết mới; giữ nguyên toàn bộ trang ruột nguồn R1-G01 v1.3.','source_qr_sha256':sha(QR.read_bytes()),'canonical':CANON,'support_url':SUPPORT,'qa':'All body text and raster hashes match the supplied source page range; URI link counts preserved. Covers/end pages statically rendered for review.','editions':entries},ensure_ascii=False,indent=2))
print(json.dumps({'created':len(entries),'files':[e['file'] for e in entries],'contact':str(QA/'contact_all.png')},ensure_ascii=False))
