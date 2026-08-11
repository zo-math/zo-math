# Quy trình sản xuất bài khảo sát hàm số

## 1. Mục đích và phạm vi

Tài liệu này điều phối việc tạo mới, hoàn thiện và kiểm định một bài khảo sát về một hàm số cụ thể trong dự án **100+ Hàm số: Sự biến thiên và đồ thị**.

Quy trình biến một phiếu giao việc ngắn thành một chuỗi sản phẩm có thể kiểm tra:

1. hồ sơ sản xuất;
2. hồ sơ khảo sát toán học;
3. bản đồ hiện tượng;
4. đề cương vận hành;
5. bài `.qmd` và tài nguyên đi kèm;
6. hồ sơ nghiệm thu.

Tài liệu này không thay thế
`quy_chuan_khao_sat_ham_so.md` hoặc
`quy_chuan_ki_thuat_bai_ham_so_qmd.md`.

Ba tài liệu có vai trò phân biệt:

- quy chuẩn khảo sát quyết định nội dung toán học, trục nhận thức, kiến trúc bài và cách kiểm định về nội dung;
- quy chuẩn kĩ thuật quyết định hợp đồng đầu ra của QMD, tài nguyên, HTML, PDF và các cổng kiểm định kĩ thuật;
- quy trình này quyết định agent phải đọc gì, tạo gì, dừng ở đâu và bàn giao ra sao trong repository.

## 2. Phạm vi tệp và đường dẫn chuẩn

### 2.1. Phân vùng thẩm quyền

Trong phạm vi dự án này, chỉ `AGENTS.md` và các tài liệu được chỉ định trong `_quy_trinh/` có vai trò điều khiển việc sản xuất bài.

Các tệp `.qmd` nằm ngoài `_quy_trinh/` là nội dung xuất bản hoặc sản phẩm đang được xây dựng; chúng không được dùng làm tài liệu điều khiển, trừ khi quy trình dẫn chiếu rõ ràng đến một tệp cụ thể với vai trò nguồn tham khảo.

### 2.2. Cấu trúc tệp chuẩn

Trong tài liệu này, đường dẫn được hiểu là đường dẫn tính từ gốc repository.

Cấu trúc điều khiển và dữ liệu thường trực:

```text
content/thpt/zo_math_100/100_ham_so_su_bien_thien_va_do_thi/
├── AGENTS.md
├── _quy_trinh/
│   ├── quy_trinh_tao_bai_ham_so.md
│   ├── quy_chuan_khao_sat_ham_so.md
│   ├── quy_chuan_ki_thuat_bai_ham_so_qmd.md
│   ├── ho_so_san_xuat_mac_dinh.yml
│   ├── mau_ki_thuat_qmd.qmd
│   ├── nguon_li_thuyet/
│   │   └── khung_khao_sat_ham_so_hoan_chinh_04.qmd
│   └── ho_so/
└── _data/
    └── cards.yml
```

Các quy chuẩn dùng chung:

```text
quy_trinh_xay_dung/
├── huong_dan_su_dung_khoi_noi_dung.md
├── quy_chuan_do_thi_sinh_ma_nguon_tikz_pgfplots.md
└── phong_cach_viet/
    ├── index.md
    └── hoc_thuat_tinh_tai.md
```

Các tệp bài và hình:

```text
content/thpt/zo_math_100/100_ham_so_su_bien_thien_va_do_thi/
├── core/
├── depth/
└── _figures/
```

`_quy_trinh/nguon_li_thuyet/khung_khao_sat_ham_so_hoan_chinh_04.qmd` là nguồn lí thuyết nội bộ có thẩm quyền mà `quy_chuan_khao_sat_ham_so.md` dẫn chiếu. Tệp được giữ dưới `_quy_trinh/` để không lẫn với trang QMD xuất bản. Chỉ quay về nguồn đầy đủ khi quy chuẩn chưa nén hết trường hợp đang xét.

## 3. Chế độ vận hành

Hồ sơ sản xuất phải ghi đúng một chế độ:

| Chế độ       | Khi dùng                            | Phạm vi mặc định                                                    |
| ------------ | ----------------------------------- | ------------------------------------------------------------------- |
| `tao_moi`    | Chưa có bài đích                    | Tạo hồ sơ, bài, tài nguyên và kiểm định đầy đủ                      |
| `hoan_thien` | Bài đã có và người dùng yêu cầu sửa | Chẩn đoán, lập hồ sơ cần thiết, sửa trong phạm vi rồi kiểm định lại |
| `kiem_dinh`  | Người dùng chỉ yêu cầu đánh giá     | Chỉ đọc và báo cáo; không sửa nếu chưa được giao rõ                 |

Không tự chuyển từ `kiem_dinh` sang sửa bài. Không tự mở rộng một nhiệm vụ biên tập cục bộ thành việc viết lại toàn bài.

## 4. Đầu vào

### 4.1. Đầu vào người dùng cung cấp cho từng bài

Phiếu giao việc có thể rất ngắn, nhưng cần xác định được:

- hàm số hoặc họ hàm;
- miền khảo sát nếu không dùng miền tự nhiên;
- mục tiêu hoặc hiện tượng được chỉ định, nếu có;
- người đọc hoặc mức độ bài;
- chế độ vận hành;
- tệp đầu ra hoặc thẻ tương ứng, nếu đã biết;
- phong cách viết, nếu người dùng chỉ định;
- ràng buộc đặc biệt về hình, PDF hoặc xuất bản.

Không yêu cầu người dùng gửi lại những tệp điều khiển đã có trong repository.

Chỉ hỏi lại khi thiếu thông tin tạo ra nhiều đơn vị khảo sát khác nhau rõ rệt theo Mục 3.3 của `quy_chuan_khao_sat_ham_so.md`. Những quyết định nhỏ mà quy chuẩn cho phép agent tự xử lí phải được ghi vào hồ sơ, không chuyển ngược thành câu hỏi cho người dùng.

### 4.2. Đầu vào agent tự đọc

Trước khi viết, sửa hoặc kiểm định, agent phải tự đọc:

1. `AGENTS.md` ở gốc repository và các chỉ dẫn cấp trung gian;
2. `AGENTS.md` của dự án này;
3. `quy_chuan_khao_sat_ham_so.md`;
4. `quy_chuan_ki_thuat_bai_ham_so_qmd.md`;
5. hồ sơ sản xuất của bài, nếu đã tồn tại;
6. `ho_so_san_xuat_mac_dinh.yml` khi cần khởi tạo hồ sơ;
7. `mau_ki_thuat_qmd.qmd` khi tạo tệp QMD mới;
8. mục tương ứng trong `_data/cards.yml`;
9. tệp đích và toàn bộ tài nguyên mà tệp đích dẫn tới, nếu bài đã tồn tại;
10. `quy_trinh_xay_dung/huong_dan_su_dung_khoi_noi_dung.md` khi bài có hoặc dự kiến có khối nội dung;
11. quy chuẩn đồ thị khi bài cần tạo, sửa hoặc kiểm định hình TikZ/PGFPlots;
12. chỉ mục phong cách và tài liệu phong cách có hiệu lực; đối với bài khảo sát hàm số cụ thể trong dự án này, mặc định phải đọc `hoc_thuat_tinh_tai.md` theo `AGENTS.md`;
13. cấu hình Quarto, Lua filter, CSS, TeX hoặc script liên quan trực tiếp khi cần kiểm tra kĩ thuật hay render.

Quy chuẩn khảo sát phải được đọc để xác định bài cần nói điều gì và được tổ chức theo mạch nào.

Quy chuẩn kĩ thuật phải được đọc để xác định QMD, tài nguyên, HTML và PDF phải đạt những điều kiện nào.

`mau_ki_thuat_qmd.qmd` chỉ hiện thực hóa phần khung ban đầu của quy chuẩn kĩ thuật. Khi mẫu và quy chuẩn kĩ thuật không thống nhất, phải báo sai lệch; không âm thầm lấy mẫu làm nguồn có thẩm quyền cao hơn.

