from pathlib import Path
import json,re
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
root=Path(__file__).resolve().parents[1]
items=json.loads((root/'D0_ngan_hang_v1.0.json').read_text())['items']
names=['Hàm số, đạo hàm, đồ thị','Thống kê và đọc dữ liệu','Hình học, vectơ và tọa độ','Đếm và xác suất','Dãy số, mũ và lôgarit','Lượng giác và tính tuần hoàn','Nguyên hàm, tích phân và tích lũy','Mô hình hóa, tối ưu và tổng hợp']
# Hình hình học được chiếu từ đúng tọa độ không gian, không dùng ảnh sinh.
V={'A':(0,0,0),'B':(3,0,0),'C':(3,4,0),'D':(0,4,0),'A_1':(0,0,2),'B_1':(3,0,2),'C_1':(3,4,2),'D_1':(0,4,2)}
p={k:(x+.55*y,z+.22*y) for k,(x,y,z) in V.items()}
fig,ax=plt.subplots(figsize=(6.3,3.15))
edges=[('A','B'),('B','C'),('C','D'),('D','A'),('A_1','B_1'),('B_1','C_1'),('C_1','D_1'),('D_1','A_1'),('A','A_1'),('B','B_1'),('C','C_1'),('D','D_1')]
for a,b in edges:
 hidden=(a,b) in [('C','D'),('D','A'),('D','D_1')]
 ax.plot([p[a][0],p[b][0]],[p[a][1],p[b][1]],'--' if hidden else '-',c='#334155',lw=1.2)
for a,b in [('A','C'),('A','C_1')]:ax.plot([p[a][0],p[b][0]],[p[a][1],p[b][1]],'--' if b=='C' else '-',c='#9b2028',lw=1.5)
off={'A':(-.15,-.2),'B':(.06,-.2),'C':(.08,-.06),'D':(-.22,-.12),'A_1':(-.26,.03),'B_1':(.08,.01),'C_1':(.09,.02),'D_1':(-.20,.1)}
for k,(xx,yy) in p.items():ax.text(xx+off[k][0],yy+off[k][1],f'${k}$',fontsize=11)
ax.text(1.4,-.26,'3 m',fontsize=10);ax.text(.55,.64,'4 m',fontsize=10,rotation=35);ax.text(-.4,.95,'2 m',fontsize=10,rotation=90)
ax.set_aspect('equal');ax.axis('off');ax.set_xlim(-.55,5.7);ax.set_ylim(-.45,3.65);fig.tight_layout(pad=0)
fig.savefig(root/'src/hinh_hop.pdf',bbox_inches='tight');fig.savefig(root/'src/hinh_hop.png',dpi=180,bbox_inches='tight');plt.close(fig)

