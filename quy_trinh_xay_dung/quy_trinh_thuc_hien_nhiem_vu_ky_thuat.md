# Quy trình thực hiện nhiệm vụ kỹ thuật trong repository ZO Math
## 1. Mục đích

Quy trình này quy định cách agent tiếp nhận và thực hiện trọn vẹn một nhiệm vụ kỹ thuật trong repository ZO Math.

Mục tiêu là để người dùng tập trung vào nội dung, tư duy toán học, sư phạm và quyết định thiết kế; agent chịu trách nhiệm thực hiện các thao tác kỹ thuật trong VS Code và repository.

Agent phải tự đọc tệp, chỉnh sửa mã, chạy lệnh, đọc kết quả, xử lý lỗi trong phạm vi được giao và báo cáo kết quả. Không yêu cầu người dùng sao chép lệnh sang Terminal hoặc chuyển kết quả Terminal trở lại cuộc trò chuyện, trừ khi agent thực sự bị chặn bởi quyền hệ thống, thao tác bên ngoài VS Code hoặc một quyết định chỉ người dùng mới có thể đưa ra.

## 2. Tiếp nhận nhiệm vụ

Khi nhận nhiệm vụ, agent phải:

1. Đọc `AGENTS.md` và các tài liệu hiện hành được dẫn chiếu phù hợp với phạm vi công việc.
2. Xác định mục tiêu, phạm vi, tệp liên quan và kết quả cần đạt.
3. Phân biệt rõ:
   - nội dung ZO Math dành cho người đọc;
   - mã nguồn, tài sản và tài liệu nội bộ phục vụ xây dựng ZO Math.
4. Kiểm tra hiện trạng thực tế trước khi đề xuất hoặc thực hiện thay đổi.
5. Xác định nguồn chính thức, tệp đầu ra tự động, quan hệ phụ thuộc và phạm vi ảnh hưởng.
6. Không tự mở rộng nhiệm vụ sang các lỗi hoặc khu vực lân cận.

Nếu yêu cầu đã rõ mục tiêu, phạm vi và cho phép thực hiện, agent phải bắt đầu công việc mà không hỏi lại một cách không cần thiết. Một yêu cầu bằng ngôn ngữ tự nhiên đã đủ để khởi động nhiệm vụ trong dự án đã được tích hợp; agent tự xác định lệnh và tài liệu cần dùng, không yêu cầu người dùng dịch yêu cầu thành cú pháp kĩ thuật. Nếu không tìm thấy cấu hình dự án hoặc loại bài phù hợp, phải dừng ở bước khảo sát và báo đây là nhiệm vụ tích hợp dự án mới.

Agent chỉ dừng để hỏi khi:

- thiếu một quyết định về nội dung, toán học, sư phạm hoặc thiết kế;
- có hai nguồn chỉ dẫn cùng cấp mâu thuẫn;
- thao tác có nguy cơ phá hủy dữ liệu hoặc vượt phạm vi đã giao;
- không thể xác định chắc chắn nguồn cần sửa;
- kết quả có nhiều cách hiểu và không thể chọn một phương án tốt nhất từ các quy tắc hiện hành.

## 3. Khảo sát trước khi sửa

Trước khi thay đổi tệp, agent phải khảo sát đủ để trả lời:

- Tệp nào là nguồn cần sửa?
- Tệp nào được sinh tự động?
- Thành phần này đang được cấu hình hoặc nạp từ đâu?
- Có quy tắc, token, class, helper, script hoặc component hiện có để tái sử dụng không?
- Thay đổi có thể ảnh hưởng đến những trang, đầu ra hoặc công cụ nào?
- Repository hiện có những thay đổi chưa commit nào cần tránh đụng vào?

Agent được tự chạy các lệnh chỉ đọc cần thiết để khảo sát.

Không coi ngày sửa tệp, tên tệp hoặc tài liệu cũ là bằng chứng đủ để xác định nguồn có thẩm quyền.

## 4. Trình bày phương án

Trước thay đổi quan trọng, agent phải trình bày ngắn gọn:

- nguyên nhân hoặc hiện trạng đã xác định;
- tệp dự kiến sửa;
- cách thực hiện;
- phạm vi ảnh hưởng;
- cách kiểm tra sau khi sửa.

Chỉ trình bày một phương án tốt nhất.

Không cần trình bày lại phương án đối với thao tác nhỏ, hiển nhiên và đã được yêu cầu trực tiếp, miễn là thao tác đó không làm thay đổi nội dung, kiến trúc hoặc thiết kế đã được chốt.

## 5. Thực hiện thay đổi

Trong quá trình thực hiện, agent phải:

