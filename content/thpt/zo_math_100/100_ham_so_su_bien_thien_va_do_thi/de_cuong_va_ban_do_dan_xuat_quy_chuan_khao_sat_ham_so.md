# Đề cương và bản đồ dẫn xuất `quy_chuan_khao_sat_ham_so.md`

## 1. Trạng thái và mục đích

Tài liệu này là bản thiết kế để dẫn xuất một quy chuẩn vận hành dành cho AI từ bản nguồn lí thuyết:

`khung_khao_sat_ham_so_hoan_chinh_04.qmd`

Bản `_04` được chốt làm **bản nguồn lí thuyết chính thức** cho lần dẫn xuất này. Nội dung của bản ấy không được sửa trong quá trình viết quy chuẩn. Nếu về sau phát hiện một vấn đề thuộc chính khung lí thuyết, cần tạo một phiên bản nguồn mới và ghi rõ thay đổi; không sửa âm thầm `_04`.

Dấu nhận diện của bản nguồn đã chốt:

```text
SHA-256: c9a6ff3040a38658c9e55068395672da1fdb04d58bdd21c4ec027b85ac0d48aa
Kích thước: 698028 byte
Cấu trúc: 6 phần, 21 chương, 212 kết quả được đánh số
```

Sản phẩm sẽ được viết ở bước sau:

`quy_chuan_khao_sat_ham_so.md`

Quy chuẩn tương lai phải giúp AI nhận một hàm số hoặc họ hàm cùng phạm vi nhiệm vụ, rồi tạo ra bài khảo sát `.qmd` đúng về toán học, có mạch giải thích và có thể nghiệm thu. Nó không phải bản tóm tắt tuần tự của 21 chương và không thay thế bản nguồn lí thuyết.

## 2. Quan hệ giữa ba tài liệu

| Tài liệu | Thẩm quyền trực tiếp | Không phụ trách |
|---|---|---|
| `khung_khao_sat_ham_so_hoan_chinh_04.qmd` | Nền tảng toán học; quan niệm về khảo sát; lựa chọn, tổ chức và kiểm định nội dung | Chỉ dẫn kỹ thuật chi tiết để sinh mã đồ thị; quy định một phong cách viết cụ thể |
| `quy_chuan_do_thi_sinh_ma_nguon_tikz_pgfplots.md` | Phân tích và sinh tệp `.tex`; miền quan sát; lấy mẫu; hệ trục; phong cách thị giác; chuỗi render và nghiệm thu hình | Kiến trúc toàn bài khảo sát |
| `hoc_thuat_tinh_tai.md` | Giọng, nhịp, ngôn ngữ, tổ chức văn xuôi và kiểm định phong cách khi người dùng chỉ định **Học thuật tĩnh tại** | Nội dung toán học bắt buộc của mọi bài; phong cách mặc định cho toàn bộ ZO Math |

`quy_chuan_khao_sat_ham_so.md` phải đứng ở giữa ba lớp trên:

- lấy nền tảng toán học và quy trình kiến tạo bài từ bản `_04`;
- giao phần sinh mã và nghiệm thu hình sang quy chuẩn TikZ/PGFPlots;
- chỉ kích hoạt Học thuật tĩnh tại khi nhiệm vụ gọi đúng phong cách này.

Quy chuẩn khảo sát có thể quy định **hình cần làm công việc gì** và **mệnh đề nào hình phải biểu diễn**, nhưng không chép lại thông số màu, nét, trục, lấy mẫu hay cấu trúc tệp `.tex`.

## 3. Nguyên tắc dẫn xuất

### 3.1. Chuyển lí thuyết thành hành động

Mỗi nội dung đưa từ `_04` sang quy chuẩn phải được chuyển thành ít nhất một trong các dạng sau:

- dữ liệu đầu vào cần xác định;
- câu hỏi AI phải trả lời;
- thao tác AI phải thực hiện;
- điều kiện kích hoạt một phương diện;
- sản phẩm trung gian phải tạo;
- tiêu chí kiểm định;
- điều kiện dừng;
- điểm phải chuyển giao sang quy chuẩn khác.

Không chép các định nghĩa, định lí, ví dụ và chứng minh dài nếu chúng không trực tiếp thay đổi hành động của AI.

### 3.2. Giữ khả năng truy nguyên

