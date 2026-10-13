# Nội dung, Toán, hình và bảng

## Giữ ý nghĩa trước khi đổi diện mạo

Kiến trúc tham chiếu R6: ý nghĩa toán → vai trò → biểu diễn → thích ứng phương tiện → mã thực hiện. Đổi màu/nét không được làm đổi tập xác định, trạng thái điểm, điều kiện hoặc quan hệ. Nét khuất của hình 3D không có nghĩa điểm bị loại khỏi tập xác định. Tiếp tuyến/tiệm cận là đối tượng toán, không gộp thành đường trang trí phụ.

Nguồn nội dung của một sản phẩm là QMD/JSON/kịch bản hiện tại trong repo của sản phẩm đó. R1-G01 mẫu chỉ phục vụ so thiết kế. Không lấy PDF hoặc HTML 0.4 ghi đè bản nội dung mới hơn.

## Công thức và lời văn

Dùng $...$ inline, $$...$$ display trong nguồn Markdown/QMD. Công thức toán phải được render, không hiện mã. Ưu tiên câu văn cho suy luận khi phù hợp; không dùng kí hiệu suy ra/tương đương để thay cả lập luận. Phần giải thích là lời, biểu thức là toán.

Hàm từng khoảng dùng “khi” giữa biểu thức và điều kiện. Ví dụ nguồn:

```latex
$$
f(x)=\begin{cases}
x+1 & \text{khi }x<0,\\
x^2 & \text{khi }x\ge 0.
\end{cases}
$$
```

Ở đây `\text{khi }` là từ nối; không bọc cả biểu thức toán vào text. Các dấu câu ở cuối từng dòng và dấu chấm ở dòng cuối được giữ theo yêu cầu. Dùng lệnh xuống dòng của cases, không dùng dấu phẩy làm lệnh xuống dòng.

Phụ đề/mô tả chỉ nhận văn bản thuần: dùng Unicode cho biểu thức đơn giản, đưa biểu thức phức tạp sang vùng công thức đã render. Không đưa dấu đô-la hoặc lệnh LaTeX vào SRT/ASS text hiển thị. Đây là thích ứng theo phương tiện, không thay quy tắc LaTeX của học liệu.

## Đồ thị và hình học

Mẫu dùng đỏ cho đối tượng chính, xám cho cấu trúc/ngữ cảnh, vàng nhạt cho vùng chú ý. Nhãn và loại nét giúp nhận biết ngoài màu. Giữ ánh xạ đối tượng xuyên cảnh, kể cả lúc phóng đại hoặc chuyển từ tĩnh sang động.

Thông số tham khảo trong roles_0_4: đường chính 1.1pt, trục .8pt, đường phụ .6pt, nét khuất .7pt, khung .45pt. Chúng thuộc hệ TeX mẫu; không sao chép nguyên số sang đơn vị Manim. Độ dày phải được đối chiếu sau render ở kích thước sử dụng.

Kiểm tỉ lệ trục phù hợp ý nghĩa: khi nói góc, khoảng cách hoặc hình dạng hình học, tỉ lệ biểu diễn phải hợp lệ. Phân biệt phạm vi lấy mẫu với tập xác định và cửa sổ xem; không nối qua tiệm cận/điểm gián đoạn. Nhãn không đè lên đường, mốc hoặc marker.

## Bảng

Bảng dùng lưới ngang-dọc đầy đủ và nét đồng đều; không làm hai đường đầu/cuối lấn nội dung. Dùng heading row/column có ngữ nghĩa, caption và vùng cuộn khi cần. Các công thức phải render từ LaTeX.

Phân vai tám loại trong mẫu: giá trị; dữ liệu/tần số; đối chiếu; hai chiều; dấu; biến thiên; tiêu chí đánh giá; quy trình/thuật ngữ. Khác biệt là cách đọc/căn dữ liệu/nhấn/đơn vị, không chỉ đổi màu tiêu đề. Hàng/cột đang xét yellow-1, ô giao yellow-2, tổng gray-2 là cấu hình thử.

BBT lấy từ một nguồn dữ liệu; hàng hàm số phẳng. Không ép mọi bảng có ba hàng; bản nguồn có bảng chỉ mốc và giá trị, hoặc mốc và dấu. Giữ điểm loại, giới hạn một phía, không tồn tại, ô khoảng và ví dụ sai có chủ ý. Khi điểm loại chứa hai giới hạn khác nhau, phải có cấu trúc biểu đạt rõ, không gộp mất dữ kiện để bảng gọn.

HTML dùng bảng native có toán render; PDF hướng tới bảng LaTeX thường. Đầu ra SVG/PDF vector cũ có thể còn dùng trong sản phẩm chưa chuyển, phải ghi trạng thái. Nếu dùng lại cách vẽ khi native không đạt chất lượng, nêu ca cụ thể và bỏ nền dư ngoài khung theo yêu cầu trước đó.

## Khối nội dung

Vai trò như định nghĩa, định lí, ví dụ, nhiệm vụ, phản ví dụ, gợi ý, lời giải, tự kiểm tra phải gắn với nội dung thật. Tag nhắc vai trò, không chiếm trọng tâm. Không đồng nhất khối trình bày với cấu trúc tiến trình học: thay giao diện không tự đổi thứ tự bài, cách mở lời giải hay tiêu chí hoàn thành.