1. Chỉ sửa những tệp cần thiết cho mục tiêu.
2. Giữ diff nhỏ, rõ và có thể kiểm tra.
3. Không tiện tay dọn dẹp, đổi định dạng, tái cấu trúc hoặc sửa lỗi ngoài phạm vi.
4. Không chỉnh trực tiếp đầu ra tự động khi đã xác định được nguồn sinh.
5. Tái sử dụng hệ thống hiện có trước khi tạo class, component, màu, helper, script hoặc quy ước mới.
6. Không tự thay đổi ý nghĩa toán học, lập luận, mục tiêu sư phạm, cấu trúc nhận thức hoặc giọng văn.
7. Đặt tệp tạm, bản chụp, script kiểm tra và báo cáo phát sinh trong `_audit/`, trừ khi nhiệm vụ quy định nơi khác.
8. Ưu tiên đường dẫn tương đối và cấu hình có thể dùng trên máy khác.
9. Không tự động commit, push, restore, xóa hoặc di chuyển tệp nếu chưa được người dùng yêu cầu rõ.

### Chạy lệnh Python

Lệnh Python trong quy trình kỹ thuật phải đi qua trình khởi chạy repository-local. Cú pháp chuẩn là:

```text
python scripts/zo_python.py script.py [tham số...]
python scripts/zo_python.py -m module [tham số...]
```

Khi đã dùng trình khởi chạy, không thêm thủ công `PYTHONUTF8=1` vào từng lệnh. Trình khởi chạy chỉ bảo đảm chế độ UTF-8 cho tiến trình Python con; nó không thay đổi logic hoặc dữ liệu của script đích. Báo cáo kết quả phải ghi đúng lệnh thực tế đã dùng.

### Chạy lệnh Quarto

Lệnh Quarto phải đi qua trình khởi chạy repository-local theo cú pháp:

```text
python scripts/zo_python.py scripts/zo_quarto.py <quarto-command> [tham số...]
python scripts/zo_python.py scripts/zo_quarto.py render PAGE
```

Lệnh `render` của lớp vận hành QMD điều phối checker lõi, và checker dùng cùng cơ chế chuẩn bị môi trường. Không đặt thủ công `QUARTO_PYTHON` hoặc `RETICULATE_PYTHON` trong từng lệnh và không ghi đường dẫn Python cá nhân vào metadata QMD. Trình khởi chạy chọn Python hiện hành cho Jupyter và reticulate, đồng thời giữ nguyên giá trị mà người gọi đã chủ động cung cấp. Báo cáo cuối phải ghi đúng lệnh thực tế đã chạy.

### Kiểm định kĩ thuật thống nhất

Với bài QMD thuộc hệ thống có cấu hình, dùng điểm vào vận hành:

```text
python scripts/zo_python.py scripts/zo_qmd.py check <pham-vi-qmd>...
python scripts/zo_python.py scripts/zo_qmd.py render <pham-vi-qmd>...
```

- `check` điều phối kiểm định nguồn cho một hoặc nhiều phạm vi tường minh;
- `render` chỉ dùng khi nhiệm vụ cần dựng và kiểm định đầu ra;
- `--staged` chỉ dùng khi cần kiểm tra vùng staged;
- `--report` chỉ dùng khi báo cáo JSON máy đọc được trong `_audit/` thực sự hữu ích.

`scripts/zo_check_repo.py` là checker lõi được lớp vận hành gọi phía sau. Chỉ gọi trực tiếp `quick`, `scope` hoặc `render` khi nhiệm vụ là bảo trì, chẩn đoán checker, hoặc kiểm tra kĩ thuật ngoài vòng đời một bài QMD có cấu hình; phải nêu rõ lí do trong báo cáo.

Công cụ kiểm định không tự sửa lỗi, stage hoặc commit. Trước commit, agent vẫn phải đọc diff, xác nhận phạm vi Git và thực hiện các kiểm tra staged phù hợp.

Agent chịu trách nhiệm tự chạy các lệnh kỹ thuật cần thiết. Không chuyển việc vận hành Terminal cho người dùng chỉ vì thao tác đó có thể được thực hiện bằng lệnh.

### Vòng đời thư mục `_audit/`

`_audit/` dùng để chứa đầu ra kiểm tra, báo cáo, bản chụp, log, preview và mẫu thử tạm thời; đây không phải nơi chứa nguồn thực thi chính thức. Script hoặc công cụ cần sử dụng lâu dài phải được đặt trong `scripts/`, được kiểm định và được Git theo dõi. Không dùng tệp trong `_audit/` làm nguồn duy nhất cho build, render, sinh dữ liệu hoặc vận hành repository.

Agent được tạo tệp tạm trong `_audit/` khi nhiệm vụ cần. Trước khi kết thúc nhiệm vụ, agent phải:

1. xóa mẫu thử, log và preview không còn cần thiết;
2. xóa đầu ra có thể tái tạo khi chúng không còn phục vụ đối chiếu;
3. xác nhận không còn thư mục tạm hoặc cache do nhiệm vụ tạo ra;
4. chỉ giữ báo cáo hiện hành do công cụ kỹ thuật trực tiếp tạo hoặc báo cáo mà nhiệm vụ vẫn cần đối chiếu.