Mỗi nhóm quy tắc trong tài liệu tương lai phải truy được về một chương hoặc mục của `_04`. Không nhất thiết chèn dẫn chiếu vào từng câu, nhưng cấu trúc quy chuẩn phải tương ứng với bảng ánh xạ tại Mục 9 của tài liệu này.

### 3.3. Không biến khung thành thủ tục máy móc

Quy chuẩn phải giữ nguyên nguyên tắc trung tâm của `_04`:

> Không có một danh sách hữu hạn các phép tính bắt buộc cho mọi hàm số.

Vì vậy, quy trình chỉ bắt buộc AI:

1. rà các phương diện nền tảng để bảo vệ tính đúng đắn;
2. kích hoạt các phương diện khác theo cấu trúc của hàm và câu hỏi dẫn đường;
3. chọn nội dung theo chức năng;
4. chứng minh đúng mức;
5. tổ chức kết quả thành một cách hiểu thống nhất.

Quy trình không bắt buộc mọi bài phải có đạo hàm, bảng biến thiên, tiệm cận, độ cong, ứng dụng hoặc phần mở rộng.

### 3.4. Phân biệt ba mức quy tắc

Quy chuẩn tương lai dùng ba mức sau:

| Mức | Ý nghĩa |
|---|---|
| **Bắt buộc** | Luôn phải thực hiện hoặc phải xác nhận rõ là không áp dụng |
| **Kích hoạt khi thích hợp** | Chỉ thực hiện khi hàm số, phạm vi hoặc câu hỏi dẫn đường tạo ra nhu cầu |
| **Chuyển giao** | Quy chuẩn khảo sát xác định yêu cầu chức năng rồi giao việc triển khai chi tiết sang một quy chuẩn chuyên biệt |

Ba mức này phải hiện rõ trong cách viết; không để AI hiểu một kho phương diện là một danh sách đề mục bắt buộc.

## 4. Đầu vào của quy chuẩn tương lai

Quy chuẩn phải yêu cầu AI xác lập một **đơn vị khảo sát** gồm:

| Trường đầu vào | Nội dung |
|---|---|
| Đối tượng | Hàm số, họ hàm, quan hệ hoặc quy tắc đang xét |
| Phạm vi | Tập xác định tự nhiên hoặc miền hạn chế; phạm vi địa phương hay toàn cục |
| Tham số | Tham số tự do, miền tham số và trường hợp suy biến nếu có |
| Người đọc | Nền tảng toán học dự kiến và những khái niệm cần được xây cầu nối |
| Mục tiêu | Bài khảo sát đầy đủ trong phạm vi nào, hay tập trung vào hiện tượng nào |
| Đầu ra | Tệp `.qmd`, các bảng, hình và tệp nguồn phụ trợ cần bàn giao |
| Phong cách | Phong cách được người dùng chỉ định; không tự mặc định Học thuật tĩnh tại |
| Ràng buộc dự án | Quy ước cục bộ, tệp mẫu, đường dẫn, metadata và yêu cầu render |

Khi thiếu thông tin, AI tự suy ra những chi tiết không làm thay đổi bản chất nhiệm vụ. AI chỉ hỏi lại khi nhiều cách hiểu hợp lí dẫn đến các đơn vị khảo sát khác nhau rõ rệt, chẳng hạn khác miền, khác đối tượng hoặc khác hiện tượng trung tâm.

## 5. Chuỗi sản phẩm

Quy chuẩn phải phân biệt bốn sản phẩm, thay vì đi thẳng từ công thức đến bài viết.

### 5.1. Hồ sơ khảo sát

Hồ sơ khảo sát là kho làm việc rộng, gồm:

- đối tượng, miền và quy ước;
- các mệnh đề đã xác lập;
- chứng cứ và điều kiện áp dụng;
- dự đoán chưa xác lập;
- ngoại lệ và trường hợp biên;
- kết quả biểu tượng và số;
- yêu cầu đối với bảng và hình;
- hồ sơ kiểm định biểu diễn.

Hồ sơ có thể chứa nhiều nội dung hơn bài cuối cùng.

### 5.2. Bản đồ hiện tượng

Bản đồ hiện tượng phải nối:

