# ZO Math — Thuật ngữ FHSM
## NCTM — *Focus in High School Mathematics: Reasoning and Sense Making* (2009)

**STATUS: LOCKED_FOR_EDITORIAL_USE_V1**

Glossary này được khóa sau:
- Terminology Audit R1;
- nghiên cứu ngữ nghĩa chuyên sâu theo từng họ thuật ngữ;
- Terminology Audit R2 stress-test trên 821 occurrence;
- R2: `FAIL=0`, `BLOCKER=0`.

Đây là authority dịch thuật cho vòng hiệu chỉnh FHSM:RSM tiếp theo. Không phải bảng search-and-replace.

---

# 1. Canonical editorial source

**CANONICAL_EDITORIAL_SOURCE = modular TeX**

Thư mục:
`content/di_tim/di_tim_ly_luan_toan_hoc/fhsm_tex/`

Các nguồn biên tập canonical:
- `tieu_luan_dan_nhap_fhsm_ban_chuyen_ngu.tex`
- `dan_nhap.tex`
- `chuong_01.tex`–`chuong_11.tex`
- `thu_muc_chu_giai.tex`
- `khao_luan_he_thuat_ngu_ban_chuyen_ngu.tex`
- `references.bib`

Driver:
- `main.tex`

Quyết định này là **project/human editorial authority decision** sau R2. Cơ sở:
- toàn bộ quá trình hiệu chỉnh FHSM trước đây được thực hiện tuần tự trên các tệp TeX mô-đun;
- `main.tex` trực tiếp build đúng bộ mô-đun này;
- QMD là representation song song/publication-side đã phân kỳ và không phải nhánh được tiếp tục hiệu chỉnh;
- `luan_va_hieu.tex` là aggregate riêng, không được `main.tex` include.

Hệ quả:
- TeX mô-đun là nguồn để chỉnh.
- QMD không được dùng để ghi đè TeX.
- QMD/aggregate chỉ được đồng bộ từ canonical sau khi bản TeX đã được hiệu chỉnh và kiểm định.

---

# 2. Nguyên tắc vận hành

1. Dịch NCTM theo hệ khái niệm NCTM trước; không dùng triết lí riêng của ZO Math để ép nghĩa.
2. Không search-and-replace máy móc.
3. Không ép một từ tiếng Anh luôn tương ứng một chuỗi tiếng Việt duy nhất.
4. Khi NCTM dùng các thuật ngữ khác nhau để phân biệt khái niệm, bản dịch phải giữ phân biệt ấy.
5. Phân biệt ba tầng khi giải thích quyết định:
   - A. NCTM thực sự viết gì;
   - B. phân tích ngữ nghĩa/dịch thuật;
   - C. quyết định tiếng Việt.
6. Từ chỉ process/activity trong câu không tự động trở thành một phần cố định của tên thuật ngữ.
7. Dạng phái sinh tiếng Anh phải được Việt hóa theo cú pháp, không ghép cơ học.

---

# 3. Họ reasoning

| English | Vietnamese v1 | Rule |
|---|---|---|
| `reasoning` | **suy lí** | Hoạt động nhận thức rộng; không đồng nhất với inference/argument/proof. |
| `reason` (verb, reasoning-family) | **suy lí** | `reason mathematically` → `suy lí toán học`; `reason about` → `suy lí về...`. |
| `reason` (noun) | **lí do / căn cứ** | Theo câu; không dịch `suy lí`. |
| `mathematical reasoning` | **suy lí toán học** | |
| `formal reasoning` | **suy lí hình thức** | |
| `reasoning habits` | **thói quen suy lí** | |
| `statistical reasoning` | **suy lí thống kê** | Phải khác `statistical inference`. |
| `geometric reasoning` | **suy lí hình học** | |
| `reasoning with/about functions` | **suy lí về hàm số** hoặc cấu trúc Việt tự nhiên | Không giữ giới từ tiếng Anh máy móc. |
| `empirical reasoning` | **suy lí thực nghiệm** | |
| `deductive reasoning` | **suy lí suy diễn** | Khi đúng khái niệm deduction. |
| `inductive reasoning` | **suy lí quy nạp** | |

