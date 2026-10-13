# Phong cách ZO Math

Phiên bản 0.6 — Bản dùng thử, dễ cập nhật.

**Tinh thần:** Đơn giản mà sâu sắc. Tối giản để giúp tiếp thu; vẫn có điểm nhấn, nhịp điệu và sự khám phá.

Dùng chung cho sản phẩm ZO Math tạo bằng NotebookLM Studio. Mỗi sản phẩm áp dụng những phần phù hợp với hình thức của nó. Tài liệu này hướng dẫn cách trình bày, không phải nội dung để đọc thành lời hoặc giảng cho người học.

## 1. Diện mạo — sửa ở đây khi muốn thay đổi hình thức

| Thành phần        | Quy định                                                                                                                                                                               |
| ----------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Hai màu nhận diện | Đỏ #EF5350 và vàng #FFCF3D. Đỏ làm điểm nhấn chính; vàng làm điểm nhấn đồng hành, có chủ đích.                                                                                         |
| Nền               | Trắng ấm #FBFAF8; có thể dùng nền vàng rất nhạt #FFF9E9 cho vùng minh họa.                                                                                                             |
| Chữ               | Xám đậm #3E3A35. Chữ rõ, ít kiểu chữ, phân cấp tiêu đề và nội dung nhất quán.                                                                                                          |
| Phông mục tiêu    | Be Vietnam Pro cho chữ; STIX Two Math cho công thức khi công cụ hỗ trợ. Ưu tiên đúng dấu và dễ đọc.                                                                                    |
| Bố cục            | Thoáng; mỗi cảnh hoặc vùng nội dung có một trọng tâm. Dùng khoảng trống để làm rõ quan hệ.                                                                                             |
| Hình minh họa     | Đồ thị, sơ đồ và hình học phục vụ ý nghĩa toán học. Nhãn, điểm, trục và đường phụ phải đúng và cần thiết.                                                                              |
| Nhấn mạnh         | Chỉ làm nổi một lần: một chi tiết được nhấn bằng màu thì không thêm gạch chân, tô nền, tăng cỡ hay hiệu ứng để nhấn lại. Nhãn và loại nét vẫn dùng khi cần phân biệt ý nghĩa toán học. |
| Tên thương hiệu   | Viết đúng “ZO Math”, đặt gọn, không lấn nội dung. Chỉ dùng logo gốc khi được cung cấp; không tự tạo logo.                                                                              |

Giữ màu của cùng một đối tượng nhất quán trong một sản phẩm. Không buộc mỗi cảnh phải có đủ cả hai màu. Tránh màu neon, trang trí thừa, khung hộp dày đặc và các cảnh toàn chữ lặp lại đơn điệu.

Ghi chú cho người biên tập: vàng #FFCF3D đang là mã dùng thử; cần đối chiếu lại với vàng nhấn #FFCA28 trong báo cáo repository trước khi chốt mã chính thức. Khi xác minh xong, chỉ sửa dòng màu nhận diện ở trên và bỏ ghi chú này.

### Quy tắc chung: nhấn mạnh và phân vùng

- **Chỉ làm nổi một lần.** Mỗi từ, cụm từ hay đối tượng chỉ dùng một cách nhấn chính. Chữ đã đỏ không thêm gạch chân vàng, tô nền hoặc phóng to riêng. Cỡ và độ đậm của phần được đổi màu giữ cùng cấp với phần còn lại.
- Quy tắc này áp dụng lâu dài cho video, trình chiếu, tài liệu và đồ họa thông tin. Không cấm nhãn, đơn vị hoặc loại nét cần thiết để đọc đúng toán học.
- **Tách hình, kết luận và phụ đề.** Trong hình chỉ giữ nhãn trực tiếp cần thiết: tên trục, tọa độ, đường, điểm. Câu kết luận và diễn giải dài đặt ngoài hình; ưu tiên dưới hình và trên vùng phụ đề, có khoảng trống rõ.
- Dành trước vùng phụ đề; không tận dụng vùng ấy để đặt kết luận hoặc công thức. Khi quá chật, chia cảnh hoặc rút lượng chữ hiển thị mà giữ nguyên ý; không thu nhỏ toàn bộ chữ.
- **Trục nhẹ, đường chính rõ.** Đầu mũi tên trục dùng dạng mở gồm hai nét mảnh, nhỏ và đồng bộ giữa các trục. Không dùng tam giác đặc lớn. Mũi tên không lấn át đường cong hoặc nhãn toán học.
- Quy tắc trục này dành cho mẫu sản phẩm Studio; không tự thay đổi mã nguồn hay quy chuẩn TikZ trong repository.
- Giữ nền và vai trò màu ổn định giữa các cảnh. Không tự chuyển từ nền sáng ấm sang nền xám xanh.
- Không để chữ, công thức, nhãn và kí hiệu che nhau hoặc chạm nhau ngoài cấu trúc toán học cần thiết.
- Nhãn tập xác định và nhận xét về dấu phải có vị trí riêng, không chen vào phân số hoặc công thức khác.
- Tại một mốc trên đồ thị, tránh dồn số, ngoặc khoảng, dấu đánh dấu và đường phụ vào cùng vị trí. Dời nhãn ra vùng trống; chỉ giữ các kí hiệu cần thiết.
- Kết luận đặt ngoài đồ thị; phụ đề có vùng riêng. Nếu thiếu chỗ, chia thành các cảnh kế tiếp, không chồng thêm lớp.