| Thành phần | Câu hỏi |
|---|---|
| Hiện tượng | Điều gì cần được hiểu? |
| Cơ chế | Cấu trúc nào tạo ra điều ấy? |
| Dấu hiệu | Hiện tượng biểu hiện ở đâu? |
| Chứng cứ | Dựa vào đâu để xác lập quan hệ? |
| Biểu diễn | Quan hệ được làm hiện rõ bằng cách nào? |

Hiện tượng trung tâm ban đầu chỉ là một giả thuyết tổ chức. AI phải sửa hoặc thay nó nếu hồ sơ khảo sát không nâng đỡ được.

### 5.3. Đề cương vận hành

Đề cương vận hành là sản phẩm trung gian bắt buộc trước khi viết văn xuôi. Mẫu tối thiểu:

| Thành phần | Nội dung phải ghi |
|---|---|
| Đối tượng và phạm vi | Hàm, miền, tham số và người đọc |
| Hiện tượng trung tâm | Hành vi cần được giải thích |
| Câu hỏi dẫn đường | Câu hỏi bài phải trả lời |
| Câu trả lời dự kiến | Kết luận trung tâm sau khi đã kiểm tra |
| Bản đồ hiện tượng | Cơ chế, dấu hiệu, chứng cứ và biểu diễn |
| Các mạch lập luận | Vấn đề, tiền đề, chứng cứ, kết luận, giải nghĩa và điểm nối |
| Mạng phụ thuộc | Mạch nào cần mạch nào |
| Trật tự nhận thức | Thứ tự dự kiến và lí do |
| Mức hiển thị | Mạch chính, mở rộng, biểu diễn hoặc ngoài bài |
| Điểm kết tinh | Bảng, hình hoặc quan hệ tổng hợp |
| Điều kiện dừng | Tiêu chí phải đạt trước khi nghiệm thu |

### 5.4. Bài khảo sát và hồ sơ nghiệm thu

Đầu ra cuối gồm:

- bài khảo sát `.qmd`;
- các bảng và hình được bài sử dụng;
- tệp nguồn của hình nếu nhiệm vụ yêu cầu;
- kết quả của ba lượt kiểm định;
- danh sách tiêu chí *không áp dụng* kèm lí do;
- những giới hạn hoặc hướng mở rộng còn lại.

## 6. Quy trình vận hành sẽ đưa vào quy chuẩn

### Bước 1. Xác lập đúng đối tượng

- Ghi hàm, tập xác định, tập đích khi cần và tập giá trị chưa biết.
- Phân biệt hàm số với biểu thức.
- Kiểm tra định nghĩa từng phần, quan hệ, thuật toán và miền tham số.
- Xác định phạm vi địa phương hoặc toàn cục của bài.

### Bước 2. Đọc cấu trúc của miền

- Phân tích các thành phần liên thông, đầu mút, điểm biên, điểm bị loại, điểm cô lập và điểm tụ có liên quan.
- Lập bản đồ các cách tiếp cận được phép từ trong miền.
- Không dùng ngôn ngữ khoảng một cách máy móc cho miền tổng quát.

### Bước 3. Lập hồ sơ khảo sát

Rà hai vòng:

**Vòng nền tảng**

- đối tượng và tập xác định;
- cấu trúc của miền;
- tập giá trị hoặc các mức quan trọng;
- nghiệm, dấu và giao trục;
- hành vi tại biên miền;
- liên tục hoặc gián đoạn;
- biến thiên và các điểm đặc biệt;
- ràng buộc cần để dựng hoặc đọc đồ thị.

**Vòng kích hoạt**

- đối xứng hoặc tuần hoàn;
- hợp hàm, hàm ngược hoặc phép biến đổi;
- tham số và các chế độ;
- tiệm cận và tốc độ tăng trưởng;
- dãy điểm đặc biệt;
- dao động, hàm bao và tập giá trị tụ;
- tính toán số hoặc nhiều cửa sổ;
- phép soi chiếu;
- ứng dụng và mô hình hóa;
- liên hệ toán học mở rộng.

“Rà” không đồng nghĩa với “đưa thành đề mục”. Kết quả không phục vụ tính đúng đắn hoặc câu hỏi dẫn đường được giữ trong hồ sơ hoặc để ngoài bài.

### Bước 4. Xác lập mệnh đề và chứng cứ

Với mỗi kết luận dự kiến:

