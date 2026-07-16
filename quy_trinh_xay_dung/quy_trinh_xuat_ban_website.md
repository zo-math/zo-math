# Quy trình xuất bản website ZO Math

## 1. Mục đích và phạm vi

Quy trình này điều hành các nhiệm vụ kiểm tra, chuẩn bị và xuất bản website ZO Math. Đây là tài liệu nội bộ, không phải nội dung dành cho người đọc website.

Nhánh `master` chứa nguồn xây dựng website. Nhánh `gh-pages` chỉ chứa cây đầu ra công khai. Commit nguồn và commit xuất bản phải luôn tách biệt.

## 2. Cấu hình công khai

`publish_public.yml` là nguồn cấu hình chính thức xác định cây đầu ra được phép xuất bản. Cơ chế lựa chọn chính là allowlist; denylist chỉ là lớp phòng vệ bổ sung.

Không mặc định công khai toàn bộ `content/`, `assets/`, `figures/` hoặc toàn bộ thư mục đầu ra Quarto. Mọi nhóm mới phải được khảo sát và thêm tường minh vào allowlist.

## 3. Công cụ chính thức

Mọi lệnh của công cụ xuất bản phải chạy qua trình khởi chạy Python repository-local:

```text
python scripts/zo_python.py scripts/zo_publish.py check
```

Hiện tại chỉ chế độ `check` được triển khai và cho phép sử dụng. Chế độ này chỉ đọc: kiểm tra Git, worktree, cấu hình, cây đầu ra hiện có, nội dung bị cấm và diff xuất bản dự kiến.

Hai giai đoạn sau mới là kiến trúc dự kiến, chưa được triển khai và chưa được phép sử dụng:

1. `prepare`: render qua `scripts/zo_quarto.py`, dựng cây công khai và chuẩn bị diff nhưng chưa commit hoặc push.
2. `publish`: kiểm định lại, stage tường minh, commit riêng trên `gh-pages` và push không force.

Không dùng `scripts/publish_public.sh` cho quy trình mới, trừ khi yêu cầu hiện tại của người dùng chỉ định rõ việc khảo sát script cũ. Không dùng `git add -A`, force push hoặc thao tác xóa diện rộng.

## 4. Nguyên tắc an toàn

- Không thay đổi `master` trong quá trình chuẩn bị hoặc xuất bản website.
- Không ghi vào worktree `gh-pages` nếu trạng thái ban đầu không sạch.
- Không xuất bản tệp ngoài allowlist hoặc tệp bị denylist chặn.
- Không commit nếu HTML, tài nguyên, đường dẫn hoặc kiểm tra nội dung riêng tư chưa đạt.
- Mọi render phải đi qua `scripts/zo_quarto.py`.
- Phải xem diff xuất bản trước khi stage và commit.
- Không push nếu remote `gh-pages` đã thay đổi sau lần kiểm tra gần nhất.
- Chỉ xuất bản khi yêu cầu hiện tại của người dùng cho phép rõ việc xuất bản website.

## 5. Trình tự dự kiến

1. Chạy `check` và xử lý mọi điểm chặn.
2. Khi `prepare` đã được triển khai và kiểm định, chạy để tạo cây công khai cho con người hoặc agent đối chiếu.
3. Chỉ khi người dùng cho phép xuất bản và `publish` đã được triển khai, kiểm định lại remote, commit riêng trên `gh-pages` và push.