### Công thức toán học

- Công thức đứng riêng và công thức chính trong hình phải được dàn bằng LaTeX và hiển thị thành công thức hoàn chỉnh.
- Trong mọi văn bản dạng câu — phụ đề, tiêu đề, câu hỏi, câu kết luận, chú thích — biểu thức toán dùng Unicode thông thường, chính xác và dễ đọc. Ví dụ: x², f′(x), x ≠ 2, (1; 2).
- Tuyệt đối không để lộ mã LaTeX, dấu đô-la hoặc lệnh định dạng trong văn bản hiển thị và phụ đề.
- Nếu biểu thức quá phức tạp để viết rõ bằng Unicode, đưa nó ra vùng công thức riêng; trong câu chỉ diễn đạt hoặc nhắc đến biểu thức ấy.
- Giữ đúng chữ hoa/thường của biến, kể cả khi phụ đề viết IN HOA.

### Dấu nhấn ZO

- Họa tiết nhận diện phụ trợ: hai vạch bo tròn, đỏ dài bên trái và vàng ngắn bên phải. Dùng cùng logo, không thay logo.
- Lấy độ dày là u: chiều dài đỏ 15u, vàng 8u, khoảng hở 1,75u, bán kính bo 0,5u. Thu phóng đồng tỉ lệ; khoảng trống quanh dấu ít nhất 2u.
- Màu theo bảng màu ở đầu tệp. Dùng ở chân khung/trang hoặc làm dấu ngăn dưới logo, không dùng để nhấn thêm một cụm đã có màu.
- Mặc định một dấu mỗi trang/cảnh; giữ hai vị trí trong khung kết đang thử theo mẫu đã được nhận xét tạm ổn. Không thêm hiệu ứng, đảo màu hoặc dùng như kí hiệu toán học.
- Đây là mẫu chuẩn hóa đề xuất để dùng lâu dài sau khi duyệt; không tự thay đổi logo hoặc website.

### Khung mở đầu video

- Dùng một mẫu bố cục nhất quán: nền trắng ấm, logo gốc ZO Math nhỏ ở góc trên bên phải; một khung nền vàng rất nhạt, viền đỏ mảnh chứa câu hỏi/gợi ý chính; chữ xám đậm và điểm nhấn đỏ.
- Câu hỏi/gợi ý được rút từ chính nội dung đã có trong video và nguồn được chọn. Nêu rõ điều học sinh sẽ hiểu hoặc phân biệt được; không tự đặt chủ đề mới, không giật gân.
- Giữ câu ngắn, khoảng 2–3 dòng dễ đọc trên điện thoại. Hiện ngay đầu video, đủ thời gian đọc; không mở bằng đoạn logo riêng kéo dài.
- Video ngắn dùng khung dọc 9:16; video dài YouTube dùng khung ngang 16:9. Bố trí lại theo tỉ lệ, không kéo giãn mẫu dọc.
- Khung mở đầu giữ bố cục và vị trí thương hiệu; nội dung câu hỏi thay đổi theo từng video. Nội dung phía sau phải giải đáp điều đã đặt ra.

### Khung kết và ghi nhận công cụ