`depth/ham_sin_mot_tren_x.qmd` chỉ là ca kiểm nghiệm và tham chiếu kĩ thuật. Không dùng kiến trúc nội dung của bài này làm mục lục mặc định cho bài khác.

## 5. Thứ tự thẩm quyền

Khi có nhiều chỉ dẫn cùng áp dụng:

1. yêu cầu hiện tại của người dùng;
2. `AGENTS.md` và quy ước tại đúng phạm vi repository;
3. `quy_chuan_khao_sat_ham_so.md` đối với nội dung toán học, trục nhận thức và kiến trúc bài;
4. `quy_chuan_ki_thuat_bai_ham_so_qmd.md` đối với QMD, tài nguyên, HTML, PDF và kiểm định đầu ra;
5. quy chuẩn chuyên trách được kích hoạt;
6. nguồn lí thuyết đầy đủ dùng để giải thích phần chưa được nén;
7. mẫu kĩ thuật và bài tham chiếu trong đúng vai trò đã được xác định.

`mau_ki_thuat_qmd.qmd` không được dùng để ghi đè quy chuẩn kĩ thuật.

Một bài đã xuất bản không được dùng để ghi đè quy chuẩn khảo sát hoặc quy chuẩn kĩ thuật chỉ vì nó đang tồn tại và render được.

Nếu hai chỉ dẫn cùng cấp mâu thuẫn trực tiếp và làm thay đổi đầu ra, phải dừng và hỏi người dùng. Không tự hòa giải bằng một thay đổi âm thầm.

## 6. Sản phẩm làm việc

Mỗi bài được tạo hoặc hoàn thiện theo quy trình phải có một hồ sơ:

```text
_quy_trinh/ho_so/<slug>.yml
```

Hồ sơ được khởi tạo từ `ho_so_san_xuat_mac_dinh.yml`, sau đó điền bằng dữ kiện thực. Không sửa tệp mặc định cho riêng một bài.

Hồ sơ là nơi lưu:

- đơn vị khảo sát;
- phạm vi và người đọc;
- suy định của agent;
- bản đồ miền;
- bảng mệnh đề–chứng cứ;
- kết quả hai vòng rà;
- hiện tượng trung tâm và bản đồ hiện tượng;
- đề cương vận hành;
- đặc tả biểu diễn;
- trạng thái tài nguyên;
- kết quả kiểm định và nghiệm thu;
- những tiêu chí không áp dụng cùng lí do.

Các trường chưa làm phải giữ trạng thái `chua_thuc_hien` hoặc giá trị `null`. Không điền `dat` trước khi có căn cứ.

Trong chế độ `kiem_dinh`, nếu không có hồ sơ cũ, được tạo một hồ sơ chẩn đoán tối thiểu khi người dùng cho phép tạo tệp. Nếu nhiệm vụ chỉ cho phép đọc và báo cáo, không coi việc thiếu hồ sơ là lỗi của bài.

## 7. Quy trình thực hiện

### Giai đoạn 0 — Khóa phạm vi

1. Xác định chế độ vận hành.
2. Đọc trạng thái Git và nhận diện các thay đổi đã có.
3. Xác định chính xác những tệp được phép đọc, tạo và sửa.
4. Ghi các thay đổi ngoài phạm vi là tài sản hiện có của người dùng; không sửa, xóa, phục hồi, staging hoặc gộp chúng.
5. Xác định điều kiện dừng và thành phần bàn giao của nhiệm vụ.

Kết quả của giai đoạn này được ghi vào các nhóm `nhiem_vu`, `pham_vi_thay_doi` và `ban_giao` trong hồ sơ.

### Giai đoạn 1 — Khởi tạo hồ sơ sản xuất

1. Tìm thẻ của hàm trong `_data/cards.yml`.
2. Xác định `slug`, số thẻ, nhãn, đường dẫn QMD, ảnh thẻ và trạng thái xuất bản.
3. Sao chép cấu trúc của `ho_so_san_xuat_mac_dinh.yml` thành `_quy_trinh/ho_so/<slug>.yml`; giữ Học thuật tĩnh tại là phong cách mặc định cục bộ, trừ khi yêu cầu trực tiếp của người dùng chỉ định khác.
4. Điền phiếu giao việc và các thông tin có thể truy trực tiếp.
5. Ghi rõ mọi suy định.
6. Chỉ hỏi lại những trường hợp đạt điều kiện phải hỏi của quy chuẩn.

