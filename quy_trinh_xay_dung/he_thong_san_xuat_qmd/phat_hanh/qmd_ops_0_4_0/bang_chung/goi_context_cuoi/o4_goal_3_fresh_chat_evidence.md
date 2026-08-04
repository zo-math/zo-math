# Bằng chứng Mục tiêu 3 — Chat-box mới chỉ dùng gói context cuối

## Gói được thử

- Package ID: `qmd-context-20260804-031754`
- Commit nguồn: `335fbbeb1b631eecc642fbeb05bd6644025cd87e`
- Tệp: `o4_final_context_20260804_031748.zip`
- SHA-256: `4aa49bafdd10740d000af09bd7bde7f79380a707e2020316a77b614c4e98b848`

## Điều kiện thử

Một chat hoàn toàn mới chỉ nhận gói context cuối và lời nhắn:

> Hãy đọc và xác minh gói ngữ cảnh đính kèm, rồi thực hiện đúng theo PROMPT.md.
>
> Trong phản hồi đầu tiên, không sửa tệp và không sử dụng ngữ cảnh từ bất kì cuộc trò chuyện nào khác.

## Kết quả phản hồi

Chat-box mới đã:

- xác minh đúng package ID, commit nguồn, loại gói và giới hạn `repository.dirty: unknown`;
- kiểm tra CRC, checksum, tệp thiếu/thừa và nguồn bắt buộc;
- phân biệt nguồn hiện hành, nguồn chuyên trách và tài liệu lịch sử;
- mô tả đúng giao diện người dùng bằng ngôn ngữ tự nhiên;
- phân chia đúng trách nhiệm người dùng, agent, lớp vận hành và checker lõi;
- nhận diện đúng hai dự án `functions_100` và `real_world_100`;
- giải thích đúng ba cổng V, A, P;
- xác định đúng O4 chưa nghiệm thu và `publication` vẫn `pending`;
- không tuyên bố đã truy cập hoặc kiểm tra repository sống;
- không sửa tệp và không tạo bản vá.

Phản hồi cũng nêu đúng rằng gói không tự chứng minh worktree sạch vì manifest khai báo
`repository.dirty: unknown`. Bằng chứng worktree sạch và hai phép `verify` được lưu từ
phiên vận hành bên ngoài gói.

Một sai lệch nhỏ, không chặn nghiệm thu: phản hồi gọi cả `scripts/zo_qmd.py` và
`scripts/zo_check_repo.py` là “hai điểm vào hiện hành”. Theo hợp đồng giao diện,
điểm vào thống nhất dành cho agent là `scripts/zo_qmd.py`; `scripts/zo_check_repo.py`
là checker lõi nội bộ. Phần phân chia trách nhiệm phía sau vẫn mô tả đúng quan hệ này.

## Đánh giá

- Tính toàn vẹn gói: PASS
- Tái hiện đúng mô hình vận hành: PASS
- Tái hiện đúng giao diện người dùng: PASS
- Tái hiện đúng phạm vi hai dự án: PASS
- Tái hiện đúng V/A/P: PASS
- Nhận biết giới hạn snapshot: PASS
- Không dùng repository sống hoặc lịch sử chat: PASS
- Không sửa tệp: PASS

**Kết quả: `GOAL_3=PASS`.**

## Phản hồi đầy đủ của chat-box mới

# Báo cáo xác minh gói ngữ cảnh O4

## 1. Kết quả kiểm tra gói

**Kết luận:** gói đạt yêu cầu về cấu trúc và tính toàn vẹn nội bộ.

- **Package ID:** `qmd-context-20260804-031754`
- **Loại gói:** `context`
- **Mục đích:** gói context cuối để nghiệm thu chat-box trong O4
- **Thời điểm tạo:** `2026-08-04T03:17:54+07:00`
- **Nguồn:** `exported_snapshot`
- **Nhánh được khai báo:** `o4-qmd-operations`
- **Commit nguồn:** `335fbbeb1b631eecc642fbeb05bd6644025cd87e`
- **Trạng thái worktree:** `unknown`
- **Ahead of origin:** `unknown`

Kiểm tra trực tiếp ZIP cho kết quả:

- CRC của ZIP hợp lệ;
- đủ **66 mục** được liệt kê trong `FILES.sha256`;
- không thiếu tệp;
- không có checksum sai;
- không có tệp ngoài danh sách checksum;
- đủ **63 nguồn bắt buộc** và **1 nguồn có điều kiện** được manifest khai báo;
- hai điểm vào hiện hành đều có trong payload:
  - `scripts/zo_qmd.py`;
  - `scripts/zo_check_repo.py`.

Vì manifest khai báo `repository.dirty: unknown`, gói này **không tự chứng minh** rằng nó được tạo từ một worktree sạch, dù commit nguồn đã được ghi rõ.

## 2. Phân loại nguồn trong snapshot

### Nguồn hiện hành

Các nguồn dùng để hiểu và vận hành trạng thái hiện tại gồm:

- `AGENTS.md` ở gốc;
- `README.md` của hệ thống sản xuất QMD;
- `kien_truc_van_hanh_co_may_qmd.md`;
- `giao_thuc_agent_chat_box_va_goi_ngu_canh.md`;
- `tieu_chi_nghiem_thu_lop_van_hanh.md`;
- `vong_doi_bai_qmd.md`;
- các script hiện hành, đặc biệt `zo_qmd.py`, `zo_qmd_package.py`, `zo_qmd_prepublish.py` và checker lõi.

Release đang có hiệu lực là **lớp vận hành `0.3.0`**. `0.4.0` mới là ứng viên O4, chưa phát hành.

### Nguồn chuyên trách

Nguồn riêng của từng dự án nằm trong `content/.../<du_an>/AGENTS.md` và `_quy_trinh/`, gồm:

- cấu hình dự án;
- hồ sơ sản xuất;
- quy chuẩn nội dung và kĩ thuật;
- mẫu;
- adapter hoặc validator chuyên biệt;
- bài QMD dùng làm đường cơ sở hồi quy.

Nguồn lí thuyết đầy đủ `khung_khao_sat_ham_so_hoan_chinh_04.qmd` là **nguồn có điều kiện**: chỉ đọc khi quy chuẩn nén không đủ cho trường hợp đang xét.

### Tài liệu lịch sử và bằng chứng

Mặc dù `sources.historical` trong manifest đang rỗng, nội dung `README.md` tự phân loại một số tệp là lịch sử:

- hồ sơ Giai đoạn 0:
  - `kiem_ke_he_thong_hien_tai.md`;
  - `ban_do_kien_truc_hien_trang.md`;
  - `phan_loai_quy_tac_chung_rieng.md`;
- hồ sơ chuyển đổi:
  - `ke_hoach_chuyen_doi.md`;
  - `duong_co_so_hoi_quy_ham_ln_x.md`;
- bộ hồ sơ phát hành `qmd_ops_0_3_0` là bằng chứng của O3.

Các tài liệu này dùng để đối chiếu và truy nguyên, không được ghi đè tài liệu vận hành hiện hành.

## 3. Cỗ máy QMD được dùng như thế nào

Người dùng giao nhiệm vụ bằng ngôn ngữ tự nhiên, chẳng hạn:

> Hãy viết về hàm \(y=e^x\).

Nếu dự án đã được tích hợp, người dùng không phải biết tên script, cú pháp Terminal, vị trí cấu hình hay cách gọi checker.

Agent chuyển yêu cầu đó thành vòng vận hành:

```text
nhận diện dự án
→ đọc nguồn có thẩm quyền
→ khóa phạm vi
→ lập kế hoạch
→ tạo hoặc sửa QMD và tài nguyên
→ kiểm định nguồn
→ render khi cần
→ kiểm định đầu ra
→ kiểm định có người quan sát
→ báo cáo trước xuất bản
```

Xuất bản là một nhiệm vụ riêng và chỉ được thực hiện khi người dùng yêu cầu rõ.

## 4. Chuỗi trách nhiệm

### Người dùng

Người dùng chịu trách nhiệm:

- xác nhận mục tiêu nội dung và các quyết định còn mở;
- đánh giá ý nghĩa toán học, sư phạm, hình thức và đầu ra thực tế;
- quyết định chấp nhận;
- quyết định commit, push, xuất bản hoặc thao tác phá hủy khi chưa ủy quyền.

### Agent

Agent chịu trách nhiệm:

- đọc repository và toàn bộ chuỗi `AGENTS.md` có hiệu lực;
- nhận diện dự án, hồ sơ và quy chuẩn;
- tự thực hiện các thao tác kĩ thuật;
- tạo hoặc sửa sản phẩm trong phạm vi;
- chạy kiểm định và đọc kết quả;
- render và quan sát đầu ra khi nhiệm vụ yêu cầu;
- báo cáo đúng bằng chứng thực tế;
- không dựa vào lịch sử chat để bù cho tài liệu thiếu.

### Lớp vận hành

Lớp vận hành chịu trách nhiệm:

- cung cấp điểm vào thống nhất `scripts/zo_qmd.py`;
- khám phá dự án và nguồn có thẩm quyền;
- khóa phạm vi;
- điều phối checker và các công cụ hiện có;
- tạo manifest phiên, gói context hoặc gói release;
- tổng hợp báo cáo trước xuất bản;
- hỗ trợ bảo trì, phát hành và khôi phục.

Lớp này không được tự sửa nội dung chuyên môn, tự nghiệm thu, tự chuyển sang `published`, tự stage, commit hoặc xuất bản.

### Checker lõi

`scripts/zo_check_repo.py`:

- kiểm tra những điều có thể mã hóa;
- chạy validator lõi và validator dự án;
- kiểm tra nguồn và đầu ra theo cấu hình;
- trả về `PASS`, cảnh báo hoặc `FAIL`.

Checker không thay thế kiểm định trực quan, không tự chấp nhận bài và không có quyền xuất bản.

## 5. Hai dự án đã được tích hợp và kiểm nghiệm

1. **`functions_100` — 100+ Hàm số: Sự biến thiên và đồ thị**
   - Loại bài: `function_article`
   - Adapter: `functions-article`
   - Bài hồi quy: `core/ham_ln_x.qmd`
   - Trạng thái xuất bản đường cơ sở vẫn `pending`.