Hồ sơ lịch sử, bản nháp, script patch dùng một lần và phiên bản cũ cần bảo toàn phải được chuyển ra vùng lưu trữ ngoài repository, không tích lũy lâu dài trong `_audit/`. Khi chuyển tệp cần bảo toàn, phải chép và xác minh SHA-256 của bản đích trước khi xóa nguồn.

Không stage hoặc commit nội dung `_audit/` khi thư mục này vẫn được `.gitignore` loại trừ. Nếu nhiệm vụ đã tạo hoặc sử dụng tệp trong `_audit/`, báo cáo cuối phải xác nhận tình trạng các tệp tạm liên quan.

Đường biên dịch chính thức phải chạy được từ nguồn mà không có lịch sử
`_audit/`. `scripts/zo_build_boundary.py` kiểm đầu vào trước render; launcher
Quarto bật guard đọc tệp cho các tiến trình Python con (hook và kernel), kể cả
qua `scripts/zo_python.py`, bằng runtime cục bộ `scripts/zo_build_runtime/`.
Nguồn include, filter, template, tài nguyên và mã thực thi không được lấy
từ `_audit/`, kể cả qua đường dẫn vòng hoặc alias. Đầu ra báo cáo mới có thể
ghi tại đó; việc đọc báo cáo để xem xét nghiệm thu là một bước kiểm định riêng,
không trở thành đầu vào sinh nội dung. Fixture dùng lâu dài thuộc
`scripts/fixtures/`; so bản lịch sử phải nhận đầu vào tường minh, không tự
chọn thư mục theo ngày hoặc tên `current` trong `_audit/`.
Tệp trung gian biên dịch PDF và vector chính thức dùng `.quarto/`, tự dọn
theo vòng đời công cụ; `_audit/` chỉ giữ đầu ra kiểm định và bằng chứng.

## 6. Xử lý lỗi trong quá trình làm việc

Khi lệnh hoặc kiểm tra thất bại, agent phải:

1. Đọc đầy đủ thông báo lỗi.
2. Xác định lỗi có thuộc phạm vi nhiệm vụ hay không.
3. Nếu thuộc phạm vi, tự sửa và chạy lại kiểm tra.
4. Nếu không thuộc phạm vi, không tự sửa; ghi nhận rõ trong báo cáo.
5. Không che giấu cảnh báo hoặc coi lệnh thành công khi chưa kiểm tra mã thoát và đầu ra cần thiết.
6. Không lặp lại cùng một thao tác thất bại mà không thay đổi giả thuyết hoặc cách xử lý.

Khi cần chạy lệnh ngoài sandbox hoặc cần người dùng phê duyệt, agent phải nêu rõ:

- lệnh sẽ chạy;
- mục đích;
- thao tác chỉ đọc hay có ghi dữ liệu;
- phạm vi ảnh hưởng;
- lý do cần vượt giới hạn hiện tại.

## 7. Kiểm tra sau thay đổi

Agent phải chọn kiểm tra phù hợp với loại nhiệm vụ, không chạy máy móc mọi kiểm tra của toàn repository.

Tối thiểu phải xác nhận:

1. Tệp yêu cầu đã được sửa đúng.
2. Không có tệp ngoài phạm vi bị thay đổi.
3. Cú pháp hoặc cấu trúc liên quan hợp lệ.
4. Lệnh build, render, compile hoặc script mục tiêu hoàn thành, nếu nhiệm vụ cần.
5. Các cảnh báo và lỗi đã được đọc.
6. Đầu ra được sinh từ nguồn đã đồng bộ, nếu có.
7. Diff không chứa thay đổi ngoài ý muốn, tàn dư lệnh, lỗi EOL hoặc khoảng trắng đáng chú ý.
8. Kết quả đáp ứng mục tiêu đã giao.

Khi nhiệm vụ tác động đến giao diện, kiểm tra kỹ thuật không thay thế cho đánh giá trực quan. Agent phải xác định trang hoặc đầu ra cần người dùng xem và mô tả rõ nội dung cần duyệt.

### 7.1. Đường cập nhật tối thiểu cho sửa đổi nhỏ

Áp dụng ngay khi tiếp nhận yêu cầu sửa, không đợi người dùng nhắc về thời gian.
Trước khi ghi tệp, xác định ngắn gọn: nguồn cần sửa → đầu ra chịu ảnh hưởng →
phép kiểm cần chạy → điều kiện dừng. Đây là bước chọn phạm vi, không phải yêu
cầu lập thêm hồ sơ hoặc xin duyệt lại việc đã được giao.

- Chỉ đọc chỉ dẫn bắt buộc và phụ thuộc liên quan; tái sử dụng thông tin đã đọc
  trong phiên nếu không có dấu hiệu thay đổi. Không khảo sát lại toàn dự án.