1. phát biểu đúng đối tượng, miền và lượng từ;
2. phân biệt dự đoán với kết quả đã xác lập;
3. ghi giả thiết và công cụ;
4. kiểm tra điều kiện áp dụng;
5. xác định chứng cứ quyết định;
6. kiểm tra tồn tại, duy nhất và tính đầy đủ khi có liên quan;
7. tìm phản ví dụ hoặc trường hợp biên có thể bác bỏ kết luận mạnh hơn;
8. đối chiếu kết luận với công thức, bảng, số và hình.

Hình vẽ và dữ liệu hữu hạn chỉ là chứng cứ hỗ trợ, trừ khi nhiệm vụ chỉ yêu cầu một kết luận số với mức bảo đảm đã công bố.

### Bước 5. Chọn hiện tượng trung tâm

Hiện tượng trung tâm phải:

- thật sự xảy ra trong phạm vi bài;
- có chứng cứ đủ để giải thích;
- kết nối được nhiều dữ kiện quan trọng;
- làm thay đổi hoặc làm sâu cách đọc hàm số.

Từ hiện tượng ấy, viết một câu hỏi dẫn đường cụ thể. Câu hỏi không được chứa sẵn một kết luận chưa được kiểm tra.

### Bước 6. Lập bản đồ hiện tượng

Nối hiện tượng với cơ chế, dấu hiệu, chứng cứ và biểu diễn. Kiểm tra từng đường nối:

- có dấu hiệu nhưng thiếu cơ chế: mới mô tả;
- có cơ chế nhưng thiếu chứng cứ: mới phỏng đoán;
- có chứng cứ nhưng thiếu giải nghĩa: mới tính toán;
- có hình nhưng không truy về mệnh đề: mới minh họa bề mặt;
- có nhiều kết quả nhưng không quay lại hiện tượng: mới tích lũy dữ liệu.

### Bước 7. Chọn nội dung theo chức năng

Gán cho mỗi dữ kiện một vai trò chính:

- định hướng;
- thiết lập;
- chứng minh;
- giải thích;
- tổng hợp;
- soi chiếu;
- mở rộng.

Một kết quả chỉ thuộc mạch chính khi có đường nối rõ tới câu trả lời trung tâm: xác lập hiện tượng, giải thích cơ chế, cung cấp tiền đề bắt buộc, kiểm soát cách hiểu sai hoặc kết tinh quan hệ trên biểu diễn.

### Bước 8. Tạo các mạch lập luận

Mỗi mạch phải thực hiện sáu chức năng:

1. nêu vấn đề cục bộ;
2. đưa ra tiền đề;
3. cung cấp chứng cứ;
4. phát biểu kết luận đúng phạm vi;
5. giải nghĩa kết luận đối với hàm số;
6. nối về câu hỏi trung tâm hoặc mạch tiếp theo.

Không gom bài theo tên phép tính nếu các phép tính phục vụ những hiện tượng khác nhau.

### Bước 9. Xây mạng phụ thuộc và trật tự nhận thức

- Tiền đề, định nghĩa, kí hiệu và điều kiện phải đứng trước nơi sử dụng.
- Không dùng hình làm chứng minh cho chính những mệnh đề đã dùng để dựng hình.
- Phá mọi vòng tròn phụ thuộc bằng chứng cứ độc lập hoặc bằng cách sửa phạm vi.
- Trong các thứ tự hợp logic, chọn thứ tự giúp người đọc nhận ra vấn đề, hình thành dự đoán, kiểm tra, sửa trực giác và kết tinh kết quả.

### Bước 10. Quyết định mức hiển thị

Mỗi nội dung thuộc một trong bốn mức:

1. mạch chính;
2. khối mở rộng;
3. bảng, hình hoặc chú thích;
4. ngoài bài.

Không giấu mắt xích bắt buộc trong khối tùy chọn. Không dùng hình thức hiển thị để làm kết luận mạnh hơn chứng cứ.

### Bước 11. Xác định kiến trúc bài

Bài phải thực hiện các chức năng:

- khơi mở;
- nhận diện;
- triển khai;
- kết tinh;
- soi chiếu khi thích hợp;
- khép lại.

Đây là các chức năng, không phải sáu tiêu đề bắt buộc. Tiêu đề và đề mục phải phát sinh từ mạch nhận thức của chính hàm số.

### Bước 12. Đặc tả bảng và hình

Trước mỗi bảng hoặc hình, ghi:

- mệnh đề hoặc quan hệ cần biểu diễn;
- chức năng đối với mạch bài;
- miền và phạm vi đọc;
- chi tiết bắt buộc;
- chi tiết có thể lược;
- giới hạn của biểu diễn;
- yêu cầu đọc ngược sau biểu diễn.

Nếu cần sinh đồ thị TikZ/PGFPlots, chuyển đặc tả này sang `quy_chuan_do_thi_sinh_ma_nguon_tikz_pgfplots.md`. Quy chuẩn khảo sát không tự đặt lại các thông số kỹ thuật của hình.

### Bước 13. Viết bài `.qmd`

- Viết từ đề cương vận hành đã kiểm tra.
- Giữ nhất quán công thức, miền, kí hiệu, thuật ngữ, tham số và quy ước.
- Phân biệt quan sát, dự đoán, kết luận đã chứng minh và phần còn mở.
- Sau mỗi kết quả quan trọng, làm rõ vai trò của nó đối với hiện tượng hoặc hình dạng.
- Sau bảng và hình, đọc ngược về những mệnh đề đã tạo nên biểu diễn.
- Chỉ áp dụng tài liệu `hoc_thuat_tinh_tai.md` khi phong cách ấy được chỉ định.

### Bước 14. Thực hiện ba lượt kiểm định

**Kiểm định toán học**

- đúng đối tượng và miền;
- đúng điều kiện và phạm vi;
- không vượt quá chứng cứ;
- xử lí trường hợp biên;
- không mâu thuẫn giữa công thức, bảng, hình và văn xuôi;
- kết quả số có đúng mức bảo đảm.

**Kiểm định mạch giải thích**

- câu hỏi dẫn đường điều khiển việc chọn nội dung;
- mỗi mạch đủ vấn đề, chứng cứ, kết luận, giải nghĩa và điểm nối;
- quan hệ phụ thuộc được tôn trọng;
- bảng và hình tổng hợp kết quả đã xác lập;
- kết luận trả lời câu hỏi mở đầu.

**Kiểm định giá trị nhận thức**

- hiện tượng trung tâm đủ đặc trưng;
- khái niệm mới xuất hiện đúng lúc;
- chi tiết kỹ thuật không che cơ chế;
- phần mở rộng không cắt mạch chính;
- bài tạo ra một cách hiểu, không chỉ hoàn thành thủ tục.

Mỗi tiêu chí chỉ được xác nhận khi chỉ ra được căn cứ cụ thể trong bài, bảng hoặc hình. Tiêu chí không liên quan phải ghi *không áp dụng* kèm lí do.

### Bước 15. Kiểm tra điều kiện dừng và bàn giao

Chỉ bàn giao khi:

1. câu hỏi dẫn đường đã được giải quyết trong phạm vi công bố;
2. mọi kết luận thiết yếu có chứng cứ;
3. không còn ngoại lệ làm đổi kết luận;
4. các mạch tạo thành một con đường liên tục;
5. mỗi thành phần có chức năng;
6. biểu diễn không vượt quá chứng cứ;
7. người đọc dự kiến không phải tự bổ sung mắt xích quan trọng;
8. phần còn mở được gọi đúng là mở rộng.

Bài cuối phải có thể được nén thành chuỗi:

> hiện tượng → cơ chế → chứng cứ → hình dạng → nhận thức.

## 7. Cấu trúc dự kiến của `quy_chuan_khao_sat_ham_so.md`

### 1. Mục đích, phạm vi và thẩm quyền

- Đối tượng sử dụng.
- Loại nhiệm vụ được điều chỉnh.
- Thứ tự ưu tiên giữa yêu cầu người dùng, quy ước dự án và các quy chuẩn.
- Quan hệ với bản `_04`, quy chuẩn đồ thị và hệ thống phong cách.

### 2. Nhiệm vụ của AI và chuỗi sản phẩm

- Hồ sơ khảo sát.
- Bản đồ hiện tượng.
- Đề cương vận hành.
- Bài `.qmd` và hồ sơ nghiệm thu.

### 3. Đầu vào và cách xử lí thông tin thiếu

- Mẫu đơn vị khảo sát.
- Điều AI được tự quyết.
- Điều kiện phải hỏi lại.

### 4. Nguyên tắc vận hành bất biến