Nếu công thức chưa có trong `cards.yml`, không tự ý thêm thẻ khi người dùng chưa giao việc thay đổi danh mục. Ghi vấn đề vào hồ sơ và tiếp tục phần nội dung nếu đường dẫn đầu ra đã rõ.

Điểm kiểm soát G1 đạt khi đơn vị khảo sát, chế độ, phạm vi tệp và đầu ra đã xác định đủ để không tạo nhầm bài.

### Giai đoạn 2 — Lập hồ sơ khảo sát toán học

Thực hiện theo Mục 4 và Mục 5 của `quy_chuan_khao_sat_ham_so.md`:

1. lập bản đồ miền;
2. thực hiện vòng rà nền tảng;
3. kích hoạt những phương diện thực sự cần;
4. tạo bảng mệnh đề–chứng cứ;
5. phân biệt kết quả biểu tượng, kết quả số, quan sát và phần còn mở;
6. kiểm tra chéo toàn hồ sơ;
7. xử lí mọi mâu thuẫn có thể làm đổi kết luận.

Không viết văn xuôi dài của bài trong giai đoạn này.

Sau vòng rà, phải truy đúng phần liên quan trong `_quy_trinh/nguon_li_thuyet/khung_khao_sat_ham_so_hoan_chinh_04.qmd` đối với những phương diện sẽ đi vào mạch chính hoặc làm căn cứ cho hiện tượng trung tâm, đặc biệt khi phần nguồn chứa định nghĩa, điều kiện, giới hạn phương pháp hoặc một phân biệt dễ gây nhầm. Việc này vẫn cần thực hiện khi quy chuẩn nén có vẻ đã đủ để tính toán kết quả.

Trong `vi_tri_da_dung`, ghi chương/mục hoặc vị trí nội dung cụ thể đã dùng; không dùng một mô tả chung như “khung hồ sơ” hay “trục nhận thức”. Trường `da_dung` và danh sách vị trí chỉ tạo khả năng truy xuất, không thay thế việc kiểm tra sản phẩm cuối.

Điểm kiểm soát G2 đạt khi không còn lỗi toán học thiết yếu và các kết luận quan trọng đều truy được về chứng cứ.

### Giai đoạn 3 — Chọn trục nhận thức và lập đề cương

Thực hiện theo Mục 6–9 của quy chuẩn:

1. đề xuất hiện tượng trung tâm từ hồ sơ;
2. kiểm tra hiện tượng ấy bằng chứng cứ, đồng thời tách phát biểu toán học chính xác khỏi ẩn dụ hoặc trực giác; loại bỏ trục nhận thức dựa trên một quan hệ mơ hồ hoặc sai;
3. viết câu hỏi dẫn đường và câu trả lời dự kiến; câu hỏi phải đủ ngắn và không chứa một kết luận chưa được hồ sơ nâng đỡ;
4. lập bản đồ hiện tượng đủ năm thành phần;
5. chọn nội dung theo chức năng;
6. tạo các mạch lập luận;
7. lập mạng phụ thuộc và phá vòng tròn;
8. chọn trật tự nhận thức;
9. xác định mức hiển thị của từng nội dung;
10. xác định điểm kết tinh và kiến trúc bài;
11. xác lập điều kiện dừng riêng.

Không dùng một mục lục cố định. Các chức năng khơi mở, nhận diện, triển khai, kết tinh, soi chiếu và khép lại phải được thực hiện, nhưng không bắt buộc trở thành sáu tiêu đề.

Điểm kiểm soát G3 đạt khi đề cương có thể giải thích vì sao từng phần tồn tại, phần nào cần đứng trước và toàn bài sẽ trả lời câu hỏi trung tâm bằng chứng cứ nào.

### Giai đoạn 4 — Đặc tả tài nguyên và chuẩn bị QMD