- Tài liệu quản lý thuần văn bản: đọc diff và kiểm liên kết/quy tắc liên quan;
  không render học liệu. Nội dung một trang: kiểm nguồn và render đúng trang,
  đúng định dạng cần xem. Đổi ảnh: sinh/cập nhật đúng ảnh và trang sử dụng nó;
  không dựng lại các hình toán, bảng biến thiên hoặc PDF không chịu ảnh hưởng.
- Tận dụng lựa chọn phạm vi và chế độ HTML-only đang có. Không render cả thư
  mục chỉ vì ví dụ lệnh trong hướng dẫn dùng tên thư mục. Không bỏ các cổng
  bắt buộc của lệnh đã chọn để đạt tốc độ.
- Tái sử dụng tài nguyên/bằng chứng còn phù hợp khi đầu vào và phụ thuộc của
  chúng không đổi; không coi PASS cũ là PASS cho phần vừa sửa. Giữ các phép
  kiểm toàn vẹn nhẹ vốn nằm trong adapter; kiểm hash không đồng nghĩa tái dựng.
- Kiểm tự động trước, xem trực quan vùng thay đổi sau. Khi đã đạt điều kiện
  dừng thì bàn giao; chỉ lặp lại khi có thay đổi mới, lỗi hoặc nghi vấn cụ thể.
- Chỉ mở rộng kiểm tra khi thay đổi thành phần dùng chung, phát hiện phụ thuộc
  bị ảnh hưởng hoặc có yêu cầu nghiệm thu/phát hành tương ứng. Nêu căn cứ mở
  rộng. Không ghép chuẩn hóa, tái cấu trúc hay cải tiến công cụ vào sửa nhỏ.

Ghi thời gian thực tế của từng bước chạy đáng kể (kiểm nguồn, sinh tài nguyên,
render, kiểm đầu ra) bằng đồng hồ của công cụ hoặc bộ đo thời gian của shell;
phân biệt với thời gian khảo sát/biên tập. Báo ngắn bước chậm và số lần chạy lại
khi có chậm trễ; không suy đoán lỗi công cụ từ tổng thời gian hội thoại. Không
chạy thêm build chỉ để đo. Không đặt cam kết số phút khi chưa có số đo.

## 8. Điều kiện hoàn thành nhiệm vụ

Một nhiệm vụ kỹ thuật chỉ được xem là hoàn thành khi:

- mục tiêu đã được thực hiện trong đúng phạm vi;
- các kiểm tra phù hợp đã chạy;
- lỗi thuộc phạm vi đã được xử lý;
- các giới hạn hoặc vấn đề còn lại đã được nêu rõ;
- không có thay đổi ngoài ý muốn;
- người dùng nhận được báo cáo đủ để đánh giá mà không phải tự khảo sát lại repository.

Agent không được tuyên bố hoàn thành chỉ vì đã sửa mã. Việc kiểm tra là một phần của nhiệm vụ.

## 9. Báo cáo kết quả

Báo cáo cuối nhiệm vụ phải ngắn gọn và gồm:

### Kết quả

Mô tả điều đã thực hiện và trạng thái đạt được.

### Tệp đã thay đổi

Liệt kê chính xác các tệp được tạo, sửa, xóa hoặc tái sinh.

### Kiểm tra đã chạy

Liệt kê các lệnh hoặc kiểm tra quan trọng và kết quả của chúng.

### Nội dung cần người dùng duyệt

Chỉ nêu những quyết định, đánh giá trực quan hoặc vấn đề mà agent không thể tự kết luận.

### Giới hạn còn lại

Nêu rõ lỗi, cảnh báo hoặc vấn đề chưa xử lý, nếu có. Không tạo mục này khi không còn giới hạn đáng kể.

Không kể lại toàn bộ quá trình suy luận nội bộ và không đưa một danh sách dài các khả năng không cần thiết.

### 9.1. Bàn giao và mở lại bản xem HTML trên máy

Liên kết `http://127.0.0.1:<cổng>/...` chỉ hoạt động khi máy chủ trên chính máy đó đang chạy. Kết sổ ngày hoặc khởi động lại máy có thể dừng tiến trình dù HTML còn nguyên. Không xem một lần HTTP 200 là bảo đảm liên kết luôn mở được; nhấp liên kết trình duyệt không tự khởi động máy chủ.

- Bàn giao phải ghi đường dẫn HTML thật, URL, cổng và cách mở lại. Dùng `scripts/zo_html_preview.py` qua launcher; công cụ đọc HTML có sẵn, kiểm SHA-256 nội dung HTTP đúng tệp, tái dùng máy chủ đúng hoặc khởi động máy chủ nền chỉ ở `127.0.0.1`. Cổng đang phục vụ nội dung khác thì báo rõ, không giết tiến trình hoặc tự đổi cổng làm hỏng liên kết đã bàn giao.
- Khi người dùng yêu cầu “mở lại bản xem HTML” hoặc báo không xem được, agent kiểm tệp trước rồi tự chạy lệnh mở lại; không yêu cầu người dùng dựng trang hoặc tự vận hành Terminal. Không tự khôi phục snapshot đã lưu kho để thay nguồn hiện hành. Tệp mất thì đối chiếu biên nhận trước, ghi rõ thiếu tệp.
- Khi bàn giao bản xem trên Windows, thêm `--shortcut` để tạo `Mo_ban_xem_HTML.cmd` cạnh trang đầu vào. Người dùng có thể nhấp đúp tệp ấy trong File Explorer sau khi khởi động máy; tệp gọi công cụ canonical, chờ HTTP đúng nội dung rồi mở trình duyệt mặc định. Không cài dịch vụ hay tác vụ tự khởi động Windows. Nếu dùng Codex, agent có thể thêm `--no-browser`, xác minh rồi mở URL trong panel.

