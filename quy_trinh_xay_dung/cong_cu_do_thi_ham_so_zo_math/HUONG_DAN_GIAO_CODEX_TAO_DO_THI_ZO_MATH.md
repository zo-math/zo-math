# Hướng dẫn giao Codex tạo đồ thị bằng bộ công cụ ZO Math

## 1. Mục đích của ghi chú này

Khi cần tạo một đồ thị mới, mở tệp này, điền thông tin vào prompt mẫu ở Mục 3 rồi giao toàn bộ prompt cho Codex đang mở tại kho:

```text
E:\zo_math
```

Không cần nhớ cuộc trò chuyện đã dùng để xây bộ công cụ và không cần tự viết TikZ/PGFPlots.

Bộ công cụ canonical nằm tại:

```text
E:\zo_math\quy_trinh_xay_dung\cong_cu_do_thi_ham_so_zo_math\
```

Commit thiết lập bộ công cụ:

```text
354fb22 feat(graph): add ZO Math function graph toolkit
```

## 2. Quy trình ngắn gọn

1. Xác định đồ thị cần thể hiện và mục đích sư phạm.
2. Điền prompt mẫu ở Mục 3.
3. Giao prompt cho Codex trong kho `E:\zo_math`.
4. Codex tạo bản thử trong `_audit`, gồm nguồn TEX, PDF và SVG.
5. Mở trang đối chiếu do Codex tạo và nghiệm thu bằng mắt.
6. Nếu cần, yêu cầu Codex chỉnh đúng điểm chưa đạt rồi dựng lại.
7. Khi hình đạt, yêu cầu Codex tích hợp ba tệp TEX/PDF/SVG vào bài học.
8. Codex dựng lại HTML và PDF của bài để kiểm tra trong ngữ cảnh thật.
9. Chỉ staging và commit sau khi đã kiểm tra diff và toàn bộ thành phẩm.

## 3. Prompt mẫu giao Codex

Thay mọi phần nằm trong dấu ngoặc vuông bằng thông tin của đồ thị cần tạo.

```text
Hãy dùng bộ công cụ đồ thị ZO Math tại:

E:\zo_math\quy_trinh_xay_dung\cong_cu_do_thi_ham_so_zo_math\

để tạo bản thử cho đồ thị sau.

## Nội dung toán học

- Tên tệp dự kiến: [ví dụ: do_thi_sin]
- Hàm số hoặc các đối tượng cần vẽ: [ví dụ: y=sin x]
- Mục đích sư phạm: [đồ thị cần giúp người học nhìn thấy điều gì]
- Miền lấy mẫu: [ví dụ: từ -2π đến 2π]
- Cửa sổ quan sát: [xmin, xmax] × [ymin, ymax]
- Vạch chia và nhãn trục cần có: [liệt kê]
- Điểm đặc biệt cần đánh dấu: [liệt kê hoặc ghi không có]
- Đường phụ, tiếp tuyến, tiệm cận hoặc miền tô: [liệt kê hoặc ghi không có]
- Nội dung nhãn trực tiếp hoặc hộp chú thích: [ghi rõ]

## Yêu cầu trình bày

- Tuân thủ Quy chuẩn đồ thị hàm số ZO Math v0.2 và dùng style canonical.
- Chọn mẫu nguồn phù hợp trong thư mục mau của bộ công cụ.
- Dùng font, màu, độ dày, nền và trục canonical; không tự tạo style song song.
- Nếu dùng nhãn trực tiếp cho công thức hàm, đặt nhãn gần một đầu mút nhìn thấy của đường cong.
- Nhãn công thức phải chạm nhẹ vào đường cong để quan hệ được nhận ra ngay; nền bảo vệ không cho đường xuyên chữ.
- Vị trí nhãn do người biên soạn lựa chọn có chủ ý, không bố trí tự động thiếu kiểm soát.
- Không thêm điểm, nghiệm, giao điểm hoặc dữ kiện không phục vụ mục đích sư phạm.
- Bảo đảm dễ đọc trên desktop, mobile 390 px và bản in.

## Nơi tạo bản thử

Chỉ tạo tệp trong:

E:\zo_math\_audit\[ten_thu_muc_thu_nghiem]\

Không sửa tệp canonical, không staging, commit, push, prepare hoặc publish.

## Dựng và kiểm tra

1. Tạo nguồn .tex.
2. Dùng zo_graph_build.py với --check để sinh PDF và SVG.
3. Tạo doi_chieu.html dùng trực tiếp SVG mới.
4. Tạo ảnh chụp desktop 1440 px và mobile 390 px.
5. Kiểm tra:
   - nội dung toán học;
   - cửa sổ quan sát;
   - nhãn và marker;
   - PDF một trang và giữ dạng vector;
   - font STIX;
   - SVG có viewBox và không dùng tài nguyên ngoài;
   - không tràn ngang;
   - không còn tệp build tạm hoặc listener.

## Bàn giao

Báo đường dẫn của:

- nguồn TEX;
- PDF;
- SVG;
- trang đối chiếu HTML;
- ảnh desktop;
- ảnh mobile.

Nêu rõ mọi quyết định bố trí quan trọng và những điểm tôi cần duyệt bằng mắt. Dừng để tôi nghiệm thu; chưa tích hợp vào bài học.
```

