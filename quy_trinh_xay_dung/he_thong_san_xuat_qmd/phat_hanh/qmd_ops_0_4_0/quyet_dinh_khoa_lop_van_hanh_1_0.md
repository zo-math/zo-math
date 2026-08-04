# Quyết định khóa lớp vận hành QMD 1.0

- Ngày quyết định: 2026-08-04
- Điểm trước quyết định: `23ce5eac6c8482f85eeccbf22cf6c934aff9490f`
- Release được chấp thuận: `0.4.0`
- Package ID: `qmd-release-0-4-0-20260804-142216`
- Candidate commit: `6425dec241cc27cad76bf55f8385531e56fb1a86`
- SHA-256 của ZIP: `b95f7dc2fd131be0024747189cf576d6efdc12114c2967b60abeca7614f92a4f`
- Xác minh ngoài gói: PASS
- Xác minh tự thân: PASS

## Quyết định

Người dùng chấp thuận RC `0.4.0` làm release hiện hành và khóa lớp vận hành
QMD ở mốc nghiệm thu `1.0`.

## Giải thích phiên bản

Mốc nghiệm thu `1.0` ghi mức trưởng thành của toàn bộ lớp vận hành. Hằng số
máy đọc được `OPERATIONS_CONTRACT_VERSION` tiếp tục là `0.4`, vì nó phải
khớp `MAJOR.MINOR` của release `0.4.0`. Quyết định này không tạo một release
`1.0.0` mới và không làm thay đổi danh tính RC đã xác minh.

Các danh tính sau được giữ nguyên:

- release lớp vận hành: `0.4.0`;
- CLI vận hành: `0.4.0`;
- hợp đồng vận hành máy đọc được: `0.4`;
- mô-đun đóng gói: `0.3.1`;
- lõi kĩ thuật QMD: `1.0`;
- checker: `2.6.0`.

## Ngoài phạm vi quyết định

Quyết định này không tự tạo Git tag, không push, không publish, không tích hợp
vào repository sống `E:\zo_math` và không dọn các worktree trung gian.