1. Với mỗi bảng hoặc hình, hoàn thành đặc tả tại Mục 10.2 của quy chuẩn khảo sát.
2. Chỉ kích hoạt quy chuẩn đồ thị khi cần tạo hoặc sửa hình TikZ/PGFPlots.
3. Mỗi tệp `.tex` mới phải tự chứa toàn bộ màu và style cần dùng; không phụ thuộc `zo-graph-styles.tex`.
4. Xác định đường dẫn nguồn `.tex`, PDF, SVG và đường dẫn chèn vào bài.
5. Phân loại bố cục QMD của từng hình và ghi quyết định vào hồ sơ:
   - `thuong`: mặc định cho cả HTML và PDF; hình nằm trong bề ngang nội dung và không dùng `.column-screen-inset-shaded`;
   - `mo_rong_html`: chỉ dùng khi bề ngang thông thường không đủ để đọc chi tiết thiết yếu;
   - hình `mo_rong_html` phải có nhãn `fig-*`, lí do mở rộng và lớp `.column-screen-inset-shaded` chỉ được xuất hiện trong nhánh `when-format="html"`.
6. Đối chiếu các quyết định về YAML, hệ tiêu đề, mã thực thi, khối nội dung, tài nguyên, bài tập, PDF và cấu trúc bị cấm với `quy_chuan_ki_thuat_bai_ham_so_qmd.md`.
7. Khi tạo QMD mới, sao chép phần khung ban đầu từ `mau_ki_thuat_qmd.qmd`, rồi hoàn thiện theo quy chuẩn kĩ thuật và hồ sơ của chính bài.
8. Với mỗi nội dung dự kiến đặt trong khối, ghi rõ:
   - lí do cần tách thành khối thay vì dùng văn bản hoặc tiêu đề thông thường;
   - nội dung thuộc mạch chính hay phần đọc thêm;
   - trạng thái mở cố định hoặc thu gọn;
   - màu đỏ, vàng hoặc xám theo đúng chức năng;
   - tiêu đề cụ thể của khối;
   - cú pháp lớp hiện hành sẽ sử dụng.
9. Không đưa một nội dung vào khối chỉ để trang trí hoặc nhấn mạnh. Không thu gọn mắt xích bắt buộc của mạch chính.
10. Ghi vị trí dự kiến của từng khối trong mạch bài và lí do đặt ở đó. Không gom các khối ứng dụng, lịch sử, so sánh hoặc khám phá vào một mục cuối chỉ vì chúng đều là phần đọc thêm; phân bố chúng tại nơi chúng làm sáng tỏ kết quả vừa được xác lập.
11. Đối với bài production chuẩn, thiết kế hệ bài tập như phần tiếp tục của bài học: một mạch giúp tái dựng nội dung cốt lõi và một mạch mở rộng–đào sâu. Hai chức năng này chỉ là mục tiêu nội bộ. Theo contract kĩ thuật hiện hành, H3 dùng cho nhóm toán học tự nhiên và H4 cho từng bài; không dùng chính tên hai mục tiêu nội bộ làm heading công khai. Chỉ bỏ hệ bài tập khi yêu cầu trực tiếp của người dùng hoặc loại nhiệm vụ thực sự cho phép, và phải ghi rõ ngoại lệ trong hồ sơ.
12. Với bài dự kiến chuyển sang `published`, xác định tên PDF, `zo-pdf-download`, `zo-pdf-branding`, URL chính tắc và quy trình build PDF.
13. Thay toàn bộ giá trị giữ chỗ bằng metadata thật. Trước G4, đối chiếu chức năng riêng của `subtitle`, `summary`, `description`, `abstract` và `keywords`; phần mô tả phải là lời giới thiệu bằng văn xuôi, không phải danh sách từ khóa.
14. Trong đặc tả hình, ghi rõ những điểm/mốc nào là neo nhận thức, đường chiếu nào thực sự cần để đọc tọa độ và `fig-alt` dự kiến mô tả những gì sẽ hiện trên artifact.
15. Xóa các chú thích hướng dẫn không thuộc bài cuối.

