# Release checklist — QMD Operations 0.3.0

## Danh tính ứng viên

- Phiên bản ứng viên: `0.3.0`
- Tag dự kiến: `qmd-ops-v0.3.0`
- Tag thật đã tạo: không
- Phiên bản trước: `0.2.0`
- Commit quay lại: `c1b26b9a0536b17e0885d8158fddbd20413767c2`
- Commit mã ứng viên trước hồ sơ: `902991bb3780aeb20d4d6f31e5c2abb795051428`

## Điều kiện trước khi đóng gói

- [x] Hai worktree previous và candidate được tạo ngoài worktree sống.
- [x] Hai worktree ở trạng thái detached và sạch.
- [x] Hồi quy nguồn và render tại phiên bản trước đạt, mã thoát `0`.
- [x] Hồi quy nguồn và render tại ứng viên đạt, mã thoát `0`.
- [x] Checker vẫn ở phiên bản `2.6.0`.
- [x] Hai QMD hồi quy có SHA-256 giống hệt trước và sau.
- [x] Trạng thái xuất bản của hai bài vẫn `pending`.
- [x] Rollback drill không sửa hai bài hồi quy để thích nghi.
- [x] Không dùng thao tác phá hủy worktree sống.
- [x] Hồ sơ phát hành và mọi bằng chứng bắt buộc có trong commit ứng viên.
- [x] `tag_created` vẫn là `false`.
- [x] Không push và không publish.

## Bước hậu commit

Sau khi hồ sơ này được commit, release candidate phải được tạo từ một worktree sạch tại commit chứa hồ sơ, đặt ngoài repository, rồi được kiểm tra bằng:

```bash
python scripts/zo_python.py scripts/zo_qmd.py verify <release-candidate>
```

Việc tạo ZIP và kết quả `verify` không được tuyên bố hoàn tất trước khi lệnh thực sự chạy.