- Khung kết dọc mẫu 01 được giữ làm cơ sở vì chủ dự án nhận xét tạm ổn; bản ngang giữ cùng hệ nhận diện và bố trí phù hợp 16:9.
- Bổ sung khung kết riêng của ZO Math sau đoạn nhận diện gốc của công cụ: nền sáng ấm, logo gốc ZO Math làm trọng tâm, điểm nhấn đỏ/vàng tiết chế; thời lượng mục tiêu 2–3 giây.
- Dòng ghi công đề xuất: “Biên soạn và biên tập: ZO Math” và “Hỗ trợ tạo video: Gemini Notebook”. Chỉ dùng mô tả vai trò đúng với công việc thực tế.
- Giữ nguyên dấu nhận diện và đoạn kết gốc của Google trong phương án hiện tại. Chưa xác minh ngoại lệ chính thức cho phép bỏ đoạn kết của định dạng Short.
- Không ghép logo hoặc dùng “hợp tác với Google” / “ZO Math × Google” khi không có quan hệ đối tác chính thức. Ghi tên công cụ bằng chữ thông thường là đủ.
- Mẫu đầu/cuối cố định có thể cần được ghép ở bước biên tập sau khi tải video. Chỉ dẫn tạo sinh không bảo đảm bố cục chính xác.

### Phụ đề video

- Phụ đề chỉ dùng văn bản thuần và kí hiệu Unicode. Quy tắc này áp dụng cả với số đứng riêng: viết 1, 2, 3; không bao số hoặc biểu thức bằng dấu đô-la.
- Chuyển mọi biểu thức từ nguồn sang Unicode trước khi đưa vào phụ đề; không sao chép nguyên mã LaTeX. Công thức LaTeX chỉ dành cho vùng công thức riêng đã được dàn hoàn chỉnh.
- Kiểm tra toàn bộ phụ đề trước khi xuất: không còn dấu đô-la hoặc lệnh LaTeX.
- Chữ lời nói IN HOA, đủ dấu tiếng Việt, nét bán đậm; công thức và kí hiệu toán giữ nguyên hoa/thường theo ý nghĩa.
- Màu chữ mặc định: vàng ZO ở bảng màu trên. Từ đang được nói chuyển sang đỏ ZO; đề xuất trở lại vàng sau khi nói xong để chỉ có một điểm nhấn di chuyển.
- Nền phụ đề: xám ấm đậm #25221F, đặc 100%, bo góc nhẹ, có khoảng đệm quanh chữ. Không dùng nền trong suốt để giữ tương phản ổn định.
- Đặt gọn phía dưới, tối đa hai dòng, không che công thức hoặc đồ thị. Giữ vị trí chữ ổn định khi đổi màu, không nhảy hoặc phóng to từng từ.
- Đây là yêu cầu thiết kế cần kiểm tra trên video thực tế; chưa xác nhận NotebookLM hỗ trợ đồng bộ đổi màu từng từ. Không coi việc thêm quy định này là đã sửa video đang tạo.

## 2. Cách diễn đạt — sửa ở đây khi muốn đổi văn phong hoặc lời dẫn

- Điềm tĩnh, rõ, chính xác và gần gũi; tôn trọng người học.
- Câu nói dễ theo dõi. Giải thích ý nghĩa của công thức thay vì chỉ đọc từng kí hiệu.
- Dùng thuật ngữ nhất quán; nêu đủ điều kiện của kết luận.
- Đặt câu hỏi có mục đích, có giải thích hoặc cơ hội tự suy nghĩ đi kèm.
- Tránh giật gân, lên gân, lời khen sáo rỗng và lời hứa học nhanh tuyệt đối.
- Dùng tên gọi có nghĩa với người học, như “Ví dụ 1”; không đưa mã quản lí nội bộ vào sản phẩm.

## 3. Cách dẫn dắt việc học — sửa ở đây khi muốn đổi cách giảng giải

- Mỗi sản phẩm có mục tiêu học tập rõ.
- Chọn vấn đề hoặc hiện tượng giúp người học thấy điều cần tìm hiểu.
- Giải thích có căn cứ. Ví dụ, phản ví dụ và hình ảnh phải làm rõ một ý cụ thể.
- Kết nối lời, công thức, bảng và hình khi hữu ích. Không bắt mọi bài có cùng trình tự hoặc đầy đủ mọi loại biểu diễn.
- Phân biệt quan sát trên hình với chứng minh. Không bỏ điều kiện để rút ngắn nội dung.
- Khi phù hợp, kết thúc bằng một kết luận và một câu hỏi nhỏ để người học tự kiểm tra.

## 4. Áp dụng riêng — sửa đúng dòng sản phẩm muốn tinh chỉnh

