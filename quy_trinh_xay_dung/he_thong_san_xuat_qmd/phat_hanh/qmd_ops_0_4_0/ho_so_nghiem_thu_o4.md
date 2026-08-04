# Hồ sơ nghiệm thu O4 — lớp vận hành QMD

## Tổng kết nhanh

- Commit kiểm tra: `335fbbeb1b631eecc642fbeb05bd6644025cd87e`
- Nhánh hiện tại: `o4-qmd-operations`
- Trạng thái Git trước khi lập hồ sơ: nhánh `o4-qmd-operations` ở commit `335fbbeb1b631eecc642fbeb05bd6644025cd87e` và worktree sạch.
- Trạng thái tổng quát: bảy mục tiêu có bằng chứng; hồ sơ tổng hợp O4 đã được lập trong thư mục `qmd_ops_0_4_0`; release candidate `0.4.0` chưa được tạo hoặc xác minh; chưa tag, push hoặc publish; việc khóa lớp vận hành `1.0` vẫn cần release candidate được xác minh và quyết định riêng của người dùng.

## Quy ước lưu bằng chứng

- Các dẫn chiếu trong hồ sơ này dùng đường dẫn tương đối tính từ thư mục `qmd_ops_0_4_0`.
- Đường dẫn tuyệt đối còn xuất hiện bên trong log hoặc manifest thô được giữ nguyên như dữ liệu lịch sử của lần chạy trên máy nguồn; chúng không phải phụ thuộc vận hành hiện hành của hồ sơ.
- Tính toàn vẹn của bộ bằng chứng sao lưu trong repository được kiểm tra bằng `bang_chung/SHA256SUMS.txt`.

## Mục tiêu 1 — Người dùng mô tả được cỗ máy

- Điều kiện trước: README hiện hành và quy trình vận hành đã được khóa ở commit `335fbbeb1b631eecc642fbeb05bd6644025cd87e`; repository ở trạng thái sạch.
- Phép thử: một người dùng đọc README và trả lời bằng ngôn ngữ thông thường về giao diện, phạm vi, trách nhiệm agent/kiểm tra và quyền chấp nhận/xuất bản, mà không được hỏi tên script hoặc cú pháp Terminal.
- Bằng chứng: `bang_chung/muc_tieu_1/o4_goal_1_user_understanding.md` ghi kết quả `GOAL_1=PASS` và nêu rõ người dùng hiểu đúng giao diện ngôn ngữ tự nhiên, giới hạn của kiểm định tự động và quyền của con người trong chấp nhận/xuất bản.
- Commit hoặc phiên bản liên quan: commit `335fbbeb1b631eecc642fbeb05bd6644025cd87e`.
- Kết quả: PASS.
- Giới hạn: hồ sơ này chứng minh hiểu đúng cách sử dụng từ góc nhìn người dùng, chứ không thay thế kiểm định kỹ thuật.
- Kết luận: PASS.

## Mục tiêu 2 — Agent mới trong VS Code sử dụng được

- Điều kiện trước: repository ở commit `335fbbeb1b631eecc642fbeb05bd6644025cd87e`, detached HEAD đúng và worktree sạch.
- Phép thử: mở một agent mới không có lịch sử chat, đọc `AGENTS.md` gốc và `AGENTS.md` dự án, nhận diện đúng dự án/loại bài/hồ sơ, chạy đúng điểm vào vận hành và không sửa bài hồi quy.
- Bằng chứng: `bang_chung/muc_tieu_2/` chứa `report.md`, `transcript.txt`, `setup.txt`, `cli_help.txt` và `final_state.txt`; báo cáo ghi đúng commit `335fbbeb1b631eecc642fbeb05bd6644025cd87e`, `doctor/inspect/check` đều đạt, worktree thử vẫn sạch và không có tracked modification.
- Commit hoặc phiên bản liên quan: commit `335fbbeb1b631eecc642fbeb05bd6644025cd87e`; CLI ứng viên `0.4.0`.
- Kết quả: PASS.
- Giới hạn: phép thử này xác minh nhận diện và kiểm định ban đầu, không thay thế việc chấp nhận nội dung chuyên môn.
- Kết luận: PASS.

## Mục tiêu 3 — Chat-box làm việc qua gói chuẩn

