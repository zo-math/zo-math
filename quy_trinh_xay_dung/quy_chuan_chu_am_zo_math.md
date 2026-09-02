# Quy chuẩn chú âm ZO Math

**Trạng thái:** Chính thức  
**Phạm vi:** Toàn bộ nội dung ZO Math  
**Tính chất:** Tài liệu sống, cập nhật liên tục; lịch sử thay đổi được quản lý bằng Git  
**Tệp dữ liệu đi kèm:** `quy_trinh_xay_dung/tu_dien_chu_am_zo_math.yml`

---

## 1. Vai trò của quy chuẩn

Tài liệu này là quy chuẩn nội bộ chính thức của ZO Math về cách **chú âm tiếng Việt** cho tên riêng, thuật ngữ và những biểu thức không phải tiếng Việt.

Quy chuẩn phục vụ đồng thời hai nhóm đối tượng:

- người viết, biên tập và kiểm định nội dung ZO Math;
- ChatGPT, Codex và các tác tử AI khác làm việc với kho mã ZO Math.

Quy chuẩn này là **house style của ZO Math**, không phải quy chuẩn quốc gia về phiên âm hoặc chính tả tiếng Việt.

Trong tài liệu này:

- **BẮT BUỘC**: phải tuân thủ;
- **KHÔNG ĐƯỢC**: bị cấm trong nội dung chính thức;
- **NÊN**: mặc định phải làm như vậy, trừ khi có lý do rõ ràng;
- **CÓ THỂ**: tùy ngữ cảnh.

---

## 2. Mục tiêu

ZO Math ưu tiên giữ **dạng viết gốc hoặc dạng viết quốc tế được lựa chọn** của tên và thuật ngữ, đồng thời có thể thêm một **chú âm Việt** để người đọc tiếng Việt biết cách đọc gần đúng.

Mẫu hiển thị:

> Pascal (Pát-can)

Trong đó:

- `Pascal` là dạng viết được giữ trong nội dung;
- `Pát-can` là chú âm Việt;
- chú âm không thay thế tên gốc;
- chú âm không phải IPA;
- chú âm không phải phiên âm âm vị học;
- chú âm không phải một tên Việt hóa độc lập.

Mục tiêu của chú âm là:

> Một người đọc tiếng Việt không biết ngôn ngữ nguồn vẫn có thể nhìn phần chú âm và đọc thành tiếng ngay bằng cơ chế đọc chữ Quốc ngữ, trong khi âm đọc giữ được mức tương đồng hợp lý với phát âm nguồn.

---

## 3. Quan hệ giữa quy chuẩn và từ điển

Hai tệp có vai trò khác nhau:

### `chuan_chu_am_zo_math.md`

Quy định **phải xử lý như thế nào**.

### `tu_dien_chu_am_zo_math.yml`

Lưu **những trường hợp cụ thể đã được nghiên cứu và quyết định đến đâu**.

Nguyên tắc authority:

1. Tra từ điển trước.
2. Mục từ `approved` có thẩm quyền cao hơn suy luận mới của AI.
3. Mục từ `trial` chỉ được dùng trong phạm vi thử nghiệm đã chỉ định.
4. Nếu chưa có mục từ hoặc mục từ chưa đủ dữ liệu, áp dụng quy chuẩn này để nghiên cứu và đề xuất.
5. AI không được tự biến một đề xuất mới thành chuẩn chính thức.

---

## 4. Thuật ngữ

### 4.1. Dạng viết

Tên hoặc thuật ngữ được giữ nguyên trong văn bản chính.

Ví dụ: `Pascal`.

### 4.2. Ngôn ngữ nguồn

Ngôn ngữ được chọn làm căn cứ phát âm cho đúng thực thể hoặc đúng ngữ cảnh.

### 4.3. Phát âm nguồn

Phát âm đã được xác minh trong ngôn ngữ nguồn. Trong dữ liệu nội bộ, phát âm nguồn NÊN được lưu bằng IPA.

### 4.4. Chú âm Việt

Cách ghi gần đúng phát âm nguồn bằng chữ Quốc ngữ, được thiết kế để người Việt có thể đọc trực tiếp.

### 4.5. Mục từ

Một bản ghi trong `tu_dien_chu_am_zo_math.yml` tương ứng với **một dạng viết trong một nghĩa/ngữ cảnh xác định**.

Cùng một chuỗi chữ có thể cần nhiều mục từ nếu thực thể hoặc cách phát âm khác nhau.

---

## 5. Khi nào cần chú âm

### 5.1. NÊN chú âm

NÊN thêm chú âm khi:

- tên riêng nước ngoài có cách đọc không dễ suy ra với người đọc tiếng Việt;
- tên nhà toán học, nhà khoa học hoặc nhân vật có vai trò đáng kể trong bài;
- thuật ngữ nước ngoài được giữ nguyên dạng gốc và việc biết cách đọc giúp ích cho người học;
- cách đọc thông dụng trong tiếng Việt dễ sai đáng kể so với ngôn ngữ nguồn.

### 5.2. Không cần chú âm

Không cần chú âm khi:

- từ đã được Việt hóa hoặc có dạng tiếng Việt ổn định mà ZO Math chủ ý sử dụng;
- ký hiệu toán học, mã, tên biến, đường dẫn hoặc đoạn mã;
- từ chỉ xuất hiện trong danh mục tài liệu tham khảo hoặc dữ liệu trích dẫn;
- việc thêm chú âm làm nặng dòng chữ nhưng không đem lại lợi ích đọc hiểu rõ ràng.

### 5.3. Vị trí xuất hiện

Mặc định:

- chú âm ở **lần xuất hiện có ý nghĩa đầu tiên trong thân bài**;
- những lần sau chỉ dùng dạng viết;
- tiêu đề, phụ đề, breadcrumb, mục lục và metadata không được tính là lần xuất hiện đầu tiên;
- không lặp chú âm cơ học trong cùng một bài.

Nếu một bài rất dài và tên chỉ xuất hiện lại sau một khoảng cách lớn, người biên tập CÓ THỂ chú âm lại một lần nếu thực sự hữu ích.

---

## 6. Hình thức trình bày

### 6.1. Cú pháp chuẩn

> **Dạng viết (chú âm Việt)**

Ví dụ thử nghiệm:

> Pascal (Pát-can)

### 6.2. Dấu ngoặc

BẮT BUỘC dùng **ngoặc tròn `( )`** cho chú âm trong văn bản phổ thông.

KHÔNG ĐƯỢC dùng:

- `/ /` cho chú âm Việt;
- `[ ]` cho chú âm Việt;
- `< >` cho chú âm Việt.

Lý do: `/ /` và `[ ]` đã có chức năng chuyên môn trong mô tả phát âm; `< >` có thể được dùng để nói về hình thức chữ viết trong ngôn ngữ học. ZO Math dành ngoặc tròn cho lớp chỉ dẫn đọc phổ thông.

### 6.3. Gạch nối

BẮT BUỘC dùng dấu gạch nối giữa các âm tiết của chú âm khi chú âm có từ hai âm tiết trở lên:

> Pát-can

Gạch nối chỉ thể hiện ranh giới âm tiết của **chú âm Việt**, không nhất thiết phản ánh ranh giới hình thái hoặc cách viết của nguyên ngữ.

### 6.4. Viết hoa

- Nếu dạng viết là tên riêng, âm tiết đầu của chú âm viết hoa.
- Nếu chú âm thuộc một từ thường, cách viết hoa theo vị trí câu.
- Không viết hoa toàn bộ âm tiết để biểu thị trọng âm.

---

## 7. Xác định ngôn ngữ nguồn

KHÔNG ĐƯỢC mặc định đọc mọi tên theo tiếng Anh.

Thứ tự ưu tiên:

1. ngôn ngữ gắn với chính thực thể đang được nói đến;
2. cách tự gọi hoặc cách phát âm có căn cứ của cộng đồng/ngôn ngữ nguồn;
3. cách phát âm chuyên ngành nếu thuật ngữ đã có quy ước quốc tế đặc thù;
4. cách phát âm của ngôn ngữ trung gian chỉ khi ZO Math chủ ý dùng ngôn ngữ trung gian đó.

Ví dụ: khi nói về **Blaise Pascal**, họ `Pascal` được nghiên cứu từ phát âm tiếng Pháp, không từ cách đọc tiếng Anh.

Nếu chưa xác định chắc ngôn ngữ nguồn, mục từ phải ở trạng thái `research` hoặc `needs_review`; KHÔNG ĐƯỢC xuất bản một chú âm như thể đã chuẩn hóa.

---

## 8. Xác minh phát âm nguồn

Nguồn NÊN được ưu tiên theo thứ tự:

1. từ điển hoặc cơ quan ngôn ngữ có uy tín của ngôn ngữ nguồn;
2. nguồn học thuật hoặc từ điển phát âm có IPA;
3. bản ghi âm người bản ngữ từ nguồn đáng tin;
4. nghiên cứu ngữ âm học, âm vị học hoặc nghiên cứu từ vay liên quan;
5. nhiều nguồn độc lập dùng để kiểm tra chéo.

