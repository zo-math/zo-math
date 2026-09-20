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
python scripts/zo_python.py scripts/zo_publish.py prepare
python scripts/zo_python.py scripts/zo_publish.py publish
```

`check` chỉ đọc: kiểm tra Git, worktree, cấu hình, cây đầu ra hiện có, nội dung bị cấm và diff xuất bản dự kiến.

`prepare` render toàn website qua `scripts/zo_quarto.py` vào staging sạch trong `_audit/`, dựng và kiểm định cây công khai, tạo báo cáo chuẩn bị rồi đồng bộ có kiểm soát sang worktree `gh-pages`. Lệnh này không stage, commit hoặc push. Chỉ chạy khi người dùng yêu cầu rõ và worktree đích hoàn toàn sạch; báo cáo chuẩn bị là căn cứ cho bước xuất bản tiếp theo.

`publish` không render và không tự chạy `prepare`. Lệnh chỉ dùng báo cáo cùng cây công khai do một lần `prepare` thành công tạo ra; kiểm tra lại SHA nguồn, remote, manifest, validator và diff trước khi stage từng đường dẫn tường minh, commit riêng trên `gh-pages` rồi push không force. Nguồn phải được push lên `origin/master` trước, `origin/gh-pages` không được thay đổi sau `prepare`, và người dùng phải yêu cầu rõ việc xuất bản.

Nếu push bị từ chối, công cụ giữ commit `gh-pages` cục bộ và báo lỗi; không tự merge, rebase, sửa lịch sử hoặc force push. Sau khi push thành công hoặc xác nhận không có thay đổi, dữ liệu tạm và báo cáo của lần `prepare` được dọn. Commit nguồn trên `master` và commit website trên `gh-pages` luôn tách biệt.

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
2. Khi người dùng yêu cầu rõ, chạy `prepare` để tạo cây công khai cho con người hoặc agent đối chiếu.
3. Chỉ khi người dùng cho phép xuất bản, chạy `publish` để kiểm định lại remote, manifest và diff, sau đó commit riêng trên `gh-pages` và push thường.

## 6. Bản nháp và ranh giới nội bộ

`draft: true` trong Quarto không thay thế chính sách public. Chuyên mục `content/thpt/on_thi_toan_thpt` hiện bị chặn toàn bộ trong `publish_public.yml`; `_quy_trinh` tiếp tục bị chặn ngay cả khi sau này chuyên mục được mở công khai. Chỉ thay đổi ranh giới này khi người dùng phê duyệt riêng.

Profile `on-thi-preview` chỉ phục vụ preview trên `127.0.0.1`. Công cụ xuất bản từ chối profile này khi có trong `QUARTO_PROFILE` hoặc profile mặc định của dự án, trước khi fetch, render hoặc tác động worktree public. Không dùng `prepare` như một lệnh preview.

`check` và validator của quy trình hiện hành kiểm tra đường dẫn bị cấm sau giải mã và chuẩn hóa trong manifest, HTML (kể cả chuỗi đường dẫn không phải liên kết), `search.json` và sitemap. Chỉ loại tệp khỏi manifest là chưa đủ nếu chỉ mục hoặc HTML vẫn tham chiếu tới vùng bị cấm. Chỉ mục JSON/XML không đọc được phải làm kiểm tra thất bại.

Kiểm thử mục tiêu của hàng rào:

```text
python scripts/zo_python.py scripts/zo_publish_selftest.py
```

Fixture của bộ kiểm thử nằm trong `_audit/` và được tự dọn. Khi mở rộng validator, phải phân biệt phát hiện mới trên đầu ra cũ với hồi quy do thay đổi nguồn; không tự dọn các vấn đề ngoài nhiệm vụ.