```text
python -B scripts/zo_python.py -B scripts/zo_html_preview.py --page <HTML-tuong-doi-tu-repo> --port 8877 --shortcut
```

`--no-browser` chỉ kiểm/khởi động máy chủ và in URL. Hai cờ `-B` tắt sinh bytecode ở cả launcher và tiến trình con, tránh tạo lại cache khi xác minh kết sổ. Công cụ mở lại không render, sửa HTML/PDF, cấp nghiệm thu, commit hoặc xuất bản.

Trước kết sổ, bảo vệ trang đầu vào, toàn bộ HTML/tài nguyên liên kết, tệp mở nhanh và bằng chứng còn cần duyệt bằng `--protect`/manifest của `zo_end_day.py`; không chỉ giữ mỗi URL. Kiểm tệp mở nhanh còn gọi được công cụ canonical sau khi chuyển mirror/cache ra kho. Biên nhận kết sổ phải phân biệt bảo toàn tệp với tiến trình máy chủ: không hứa localhost còn chạy sau reboot; ghi cách mở lại và phần chờ duyệt. Không tự đóng máy chủ của phiên khác.

Kiểm phụ thuộc theo chuỗi HTML → CSS → CSS nhập/font/ảnh và tệp tải xuống, kể cả khi nằm ngoài thư mục chứa trang, bằng `scripts/zo_html_dependencies.py`. Cổng bàn giao dùng cùng tập này để khóa hash và kiểm HTTP. Cổng kết sổ tự mở rộng bảo vệ theo phụ thuộc thật và chặn kế hoạch lưu kho bất kỳ tệp nào trong chuỗi; thư mục tên `delivery` không tự là bản trung gian được phép dọn. Thiếu tài nguyên của trang được bảo vệ thì scan phải thất bại. Sau dọn phải chạy lại cổng bàn giao khi gửi lại liên kết, không dùng trạng thái Git sạch hoặc tệp shortcut còn tồn tại làm bằng chứng bản xem hoạt động.

Kiểm chống tái diễn: `python -B scripts/zo_python.py -B scripts/zo_html_preview_selftest.py` dùng máy chủ thật để kiểm khởi động lại sau khi dừng, mở lặp không tạo máy chủ thừa, cổng sai, tài nguyên tương đối, HTML thiếu/sai đường dẫn và tệp mở nhanh. Chỉ mở bản đã dựng, không dựng học liệu để kiểm khởi động máy chủ.


#### Cổng bắt buộc ngay trước mỗi lần bàn giao

Mỗi lần gửi hoặc gửi lại liên kết HTML, kể cả trả lời “bước tiếp theo”, phải thực hiện mới đủ ba bước. PASS cũ, tệp HTML tồn tại, HTTP 200 hoặc `browser_requested=true` không thay thế bước nào. Lần trước đã mở được không chứng minh lần này máy chủ còn chạy.

1. **Chuẩn bị đúng bản hiện hành.** Chạy `zo_html_handoff.py prepare` qua launcher với tài liệu điều hành có thẩm quyền. Liên kết localhost trỏ `_audit/...html` đầu tiên trong tài liệu ấy là bản đang vận hành; các liên kết sau là lịch sử. Đây là hợp đồng trình bày của tài liệu điều hành, không chọn theo tên thư mục hoặc ngày sửa. Công cụ khởi động/tái dùng máy chủ, so SHA-256 HTTP với trang đầu, tất cả trang trong hub và tài nguyên trực tiếp, tạo shortcut và biên nhận mới có mã phiên. Thiếu/sai nội dung thì dừng, không bàn giao.
2. **Mở và quan sát bằng trình duyệt.** Agent mở đúng URL biên nhận trong trình duyệt người dùng, nhìn thấy nội dung thật; nếu là hub thì mở thêm một trang nội dung thuộc bộ ấy. Thu snapshot có URL/tiêu đề và ảnh chụp PNG/JPEG của mỗi trang đã quan sát, ghi giờ quan sát sau giờ chuẩn bị cùng mã phiên vào JSON bằng chứng. Kiểm không có trang lỗi/trắng, xác nhận nội dung hiển thị; không lấy log HTTP hoặc ảnh chụp lịch sử làm bằng chứng trình duyệt. Trong Codex, gọi `markDeliverable()` để tab bàn giao còn mở khi kết thúc lượt. Nếu công cụ trình duyệt không hoạt động, báo “đã kiểm HTTP, chưa xác nhận xem được”; không tự điền đã xem hoặc tuyên bố bàn giao đạt.
3. **Khép và kiểm lại ngay trước câu trả lời.** Chạy `confirm`, sau đó `check` trên biên nhận đã xác nhận. Cổng bắt buộc bằng chứng bước hai, đúng URL hiện hành, đúng hash, máy chủ vẫn phục vụ đúng nội dung; từ chối biên nhận quá mười phút, bản cũ, nguồn HTML đổi hoặc bằng chứng bị thay. Sau thời hạn phải chuẩn bị và quan sát lại, không gia hạn timestamp. Chỉ gửi trạng thái “xem được” khi `handoff_ready=true`. Không coi thao tác mở trình duyệt thành nghiệm thu nội dung hoặc xuất bản.