- Điều kiện trước: có gói context cuối được tạo từ commit sạch tại `335fbbeb1b631eecc642fbeb05bd6644025cd87e`.
- Phép thử: cung cấp gói context cho một chat-box mới không có quyền truy cập repository; chat-box phải đọc `PROMPT.md`, `MANIFEST.yml`, kiểm tra checksum và phản hồi đúng phạm vi, giới hạn và trách nhiệm vận hành.
- Bằng chứng: `bang_chung/goi_context_cuoi/o4_goal_3_fresh_chat_evidence.md` ghi package ID `qmd-context-20260804-031754`, commit nguồn `335fbbeb1b631eecc642fbeb05bd6644025cd87e`, SHA-256 của gói và kết luận `GOAL_3=PASS`. Hai tệp `bang_chung/goi_context_cuoi/verify_external.txt` và `bang_chung/goi_context_cuoi/verify_self.txt` xác nhận verify ngoài gói và verify tự thân đều đạt `PASS | EXIT=0`; `MANIFEST.yml` và `FILES.sha256` được lưu cùng thư mục để kiểm tra cấu trúc và danh mục toàn vẹn của gói.
- Commit hoặc phiên bản liên quan: package `qmd-context-20260804-031754`, commit `335fbbeb1b631eecc642fbeb05bd6644025cd87e`.
- Kết quả: PASS.
- Giới hạn: hai bản verify và gói context chứng minh tính toàn vẹn, khả năng tái hiện và phản hồi đúng phạm vi; chúng không tự chứng minh worktree sạch, vì trạng thái sạch của worktree cần được xác nhận riêng bằng Git.
- Kết luận: PASS.

## Mục tiêu 4 — Giao diện kĩ thuật thống nhất cho agent

- Điều kiện trước: CLI ứng viên `0.4.0` đã nằm trong repository, và `scripts/zo_check_repo.py` vẫn là checker lõi.
- Phép thử: chạy `--help` và các lệnh `doctor`, `inspect`, `start`, `prepublish`, `check`, `render`, `regression`, `pack`, `verify` qua cùng một điểm vào `python scripts/zo_python.py scripts/zo_qmd.py ...`.
- Bằng chứng: `bang_chung/muc_tieu_2/cli_help.txt` và `bang_chung/muc_tieu_2/transcript.txt` chứng minh giao diện chung cùng việc thực thi `doctor`, `inspect` và `check`. Các lệnh `start`, `render` và `prepublish` được chứng minh lần lượt bằng `bang_chung/trinh_dien_dau_cuoi/start_round_2.txt`, `session_round_2.json`, `render_round_3.json` và `prepublish_blocked_round_3.json`. Sản phẩm của `pack` được đại diện bằng `bang_chung/goi_context_cuoi/MANIFEST.yml`, `FILES.sha256`, package ID `qmd-context-20260804-031754` và SHA-256 ghi trong hồ sơ Mục tiêu 3; không có transcript riêng cho lệnh `pack`. Hai lần `verify` được chứng minh bằng `verify_external.txt` và `verify_self.txt`; `regression` được chứng minh bằng `bang_chung/trinh_dien_dau_cuoi/regression_round_3.txt`. Các phép thử trải qua commit `b5156d18d4e8dd5d56f3191d259b67c4fad18e9c` và snapshot cuối `335fbbeb1b631eecc642fbeb05bd6644025cd87e`, cùng dùng CLI `0.4.0`.
- Commit hoặc phiên bản liên quan: CLI `0.4.0` tại commit `335fbbeb1b631eecc642fbeb05bd6644025cd87e`.
- Kết quả: PASS.
- Giới hạn: mục tiêu này kiểm tra giao diện và đường vào thống nhất; nó không thay thế bằng chứng kiểm định hay xuất bản.
- Kết luận: PASS.

## Mục tiêu 5 — Gói phát hành và manifest

- Điều kiện trước: O3 đã có release candidate, hồ sơ phát hành và bằng chứng verify; O4 chưa tạo release candidate `0.4.0`.
- Phép thử: tạo release candidate từ worktree sạch, mở gói trong thư mục sạch và chạy verify; lưu manifest, checksum, checklist, changelog, rollback log và bằng chứng hồi quy.
- Bằng chứng: hồ sơ O3 tại `quy_trinh_xay_dung/he_thong_san_xuat_qmd/phat_hanh/qmd_ops_0_3_0/release_verification.md` ghi package ID `qmd-release-0-3-0-20260802-223550`, candidate commit `99a7c04c69eb0a54d381f5afd0d3e79fe26e9cab`, `tag_created: false`, và hai phép verify đều PASS; `ho_so_release_candidate.yml` và `release_checklist.md` cùng xác nhận release candidate được tạo ngoài repository với checksum và manifest đầy đủ.
- Commit hoặc phiên bản liên quan: release candidate O3 `0.3.0`, commit `99a7c04c69eb0a54d381f5afd0d3e79fe26e9cab`.
- Kết quả: PASS, với lưu ý rằng đây là bằng chứng O3; O4 vẫn chưa tạo release candidate `0.4.0`.
- Giới hạn: O4 chưa có release candidate `0.4.0` được tạo hoặc xác minh; hồ sơ này chỉ khẳng định lớp vận hành có quy trình release/verify đã được chứng minh ở O3.
- Kết luận: PASS.

