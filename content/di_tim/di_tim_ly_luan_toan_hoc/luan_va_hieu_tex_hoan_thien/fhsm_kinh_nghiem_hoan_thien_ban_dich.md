# Kinh nghiệm làm việc sau khi hiệu chỉnh FHSM

## 1. Nguyên tắc tổng quát

Khi làm việc với bản dịch FHSM hoặc dự án tương tự, xem bản tiếng Việt là văn bản chính cần hoàn thiện. Bản gốc tiếng Anh dùng để đối chiếu nghĩa, thuật ngữ, cấu trúc lập luận và xác định thứ tự đoạn/mục.

Mục tiêu không phải dịch lại từ đầu, mà là hiệu chỉnh bản dịch hiện có sao cho chính xác, tự nhiên, nhất quán, bám tinh thần gốc và dùng được lâu dài.

Chỉ sửa khi có lí do thực chất: sai nghĩa, lệch thuật ngữ, chưa sát bản gốc, gượng tiếng Việt, sai ngữ pháp, không nhất quán chính tả i/y, sai quy ước viết số, sai quy ước tên riêng/thư mục, hoặc có thể lược “một/các/những/của” mà câu vẫn tự nhiên.

Không thay từ gần nghĩa hoặc diễn đạt gần tương đương chỉ để tạo cảm giác có chỉnh sửa. Nếu bản dịch đã ổn, nói rõ: **Giữ nguyên**.

Sau khi đối chiếu bản gốc, luôn đọc lại bản Việt như văn bản tiếng Việt độc lập. Nếu câu gượng, phải sửa cho tự nhiên mà vẫn giữ đúng ý.

Ưu tiên một phương án tốt nhất, không liệt kê nhiều phương án phụ.

## 2. Quy trình làm việc với tệp `.tex`

Khi người dùng gửi tệp `.tex`, không tự tạo lại hoặc gửi lại toàn bộ tệp, trừ khi được yêu cầu rõ. Làm lần lượt từng đoạn/mục theo đúng thứ tự trong tệp.

Với các chương hoặc đoạn dài, phản hồi theo giao thức:

1. Độ trung thành với tinh thần bản gốc.
2. Mức độ nhất quán thuật ngữ.
3. Đề xuất hiệu chỉnh kèm lí do.
4. Khuyến nghị giữ/sửa/rút gọn/bỏ `\NOTE{...}` nếu cần.

Khi người dùng yêu cầu chỉ rõ lỗi, đưa danh sách hiệu chỉnh trong cửa sổ TeX theo dạng “Tìm / Thay bằng” thay vì viết lại toàn khối.

Khi các mục ngắn như `thu_muc_chu_thich.tex`, có thể phản hồi bằng bản chỉnh sửa cả cụm, nhưng vẫn nêu rõ lí do sửa.

Giữ nguyên số câu trong mỗi đoạn `\VI{...}`, trừ khi người dùng cho phép thay đổi.

Không làm đổi ý bản gốc, không làm mất từ khóa chính, không tự thêm ý vào bản dịch chính.

Nếu bản gốc nói tắt, có lỗi hoặc chưa tự đứng vững, không lén sửa trong bản dịch chính; nếu cần thì giải thích riêng trong `\NOTE{...}`.

## 3. Quy tắc viết `\NOTE{...}`

`\NOTE{...}` phải đi thẳng vào ý cần làm rõ, trung tính, học thuật, tự nhiên.

Tránh mở đầu kiểu:

- “Đoạn này…”
- “Câu này…”
- “Tác giả muốn…”

Không biến `NOTE` thành checklist nếu không cần.

Khi sửa `\NOTE{...}`, ưu tiên tinh gọn, sắc, bỏ lặp, không thêm bình luận quá dài hoặc nhận xét không có cơ sở từ bản gốc.

Nếu bản dịch chính đã đủ rõ, không thêm `NOTE` chỉ để giải thích thêm.

## 4. Quy tắc riêng cho thư mục chú giải

`Annotated Bibliography` chốt là **Thư mục chú giải**, không dùng **Thư mục chú thích**.

Lí do: đây là danh mục tài liệu kèm chú giải, tóm lược hoặc bình giải ngắn cho từng tài liệu, không phải chú thích phụ cho một chi tiết văn bản.

Với thư mục chú giải, cần giữ chính xác:

- tên tác giả;
- năm xuất bản;
- nhan đề tài liệu;
- tên tổ chức;
- tên sách;
- tên tạp chí;
- số tập;
- số kì;
- số trang;
- nơi xuất bản;
- nhà xuất bản.

Không Việt hóa tên riêng hoặc nhan đề tiếng Anh, trừ khi bản dịch có chủ đích rõ.

Nếu nghi ngờ lỗi chế bản/OCR trong tên riêng, năm, số trang, nhan đề hoặc kí hiệu, phải nêu nghi vấn rõ thay vì tự sửa lặng lẽ.

Giữ trích dẫn tác giả-năm với “and”, không đổi thành “và” trong ngoặc hoặc thông tin thư mục.

## 5. Thuật ngữ FHSM đã chốt

- reasoning = luận
- sense making = hiểu
- reasoning and sense making = luận và hiểu
- mathematical reasoning = luận toán học
- reasoning habits = thói quen luận
- formal deduction = suy diễn hình thức
- deductive reasoning = luận suy diễn, nếu đang nói về năng lực/mạch luận
- logical deductions = suy diễn logic
- inductive observations = những quan sát mang tính quy nạp
- procedures = thủ tục
- process = quá trình
- focus = trọng tâm
- key element = yếu tố then chốt
- formative assessment = đánh giá quá trình
- summative assessment = đánh giá tổng kết
- validating a solution = thẩm định lời giải
- statistical inference = suy luận thống kê
- inferential statistics = thống kê suy luận
- statistical reasoning = luận thống kê
- random assignment = phân bổ ngẫu nhiên
- random selection = chọn ngẫu nhiên
- population = tổng thể
- sample = mẫu
- sampling distribution = phân phối lấy mẫu
- probability distribution = phân phối xác suất
- data distribution = phân bố dữ liệu
- random variable = biến ngẫu nhiên
- mathematical modeling = mô hình hóa toán học
- mathematical model = mô hình toán học

## 6. Khung Adding It Up

Giữ tên thành tố như sau:

- conceptual understanding = Hiểu khái niệm
- procedural fluency = Thành thạo thủ tục
- strategic competence = Năng lực chiến lược
- adaptive reasoning = Suy luận thích ứng
- productive disposition = Khuynh hướng tích cực

Trong ngữ cảnh này, không đổi `adaptive reasoning` thành “luận thích ứng”, vì đây là tên thành tố đã quen dùng trong khung Adding It Up.

## 7. Một số thuật ngữ và quy ước khác

- Communication = Giao tiếp
- Reasoning and Proof = Luận và chứng minh
- NCTM = Hội đồng Quốc gia Giáo viên Toán học Hoa Kì (NCTM)
- Progression of Reasoning = Tiến trình phát triển của luận
- reasoned connections = kết nối có cơ sở luận
- stance trong “a stance toward learning mathematics” = lập trường
- addressed trong nội dung/chương trình học = xử lí
- alignment = sự liên kết
- coherent/coherence = nhất quán / tính nhất quán
- number sense = cảm thức số
- order of magnitude = bậc độ lớn
- radicals = căn thức
- mindless manipulation = biến đổi máy móc
- mindful manipulation = biến đổi có ý thức
- meaningful use of symbols = sử dụng kí hiệu có nghĩa
- basis for reasoning = cơ sở cho luận
- graphically trong ngữ cảnh dùng đồ thị = bằng đồ thị
- fixed point = điểm bất động
- transition function = hàm chuyển tiếp
- sinusoidal function = hàm số hình sin
- graph theory = lí thuyết đồ thị
- discrete mathematics = toán học rời rạc
- vertex-edge graph = đồ thị đỉnh-cạnh
- algorithm = thuật toán
- tracking/track trong phân nhóm học sinh = phân luồng/luồng
- multiple entry points = nhiều điểm vào
- English Language Learners (ELLs) = học sinh học tiếng Anh (English Language Learners, ELLs); sau đó dùng học sinh ELL
- Hispanic giữ là Hispanic trong ngữ cảnh nhân khẩu học Hoa Kì
- students of color = học sinh da màu

## 8. Phân biệt một số cặp dễ lẫn

`sense making` và `understanding` không hoàn toàn đồng nghĩa.

`sense making` nhấn mạnh quá trình làm cho tình huống, bối cảnh hoặc khái niệm trở nên rõ nghĩa bằng cách kết nối điều ấy với tri thức đã có.