## 3.1. Inference

| English | Vietnamese v1 | Rule |
|---|---|---|
| `inference` | **suy luận** | Có thể là hoạt động suy ra hoặc kết luận được suy ra; theo cú pháp. |
| `statistical inference` | **suy luận thống kê** | Khác `statistical reasoning` = `suy lí thống kê`. |
| `scope of inference` | **phạm vi suy luận** | |
| `inferences from data` | **các suy luận từ dữ liệu** | |
| `inferential` | Việt hóa theo chức năng | Không ghép máy móc. |
| `inferential reasoning` | giữ hạt nhân **suy lí**, diễn đạt theo ngữ cảnh | Không dùng `suy lí suy luận`; trong thống kê có thể diễn đạt `suy lí trong/cho suy luận thống kê`. |
| `informal inferential reasoning` | **suy lí phi hình thức trong suy luận thống kê** khi đúng ngữ cảnh | |
| `relational-inferential reasoning` | **suy lí dựa trên quan hệ và suy luận** | Tên kĩ thuật mức van Hiele thứ ba; hiểu là liên hệ các thuộc tính rồi thực hiện suy luận giữa chúng. |

## 3.2. Argument / argumentation

| English | Vietnamese v1 |
|---|---|
| `argument` | **lập luận** |
| `argumentation` | **hoạt động lập luận** |
| `formal argument` | **lập luận hình thức** |
| `formal argumentation` | **hoạt động lập luận hình thức** |
| `partial argument(s)` | dịch theo câu; ưu tiên **lập luận từng phần** khi tự nhiên |

Phân biệt:
- `reasoning/suy lí`: hoạt động nhận thức.
- `argument/lập luận`: chuỗi/cấu trúc lí lẽ.
- `argumentation/hoạt động lập luận`: kiến tạo, trình bày, đọc và thẩm định lập luận.

## 3.3. Justify / justification

| English | Vietnamese v1 |
|---|---|
| `justify` | **biện minh** |
| `justification` | **biện minh / sự biện minh** theo cú pháp |

Neo:
- `support` có thể hỗ trợ mà chưa đủ để `justify`.
- `justification` không đồng nhất với proof.
- Biện minh nhấn vào **căn cứ làm cho khẳng định/kết luận đứng vững**.

## 3.4. Proof / prove / proving

| English | Vietnamese v1 |
|---|---|
| `proof` | **chứng minh / một chứng minh** |
| `prove` | **chứng minh** |
| `proving` | **hoạt động chứng minh / quá trình chứng minh** khi cần làm rõ process |
| `formal proof` | **chứng minh hình thức** |

Phân biệt:
- `proof` có thể thực hiện chức năng biện minh/xác lập;
- `proof` có thể giải thích;
- `proof` không đồng nhất với `justification` hay `explanation`.

## 3.5. Explain / explanation

| English | Vietnamese v1 |
|---|---|
| `explain` | **giải thích** |
| `explanation` | **giải thích / sự giải thích / lời giải thích** theo cú pháp |
| `informal explanation` | **giải thích phi hình thức** |
| `partial explanation(s)` | **giải thích từng phần / giải thích còn dang dở** theo câu |

Phân biệt:
- `justification`: có đủ căn cứ để chấp nhận không?
- `explanation`: vì sao/thế nào điều đó đúng hoặc xảy ra?
- một proof có thể làm cả hai.

---

# 4. Họ sense making

| English | Vietnamese v1 | Rule |
|---|---|---|
| `sense making` | **kiến tạo ý nghĩa** | Thuật ngữ trung tâm. Là phép chuyển ngữ khái niệm của toàn cụm, không phải `sense=ý nghĩa + making=kiến tạo`. |
| `sense-making` | **kiến tạo ý nghĩa** | Cùng khái niệm. |
| `make sense (of)` | dịch tự nhiên theo câu | Thường: `hiểu`, `hiểu được`, `làm cho ... trở nên có nghĩa/hiểu được`; không thay máy móc bằng `kiến tạo ý nghĩa`. |
| `reasoning-and-sense-making` | **suy lí và kiến tạo ý nghĩa** | Việt hóa cấu trúc bổ nghĩa theo câu. |