```text
python -B scripts/zo_python.py -B scripts/zo_html_handoff.py prepare --authority <tai-lieu-dieu-hanh.md> --report _audit/<phien>/prepared.json
# Mở URL, quan sát trang đầu + trang nội dung; lưu snapshot/PNG hoặc JPEG và browser.json.
python -B scripts/zo_python.py -B scripts/zo_html_handoff.py confirm --report _audit/<phien>/prepared.json --evidence _audit/<phien>/browser.json --output _audit/<phien>/confirmed.json
python -B scripts/zo_python.py -B scripts/zo_html_handoff.py check --report _audit/<phien>/confirmed.json
```

JSON bằng chứng gồm `nonce` của biên nhận, `observed_at` (UTC Unix giây), và `visits`: mỗi lần mở có `page` (đường dẫn repo), `url`, `title`, `snapshot`, `screenshot` (hai đường dẫn repo) và `visible_content_confirmed: true`. Chỉ ghi xác nhận sau quan sát thật. Cổng kiểm tính mới/toàn vẹn của bằng chứng; trách nhiệm đánh giá trang nhìn thấy vẫn thuộc agent. Dùng tệp báo cáo mới, không ghi đè lịch sử. `zo_html_preview.py` và shortcut chỉ phục vụ mở lại, luôn trả `handoff_ready=false` vì chưa có bằng chứng quan sát.

Chạy hồi quy `zo_html_preview_selftest.py` và `zo_html_handoff_selftest.py` qua launcher khi sửa cơ chế: máy chủ dừng/sai nội dung, bản cũ, biên nhận hết hạn, HTML đổi, chỉ mở hub, URL sai, trang lỗi, thiếu ảnh, bằng chứng sai phiên hoặc bị sửa phải bị chặn. Không dựng lại học liệu để kiểm cơ chế bàn giao.

## 10. Những việc agent không chuyển lại cho người dùng

Trong điều kiện VS Code, repository và công cụ đang hoạt động bình thường, agent không được yêu cầu người dùng:

- tự tìm tệp liên quan;
- tự chép và chạy lệnh Terminal;
- tự gửi lại log mà agent có thể đọc;
- tự kiểm tra Git status hoặc diff;
- tự tạo tệp audit;
- tự sửa những lỗi kỹ thuật thuộc phạm vi đã giao;
- tự lặp lại các bước mà agent có thể thực hiện trực tiếp.

Người dùng giữ quyền quyết định về:

- nội dung và ý nghĩa toán học;
- mục tiêu sư phạm;
- cấu trúc nhận thức;
- nguyên tắc và ngoại lệ thiết kế;
- đánh giá thẩm mỹ;
- commit, push, xuất bản hoặc thao tác phá hủy khi chưa được ủy quyền.

## 11. Agent kết sổ cuối ngày — toàn ZO Math

### Kích hoạt và giới hạn ủy quyền

Người dùng chỉ cần nói **"Kết thúc ngày làm việc"** trong phiên agent đang
làm việc với repository. Đây là yêu cầu tường minh để agent kiểm kê toàn
repository, tạo commit cục bộ theo từng nhóm nguồn đã phân loại, và chuyển
tệp tạm không còn cần ra kho ngoài repository sau khi xác minh SHA-256.
Không cần hỏi lại quyền thực hiện các thao tác đã nằm trong phạm vi này.

Yêu cầu xây dựng cơ chế, hỏi tình trạng hoặc việc agent kết thúc một nhiệm vụ
không phải yêu cầu kết sổ. Không tự hẹn giờ hay tự suy đoán thời điểm kết thúc.
Không push, xuất bản, reset, stash, đổi nhánh, bỏ qua hook Git hoặc ép xóa.
Commit bảo toàn không xác nhận nghiệm thu, đọc hiểu của học sinh hay duyệt thị
giác. Công việc chưa xong vẫn được lưu với nhãn `wip(eod)` và lỗi đã biết;
nhóm đã kiểm kỹ thuật dùng `checkpoint(eod)`, không gọi là đã nghiệm thu.