def front(title,subtitle):return f'''---
title: "{title}"
subtitle: "{subtitle}"
author: "ZO Math biên soạn"
date: "Nội dung v1.0 · Kế hoạch 0.5 · 09/09/2026"
---

'''
breakpage='\n\\clearpage\n\n'
student=front('D0 · Khảo sát đầu vào','Bản học sinh · Ôn thi Toán THPT 2027')+'''## Trước khi bắt đầu

Bộ này giúp em biết cần ôn phần nào tiếp theo. Có 24 nhiệm vụ thuộc tám mạch; **em chỉ làm những câu được giao, thuộc kiến thức đã học**. Không phải làm hết cả ngân hàng và không quy kết quả thành điểm thi dự báo.

**Họ tên/mã học sinh:** ........................................................

**Lớp; ngày làm:** .............................................................

**Mục tiêu điểm do em lựa chọn:** ........ **Thời gian có thể ôn/tuần:** ........

**Mã câu được giao lượt này:** .................................................

**Bắt đầu lúc:** ....................... **Kết thúc lúc:** ......................

### Cách làm

1. Đọc phần “Cần đã học” của mỗi câu. Nếu chưa học, ghi **CH** và báo người hướng dẫn; không cần đoán.
2. Làm độc lập trên giấy riêng, ghi đúng mã câu và các bước chính. Câu chọn đáp án hoặc đúng/sai vẫn cần lời giải thích ngắn theo yêu cầu.
3. Được dùng máy tính cầm tay thông thường, giấy nháp và thước; không mở tài liệu, lời giải hay nhận gợi ý trong lượt làm độc lập. Ghi rõ nếu đã nhận hỗ trợ.
4. Ghi thời gian từng câu; đánh dấu **đoán/chưa chắc** nếu đúng với quá trình làm. Không thay bài ban đầu sau khi mở lời giải.
5. Nếu từng gặp câu này, câu tương tự hoặc đã xem lời giải, ghi rõ. Thông tin đó giúp chọn câu kiểm tra phù hợp.

Các dữ liệu về cước xe, sản xuất, mực nước, diện tích bèo và khảo sát trong bộ này là **dữ liệu giả định để học toán**. Chúng không phải dữ liệu điều tra hay mức giá thực tế.

Một số câu có nhiều ý. Tính từng ý từ giả thiết chung. Với câu đúng/sai, đánh dấu riêng a, b, c, d; không xem một khẳng định trong đề là dữ kiện đã đúng.

**Lượt này chưa cần mở bản thử lại.** Người hướng dẫn sẽ chọn câu thử lại sau khi xem bài của em.
'''+breakpage+'''## Khai báo phần đã học

Ở mỗi hàng, ghi nội dung em **đã học**, **chưa học** và **không nhớ rõ đã học chưa**. Không chỉ đánh dấu chung “đã học lớp 12”.

| Mạch | Những nội dung được hỏi trong bộ này | Phần đã học / chưa học |
|:---|:---|:---|
| R1 | Tập xác định; đạo hàm, tiếp tuyến; dấu đạo hàm và cực trị |  |
| R2 | Trung bình, trung vị; trung bình ghép nhóm; phương sai ghép nhóm |  |
| R3 | Vectơ cùng phương; khoảng cách điểm–mặt phẳng; góc đường–mặt |  |
| R4 | Độc lập, xung khắc; tổ hợp và xác suất; xác suất điều kiện |  |
| R5 | Cấp số; lôgarit; tăng trưởng theo chu kì |  |
| R6 | Độ và radian; phương trình sin; chu kì |  |
| R7 | Nguyên hàm; điều kiện đầu; tích phân và chuyển động |  |
| R8 | Biến, ràng buộc; chi phí; lựa chọn phương án khả thi |  |

### Ghi sau mỗi câu

**Mã câu:** ........ **Thời gian:** ........ phút.

**Đã từng gặp/cùng họ, đã xem lời giải?** .......................................

**Tự làm được / còn đoán / đã nhận hỗ trợ ở bước nào?** ..........................

**Nếu bỏ câu, lý do:** chưa học / chưa tìm ra cách / chưa đủ thời gian / ..........

Em không cần tự gán nhãn trình độ. Sau khi xem bài, người hướng dẫn sẽ cùng em chọn tối đa hai việc cần sửa và ngày thử lại.
'''
for r in range(1,9):
 student+=breakpage+f'## R{r}. {names[r-1]}\n\n'
 for it in [i for i in items if i['r']==f'R{r}']:
  student+=f"### {it['id']} · {it['title']}\n\n**Cần đã học:** {it['prereq']}\n\n{it['question']}\n\n*Thời gian: ...... phút. Đoán/chưa chắc/đã gặp: ........................*\n\n"
(root/'2027_D0_hoc_sinh_v1.0.md').write_text(student)