Đối với mục từ `trial` hoặc `approved`, BẮT BUỘC:

- có ít nhất một nguồn xác minh phát âm;
- lưu phát âm nguồn ở mức đủ để kiểm tra quyết định chú âm;
- ghi rõ nếu tồn tại nhiều cách phát âm được chấp nhận.

Không suy phát âm chỉ từ mặt chữ nếu ngôn ngữ nguồn có quan hệ chữ–âm không minh bạch.

---

## 9. Nguyên tắc cấu tạo chú âm Việt

### 9.1. Điều kiện cứng: phải đọc được bằng tiếng Việt

Mỗi âm tiết trong chú âm phải có thể được người đọc tiếng Việt phát âm trực tiếp theo cơ chế chữ Quốc ngữ.

KHÔNG ĐƯỢC tạo một chuỗi chỉ “trông giống phiên âm” nhưng không vận hành như một âm tiết tiếng Việt.

Ví dụ:

- `xcan`: không đạt;
- một cụm phụ âm mà người đọc phải biết quy tắc ngoại ngữ mới đọc được: không đạt.

“Đọc được” ở đây không có nghĩa âm tiết phải là một từ có nghĩa trong tiếng Việt; nó có nghĩa cấu trúc chữ–âm phải khả dụng đối với người đọc tiếng Việt.

### 9.2. Đi từ âm thanh, không đi từ từng chữ cái

BẮT BUỘC xây chú âm từ **phát âm nguồn đã xác minh**.

KHÔNG ĐƯỢC phiên từng chữ cái của dạng viết nếu cách đó làm xa phát âm thực tế.

### 9.3. Ưu tiên bảo toàn

Sau khi thỏa điều kiện đọc được bằng tiếng Việt, NÊN tối ưu theo thứ tự:

1. độ tương đồng tổng thể với phát âm nguồn;
2. những âm có giá trị nhận diện cao;
3. số âm tiết;
4. nhịp âm tiết;
5. nguyên âm chính;
6. phụ âm đầu;
7. phụ âm cuối;
8. tính nhất quán với các mục từ đã `approved`.

Thứ tự này là hướng dẫn đánh giá, không phải công thức máy móc.

---

## 10. Nguyên âm

NÊN chọn nguyên âm hoặc tổ hợp nguyên âm tiếng Việt gần nhất theo cảm nhận phát âm.

Khi cần so sánh, xét:

- độ mở;
- vị trí trước/sau;
- độ tròn môi;
- chất lượng nguyên âm;
- độ dài nếu sự khác biệt có giá trị nhận diện đáng kể.

KHÔNG ĐƯỢC phát minh ký hiệu mới ngoài hệ chữ dùng cho chú âm chỉ để giữ một khác biệt nhỏ của nguyên ngữ.

---

## 11. Phụ âm đầu và cụm phụ âm

Tiếng Việt hạn chế mạnh cụm phụ âm trong một âm tiết. Khi phát âm nguồn có cụm phụ âm không phù hợp với cấu trúc tiếng Việt, CÓ THỂ dùng một trong các chiến lược:

1. giữ âm có giá trị nhận diện cao hơn và lược âm kia;
2. chèn nguyên âm để tách cụm thành các âm tiết đọc được;
3. thay một âm bằng âm tiếng Việt gần hơn;
4. phối hợp các chiến lược trên nếu cần.

Việc lựa chọn phải dựa vào âm thanh và độ tự nhiên của kết quả, không dựa vào mong muốn giữ nguyên mặt chữ.

---

## 12. Phụ âm cuối

Vị trí cuối âm tiết tiếng Việt bị hạn chế. Những phụ âm cuối không tương thích với âm tiết tiếng Việt phải được xử lý.

CÓ THỂ:

1. thay bằng một phụ âm cuối tiếng Việt gần hơn;
2. lược âm;
3. tái âm tiết hóa;
4. chèn nguyên âm nếu cần bảo toàn một âm nhận diện quan trọng.

KHÔNG ĐƯỢC xây các ánh xạ tuyệt đối như:

- mọi `/l/` đều thành `n`;
- mọi `/s/` đều thành `t`.

Mỗi quyết định phải xét ngữ cảnh âm vị, toàn bộ từ và tiền lệ đã có trong từ điển.

---

## 13. Thanh điệu

Chú âm Việt phải được đọc như các âm tiết tiếng Việt; vì vậy thanh điệu là một phần của hình thức chú âm.

### 13.1. Nguyên tắc mặc định