- Không khảo sát bằng danh sách máy móc.
- Miền là một phần của đối tượng.
- Hình không thay chứng minh.
- Nội dung được chọn theo chức năng.
- Mức hiển thị không thay mức chứng cứ.

### 5. Lập hồ sơ khảo sát

- Vòng rà nền tảng.
- Vòng kích hoạt.
- Mệnh đề, chứng cứ, ngoại lệ và trường hợp biên.
- Kết quả biểu tượng, số và biểu diễn.

### 6. Hiện tượng trung tâm và bản đồ hiện tượng

- Tiêu chuẩn chọn.
- Câu hỏi dẫn đường.
- Năm thành phần của bản đồ.
- Điều kiện sửa hoặc thay hiện tượng.

### 7. Lựa chọn nội dung

- Vai trò của dữ kiện.
- Tiêu chuẩn đưa vào mạch chính.
- Ứng dụng và mô hình hóa.
- Liên hệ toán học mở rộng.

### 8. Tạo mạch lập luận và mạng phụ thuộc

- Cấu trúc một mạch.
- Chứng cứ quyết định và hỗ trợ.
- Trật tự logic và trật tự nhận thức.
- Phá vòng tròn phụ thuộc.

### 9. Kiến trúc và mức hiển thị của bài

- Sáu chức năng của kiến trúc.
- Bốn mức hiển thị.
- Kiểm soát độ dài và độ sâu.
- Quy tắc tách một nhánh thành bài độc lập.

### 10. Bảng, đồ thị và tính toán số

- Đặc tả chức năng.
- Giới hạn của dữ liệu hữu hạn.
- Cửa sổ, thang đo và nhiều hình phối hợp.
- Điểm chuyển giao sang quy chuẩn TikZ/PGFPlots.

### 11. Viết và hoàn thiện tệp `.qmd`

- Quy tắc triển khai từ đề cương.
- Tính nhất quán.
- Phân biệt mức độ khẳng định.
- Quan hệ với phong cách được chỉ định.

### 12. Ba lượt kiểm định

- Toán học.
- Mạch giải thích.
- Giá trị nhận thức.
- Giao thức ghi căn cứ và *không áp dụng*.

### 13. Điều kiện dừng và bàn giao

- Danh sách điều kiện dừng.
- Thành phần đầu ra.
- Báo cáo giới hạn và hướng mở.

### Phụ lục A. Mẫu đầu vào

Một biểu mẫu ngắn để xác lập đơn vị khảo sát.

### Phụ lục B. Mẫu hồ sơ khảo sát

Một bảng mệnh đề–chứng cứ–phạm vi–trạng thái.

### Phụ lục C. Mẫu bản đồ hiện tượng

Một bảng hiện tượng–cơ chế–dấu hiệu–chứng cứ–biểu diễn.

### Phụ lục D. Mẫu đề cương vận hành

Mẫu tối thiểu tại Mục 5.3 của tài liệu này.

### Phụ lục E. Phiếu nghiệm thu

Ba nhóm tiêu chí và nơi ghi căn cứ cụ thể.

## 8. Những nội dung không đưa nguyên dạng vào quy chuẩn

| Nội dung trong `_04` | Cách xử lí |
|---|---|
| Các chứng minh nền tảng dài | Giữ ở bản nguồn; chỉ dẫn xuất điều kiện sử dụng |
| Chuỗi ví dụ phát triển qua nhiều chương | Chỉ chọn ví dụ tối thiểu nếu cần làm rõ thao tác |
| Toàn bộ hệ định nghĩa và mệnh đề được đánh số | Không chép lại; chuyển thành câu hỏi, điều kiện và kiểm định |
| Chi tiết màu, nét, trục, font và mã TikZ/PGFPlots | Chuyển giao hoàn toàn sang quy chuẩn đồ thị |
| Quy tắc giọng, nhịp và thẩm mỹ của Học thuật tĩnh tại | Chỉ viện dẫn khi phong cách được kích hoạt |
| Mục lục truyền thống của một bài khảo sát | Không tạo; kiến trúc phải phát sinh từ hiện tượng và mạng phụ thuộc |

## 9. Bảng ánh xạ từ `_04` sang quy chuẩn