reserve=front('D0 · Câu thử lại','Bản học sinh · Chỉ giao câu được chọn')+'''## Dùng sau khi xem bài khảo sát

Bản này có 24 câu dự phòng, ghép một–một với các mục tiêu trong ngân hàng chính. **Không phải bài khảo sát thứ hai bắt buộc.** Người hướng dẫn chỉ giao câu cần kiểm tra sau sửa lỗi hoặc khi bằng chứng ban đầu chưa đủ.

Chỉ làm khi đã học phần kiến thức tương ứng và chưa xem lời giải câu được giao. Giữ bài làm độc lập, ghi thời gian và bước còn đoán. Nếu đã gặp câu hoặc được hỗ trợ, nói rõ.

**Họ tên/mã:** ........................ **Ngày:** ..............................

**Câu được giao:** .............................................................

**Nội dung vừa ôn:** ...........................................................

**Lời giải câu thử lại đã xem chưa?** ...........................................

Mỗi câu SL cùng họ với câu chính tương ứng: SL01 nối với 01, SL02 nối với 02, SL03 nối với 03 trong cùng mạch. Làm đúng câu đổi số giúp kiểm một lỗi cụ thể; chưa đủ kết luận đã vững cả mạch hoặc đã chuyển giao được sang mọi tình huống.

Được dùng máy tính cầm tay thông thường, giấy nháp và thước như lượt đầu. Các dữ liệu bối cảnh đều là giả định. Lời giải được giữ trong bản dành cho người hướng dẫn.
'''
for r in range(1,9):
 reserve+=breakpage+f'## R{r}. {names[r-1]}\n\n'
 for it in [i for i in items if i['r']==f'R{r}']:
  reserve+=f"### {it['retest_id']}\n\n**Cần đã học:** {it['prereq']}\n\n{it['retest']}\n\n*Thời gian: ...... phút. Đoán/đã gặp/hỗ trợ: ........................*\n\n"
(root/'2027_D0_thu_lai_v1.0.md').write_text(reserve)

sol=front('D0 · Lời giải và tiêu chí phân tích','Bản người hướng dẫn · 24 nhiệm vụ chính và 24 câu thử lại')+'''## Cách dùng bản lời giải

Lời giải do **ZO Math biên soạn**, có ChatGPT hỗ trợ; không phải đáp án Bộ. Dùng cùng bản học sinh và bản thử lại **v1.0**. Không đưa bản này cho học sinh trước khi kết thúc lượt làm độc lập cần đo.

Mỗi mục có đáp án, lập luận, tiêu chí quan sát, lỗi có thể gặp, nơi ôn và lời giải câu thử lại. Các lỗi nêu ra là khả năng để đối chiếu bài thật, không phải lỗi đã được ghi nhận ở học sinh.

Đánh dấu phần chưa học riêng. Đáp án đúng do đoán, đã gặp hoặc nhận hỗ trợ chưa đủ xác nhận làm được độc lập. Chấp nhận cách giải khác đúng; không quy số câu D0 thành điểm thi dự báo.

### Đối chiếu nhanh hai câu đúng/sai

| Câu | a | b | c | d |
|:---|:---:|:---:|:---:|:---:|
| D0-R1-03 | Đ | S | Đ | S |
| D0-R4-01 | Đ | S | Đ | S |
| D0-R1-SL03 | Đ | S | Đ | S |
| D0-R4-SL01 | Đ | S | Đ | S |

Sự trùng chuỗi đáp án không phải quy tắc để đoán; yêu cầu giải thích từng ý. Nếu ghi điểm định dạng đúng/sai, chấm cả câu theo mục 3.10 kế hoạch: 0/1/2/3/4 ý đúng được 0/0,1/0,25/0,5/1 điểm. Dữ liệu từng ý vẫn giữ riêng; không chấm mỗi ý cố định 0,25.

**Phạm vi kiểm tra:** tự giải từ đề; kiểm điều kiện, đáp án, dữ liệu; kiểm tính toán chính xác và các cách kiểm thêm phù hợp. Nhật ký 48 nhiệm vụ và mã kiểm nằm trong gói nguồn. Chưa có dữ liệu sử dụng và chưa có xác nhận người chủ trì duyệt.

**Kí hiệu nguồn:** S10.1/S10.2 là Toán 10 tập một/hai; tương tự cho lớp 11, 12; tất cả là bản Kết nối tri thức được cung cấp. Tr. trong chỉ dẫn ôn là trang in. Mã B và hàng tuần theo Kế hoạch 0.5.
'''
for r in range(1,9):
 for stage, ns in [('Nhận diện và thực hiện',[1,2]),('Giải thích và phối hợp',[3])]:
  sol+=breakpage+f'## R{r}. {names[r-1]}\n\n*{stage}*\n\n'
  for it in [i for i in items if i['r']==f'R{r}' and i['n'] in ns]:
   sol+=f"### {it['id']} · {it['title']}\n\n**Đáp án:** {it['answer']}\n\n{it['solution']}\n\n**Tiêu chí xem bài:** "+' '.join(it['criteria'])+f"\n\n**Lỗi cần đối chiếu:** {it['error']}\n\n**Ôn tiếp:** {it['repair']}\n\n**Thử lại {it['retest_id']}:** {it['reanswer']} {it['resolution']}\n\n"