Khi cấu trúc âm tiết cho phép và không có lý do mạnh để chọn thanh khác, NÊN ưu tiên **thanh ngang** để tránh áp một đường nét thanh điệu không tồn tại trong ngôn ngữ nguồn.

### 13.2. Âm tiết có phụ âm tắc cuối

Đối với âm tiết kết thúc bằng `-p`, `-t`, `-c/-ch`, chính tả và âm tiết tiếng Việt đặt ra những hạn chế riêng về thanh.

Khi buộc phải dùng một âm tiết kiểu này, phải chọn hình thức đọc được trong tiếng Việt và ghi lại lý do nếu lựa chọn thanh ảnh hưởng đáng kể đến độ gần âm nguồn.

### 13.3. Thanh điệu không phải trọng âm

KHÔNG ĐƯỢC dùng dấu thanh chỉ để đánh dấu trọng âm của ngôn ngữ nguồn.

---

## 14. Trọng âm và trường độ

- Không dùng CHỮ HOA để chỉ trọng âm.
- Không dùng dấu nháy hoặc ký hiệu IPA trong chú âm hiển thị.
- Không kéo dài chữ cái để mô phỏng trường độ.
- Trọng âm và trường độ được lưu trong dữ liệu phát âm nguồn khi cần.

Nếu trọng âm ảnh hưởng mạnh tới nhận diện, có thể giải thích trong ghi chú nghiên cứu nhưng không biến chú âm thành ký hiệu ngữ âm học.

---

## 15. Trường hợp có dạng tiếng Việt quy ước sẵn

Nếu một tên hoặc địa danh đã có dạng tiếng Việt/Hán–Việt/Việt hóa ổn định và ZO Math quyết định dùng dạng đó, đây là **quyết định về dạng viết**, không phải chú âm.

Ví dụ về cơ chế cần phân biệt:

- giữ dạng nước ngoài + chú âm;
- dùng dạng tiếng Việt quy ước;
- dịch nghĩa;
- chuyển tự.

Không trộn các cơ chế này trong cùng một mục từ.

---

## 16. Chữ viết không phải La-tinh

Khi dạng gốc không dùng hệ chữ La-tinh:

1. xác định ZO Math sẽ hiển thị nguyên tự dạng, một hệ chuyển tự chuẩn, hay dạng quốc tế khác;
2. tách quyết định **cách viết** khỏi quyết định **cách đọc**;
3. chú âm vẫn phải dựa trên phát âm nguồn, không dựa máy móc trên bản chuyển tự.

---

## 17. Từ viết tắt và chữ cái đọc thành tên

Acronym, initialism và tên chữ cái là trường hợp riêng.

Không suy rằng mọi chữ viết tắt đều đọc theo tiếng Anh.

Nếu cần chú âm:

- xác định nó được đọc như một từ hay đọc từng chữ cái;
- xác định ngôn ngữ dùng để đọc;
- tạo mục từ riêng trong từ điển nếu cách đọc có giá trị sử dụng lâu dài.

---

## 18. Quy trình bắt buộc cho AI

Khi AI gặp một trường hợp cần chú âm:

1. **Tra từ điển.**
2. Nếu có mục `approved`, dùng nguyên văn `vi_annotation`.
3. Nếu có mục `trial`, chỉ dùng trong `trial_scope` đã ghi.
4. Nếu có mục `needs_review` hoặc `research`, không tự coi đó là cách đọc chính thức.
5. Nếu chưa có mục:
   - xác định thực thể/nghĩa;
   - xác định ngôn ngữ nguồn;
   - tìm nguồn phát âm;
   - lưu IPA hoặc mô tả âm nguồn;
   - phân tích điểm không tương thích với tiếng Việt;
   - tạo một số ít ứng viên;
   - so sánh ứng viên theo quy chuẩn;
   - ghi mục ở trạng thái `needs_review` hoặc `research`.
6. AI có thể **đề xuất** thay đổi trạng thái nhưng KHÔNG ĐƯỢC tự đặt `approved` nếu không có chỉ thị duyệt của người có thẩm quyền trong quy trình ZO Math.
7. AI không được sửa âm chú của mục `approved` chỉ vì một lần suy luận mới cho kết quả khác; phải mở review.

---

## 19. Trạng thái mục từ

Các giá trị hợp lệ:

### `approved`

Đã được ZO Math duyệt. Được dùng tự động trong phạm vi ghi ở mục từ.

### `trial`

Đã chọn một ứng viên để thử trong nội dung thật. Chưa được dùng tự động trên toàn ZO Math.

### `needs_review`

Đã có dữ liệu và/hoặc ứng viên nhưng còn vấn đề cần quyết định.