| Sản phẩm                     | Cách áp dụng                                                                                                           |
| ---------------------------- | ---------------------------------------------------------------------------------------------------------------------- |
| Video ngắn                   | Một ý trung tâm; ít chữ; hình và lời ăn khớp; đủ nhịp để quan sát. Không mặc định phải nói về “bẫy”.                   |
| Video giải thích             | Chia đoạn theo vấn đề; mỗi đoạn làm rõ một bước; có nhịp dừng ở chỗ cần suy nghĩ.                                      |
| Tổng quan âm thanh / podcast | Giải thích đủ để nghe hiểu khi không nhìn hình; đọc kí hiệu tự nhiên; đối thoại có nhiệm vụ, tránh tán chuyện kéo dài. |
| Bản trình chiếu              | Mỗi trang một trọng tâm; tiêu đề có nghĩa; hình, công thức và chữ hỗ trợ nhau.                                         |
| Đồ họa thông tin             | Có thứ tự đọc rõ; ít nhóm thông tin; ưu tiên quan hệ và so sánh, tránh nhồi cả bài vào một hình.                       |
| Báo cáo / tài liệu học tập   | Đề mục rõ; đoạn văn vừa sức đọc; ví dụ đặt gần ý cần giải thích.                                                       |
| Sơ đồ tư duy                 | Nhánh thể hiện quan hệ có nghĩa; nhãn ngắn, tránh chia nhánh chỉ để lấp đầy.                                           |
| Thẻ ghi nhớ                  | Mỗi thẻ một ý hoặc một nhiệm vụ; đáp án ngắn, chính xác, đủ điều kiện.                                                 |
| Bài kiểm tra / câu hỏi       | Yêu cầu rõ; dữ kiện đủ; đáp án và lời giải nhất quán; phương án nhiễu phản ánh nhầm lẫn có ý nghĩa.                    |
| Bảng dữ liệu                 | Tiêu đề cột, đơn vị và dữ liệu rõ; giữ nguồn gốc dữ liệu; không tự bổ sung số liệu thiếu.                              |

Đây là hướng dẫn thiết kế. Chỉ áp dụng cho các loại sản phẩm và tùy chọn thực sự có trong tài khoản đang dùng; không phải mọi công cụ đều cho điều chỉnh màu, phông hoặc bố cục.

## 5. Cách dùng và cập nhật

**Lần đầu trong một sổ:** thêm tệp này vào Nguồn, cùng nguồn nội dung của sổ. Giữ tên tệp “Phong_cach_ZO_Math.md” ổn định.

**Mỗi lần tạo sản phẩm:** chọn nguồn nội dung phù hợp và nguồn phong cách khi giao diện cho phép; dùng mẫu dưới trong phần chỉ dẫn tùy chỉnh tương ứng. Chỉ điền loại sản phẩm; nội dung theo các nguồn và yêu cầu đã có trong sổ. Nếu có ô riêng cho phong cách hình ảnh, sao chép các yêu cầu liên quan ở mục 1 vào ô đó.

```text
Tạo [loại sản phẩm] từ các nguồn nội dung đã chọn và yêu cầu đã có trong sổ.
Không tự đề xuất thêm chủ đề, ví dụ hoặc nội dung sản xuất ngoài yêu cầu của người dùng.
Áp dụng “Phong cách ZO Math”, phiên bản 0.6 trong Nguồn, gồm quy định chung và phần dành cho loại sản phẩm này.
Dùng tài liệu phong cách để định hướng trình bày; không đưa nội dung quy chuẩn vào bài học.
```

**Khi muốn thay đổi:** sửa mục 1, 2, 3 hoặc dòng liên quan trong mục 4. Cập nhật số phiên bản và câu dẫn phiên bản trong mẫu lệnh. Bạn cũng có thể mô tả điều muốn đổi cho người hỗ trợ biên tập, không cần tự viết quy định thiết kế.

**Khi đã sửa bản gốc:** cập nhật hoặc thay bản nguồn cũ trong từng sổ đang sử dụng; kiểm tra chỉ còn bản muốn dùng. Không mặc định các sổ tự đồng bộ. Sản phẩm đã tạo cần được kiểm tra và tạo lại nếu muốn áp dụng thay đổi.

**Sau mỗi lần tạo:** xem ba điều: đúng kiến thức; dễ tiếp thu; có giữ diện mạo và cách diễn đạt ZO Math không. Nếu một yêu cầu bị bỏ qua, nhắc cụ thể yêu cầu ấy trong lần tạo tiếp theo. Việc thêm tệp vào Nguồn không bảo đảm công cụ tuân thủ từng chi tiết.

Nội dung sản xuất do người dùng và các tệp nội dung trong sổ xác định. Tài liệu phong cách chỉ quy định cách trình bày; không tự đặt chủ đề, ví dụ hoặc kịch bản sản xuất.

Riêng phụ đề: dùng văn bản thuần và Unicode, kể cả các số đứng riêng; tuyệt đối không có dấu đô-la hoặc mã LaTeX. Ví dụ phải hiển thị: “1 đến 3 không?”.