| Nguồn trong `_04` | Nội dung được dẫn xuất | Đích trong quy chuẩn tương lai | Mức |
|---|---|---|---|
| Mở đầu: Ba câu hỏi của một cuộc khảo sát | Đối tượng, hành vi và căn cứ là ba câu hỏi nền | Mục 4 | Bắt buộc |
| Mở đầu: Thuộc tính, công cụ và biểu diễn | Không đồng nhất điều đúng về hàm, cách chứng minh và cách trình bày | Mục 4, 5 và 10 | Bắt buộc |
| Mở đầu: Một khung lí thuyết, không phải một thuật toán | Không áp danh sách phép tính cho mọi hàm | Mục 4 | Bắt buộc |
| Chương 1 | Xác định hàm, miền, cách cho hàm, hàm hạn chế và mở rộng | Mục 3 và 5 | Bắt buộc |
| Chương 2 | Đọc cấu trúc miền và các cách tiếp cận hợp lệ | Mục 5 | Bắt buộc |
| Chương 3 | Tập giá trị, tập mức, nghiệm, dấu, giao trục và đồ thị toán học | Mục 5 | Bắt buộc rà |
| Chương 4 | Giới hạn và hành vi tại các biên miền | Mục 5 | Bắt buộc rà |
| Chương 5 | Liên tục, gián đoạn và điều kiện áp dụng | Mục 5 và 12 | Bắt buộc rà |
| Chương 6 | Bị chặn, cận, giá trị đạt được và cực biên | Mục 5 | Kích hoạt theo hàm |
| Chương 7 | Biến thiên, đạo hàm, điểm tới hạn và bảng biến thiên | Mục 5 và 10 | Kích hoạt theo hàm |
| Chương 8 | Độ cong, hành vi bậc hai và giới hạn của dữ kiện đạo hàm cấp hai | Mục 5 | Kích hoạt theo hàm |
| Chương 9 | Đối xứng, tuần hoàn, miền đại diện và giới hạn của sự lặp lại | Mục 5 và 7 | Kích hoạt theo hàm |
| Chương 10 | Hợp hàm và sự truyền cấu trúc qua hai tầng | Mục 5 và 6 | Kích hoạt theo hàm |
| Chương 11 | Hàm ngược, hạn chế miền và đảo chiều quan hệ | Mục 5 | Kích hoạt theo hàm |
| Chương 12 | Phép biến đổi, họ tham số, trường hợp suy biến và bản đồ chế độ | Mục 3, 5 và 7 | Kích hoạt theo hàm |
| Chương 13 | Sai lệch và mô hình tiệm cận | Mục 5 | Kích hoạt theo hàm |
| Chương 14 | Tốc độ tăng trưởng, bậc và tương đương tiệm cận | Mục 5 và 12 | Kích hoạt theo hàm |
| Chương 15 | Dãy điểm đặc biệt, tính đầy đủ và cấu trúc tích tụ | Mục 5 và 10 | Kích hoạt theo hàm |
| Chương 16 | Dao động, hàm bao, tập giá trị tụ và giới hạn của biểu diễn hữu hạn | Mục 5, 6 và 10 | Kích hoạt theo hàm |
| Chương 17 | Mệnh đề khảo sát, điều kiện, chứng cứ, phản ví dụ và kiểm tra chéo | Mục 5, 8 và 12 | Bắt buộc |
| Chương 18 | Chức năng của bảng và đồ thị; kí hiệu thị giác; đọc ngược | Mục 10 và 12 | Bắt buộc |
| Chương 19 | Miền quan sát, thang đo, nhiều cửa sổ và hồ sơ lựa chọn | Mục 10 | Chuyển giao |
| Chương 20 | Miền lấy mẫu, sai số số, nội suy, khả năng tái tạo và nghiệm thu | Mục 10 và 12 | Chuyển giao |
| Mục 21.1–21.2 | Chuỗi sản phẩm và đơn vị khảo sát | Mục 2 và 3 | Bắt buộc |
| Mục 21.3–21.4 | Hiện tượng trung tâm, câu hỏi dẫn đường và bản đồ hiện tượng | Mục 6 | Bắt buộc |
| Mục 21.5 | Hai vòng lựa chọn, vai trò nội dung, ứng dụng và liên hệ mở rộng | Mục 5 và 7 | Bắt buộc rà hoặc kích hoạt |
| Mục 21.6 | Cấu trúc mạch lập luận | Mục 8 | Bắt buộc |
| Mục 21.7 | Mạng phụ thuộc và trật tự nhận thức | Mục 8 | Bắt buộc |
| Mục 21.8 | Chức năng kiến trúc, mức hiển thị và rút gọn | Mục 9 | Bắt buộc |
| Mục 21.9 | Mẫu đề cương và ba lượt kiểm định | Mục 2, 12 và các phụ lục | Bắt buộc |
| Mục 21.10 | Điều kiện dừng và nhận thức có thể chuyển giao | Mục 13 | Bắt buộc |