`mau_ki_thuat_qmd.qmd` chỉ cung cấp khung YAML, các vị trí kĩ thuật và mẫu cú pháp. Nó không áp đặt đề mục nội dung và không thay thế `quy_chuan_ki_thuat_bai_ham_so_qmd.md`.

Không sao chép tự động lớp bố cục hình từ bài tham chiếu. Trong nhánh PDF, không dùng `.column-screen-inset-shaded` trong bất kì trường hợp nào.

Điểm kiểm soát G4 đạt khi:

- mọi biểu diễn có mục đích, phạm vi đọc và giới hạn rõ;
- từng hình đã được phân loại là `thuong` hoặc `mo_rong_html` và hồ sơ không còn khai báo bố cục chưa xác định;
- QMD đã được chuẩn bị theo hợp đồng đầu ra kĩ thuật;
- các tiêu chí kích hoạt theo điều kiện đã được quyết định;
- mọi khối dự kiến có chức năng, trạng thái, màu và cú pháp rõ;
- bài dự kiến `published` đã có kế hoạch PDF đầy đủ;
- không còn quyết định kĩ thuật quan trọng ở trạng thái chưa xác định.

### Giai đoạn 5 — Viết bài và tạo tài nguyên

Trong toàn bộ giai đoạn này, đề cương đã qua G3 điều khiển mạch nội dung; `quy_chuan_ki_thuat_bai_ham_so_qmd.md` điều khiển cách hiện thực mạch ấy thành QMD và các đầu ra xuất bản. Không dùng mẫu kĩ thuật để thay đổi kiến trúc nhận thức đã chốt.

1. Viết theo đề cương đã qua G3.
2. Giữ mắt xích bắt buộc trong mạch chính.
3. Phân biệt rõ quan sát, dự đoán, kết luận, xấp xỉ và gợi mở.
4. Sau mỗi chuỗi công thức, giải nghĩa kết quả đối với hàm.
5. Sau mỗi biểu diễn, viết phần đọc ngược về mệnh đề và giới hạn của biểu diễn.
6. Áp dụng tài liệu phong cách có hiệu lực chỉ sau khi kiến trúc toán học ổn định; với bài khảo sát hàm số cụ thể trong dự án này, Học thuật tĩnh tại là mặc định cục bộ. Ưu tiên văn xuôi khi lập luận có thể chảy liên tục, không dùng bold để nhấn câu văn thông thường và giữ đúng quy ước LaTeX của dự án.
7. Tạo và kiểm tra các tệp nguồn hình theo quy chuẩn chuyên trách.
8. Không cập nhật `cards.yml` chỉ để đánh dấu bài đã xuất bản khi bài chưa qua nghiệm thu.
9. Dùng hệ lớp `zo-block` hiện hành theo `huong_dan_su_dung_khoi_noi_dung.md`. Không dùng các lớp cũ cho nội dung mới chỉ vì chúng vẫn còn được CSS hỗ trợ để tương thích.
10. Nội dung bắt buộc đối với mạch chính không được đặt trong khối thu gọn. Khi văn bản thường và hệ tiêu đề đã đủ rõ, không tạo thêm khối.

Trong chế độ `hoan_thien`, sửa tại nguồn gần nhất tạo ra lỗi. Không viết lại phần đã đạt nếu việc đó không cần cho mục tiêu hoặc mạch bài.

Điểm kiểm soát G5 đạt khi bài hoàn chỉnh về nội dung, mọi tài nguyên tồn tại và không còn giá trị giữ chỗ.

### Giai đoạn 6 — Kiểm định nội dung

Thực hiện đúng giao thức của Mục 12 trong quy chuẩn:

1. kiểm định toán học;
2. kiểm định mạch giải thích;
3. kiểm định giá trị nhận thức;
4. kiểm định hệ thống bài tập khi bài có bài tập;
5. kiểm định hệ khối nội dung: sự cần thiết của từng khối, trạng thái hiển thị, màu theo chức năng, tiêu đề, cú pháp lớp và việc bảo toàn mạch chính;
6. sửa lỗi tại nguồn gần nhất;
7. chạy lại các lượt bị ảnh hưởng.