`understanding` dịch linh hoạt là “sự hiểu”, “nền hiểu”, “hiểu biết” hoặc “hiểu” tùy ngữ cảnh, không tự động đồng nhất với thuật ngữ `sense making`.

`argument` ưu tiên dịch là **biện giải** khi cần phân biệt với `reasoning = luận`. Không nhập nhằng `argument` với “lập luận” nếu làm mất hệ thuật ngữ FHSM.

`proof` là **chứng minh**. `formal proof` = **chứng minh hình thức**. Không đổi `proof` thành “biện giải” khi bản gốc nói trực tiếp về hoạt động chứng minh.

`habits of mind` trong các tài liệu Cuoco/Goldenberg/Mark nên là **thói quen tư duy**, không ép thành **thói quen luận**.

`course taking/coursetaking` trong ngữ cảnh dữ liệu giáo dục nên dịch theo hướng **việc học / theo học / ghi danh vào các môn học**, không máy móc thành “lựa chọn môn học”.

`whole numbers` nên dịch là **số nguyên không âm** khi cần tránh nhầm với `integers` / số nguyên.

Trong dữ liệu thống kê, `distribution` của dữ liệu nên là **phân bố**, còn `distribution` trong xác suất hoặc lấy mẫu theo thuật ngữ đã chốt là **phân phối**.

`center and spread` = **trung tâm và độ phân tán**.

## 9. Quy ước về từ ngữ tiếng Việt

Dùng **Hoa Kì**, không dùng **Hoa Kỳ**.

Dùng “toán” chữ thường khi không cần viết hoa.

`areas` dịch là **phương diện** khi chỉ hướng/khía cạnh chuẩn bị lớn; dịch là **mảng** khi chỉ phần nội dung hẹp trong chương trình hoặc chương tổng quan.

`content area` = **mảng nội dung**.

`section 2` hoặc tham chiếu tương đương trong ngữ cảnh Part 2 của FHSM là **Phần 2**, không phải “mục 2”.

## 10. Quy ước chính tả i/y

Ưu tiên dùng “i” sau phụ âm đầu khi âm tiết không có âm đệm và âm cuối:

- hi vọng
- kì vọng
- kỉ niệm
- kĩ năng
- kĩ thuật
- lí do
- lí luận
- lí thuyết
- hợp lí
- xử lí
- quản lí
- vật lí
- địa lí
- bác sĩ
- kĩ sư
- tỉ lệ
- chu kì

Giữ “y” khi đứng đầu âm tiết hoặc trong vần/tổ hợp “uy”:

- ý nghĩa
- yêu cầu
- yếu tố
- quy trình
- quy định
- quy ước
- suy nghĩ
- tùy chọn
- hủy bỏ
- duy trì
- khuyến nghị

Tên riêng giữ nguyên cách viết chính thức.

## 11. Quy ước viết số

Nếu con số thuộc danh từ/thuật ngữ hoặc nằm trong văn bản thông thường để cung cấp thông tin thì viết số thường, không bọc LaTeX.

Ví dụ:

- Ví dụ 14
- Chương 7
- 3 thập kỉ
- ba kết quả

Nếu con số tham gia phép tính, quan hệ toán học, biểu thức, so sánh, hoặc đang được xét như đối tượng toán học thì bọc bằng LaTeX.

Ví dụ:

- `$360$ không chia hết cho $80$`
- `$360 \div 2 = 180$`

## 12. Quy ước về đơn vị đo kiểu Mỹ/Anh

Khi bản gốc dùng đơn vị đo kiểu Mỹ/Anh như `mile`, `foot`, `inch`, `pound`, `gallon`, không dịch đơn vị sang tiếng Việt trong bản dịch chính.

Giữ nguyên tên đơn vị theo bản gốc và thêm ghi chú chân trang ở lần xuất hiện đầu tiên nếu cần.

## 13. Tinh thần phản hồi khi hiệu chỉnh

Trong mọi phản hồi hiệu chỉnh, cần tập trung vào chỗ thật sự cần sửa: lỗi ở đâu, sửa gì, vì sao sửa.

Tránh phân tích dài khi người dùng chỉ cần chốt trực tiếp chỗ sửa.

Không đưa nhiều lựa chọn phụ. Chỉ đưa phương án tốt nhất, phù hợp nhất với hệ thuật ngữ và tinh thần bản dịch đã chốt.