## 4. Ví dụ đã điền: đồ thị $y=\sin x$

```text
Hãy dùng bộ công cụ đồ thị ZO Math tại:

E:\zo_math\quy_trinh_xay_dung\cong_cu_do_thi_ham_so_zo_math\

để tạo bản thử trong:

E:\zo_math\_audit\thu_nghiem_do_thi_sin\

Nội dung:

- Tên tệp: do_thi_sin.
- Vẽ y=sin x.
- Mục đích: thể hiện hình dạng và tính tuần hoàn của hàm sin trên hai chu kì.
- Miền và cửa sổ theo trục x: từ -2π đến 2π.
- Cửa sổ theo trục y: từ -1,5 đến 1,5.
- Nhãn trục x: -2π, -π, 0, π, 2π.
- Nhãn trục y: -1, 0, 1.
- Không marker, không đường phụ, không hộp chú thích.
- Đặt nhãn y=sin x gần đầu bên phải của đường cong; nhãn chạm nhẹ vào đường cong nhưng đường không xuyên chữ.

Yêu cầu:

1. Dùng mẫu một đường và style canonical theo Quy chuẩn v0.2.
2. Tạo do_thi_sin.tex.
3. Dùng zo_graph_build.py với --check để sinh do_thi_sin.pdf và do_thi_sin.svg.
4. Tạo doi_chieu.html và ảnh chụp ở 1440 px, 390 px.
5. Kiểm tra nội dung toán học, font, vector, viewBox, nhãn và khả năng đọc trên mobile.
6. Không sửa canonical, không staging, commit, push hoặc publish.
7. Dừng để tôi nghiệm thu bằng mắt.
```

## 5. Nghiệm thu và yêu cầu sửa

Khi xem trang đối chiếu, chỉ cần nhận xét trực tiếp điều chưa đạt. Ví dụ:

```text
Nhãn y=sin x đang cách đường cong quá xa. Hãy chuyển nhãn tới gần đầu phải, cho đường cong chạm nhẹ mép nền bảo vệ nhưng không xuyên chữ. Giữ nguyên mọi phần còn lại, dựng lại PDF/SVG và ảnh mobile.
```

Không cần tự chỉ định tọa độ nếu chưa biết tọa độ phù hợp. Codex có trách nhiệm thử vị trí, dựng lại và báo tọa độ cuối cùng.

## 6. Sau khi bản thử đạt, dùng kết quả thế nào?

Một đồ thị hoàn chỉnh có ba tệp chính:

```text
do_thi_sin.tex
do_thi_sin.pdf
do_thi_sin.svg
```

Vai trò:

| Tệp | Công dụng |
|---|---|
| `.tex` | Nguồn gốc có thể chỉnh sửa và tái dựng về sau. Phải lưu cùng sản phẩm. |
| `.svg` | Hình vector dùng cho HTML và website. QMD thường tham chiếu tệp này. |
| `.pdf` | Hình vector dùng khi dựng bản PDF để bảo đảm chữ và đường nét rõ khi in. |

Sau khi nghiệm thu, giao Codex prompt sau:

```text
Tôi đã nghiệm thu đạt đồ thị [tên đồ thị] trong:

E:\zo_math\_audit\[thư mục thử nghiệm]\

Hãy tích hợp chính thức vào [đường dẫn bài học hoặc dự án].

Yêu cầu:

1. Xác định đúng thư mục nguồn hình canonical của sản phẩm.
2. Đưa cả TEX, PDF và SVG đã duyệt vào đó.
3. QMD dùng SVG cho HTML.
4. Khi dựng PDF, dùng PDF vector tương ứng; không raster hóa thành PNG.
5. Giữ nguyên nội dung, alt và chú thích của bài, trừ khi việc tích hợp thực sự đòi hỏi sửa đường dẫn.
6. Dựng lại HTML và PDF của sản phẩm.
7. Kiểm tra hình trong HTML desktop, mobile 390 px và đúng trang PDF.
8. Tạo hồ sơ đối chiếu sau tích hợp trong _audit.
9. Báo chính xác các tệp tạo, sửa hoặc xóa và git diff riêng của phạm vi.
10. Không staging, commit, push, prepare hoặc publish.

Dừng để tôi nghiệm thu lần cuối.
```

Sau lần nghiệm thu cuối, mới xem xét staging và commit các tệp canonical.

## 7. Những điều cần nhớ

- `_audit` chỉ là nơi thử nghiệm và nghiệm thu; không phải nơi lưu nguồn chính thức.
- Không dùng riêng SVG mà bỏ mất TEX và PDF.
- Không lấy ảnh PNG làm thành phẩm canonical nếu đồ thị có thể giữ dạng vector.
- Không giao Codex sửa trực tiếp bài học trước khi bản thử được duyệt.
- Không dùng `git add .`; luôn staging bằng danh sách đường dẫn đã kiểm tra.
- Không commit cùng các thay đổi không liên quan đang có trong working tree.

## 8. Ý tưởng phát triển tiếp theo: lớp nhập liệu đơn giản

Bộ công cụ hiện tại là công cụ dựng: nó cần một nguồn `.tex` do người hoặc Codex viết. Một lần phát triển sau nên bổ sung lớp nhập liệu dành cho người không biết TikZ.

Mục tiêu:

```text
Phiếu YAML đơn giản
        ↓
tao_do_thi.py sinh nguồn TEX
        ↓
zo_graph_build.py sinh PDF và SVG
```

Lớp nhập liệu tối thiểu cần hỗ trợ:

- một hoặc nhiều hàm trên cùng hệ trục;
- công thức PGFPlots và nhãn LaTeX tách biệt;
- miền lấy mẫu và cửa sổ quan sát;
- tick và nhãn tick, kể cả bội của $\pi$;
- marker đặc, marker rỗng và nhãn điểm;
- nhãn công thức tại đầu trái hoặc đầu phải;
- đường chiếu, tiếp tuyến, tiệm cận;
- ba kiểu đường ngang cấp: liền, đứt, gạch–chấm;
- tùy chọn một panel hoặc hai panel;
- sinh TEX để người dùng vẫn có thể tinh chỉnh;
- gọi lại bộ dựng hiện hành, không tạo pipeline PDF/SVG thứ hai.

Tiêu chí nghiệm thu đầu tiên:

> Người dùng tự tạo được đồ thị $y=\sin x$ bằng cách sao chép một tệp YAML, thay các giá trị được hướng dẫn và chạy đúng một lệnh; không cần viết TikZ và không cần nhớ prompt cũ.

Không phát triển lớp này trong lúc đang chuyển đổi đồ thị R1-G01 nếu chưa mở một nhiệm vụ riêng và xác định rõ phạm vi.