Mỗi tiêu chí phải có trạng thái và căn cứ cụ thể. Trong nghiệm thu cuối, không được còn tiêu chí bắt buộc ở trạng thái `dat_mot_phan` hoặc `chua_kiem_chung`.

Điểm kiểm soát G6 đạt khi các tiêu chí bắt buộc đã quy về `dat`, `khong_dat` hoặc `khong_ap_dung`, và không còn tiêu chí `khong_dat`.

### Giai đoạn 7 — Kiểm tra kĩ thuật và bản render

Trong phạm vi môi trường cho phép:

1. kiểm tra cú pháp YAML, Markdown và Quarto;
2. kiểm tra công thức, dẫn chiếu, liên kết và đường dẫn tài nguyên;
3. kiểm tra mã hóa và khoảng trắng theo quy ước dự án;
4. biên dịch từng hình nguồn;
5. kiểm tra PDF và SVG của hình;
6. trước khi kiểm tra giao diện HTML, xác nhận bài đã được đăng kí vào đúng nhóm sidebar trong `_quarto.yml` khi dự án yêu cầu sidebar;
7. render HTML của bài;
8. xem HTML thật ở desktop và mobile; xác nhận phần tử sidebar và mục lục thật sự xuất hiện, rồi kiểm tra navbar, căn lề giữa tựa đề và thân bài, hình thường và hình mở rộng;
9. build PDF tải xuống khi bài yêu cầu; trước khi đưa một HTML có nút “Tải PDF” vào Human Review, phải bảo đảm PDF đích đã tồn tại và mở được;
10. xem PDF thật; kiểm tra hình nằm trong bề ngang nội dung, công thức, ngắt trang và kí tự lỗi;
11. kiểm tra trực quan các khối mở cố định và thu gọn trên cả HTML lẫn PDF: viền, nền, tiêu đề, khoảng cách, khả năng mở–đóng trên HTML, nội dung đầy đủ trên PDF và sự liên tục của mạch đọc;
12. kiểm tra bài mới không dùng lớp khối cũ; với bài hiện có, phải báo rõ lớp cũ nào còn tồn tại và đó là tương thích lịch sử hay sai lệch cần chuyển đổi;
13. kiểm tra nút tải PDF, metadata, URL chính tắc và tài nguyên; đối chiếu `fig-alt`, caption, các điểm/mốc và đường chiếu với artifact đã render thay vì chỉ với ý định trong source;
14. chạy lại kiểm định nội dung nếu sửa kĩ thuật làm thay đổi cách đọc.

Không tuyên bố một kiểm tra đã đạt chỉ vì lệnh trả về mã thoát `0` nếu tiêu chí cần quan sát bản render.

Nếu môi trường chặn một phép kiểm tra bắt buộc, ghi `chua_kiem_chung`, nêu nguyên nhân và không tuyên bố nghiệm thu đạt.

Điểm kiểm soát G7 đạt khi mọi đầu ra bắt buộc đã được kiểm tra theo đúng loại bằng chứng.

### Giai đoạn 8 — Xuất bản và bàn giao

Chỉ cập nhật mục tương ứng trong `_data/cards.yml` khi:

- nhiệm vụ bao gồm xuất bản hoặc cập nhật thẻ;
- bài đã qua G6 và G7;
- `href`, `image`, `status`, số thẻ và metadata đã được đối chiếu.

Trước bàn giao:

1. kiểm tra `git diff --check`;
2. xem diff của từng tệp trong phạm vi;
3. xác nhận không có tệp ngoài phạm vi bị sửa;
4. cập nhật hồ sơ bằng kết quả cuối;
5. liệt kê tệp tạo, tệp sửa, phép kiểm tra và giới hạn còn lại.

Không staging và không commit nếu người dùng chưa yêu cầu rõ.

Trong một phiên trình diễn hoặc kiểm thử cỗ máy, bài thử không mặc nhiên trở thành sản phẩm xuất bản. Nếu kiểm định có người quan sát còn `FAIL`, phải giữ `production_status: in_production`, `publication_status: pending`, để `prepublish` chặn đúng hợp đồng và lưu bằng chứng. Sau khi bằng chứng đã được bảo toàn, phải loại đối tượng thử khỏi phạm vi phát hành của lớp vận hành, trừ khi người dùng giao một nhiệm vụ sản xuất thật riêng.