(root/'2027_D0_loi_giai_v1.0.md').write_text(sol)

matrix='# D0 — Ma trận và hồ sơ câu hỏi v1.0\n\nNgày 09/09/2026; căn cứ Kế hoạch 0.5 mục 4.5–4.6, 5, 9.9, 11.1, D.18.\n\n24 nhiệm vụ chính; 24 câu SL dự phòng tách riêng, không cộng thành ngân hàng lượt đầu 48 câu. Mỗi mã chính chỉ đếm một lần theo mạch chính. Mã YC dưới đây do ZO Math đặt, không là mã Bộ. Cấp độ tư duy, năng lực và định dạng ghi riêng. Mọi thời gian đều là ước lượng thiết kế, chưa đo.\n\n'
matrix+='| Mã | Vai trò | Cụm chính/nền | Hỗ trợ | Định dạng | Phút dự kiến |\n|---|---|---|---|---|---:|\n'
for it in items:matrix+=f"| {it['id']} | {['Nhận diện/điều kiện','Thực hiện','Giải thích/phối hợp'][it['n']-1]} | {it['clusters']} | {it['support']} | {it['format']} | {it['minutes']} |\n"
matrix+='\n## Đối chiếu yêu cầu và hồ sơ từng mã\n\n'
for it in items:
 matrix+=f"### {it['id']} — {it['title']}\n\n"
 fields=[('Mục tiêu / mã yêu cầu nội bộ',f"YC-{it['id']}: {it['objective']}"),('Kiến thức học trước',it['prereq']),('Nguồn yêu cầu cần đạt',f"CT, trang in = PDF {it['ct']}; yêu cầu được diễn giải thành mục tiêu hẹp nêu trên, không trích nguyên văn."),('SGK thực đọc',it['source']),('Năng lực quan sát',it['capacity']),('Tư duy dự kiến và lý do',it['level']),('Phạm vi',it['scope']),('Họ câu và lịch sử',f"{it['family']}; câu chính và {it['retest_id']} cùng họ. {it['history']}"),('Bằng chứng chấm','; '.join(it['criteria'])),('Quy tắc chấm','Ghi Đ/M/S/CH/KCG/B theo từng lệnh; thêm cờ đoán, hỗ trợ, đã gặp. Hai câu Đ/S lưu bốn ý riêng; điểm định dạng cả câu theo hướng dẫn, không lập tổng điểm D0.'),('Lỗi và nơi ôn',it['error']+' '+it['repair']),('Tác giả',it['author']),('Kiểm chứng 09/09/2026',it['check']),('Tệp sử dụng','Bản học sinh v1.0; bản lời giải v1.0; bản thử lại v1.0; hướng dẫn v1.0. JSON giữ đề và lời giải gốc; không sửa một bản rời.'),('Trạng thái','Đã biên soạn và tự kiểm; chưa có bài học sinh; chưa có xác nhận người chủ trì duyệt. Câu v1.0, chưa có thay đổi công bố.')]
 for k,v in fields:matrix+=f'- **{k}:** {v}\n'
 matrix+='\n'
