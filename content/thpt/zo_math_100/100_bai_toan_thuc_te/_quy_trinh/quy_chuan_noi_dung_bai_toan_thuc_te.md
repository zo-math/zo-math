# Quy chuẩn nội dung tối thiểu cho bài toán thực tế

**Trạng thái:** Hợp đồng thử nghiệm M8
**Phạm vi:** Các bài QMD thuộc dự án 100+ Bài toán thực tế

## 1. Mục đích

Một bài phải cho thấy đầy đủ đường đi từ tình huống đến mô hình toán học và từ kết quả toán học trở lại tình huống. Bài không chỉ thực hiện phép tính; nó phải làm rõ dữ kiện nào được dùng, giả định nào được đặt ra, đại lượng nào được mô hình hóa và kết quả có ý nghĩa gì.

## 2. Bốn phần bắt buộc

Mỗi bài có bốn mục H2 theo đúng chức năng sau:

1. **Bối cảnh và dữ kiện:** nêu tình huống, câu hỏi, số liệu, đơn vị và phạm vi áp dụng.
2. **Mô hình hóa:** xác định biến, quan hệ, giả định và mô hình toán học.
3. **Giải quyết:** thực hiện lập luận hoặc tính toán trong mô hình.
4. **Kiểm tra và diễn giải:** kiểm tra đơn vị, độ lớn, điều kiện áp dụng và diễn giải kết quả trở lại bối cảnh.

Có thể thêm các mục khác khi cần, nhưng không được làm mờ bốn chức năng trên.

## 3. Dữ kiện và giả định

- Phân biệt dữ kiện được cho với giả định do người giải đặt ra.
- Mọi đại lượng phải có tên và đơn vị khi đơn vị có ý nghĩa.
- Không ngầm xem một mô hình là đúng ngoài phạm vi đã xác lập.
- Số liệu giả định hoặc tình huống hư cấu phải được nói rõ, không trình bày như dữ kiện thực tế đã kiểm chứng.

## 4. Mô hình và kết quả

- Mô hình phải tương ứng với dữ kiện và giả định.
- Phép tính phải giữ đơn vị nhất quán.
- Kết quả số phải có mức chính xác phù hợp với dữ kiện.
- Kết luận phải trả lời câu hỏi trong bối cảnh, không dừng ở một biểu thức hoặc con số rời rạc.

## 5. Hồ sơ sản xuất

Hồ sơ cùng tên bài phải chứa:

- trạng thái sản xuất;
- trạng thái xuất bản;
- cờ xác nhận xuất bản của người dùng;
- bối cảnh;
- danh sách đại lượng;
- danh sách giả định;
- loại mô hình;
- danh sách kiểm tra thực tế.

Trạng thái xuất bản giữ `pending` cho đến khi người dùng xác nhận rõ.
