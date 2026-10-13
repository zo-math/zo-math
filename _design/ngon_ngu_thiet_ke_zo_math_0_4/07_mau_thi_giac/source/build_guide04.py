#!/usr/bin/env python3
"""Rebuild the illustrated ZO Math 0.4 guide (ReportLab + Pillow + PyMuPDF)."""
from pathlib import Path
from io import BytesIO
import json,hashlib,wave
import numpy as np
import fitz
from PIL import Image,ImageDraw,ImageFont
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.colors import HexColor
from reportlab.lib.utils import ImageReader
ROOT=Path(__file__).resolve().parents[1];AS=ROOT/'assets';OUT=ROOT/'pdf/ZO_Math_Quy_chuan_0_4.pdf';QA=ROOT/'qa/guide_0_4';QA.mkdir(parents=True,exist_ok=True)
P=json.loads((ROOT/'design/color_system.json').read_text());C=P['palette'];S=json.loads((ROOT/'design/research_scope.json').read_text())
E=json.loads((ROOT/'design/pdf_editions.json').read_text())['editions']
for n,f in [('ZO','BeVietnamPro_Regular.ttf'),('ZOB','BeVietnamPro_SemiBold.ttf')]:pdfmetrics.registerFont(TTFont(n,str(AS/f)))
M=72/25.4;W,H=210*M,297*M;INK=C['gray-8'];MUTE=C['gray-6'];BG=C['gray-3'];RED=C['red-5'];YEL=C['yellow-4']
buf=BytesIO();c=canvas.Canvas(buf,pagesize=(W,H));page=0;titles=[]
def tx(s,x,y,size=11,bold=False,color=INK):
 c.setFont('ZOB' if bold else 'ZO',size);c.setFillColor(HexColor(color));c.drawString(x*M,H-y*M,str(s))
def lines(s,w,size=10,font='ZO'):
 out=[];line=''
 for word in s.split():
  if pdfmetrics.stringWidth(word,font,size)>w*M:
   chunks=[];part=''
   for ch in word:
    if pdfmetrics.stringWidth(part+ch,font,size)>w*M:chunks.append(part);part=''
    part+=ch
   chunks.append(part);words=chunks
  else:words=[word]
  for word in words:
   z=(line+' '+word).strip()
   if pdfmetrics.stringWidth(z,font,size)>w*M and line:out.append(line);line=word
   else:line=z
 if line:out.append(line)
 return out

def para(s,x,y,w=156,size=10.4,leading=5.7,bold=False,color=INK):
 ls=lines(s,w,size,'ZOB' if bold else 'ZO')
 for i,t in enumerate(ls):tx(t,x,y+i*leading,size,bold,color)
 return y+len(ls)*leading

def box(x,y,w,h,color='#FFFFFF',r=3):
 c.setFillColor(HexColor(color));c.roundRect(x*M,H-(y+h)*M,w*M,h*M,r*M,fill=1,stroke=0)
def pic(path,x,y,w,h=None):
 im=Image.open(path);ih=w*im.height/im.width
 if h and ih>h:w=h*im.width/im.height;ih=h
 c.drawImage(ImageReader(im),x*M,H-(y+ih)*M,w*M,ih*M,mask='auto');return ih

def link(label,url,x,y,w=150):
 tx(label,x,y,9.5,True,RED);c.linkURL(url,(x*M,H-(y+2)*M,(x+w)*M,H-(y-4)*M),relative=0,thickness=0)
def new(title,kicker='NGÔN NGỮ HÌNH ẢNH VÀ ÂM THANH / 0.4',sub=''):
 global page
 if page:c.showPage()
 page+=1;titles.append(title);box(0,0,210,297,BG,0);box(12,12,186,273,'#FFFFFF',4)
 tx(kicker,25,28,8.2,True,MUTE);para(title,25,46,160,25,11,True)
 if sub:para(sub,25,61,160,10,5.5,color=MUTE)
 tx('ZO MATH / BẢN DÙNG THỬ 0.4',25,276,7.4,True,MUTE);tx(f'{page:02}',179,276,8,True,MUTE)
 c.bookmarkPage('p'+str(page));c.addOutlineEntry(title,'p'+str(page),0)