### `research`

Đang thu thập nguồn; chưa đủ cơ sở chọn ứng viên.

### `rejected`

Chỉ dùng cho ứng viên bị bác bỏ bên trong một mục từ; không dùng làm trạng thái chính của một mục từ đang hoạt động.

---

## 20. Điều kiện chuyển sang `approved`

Một mục từ chỉ được chuyển thành `approved` khi:

- [ ] dạng viết đúng;
- [ ] thực thể/nghĩa được phân biệt rõ;
- [ ] ngôn ngữ nguồn được xác định;
- [ ] phát âm nguồn có nguồn kiểm chứng;
- [ ] chú âm gồm các âm tiết người Việt có thể đọc trực tiếp;
- [ ] không chứa cụm chữ giả ngoại ngữ;
- [ ] các biến đổi chính từ âm nguồn sang chú âm đã được giải thích;
- [ ] lựa chọn thanh điệu có chủ ý;
- [ ] đã so sánh với các ứng viên đáng kể;
- [ ] đã được đọc thành tiếng trong tiếng Việt;
- [ ] đã được thử trong ít nhất một ngữ cảnh nội dung thực nếu trường hợp có độ bất định đáng kể;
- [ ] không xung đột với mục từ `approved` khác cùng thực thể/nghĩa;
- [ ] người duyệt đã xác nhận trạng thái.

---

## 21. Hợp đồng dữ liệu của từ điển

Mỗi mục từ phải có `id` ổn định và đủ dữ liệu để con người lẫn AI hiểu đúng ngữ cảnh.

### Trường bắt buộc với mọi mục

- `id`
- `written`
- `kind`
- `source_language`
- `status`

### Bổ sung bắt buộc đối với `trial` và `approved`

- `entity_or_meaning`
- `source_pronunciation`
- `sources`
- `vi_annotation`
- `decision_notes`
- `review`

### Quy tắc dữ liệu

- `id` không thay đổi chỉ vì sửa chú âm.
- Không dùng `display_first` và `display_later` nếu có thể suy ra từ `display_policy`; tránh dữ liệu trùng lặp.
- Ngôn ngữ dùng mã BCP 47 hoặc mã ngôn ngữ ngắn rõ ràng.
- `sources` phải đủ để truy lại bằng tên nguồn, nhan đề hoặc định danh.
- Các trạng thái máy đọc dùng `snake_case`.
- YAML phải parse được bằng parser chuẩn; không dùng cấu trúc phụ thuộc trình diễn.

---

## 22. Bảo trì

Hai tệp chú âm là tài liệu sống.

- Không đánh số phiên bản trong tên tệp.
- Không duy trì nhiều bản `v1`, `v2`, `final`, `final2`.
- Git là lịch sử thay đổi.
- Khi quy tắc thay đổi, phải kiểm tra các mục `approved` có bị ảnh hưởng hay không.
- Nếu một quy tắc mới làm lung lay một mục `approved`, hạ mục đó về `needs_review` trước khi thay đổi cách dùng trên toàn site.
- Không chỉnh hàng loạt nội dung trước khi authority trong từ điển đã được cập nhật.

---

## 23. Cơ sở tham khảo

Quy chuẩn này tham khảo nhưng không sao chép máy móc các nguồn sau:

1. **Nghị định 78/2025/NĐ-CP của Chính phủ**, phụ lục về viết hoa trong văn bản quy phạm pháp luật: ghi nhận cơ chế phiên âm trực tiếp sát cách đọc của nguyên ngữ và cách dùng gạch nối trong các dạng phiên âm.
2. **Huynh Trang Nguyen & Hemanga Dutta (2017), _The Adaptation of French Consonant Clusters in Vietnamese Phonology: An OT Account_, Journal of Universal Language 18(1): 69–103**: mô tả hạn chế coda/cụm phụ âm của tiếng Việt và các chiến lược thích nghi như lược âm, chèn âm và biến đổi đoạn âm.
3. **International Phonetic Association / tài liệu ngữ âm học theo quy ước IPA**: phân biệt việc dùng `/ /` cho phiên âm rộng/âm vị và `[ ]` cho phiên âm ngữ âm chi tiết; đây là cơ sở để ZO Math không dùng hai loại ngoặc này cho chú âm phổ thông.
4. **Nguồn phát âm của từng mục từ** được ghi trực tiếp trong `tu_dien_chu_am_zo_math.yml`.

Các nguồn này là cơ sở nghiên cứu. Quyết định cuối cùng về chú âm hiển thị là quyết định biên tập nội bộ của ZO Math.