## Mục tiêu 6 — Bảo trì, nâng phiên bản và khôi phục

- Điều kiện trước: có bằng chứng rollback drill O3 và hai bài hồi quy không đổi.
- Phép thử: tạo thay đổi nhỏ có phân loại, đóng gói release candidate mới, dựng worktree trước và ứng viên riêng, chạy hồi quy bắt buộc và diễn tập khôi phục về release trước mà không phá hủy worktree sống.
- Bằng chứng: `quy_trinh_xay_dung/he_thong_san_xuat_qmd/phat_hanh/qmd_ops_0_3_0/rollback_log.md` ghi `previous_version: 0.2.0`, `previous_commit: c1b26b9a0536b17e0885d8158fddbd20413767c2`, worktree previous/candidate đã được dựng riêng, hồi quy trước và sau đều PASS, hai checksum bài hồi quy không đổi, và trạng thái `pending` được bảo toàn.
- Commit hoặc phiên bản liên quan: release trước `0.2.0` ở commit `c1b26b9a0536b17e0885d8158fddbd20413767c2`; rollback drill O3.
- Kết quả: PASS.
- Giới hạn: đây là bằng chứng rollback O3; O4 chưa có release candidate `0.4.0` để quy trình khôi phục phiên bản mới được lặp lại.
- Kết luận: PASS.

## Mục tiêu 7 — Phiên trình diễn đầu-cuối

- Điều kiện trước: phiên trình diễn đầu-cuối được bắt đầu trên nhánh `o4-qmd-operations` tại commit `b5156d18d4e8dd5d56f3191d259b67c4fad18e9c`; snapshot cuối dùng để lập hồ sơ là `335fbbeb1b631eecc642fbeb05bd6644025cd87e`.
- Phép thử: từ tiếp nhận đến báo cáo trước xuất bản, chạy chuỗi `request → doctor → inspect → start → production → check → render → human review → prepublish` với bài thử, sau đó xem prepublish có bị chặn đúng hay không.
- Bằng chứng: `bang_chung/trinh_dien_dau_cuoi/` chứa `request_round_2.md`, `start_round_2.txt`, `session_round_2.json`, `check_source_round_3.json`, `render_round_3.json`, `human_review_round_3.json` và `prepublish_blocked_round_3.json`. Phiên trình diễn đầu-cuối được thực hiện tại commit `b5156d18d4e8dd5d56f3191d259b67c4fad18e9c`; snapshot O4 cuối dùng để lập hồ sơ là commit `335fbbeb1b631eecc642fbeb05bd6644025cd87e`.
- Commit hoặc phiên bản liên quan: CLI `0.4.0` tại commit `335fbbeb1b631eecc642fbeb05bd6644025cd87e`; phiên trình diễn đầu-cuối được thực hiện tại commit `b5156d18d4e8dd5d56f3191d259b67c4fad18e9c`.
- Kết quả: PASS về khả năng vận hành đầu-cuối: human review cuối là `FAIL`, prepublish bị `blocked`, `production_status` ở `in_production` và `publication_status` ở `pending`. Bài `y=x^2` không được chấp nhận và không sẵn sàng xuất bản.
- Giới hạn: hồ sơ này chỉ xác nhận cổng prepublish hoạt động đúng theo hợp đồng; nó không chứng minh bài thử `y=x^2` đã được chấp nhận hay sẵn sàng xuất bản.
- Kết luận: PASS.

## Kết luận tổng quát

- Bảy mục tiêu đều có bằng chứng và được ghi nhận ở mức PASS.
- Hồ sơ tổng hợp O4 đã được lập trong repository tại `quy_trinh_xay_dung/he_thong_san_xuat_qmd/phat_hanh/qmd_ops_0_4_0/ho_so_nghiem_thu_o4.md`.
- Release candidate `0.4.0` chưa được tạo hoặc xác minh.
- Chưa tag, push hoặc publish.
- Việc khóa lớp vận hành `1.0` vẫn cần một release candidate được xác minh và quyết định riêng của người dùng.