def rule(title,rule,why,y,x=25,w=160):
 tx(title,x,y,12.2,True);y=para(rule,x,y+8,w,10.3,5.7)
 return para('Vì sao. '+why,x,y+3,w,9.4,5.3,color=MUTE)+7

def tag(s,x,y):tx(s.upper(),x,y,8.5,False,MUTE)

new('Một ngôn ngữ chung.',sub='Hình ảnh rõ ràng. Nhịp điềm tĩnh. Âm thanh có chủ đích.')
pic(ROOT/'logos/horizontal_color.png',25,88,96)
para('Đỏ ZO. Vàng ZO. Xám ZO.',25,152,160,20,9,True)
para('Từ một trang học đến đồ thị, bảng, PDF, video và âm thanh: cùng cách dẫn mắt, giữ trọng tâm và cho người học đủ thời gian hiểu.',25,171,157,13,7.8)
box(25,211,160,39,C['yellow-1']);para('Bản 0.4 tiếp tục hướng đã được bạn đánh giá tốt ở 0.3, đồng thời sửa những điểm còn cạnh tranh nhau. Đây là hệ mẫu để dùng thử và duyệt; chưa phải Design System 1.0.',32,222,146,10.5,5.9)

new('Phạm vi của một hệ.',sub='Ngôn ngữ hình ảnh và âm thanh là phần biểu hiện ra ngoài của hệ thiết kế.')
para('Hệ thiết kế còn bao gồm vai trò nội dung, hành vi, nguồn tài sản, cách sản xuất và tiêu chí nghiệm thu. Có mẫu đẹp chưa đồng nghĩa mọi tầng đã thành chuẩn.',25,77,160,10.5,5.8)
for i,g in enumerate(S['groups']):
 col=i%2;row=i//2;x=25+82*col;y=105+25*row
 box(x,y,78,22,C['gray-2']);tx(g['id'],x+4,y+7,8,True,MUTE)
 name=g['name'].replace(' và trạng thái UI',' và trạng thái').replace('Phân phối, ủng hộ, tiếp cận và quản trị','Phân phối, tiếp cận, quản trị')
 para(name,x+4,y+14,70,8.7,4.4,True)
para('G01–G09 và G12: có căn cứ, đang thử bằng mẫu 0.4. G10–G11: chuyển động và âm thanh mới ở mức ứng viên; cần nghe, xem và hiệu chỉnh trước khi chốt.',25,264,160,8.3,4.6,color=MUTE)

new('Ba màu. Một cách gọi.',sub='Giữ nguyên 23 mã màu đã dùng; đổi token cho liên tục và dễ vận hành.')
y=84
for family,label in [('red','Đỏ ZO'),('yellow','Vàng ZO'),('gray','Xám ZO')]:
 tx(label,25,y,15,True);colors=[(k,v) for k,v in C.items() if k.startswith(family)]
 for i,(key,color) in enumerate(colors):
  x=25+i*160/len(colors);ww=160/len(colors)-1
  box(x,y+7,ww,23,color,1);tx(key,x,y+36,7.4,True);tx(color,x,y+43,6.3,False,MUTE)
 y+=57
para('Đỏ ZO = red-4 · Vàng ZO = yellow-4 · Xám ZO = gray-8',25,253,160,10,5.5,True)
para('Số tăng từ nhạt đến đậm trong từng thang. Đây là thứ tự token, không phải khoảng cách cảm nhận bằng nhau. Ánh xạ tên cũ được giữ trong color_system.json.',25,263,160,8.4,4.7,color=MUTE)