## 8. Quy tắc riêng cho chế độ kiểm định

Khi `che_do: kiem_dinh`:

1. mặc định chỉ kiểm định đầu ra hiện có;
2. không đánh lỗi vì thiếu sản phẩm trung gian;
3. chỉ kiểm định tuân thủ quy trình khi hồ sơ và sản phẩm trung gian tồn tại;
4. dùng `chua_kiem_chung` khi thiếu căn cứ;
5. báo cáo sai lệch theo mức ảnh hưởng và chỉ ra nguồn gần nhất nên sửa;
6. chưa sửa tệp cho đến khi người dùng giao rõ.

Báo cáo phải phân biệt:

- lỗi toán học;
- lỗi mạch giải thích;
- lỗi giá trị nhận thức;
- lỗi bài tập;
- lỗi kĩ thuật;
- giới hạn chưa thể kiểm chứng.

## 9. Quy tắc cập nhật tài liệu điều khiển

Trong một nhiệm vụ sản xuất bài:

- không tự sửa `quy_chuan_khao_sat_ham_so.md`;
- không tự sửa nguồn lí thuyết `_04`;
- không tự sửa quy chuẩn đồ thị;
- không tự sửa tài liệu phong cách;
- không biến một điều chỉnh cục bộ của một bài thành quy tắc chung.

Nếu phát hiện khoảng trống hoặc mâu thuẫn, ghi vào `van_de_he_thong` của hồ sơ và báo người dùng. Chỉ cập nhật tài liệu điều khiển trong một nhiệm vụ riêng được giao rõ.

## 10. Điều kiện nghiệm thu toàn quy trình

Một bài ở chế độ `tao_moi` hoặc `hoan_thien` chỉ được tuyên bố hoàn tất khi:

- các điểm kiểm soát G1–G7 đã đạt;
- G8 đã hoàn thành trong phạm vi được giao;
- câu hỏi dẫn đường được giải quyết;
- chuỗi `hiện tượng → cơ chế → chứng cứ → hình dạng → nhận thức` được ghi trong hồ sơ;
- không còn giá trị giữ chỗ trong QMD hoặc tài nguyên;
- mọi tệp bàn giao tồn tại;
- không có thay đổi ngoài phạm vi;
- các giới hạn còn lại đã được công bố.

Một phiên kiểm thử có thể kết thúc hợp lệ ở trạng thái `in_production/pending` với `prepublish=blocked` khi mục tiêu là chứng minh cổng kiểm định và không phải nghiệm thu bài. Trạng thái ấy không được diễn đạt thành bài đã hoàn tất hoặc sẵn sàng xuất bản.

## 11. Mẫu lệnh giao việc hằng ngày

### Tạo bài mới

```text
Hãy chạy quy trình sản xuất bài hàm số ở chế độ `tao_moi`.

Hàm số: y = ln x
Miền xét: miền tự nhiên
Người đọc: người đọc của dự án 100+ Hàm số
Mức độ: bài chuyên sâu
Phong cách: Học thuật tĩnh tại
Tệp đầu ra: depth/ham_lnx.qmd

Hãy tự đọc AGENTS.md và các tài liệu do quy trình kích hoạt; tạo hồ sơ sản xuất, bài QMD và các tài nguyên cần thiết; kiểm định đầy đủ trước khi bàn giao. Không sửa tài liệu điều khiển, không staging và không commit.
```

### Kiểm định bài đã có

```text
Hãy chạy quy trình sản xuất bài hàm số ở chế độ `kiem_dinh`.

Tệp cần kiểm định: depth/ham_sin_mot_tren_x.qmd

Hãy kiểm định nội dung toán học, mạch lập luận, giá trị nhận thức, hệ thống bài tập, QMD, hình, HTML và PDF trong phạm vi có thể xác nhận. Trước hết chỉ báo cáo sai lệch và đề xuất nguồn cần sửa; chưa sửa tệp, staging hoặc commit.
```