### Trình tự agent tự thực hiện

1. Xác nhận không có phiên khác đang ghi vào cùng checkout. Nếu có hoặc
   chưa rõ người sở hữu thay đổi, dừng phần ghi và báo đúng chỗ cần xác nhận;
   không tự đóng hoặc nhắn phiên khác. Đọc chỉ dẫn từ ngoài vào trong cho mọi
   phạm vi liên quan, diff nguồn và hồ sơ điều hành hiện hành.
2. Kiểm kê Git và **cả tệp bị Git bỏ qua** bằng `scan`. Xác định các bản đã
   duyệt, bản đang chờ xem, bằng chứng và toàn bộ tài nguyên phục vụ chúng;
   truyền các vùng bảo vệ qua `--protect` hoặc manifest qua
   `--protect-manifest`. Không tái dùng danh sách xóa hay hash của lần cũ.
   Không coi mọi tệp trong `_audit/` là rác. Không dùng việc giữ bằng chứng
   làm lý do cho phép biên dịch chính thức đọc `_audit/`.
   Với bản xem HTML, áp dụng mục 9.1: bảo vệ cả tệp mở nhanh và tài nguyên;
   ghi cách mở lại máy chủ sau reboot, không chỉ bảo toàn URL.
3. Tự hoàn thiện kế hoạch: `instructions_reviewed`, `protection_reviewed`,
   các `groups`, quyết định `keep`/`archive` có lý do. Mỗi thay đổi nguồn
   thuộc đúng một nhóm, có danh sách tệp chính xác, thông điệp và trạng thái
   `in_progress` hoặc `checked`. Ghép xóa/tạo của việc đổi tên trong cùng
   nhóm. `checked` phải ghi kiểm tra thực tế ở `verification`; kiểm QMD dùng
   điểm vào và hợp đồng hiện hành, không tự render toàn repo. Ghi kết quả
   kiểm tra và quyết định bền vững vào hồ sơ đúng thẩm quyền trước khi chốt;
   không tự nâng quyết định của dự án con thành quy tắc toàn hệ thống.
4. Phân loại mọi tệp bị bỏ qua. Giữ bản cần dùng hiện hành cùng phụ thuộc;
   chuyển cache, báo cáo thừa và lịch sử không còn phục vụ công việc ra kho
   ngoài repo. Không đoán chỉ từ tên "old", "retry" hay thời gian sửa.
   Nguồn hữu ích bị ignore nhầm phải được xử lí theo quản lý nguồn hiện hành,
   không cất như rác. Không tự xử lí bí mật hoặc metadata hệ thống.
5. Chạy `check` rồi `apply` với kế hoạch hiện hành. Kho ngoài repo phải là
   thư mục riêng, không phải gốc ổ đĩa hay thư mục cha chứa repo. Dùng kho
   đã xác định nếu có; nếu chưa có, đề xuất đường dẫn anh em
   `<ten-repo>_archives/end_day` và xin quyền filesystem khi cần. Cờ
   `--authorized-day-close` chỉ được dùng khi đã có yêu cầu trực tiếp của
   người dùng; cờ không tự tạo ra quyền. Công cụ không tự nâng quyền.
6. Đọc biên nhận ngoài repo, đối chiếu trạng thái cuối và báo ngắn:
   repo đã kết sổ hay chưa, commit bảo toàn, nơi lưu trữ và việc cần tiếp tục.
   Nếu còn tệp chưa phân loại, lỗi quyền hoặc writer đồng thời, báo **chưa
   kết sổ**, không lặp thao tác phá hủy để cố đạt trạng thái sạch.

### Công cụ và kế hoạch

Các lệnh agent vận hành, không chuyển cho người dùng:

```text
python scripts/zo_python.py -B scripts/zo_end_day.py scan --summary
python scripts/zo_python.py -B scripts/zo_end_day.py scan --protect <vung-can-giu> --output _audit/end-day-plan.json
python scripts/zo_python.py -B scripts/zo_end_day.py check --plan _audit/end-day-plan.json
python scripts/zo_python.py -B scripts/zo_end_day.py apply --plan _audit/end-day-plan.json --archive-root <kho-ngoai-repo> --authorized-day-close
python scripts/zo_python.py -B scripts/zo_end_day_selftest.py
```

`scan` không có `--output` và `check` chỉ đọc. Kế hoạch mới phải nằm trong
`_audit/`, là dữ liệu thao tác tạm, không phải đầu vào biên dịch chính thức.
`groups` dùng `{state, message, paths, verification}`; `keep`/`archive` dùng
`{path, reason}` với tệp hoặc tiền tố thư mục tương đối, không dùng glob.
Manifest bảo vệ có dạng `{"files": [{"path": "duong/dan/tuong/doi"}]}`;
hash hiện tại của manifest được khóa trong kế hoạch. Hash lịch sử không
được mặc nhiên coi là hash của nguồn hiện tại.