new('Nền thay đổi. Nội dung ổn định.',sub='Sáu mặt nền để dùng thử; mặc định gray-3. Nội dung đặt trên khối trắng.')
for i,key in enumerate(P['backgrounds']):
 x=25+(i%3)*55;y=82+(i//3)*62
 box(x,y,50,53,C[key]);box(x+5,y+8,40,33,'#FFFFFF',2)
 tx('ĐƠN ĐIỆU',x+9,y+18,6.6,False,MUTE);tx('Một ý chính.',x+9,y+28,8.4,True)
 tx(key,x+5,y+49,7.6,True)
rule('Chọn nền theo cảm giác; giữ vai trò màu.', 'Nền không đổi màu chữ, công thức hay ý nghĩa nhấn. Sáu lựa chọn được gọi đúng token; Sắc xám hoạt động độc lập.', 'Người đọc đổi không khí của trang mà vẫn nhận ra cấu trúc và mức ưu tiên.',220)

new('ZO đứng vững trên hai ô.',sub='Một họ logo: hai nền Xám ZO độc lập, Z đỏ, O vàng và không có viền O.')
pic(ROOT/'logos/horizontal_color.png',25,84,105)
pic(ROOT/'logos/stack_color.png',31,143,50)
pic(ROOT/'logos/horizontal_mono.png',104,158,68)
rule('Tách nền để giữ màu chữ.', 'Hai ô tạo nền ổn định cho Z và O trên nền trang sáng hoặc đậm. Giữ khoảng hở giữa ô; không kéo dãn, đổ bóng hay thêm viền O.', 'Màu vàng giữ hình rõ mà không cần một nét khác chen vào chữ.',214)
para('Dấu nhấn đỏ–vàng là nhận diện phụ, không trở thành gạch chân liên kết hay kí hiệu toán. Logo nhỏ cần được nhìn ở kích thước sử dụng thực.',25,257,160,9,5,color=MUTE)

new('Chữ dẫn đường. Nhãn lùi lại.',sub='Be Vietnam Pro cho giao diện và lời dẫn; STIX Two cho toán và tài liệu học.')
tag('Định lí',25,84);tx('Dấu đạo hàm trên một khoảng',25,95,16,True)
para('Nhãn nói nội dung này đang làm nhiệm vụ gì. Tiêu đề và lời giải thích mới là thứ người đọc cần chú ý trước.',25,106,160,11,6.2)
box(25,132,160,42,C['gray-2']);tx('Mở bài học',33,145,11,True,RED);tx('Liên kết đang được trỏ tới',33,160,10,True,RED)
c.setStrokeColor(HexColor(RED));c.setLineWidth(1.4);c.roundRect(124*M,H-166*M,53*M,24*M,2*M,stroke=1,fill=0);tx('Thẻ đang chọn',131,156,9.6,True)
rule('Link có màu và độ đậm; focus có viền.', 'Không gạch chân. Hover đổi nền/màu; focus bàn phím có đường bao rõ. Thẻ đang hiển thị dùng khung màu và trạng thái được khai báo trong mã.', 'Trạng thái không chỉ dựa vào sắc màu; cần nhìn được cả khi dùng bàn phím hoặc Sắc xám.',192)
para('Tag small caps, nhỏ hơn chữ chính, gray-6; không hộp, đặt ngay phía trên bên trái nội dung. Khi chữ Việt không có small caps thật, dùng chữ hoa nhỏ có khoảng cách hợp lí.',25,251,160,9.1,5.1,color=MUTE)

new('Hình toán cùng một giọng.',sub='Màu gắn với vai trò; đường nét gắn với ý nghĩa toán học.')
pic(ROOT/'graphics/two_curves.png',25,82,92,66);pic(ROOT/'graphics/geometry_3d.png',126,83,55,66)
pic(ROOT/'graphics/inverse.png',25,155,73,58);pic(ROOT/'graphics/geometry_sphere.png',116,155,66,58)
rule('Nhận diện đối tượng được giữ xuyên hình.', 'Đỏ chỉ đối tượng đang xét; xám giữ ngữ cảnh; vàng nhạt đánh dấu miền hoặc phạm vi chú ý. Nét đứt, điểm hở và điểm kín giữ đúng nghĩa.', 'Đồ thị, hình học và video phối hợp được khi thay khung nhìn mà không đổi căn tính đối tượng.',233)

new('Bảng để đọc, không để giả vẽ.',sub='Bảng biến thiên dùng một hàng cho giá trị hàm số, mọi kí hiệu toán từ LaTeX.')
pic(ROOT/'tables/bbt02.png',25,85,160,43)
para('Giá trị và mũi tên đi cùng một hàng. Không chia hàng hàm số thành nhiều tầng để dựng đường lên–xuống như một hình vẽ.',25,144,160,11,6)
y=171
for title,body in [('Kết cấu','Đủ đường ngang–dọc, đồng đều 1 px ở web; không nhấn đậm đường đầu và cuối.'),('Nhấn có nhiệm vụ','Hàng hoặc cột đang đọc: yellow-1; giao điểm đối chiếu: yellow-2; tổng: nền xám nhẹ.'),('Ngữ nghĩa','Giữ ô mốc/khoảng; điểm không xác định và giới hạn trái–phải phải ghi rõ. Bảng sai có chủ ý trong bài tập vẫn giữ đúng vai trò.')]:
 tx(title,25,y,10.8,True);y=para(body,66,y,119,9.7,5.4)+7
para('Vì sao. Cùng dữ liệu có thể xuất HTML, Quarto và bảng LaTeX thường. Quy tắc không phụ thuộc việc chèn một ảnh bảng biến thiên.',25,257,160,9.3,5.2,color=MUTE)

new('Ủng hộ là một chức năng rõ ràng.',sub='Nổi bật đúng thời điểm; không chắn bài học và không dùng pop-up.')
positions=[('Đầu trang','Lời mời ngắn, cho người đã muốn đồng hành tìm nhanh.'),('Cuối chặng học','Nhắc nhẹ sau một đơn vị học, khi giá trị của học liệu đã hiện rõ.'),('Vùng tải tài liệu','Khối đầy đủ, có QR và thông tin chuyển khoản.'),('Trang cuối PDF','Một trang kết có hướng học tiếp và lời mời ủng hộ rõ ràng.')]
y=86
for title,body in positions:
 box(25,y,160,27,C['gray-2']);tx(title,32,y+9,10.5,True);para(body,32,y+19,145,9.2,5);y+=34
para('Giữ nguyên thông tin nguồn: Vietcombank · 0601000137768 · Nguyễn Tấn Nhựt · BAO TRO ZO MATH.',25,234,160,10,5.7,True)
para('Vì sao. ZO Math cần kinh phí phát triển. Lời mời phải dễ tìm và cụ thể, đồng thời giữ quyền tiếp tục học của người chưa ủng hộ. Không bịa mục tiêu tiền, lượt ủng hộ hay quyền lợi.',25,253,160,9.3,5.2,color=MUTE)

new('PDF có mở đầu và kết thúc.',sub='Tám bản R1-G01 đã được thay bìa và thiết kế trang kết trong cùng một hệ.')
pic(ROOT/'qa/pdf_editions/index_cover.png',25,80,76,110);pic(ROOT/'qa/pdf_editions/index_end.png',109,80,76,110)
para('Bìa gọi đúng nội dung và đúng bản cần dùng. Trang cuối dẫn đến việc học tiếp, rồi mời ủng hộ với QR gốc và thông tin rõ ràng.',25,203,160,10.6,5.9)
para('Giới hạn thực tế: bìa và trang kết 0.4; toàn bộ ruột giữ bản nguồn v1.3. Chưa tái dàn toàn văn theo hệ bảng, tag và nền mới.',25,227,160,11,6.1,True)
para('Đã đối chiếu hash văn bản và ảnh render của từng trang ruột, giữ bookmark và liên kết. Trang ruột giữ hệ số trang bản nguồn; trang kết mới không đánh số.',25,251,160,9.3,5.2,color=MUTE)

new('Chuyển động giúp nhìn ra điều gì?',sub='Mẫu thử có pha xuất hiện, di chuyển, dừng quan sát và đối chiếu.')
pic(ROOT/'media/motion_ngang_poster.png',25,82,160,93)
steps=[('01','Đặt đối tượng'),('02','Theo điểm chạy'),('03','Dừng tại mốc'),('04','Đối chiếu bảng')]
for i,(n,label) in enumerate(steps):
 x=25+i*41;box(x,185,37,26,C['gray-2']);tx(n,x+4,194,8.2,True,MUTE);para(label,x+4,203,30,8.3,4.4,True)
rule('Thời gian phục vụ việc hiểu.', 'Giữ màu và nhãn của đối tượng giữa các pha. Có điều khiển phát/dừng, bản bước tĩnh và hướng giảm chuyển động; không tự phát.', 'Người học cần quyết định lúc quan sát tiếp. Thời lượng mẫu đang thử, chưa phải chuẩn nhịp của ZO Math.',230)

new('Âm thanh biết khi nào im lặng.',sub='Lời đọc, chú âm, nhạc và cue có chức năng khác nhau; không gom thành một “giọng thương hiệu”.')
y=90
for title,body in [('Lời đọc và chú âm','Giữ cách đọc thuật ngữ/công thức từ quy chuẩn chú âm đã có. Ngắt sau ý khó để người nghe theo kịp.'),('Cue chú ý và khép chặng','Hai mẫu focus/close chỉ là ứng viên. Phát theo thao tác; không tự biến tiếng báo thành âm thưởng–phạt.'),('Nhạc và khoảng lặng','Có bản không nhạc. Đoạn công thức cần rõ; im lặng cũng là thành phần có chủ đích.')]:
 tx(title,25,y,13,True);y=para(body,25,y+9,160,10.5,5.9)+12
# Exact waveform of the new focus cue, labelled as a file view rather than a hearing judgment.
f=ROOT/'media/cue_focus.wav'
with wave.open(str(f),'rb') as wf:
 rate=wf.getframerate();n=wf.getnframes();channels=wf.getnchannels();samples=np.frombuffer(wf.readframes(n),dtype=np.int16)
 if channels>1:samples=samples.reshape(-1,channels).mean(axis=1)
 duration=n/rate
box(25,219,160,27,C['gray-2']);c.setStrokeColor(HexColor(RED));c.setLineWidth(.65)
for i,chunk in enumerate(np.array_split(samples,450)):
 amp=float(np.max(np.abs(chunk.astype(float))))/32768 if len(chunk) else 0
 x=(29+152*i/450)*M;y0=H-232*M;c.line(x,y0-10*M*amp,x,y0+10*M*amp)
tx(f'cue_focus.wav · {duration:.2f} giây · dạng sóng của tệp thử',25,254,8.5,False,MUTE)
para('Trạng thái: ứng viên. Đã có tệp để nghe thử; đo tín hiệu không thay cho nghe duyệt chất giọng, sắc thái và mức phối âm.',25,265,160,8.6,4.8,color=MUTE)

new('Rõ điều đã kiểm. Rõ điều còn thử.',sub='0.4 là một bản tiến triển có bằng chứng; không đổi trạng thái thành “đã chốt” chỉ vì có tài sản.')
y=86
for title,body in [('Đã xác lập từ phản hồi','Tên Đỏ ZO / Vàng ZO / Xám ZO; giữ mã màu; bỏ viền O; bỏ gạch chân; sáu nền và khối trắng; hàng hàm số đơn.'),('Đã tạo để dùng thử','Hệ logo mới, bảng phẳng, trạng thái liên kết/thẻ, R1-G01 áp dụng nền, cụm ủng hộ, tám bìa/kết PDF, mẫu chuyển động và cue âm.'),('Cần duyệt trước khi coi là chuẩn','Tỉ lệ/logo ở kích thước thật, độ dễ đọc từng nền, mức nổi bật của lời mời ủng hộ, nhịp chuyển động, cách nghe cue và phối lời.'),('Giới hạn kiểm tra','Chưa xác nhận bố cục bằng trình duyệt thực; chưa chạy Quarto tại môi trường này. PDF được dựng và xem tĩnh. Không tự tuyên bố đạt toàn bộ WCAG.')]:
 tx(title,25,y,12,True);y=para(body,25,y+9,160,10.3,5.7)+13
para('Nguồn: góp ý trực tiếp; hồ sơ nghiên cứu nội bộ; mã nguồn/đồ thị/PDF của ZO Math; W3C về use of color, animation from interactions và audio control. Chi tiết: design/research_scope.json.',25,256,160,8.8,4.9,color=MUTE)

new('Cùng giữ một nhịp học Toán.',sub='Mỗi lựa chọn nên giúp nội dung rõ hơn và làm ZO Math dễ nhận ra hơn.')
pic(ROOT/'logos/horizontal_color.png',25,85,78)
para('Bước duyệt tiếp theo',25,135,160,17,8,True)
para('Dùng R1-G01 trên một buổi học thật. Ghi lại nơi mắt bị kéo lệch, chỗ khó đọc và lúc âm thanh hoặc chuyển động chưa giúp hiểu. Phản hồi theo tình huống sẽ có giá trị hơn việc chỉ chọn mẫu đẹp.',25,150,160,11.5,6.8)
box(25,197,160,58,INK)
tx('Ủng hộ ZO Math',33,212,17,True,YEL)
para('ZO Math hiện chưa có tài trợ. Bạn có thể góp phần duy trì việc biên soạn học liệu và phát triển công cụ học Toán.',33,225,144,10.5,6,color='#FFFFFF')
c.setFillColor(HexColor(YEL));c.roundRect(33*M,H-250*M,144*M,8*M,1*M,fill=1,stroke=0)
tx('Xem thông tin ủng hộ tại zomath.vn',38,247.5,9.5,True,INK);c.linkURL('https://zomath.vn/content/support/donate.html',(33*M,H-250*M,177*M,H-242*M),relative=0,thickness=0)
para('Việc ủng hộ là tự nguyện. Ngôn ngữ hình ảnh và âm thanh 0.4 tiếp tục được hoàn thiện qua sử dụng và phản hồi của bạn.',25,266,160,8.5,4.6,color=MUTE)

c.setTitle('ZO Math — Ngôn ngữ hình ảnh và âm thanh 0.4');c.setAuthor('ZO Math');c.setSubject('Quy chuẩn dùng thử, căn cứ và phạm vi triển khai 0.4');c.save();OUT.write_bytes(buf.getvalue())
doc=fitz.open(OUT);assert len(doc)==14
for i,p in enumerate(doc):
 assert '\ufffd' not in p.get_text()
 p.get_pixmap(matrix=fitz.Matrix(1,1),alpha=False).save(QA/f'page_{i+1:02}.png')
font=ImageFont.truetype(str(AS/'BeVietnamPro_SemiBold.ttf'),12)
contact=Image.new('RGB',(1400,1540),BG);draw=ImageDraw.Draw(contact)
for i in range(len(doc)):
 im=Image.open(QA/f'page_{i+1:02}.png');im.thumbnail((265,377));x=(i%5)*280+(280-im.width)//2;y=(i//5)*510+40
 contact.paste(im,(x,y));draw.text(((i%5)*280+10,(i//5)*510+12),f'{i+1:02} · '+titles[i][:31],font=font,fill=INK)
contact.save(QA/'contact_all.png')
(ROOT/'design/guide_0_4.json').write_text(json.dumps({'file':str(OUT.relative_to(ROOT)),'pages':len(doc),'sha256':hashlib.sha256(OUT.read_bytes()).hexdigest(),'titles':titles,'status':'Quy chuẩn dùng thử; âm thanh và chuyển động là ứng viên; chưa phải1.0.','rendered':True,'visual_review_contact':str((QA/'contact_all.png').relative_to(ROOT))},ensure_ascii=False,indent=2))
print(str(OUT))