2. **`real_world_100` — 100+ Bài toán thực tế**
   - Loại bài: `real_world_problem`
   - Adapter: `real-world-problem`
   - Bài hồi quy: `core/chi_phi_di_taxi.qmd`
   - Hồ sơ giữ `production: in_production` và `publication: pending`.

Một dự án khác chưa có cấu hình, hồ sơ, quy chuẩn và đường hồi quy không tự động được hỗ trợ. Việc tích hợp dự án mới nằm ngoài phạm vi O4 hiện tại.

## 6. Ý nghĩa ba cổng V, A và P

### V — Validation

Kiểm định tự động phần có thể mã hóa:

- cấu hình hợp lệ;
- validator lõi và adapter dự án đạt;
- render adapter đạt khi cần;
- không còn `FAIL`;
- cảnh báo đã được xem xét.

Vượt V chỉ đủ điều kiện chuyển sang xem xét, chưa phải nghiệm thu.

### A — Acceptance

Kiểm định có người quan sát:

- sản phẩm đã vượt V;
- nội dung chuyên môn đạt;
- đầu ra thật đạt;
- người dùng hoặc người được ủy quyền chấp nhận.

### P — Publication

Xuất bản:

- sản phẩm đã được chấp nhận;
- người dùng xác nhận;
- dữ liệu công khai được cập nhật;
- quy trình xuất bản chạy thành công;
- không có thay đổi ngoài phạm vi.

Không cổng nào tự động mở cổng tiếp theo.

## 7. Trạng thái hiện tại của O4

Theo snapshot:

- O3 đã đạt; release hiện hành là `0.3.0`.
- CLI ứng viên O4 là `0.4.0`.
- Hai lệnh mới `start` và `prepublish` đã được triển khai.
- Self-test và các trường hợp chặn của hai lệnh đã có bằng chứng.
- Hồi quy nguồn của hai dự án đạt và SHA-256 hai QMD đường cơ sở được ghi nhận là không đổi.
- Một agent mới đã dùng đúng giao diện vận hành.
- Một snapshot O4 trước đó đã vượt phép thử context và chat-box.
- Phiên trình diễn đầu-cuối đã chứng minh `prepublish` chặn đúng khi kiểm định có người quan sát còn `FAIL`.
- Trạng thái xuất bản vẫn `pending`.
- `0.4.0` chưa được phát hành; chưa có Git tag thật, push hoặc publish.

Vì vậy, **O4 vẫn chưa đạt nghiệm thu**.

## 8. Việc còn thiếu trước nghiệm thu O4

Cần hoàn tất và lưu bằng chứng cho các việc sau:

1. Thử lại **Mục tiêu 1**: người dùng mô tả đúng cỗ máy theo hợp đồng giao việc bằng ngôn ngữ tự nhiên đã được cập nhật.
2. Chứng minh gói context cuối được tạo từ **commit sạch**.
3. Cho gói cuối vượt cả hai đường xác minh:
   - CLI bên ngoài gói;
   - CLI tự chứa trong payload.
4. Lưu kết quả phép thử một chat-box mới chỉ sử dụng gói cuối.
5. Hoàn tất bằng chứng của một yêu cầu mới đi đủ chuỗi:
   `inspect → start → sản xuất → check → render → human review → prepublish`.
6. Tổng hợp và lưu hồ sơ đủ **bảy mục tiêu nghiệm thu**.
7. Tạo và xác minh release candidate `0.4.0`.
8. Chứng minh release candidate có thể khôi phục.
9. Bảo đảm tài liệu hiện hành khớp với mã ứng viên cuối.
10. Giữ `publication: pending`.
11. Người dùng quyết định riêng có khóa lớp vận hành `1.0` hay không.

Gói hiện tại và phản hồi này có thể trở thành bằng chứng cho phép thử chat-box cuối, nhưng chưa tự tạo thành một hồ sơ nghiệm thu chính thức.

## 9. Những điều không thể xác minh về repository sống

Chỉ từ gói này, tôi không thể xác nhận:

- repository sống hiện đang ở nhánh hoặc commit nào;
- worktree hiện có sạch hay không;
- repository đang ahead hoặc behind remote bao nhiêu commit;
- nội dung repository có thay đổi sau lúc đóng gói hay không;
- commit `335fbbeb…` có thật sự được đóng gói từ worktree sạch hay không;
- hai lệnh `verify` chính thức đã được chạy trên chính gói này;
- CLI `0.4.0`, checker và môi trường Quarto/Python hiện chạy thành công trên máy sống;
- các bản HTML/PDF hiện tại có render đúng hay không;
- SHA-256 của hai bài hồi quy trong repository sống còn giữ nguyên hay không;
- đã có commit, tag, push, release hoặc xuất bản nào sau thời điểm tạo gói hay chưa;
- người dùng đã chính thức chấp nhận O4 hoặc khóa lớp vận hành `1.0` hay chưa.

Không có tệp nào được sửa và không có bản vá nào được tạo trong lần kiểm tra này.