Định nghĩa hạt nhân:
> **Chúng tôi định nghĩa kiến tạo ý nghĩa là việc phát triển sự hiểu biết về một tình huống, bối cảnh hoặc khái niệm bằng cách kết nối nó với tri thức đã có.**

Các ứng viên đã loại cho FHSM:RSM:
- `hiểu`
- `lập nghĩa`
- `diễn nghĩa`

Không hồi sinh trong hiệu chỉnh thông thường.

---

# 5. Understanding / meaning / comprehension

| English | Vietnamese v1 | Rule |
|---|---|---|
| `understanding` | **sự hiểu biết** | Hạt nhân danh từ; có thể chuyển cú pháp thành `hiểu`. |
| `understand` | **hiểu** | |
| `conceptual understanding` | **sự hiểu biết khái niệm** | Điều chỉnh cú pháp nếu câu Việt yêu cầu. |
| `meaning` | **ý nghĩa** | Không đồng nhất với `sense making` hay `understanding`. |
| `meaningful` | **có nghĩa / có ý nghĩa** | Theo đối tượng và cú pháp. |
| `meaningless` | **vô nghĩa / không có ý nghĩa** | Theo câu. |
| `comprehension` | không lập node glossary riêng | Trong occurrence FHSM hiện có, dịch tự nhiên bằng **hiểu**. |

Neo:
- `sense making` = hoạt động.
- `understanding` = sự hiểu biết được phát triển.
- `meaning` = ý nghĩa của cái được hiểu.

---

# 6. Interpret / interpretation

| English | Vietnamese v1 |
|---|---|
| `interpret` | **diễn giải** |
| `interpretation` | **diễn giải / việc diễn giải / sự diễn giải** |

Phân biệt:
- `interpretation`: kết quả/biểu thức/mô hình **nói gì, có nghĩa gì trong ngữ cảnh**.
- `explanation`: **vì sao/thế nào** điều ấy đúng hoặc xảy ra.

---

# 7. Bản đồ khái niệm làm việc

Đây là bản đồ dịch thuật, không phải sơ đồ NCTM tự tuyên bố.

## Nhánh suy lí
- **suy lí**: hoạt động nhận thức rộng;
- có thể có **suy luận**;
- có thể được tổ chức thành **lập luận**;
- kiến tạo/thẩm định lập luận là **hoạt động lập luận**;
- lập luận/căn cứ có thể **biện minh**;
- lập luận toán học đạt chuẩn thích hợp có thể là **chứng minh**;
- chứng minh có thể **giải thích**.

## Nhánh kiến tạo ý nghĩa
- **kiến tạo ý nghĩa**: làm cái đang học trở nên có mạch, có nghĩa và hiểu được bằng cách kết nối với tri thức đã có;
- hoạt động ấy phát triển **sự hiểu biết**;
- cái được nhận ra/nắm bắt là **ý nghĩa**;
- **diễn giải** làm rõ một kết quả/biểu thức có nghĩa gì trong ngữ cảnh.

NCTM nói `reasoning` và `sense making` **intertwined**:
- `reasoning` → **suy lí**
- `sense making` → **kiến tạo ý nghĩa**

---

# 8. Editorial rule

Khi một câu cụ thể buộc phải lựa chọn giữa:
- giữ nguyên chuỗi glossary nhưng tiếng Việt gượng/sai;
- hay Việt hóa cú pháp mà vẫn giữ đúng phân biệt khái niệm,

**ưu tiên Việt hóa cú pháp và bảo toàn khái niệm**.

Glossary v1 là authority ngữ nghĩa, không phải bộ quy tắc thay chuỗi.