matrix+='''## Phạm vi chưa được lấy mẫu trong D0

Bộ 24 nhiệm vụ chưa khảo sát đủ các mục tiêu của mỗi mạch. Ví dụ còn thiếu: giới hạn/liên tục, tiệm cận và cực trị trên miền có biên (R1); tứ phân vị, khoảng biến thiên, độ lệch chuẩn và đọc biểu đồ (R2); conic, phương trình đường thẳng/mặt cầu, thể tích (R3); xác suất toàn phần/Bayes (R4); tổng cấp số và giới hạn dãy, bất phương trình mũ–lôgarit (R5); công thức lượng giác và các phương trình cos/tan/cot (R6); diện tích, thể tích bằng tích phân (R7); tối ưu liên tục và các phối hợp rộng hơn (R8).

Đây là các phần chưa có bằng chứng trong D0 v1.0, không bị loại khỏi chương trình hoặc kế hoạch. Các bài dùng đơn vị, đại số, miền xác định và điều kiện nguyên chỉ lấy mẫu nền N liên quan; không chứng minh bao phủ toàn nền THCS. Không công bố tỉ lệ bao phủ chương trình từ 24 câu này.

## Danh mục nguồn được dùng

- CT: `01-Chuong-trinh-giao-duc-pho-thong-mon-Toan-2018-1-.pdf`; tr.79–80, 82–83, 85–86, 89–92, 94–96, 99–102, 105–108, 110 theo các mục tiêu tương ứng. Các trang đã đọc là phần liên quan; không tuyên bố đã rà toàn bộ chương trình.
- S10.1: `02-Toan-10-Tap-1-Ket-noi-tri-thuc-voi-cuoc-song.pdf`; bản tái bản lần thứ tư theo hồ sơ kế hoạch. Trang PDF = trang in +1 tại các vị trí dẫn.
- S10.2: `06-Toan-10-Tap-2-Ket-noi-tri-thuc-voi-cuoc-song-1-.pdf`; cùng hệ nguồn. Trang PDF = trang in +1 tại các vị trí dẫn.
- S11.1: `04-Toan-11-Tap-1-Ket-noi-tri-thuc-voi-cuoc-song.pdf`; bản mẫu. Trang PDF = trang in +1 tại các vị trí dẫn.
- S11.2: `03-Toan-11-Tap-2-Ket-noi-tri-thuc-voi-cuoc-song.pdf`; bản mẫu. Trang PDF = trang in +1 tại các vị trí dẫn.
- S12.1: `05-Toan-12-Tap-1-Ket-noi-tri-thuc-voi-cuoc-song-1-.pdf`; bản mẫu. Trang PDF = trang in +2 tại các vị trí dẫn.
- S12.2: `07-Toan-12-Tap-2-Ket-noi-tri-thuc-voi-cuoc-song-1-.pdf`; bản mẫu. Trang PDF = trang in +2 tại các vị trí dẫn.
- Kế hoạch: `08-ZO_Math_On_thi_Toan_THPT_Ke_hoach_thuc_hien_2027_0.5.md`; không sửa nội dung hoặc quyết định của kế hoạch.

Các SGK là PDF ảnh: đã xem trực tiếp các trang trích dẫn trong hồ sơ câu. Đề bài D0 được tự biên soạn; không sao chép nguyên đề thi, không nhập bảng đáp án hoặc lời giải thứ sinh. Không cần mở các đề 2025/2026, ma trận minh họa lớp 10 hoặc phiếu trả lời để hoàn thành ngân hàng chẩn đoán này; D0 không mô phỏng phiếu thi.
'''
(root/'D0_ma_tran_va_ho_so_cau_v1.0.md').write_text(matrix)
print('Đã sinh bản học sinh, thử lại, lời giải, ma trận và hình từ dữ liệu gốc.')