Công cụ khóa kế hoạch với repo, HEAD, nhánh, danh sách thay đổi và SHA-256;
chặn staged có sẵn, xung đột, đường dẫn thoát repo, symlink/reparse point,
archive bản được bảo vệ, quyết định thiếu hoặc chồng lấn. Chỉ stage danh
sách tệp cụ thể, không `git add .`. Nó không tự biết ý nghĩa nội dung hoặc
ai đã duyệt: bước đọc hồ sơ và phân loại thuộc trách nhiệm agent.

Kho ngoài repo lưu `plan.json`, `manifest.json`, `result.json` và `payload/`.
Mọi bản chép được xác minh trước khi xóa tệp gốc; không xóa đệ quy toàn
thư mục. Biên nhận ghi commit, trạng thái kỹ thuật, lỗi và các tệp giữ lại.
Kế hoạch tạm trong repo chỉ được bỏ sau khi kết sổ thành công. Nếu lỗi giữa
chừng, giữ biên nhận và mọi kết quả đã tạo, không rollback phá hủy.

Khôi phục khi cần là nhiệm vụ riêng: chép tệp từ `payload/<duong-dan-cu>`
về đúng vị trí sau khi đối chiếu manifest và tránh ghi đè nguồn mới; lấy
nguồn từ commit ghi trong biên nhận khi cần. Không tự restore toàn repo.

### Thế nào là sạch sau kết sổ?

Không còn thay đổi nguồn chưa commit; mọi tệp bị bỏ qua đã có lý do giữ
hoặc đã chuyển ra kho có hash kiểm chứng; bản cần duyệt và tài nguyên của
nó còn nguyên. **Sạch không có nghĩa là `_audit/` rỗng** hay mọi nội dung đã
hoàn thành. Không che rác bằng cách mở rộng `.gitignore`.

Kiểm thử hồi quy chạy trên Git repo giả lập tách biệt trong thư mục tạm,
không commit hay dọn nguồn thực. Cơ chế này chỉ được agent kích hoạt sau
yêu cầu người dùng; không phải dịch vụ nền hoặc hook tự động của ứng dụng.


### Bảo vệ tự động bản đang duyệt — hiệu chỉnh 19/10/2026

Sau mỗi bàn giao HTML/PDF chờ duyệt, cập nhật manifest máy đọc `content/**/_quy_trinh/ban_dang_duyet.json` trong phạm vi điều hành hiện hữu. Manifest không là nguồn biên dịch và không thay tài liệu điều hành: ghi `status: pending_owner_review`, các `entrypoints` và danh sách `files` có đường dẫn tương đối/SHA-256. Danh sách gồm bản xem, PDF tải, CSS, JS/module, phông, hình, tài nguyên được bộ dựng khai báo và đường mở lại; tệp nguồn chính thức vẫn được bảo toàn bằng cơ chế quản lý nguồn. Không cất ý tưởng hoặc mã sinh chỉ trong bản xem.

`zo_end_day.py scan/check/apply` tự phát hiện manifest đang duyệt, không phụ thuộc agent có nhớ truyền `--protect` hay không. Kiểm tiếp phụ thuộc HTML/CSS/JS/SVG, chặn tệp thiếu, đổi hash, đường dẫn thoát repo, symlink, kế hoạch lỗi thời và mọi ý định archive tệp được bảo vệ. Xóa manifest khỏi kế hoạch không làm kế hoạch cũ hợp lệ. Chỉ bỏ trạng thái cần bảo vệ sau khi có quyết định xử lý bản duyệt; không coi kết phiên là hết giá trị. Yêu cầu cập nhật cổng không cho phép thực hiện kết sổ, commit hoặc archive trên repo thật.


Bản xem localhost đứng đầu tài liệu điều hành 03 phải có trong `entrypoints` của manifest đang duyệt. Cổng kết sổ chặn cả trường hợp quên tạo manifest hoặc chỉ giữ manifest của bản xem cũ. Bảo vệ thêm các nguồn và bộ sinh cần tái tạo bản duyệt, kể cả tệp mới chưa commit; tệp mở lại phải dùng công cụ hiện hành. Lưu danh mục/hash phụ thuộc ngoài repo trong hồ sơ đồng bộ, không chuyển chúng vào thư mục tạm rồi coi là đã bảo toàn nguồn.

Khi sửa bộ sinh PDF: dựng và xem bản đầy đủ trước để phát hiện lỗi phân cấp, chú thích, hình trôi hoặc tách trang; sau đó mới dựng các biến thể. Chỉ dựng HTML chứa thẻ tải PDF sau khi mọi PDF đã qua cổng nguồn hiện hành. Khóa trạng thái nguồn trong lúc dựng; nguồn đổi giữa chừng phải từ chối bản trộn. Số trang trên thẻ tải lấy từ PDF thật, không chép lại số trang lịch sử. Cập nhật chỉ số trang phải có đối chiếu xác nhận toàn bộ chính văn và metadata khác không đổi; giữ nguyên bằng chứng nghiệm thu lịch sử.