## 10. Các quyết định đã khóa cho lần viết quy chuẩn

1. `quy_chuan_khao_sat_ham_so.md` là tài liệu vận hành tự đủ cho AI, nhưng `_04` vẫn là nguồn lí thuyết có thẩm quyền khi cần giải thích sâu hoặc xử lí trường hợp chưa được nén hết.
2. Quy chuẩn không có một mục lục bài khảo sát cố định.
3. Hồ sơ khảo sát và đề cương vận hành là hai sản phẩm bắt buộc trước bài `.qmd`.
4. Tầng nền tảng phải được rà; tầng còn lại chỉ được kích hoạt theo hàm và bối cảnh.
5. Mỗi kết luận quan trọng phải truy được về chứng cứ; mỗi bảng hoặc hình phải truy được về mệnh đề.
6. Bảng biến thiên không phải thành phần mặc định.
7. Đồ thị không thay thế chứng minh.
8. Nội dung ứng dụng và liên hệ mở rộng chỉ xuất hiện khi có chức năng thật.
9. Học thuật tĩnh tại không phải phong cách mặc định.
10. Chi tiết sinh và nghiệm thu đồ thị được chuyển giao sang quy chuẩn TikZ/PGFPlots.
11. Ba lượt kiểm định phải được giữ riêng và có căn cứ cụ thể.
12. Điều kiện dừng phụ thuộc vào phạm vi đã công bố, không phụ thuộc vào việc đã nói hết mọi điều về hàm.

## 11. Tiêu chí nghiệm thu bản quy chuẩn tương lai

`quy_chuan_khao_sat_ham_so.md` chỉ đạt khi:

- một AI có thể dùng nó để đi từ đầu vào đến bài `.qmd` mà không phải tự phát minh quy trình;
- quy chuẩn vẫn buộc AI lựa chọn theo đối tượng, không áp một mẫu khảo sát cố định;
- mọi chương của `_04` đã có nơi tiếp nhận hoặc được ghi rõ là không chuyển nguyên dạng;
- ranh giới với quy chuẩn đồ thị và phong cách viết không chồng lấn;
- mẫu hồ sơ, bản đồ hiện tượng, đề cương và phiếu nghiệm thu dùng được trong thực tế;
- quy chuẩn phân biệt rõ điều bắt buộc, điều kích hoạt và điều chuyển giao;
- bài thử nghiệm cho một hàm có cấu trúc tinh tế vẫn bảo toàn miền, chứng cứ, ngoại lệ, cửa sổ và giới hạn lấy mẫu;
- đầu ra được kiểm tra bằng ba lượt và chỉ bàn giao khi đạt điều kiện dừng.

Ca kiểm nghiệm đầu tiên sau khi viết xong quy chuẩn là bài:

$$
y=\sin\left(\frac{1}{x}\right).
$$

Đây là phép thử phù hợp vì hàm đồng thời kích hoạt miền nhiều thành phần, hợp hàm, đối xứng, giới hạn tại biên bị loại, dao động, dãy điểm đặc biệt, tập giá trị tụ, nhiều cửa sổ quan sát và rủi ro lấy mẫu. Mục đích của phép thử là đối chiếu quy trình với một bài đã có chất lượng chuẩn, không viết lại bài chỉ để làm cho nó giống một mẫu cố định.

## 12. Bước thực hiện tiếp theo

Từ tài liệu này, viết `quy_chuan_khao_sat_ham_so.md` theo đúng cấu trúc ở Mục 7, lần lượt từ Mục 1 đến Mục 13 và năm phụ lục. Sau khi hoàn tất bản đầu, kiểm tra độ bao phủ bằng bảng ánh xạ ở Mục 9, rồi chạy ca kiểm nghiệm với $y=\sin\left(\frac{1}{x}\right)$ trước khi xem quy chuẩn là ổn định.
