# Đối sánh liên gói R1 — FB029, 08/10/2026

Hồ sơ FB029 dưới đây giữ nguyên bằng chứng lỗi tại thời điểm đó. Quy tắc chung hiện hành ở [07 của khóa](../../content/thpt/on_thi_toan_thpt/tot_nghiep_thpt/2027/_quy_trinh/07_quy_chuan_cau_truc_trang_nguoi_hoc.md); trạng thái/nhiệm vụ chỉ ở bảng 03. Nền/Nhật kí/CP/Ôn lại đã được thêm nguồn sau FB034–036, không dùng danh sách thiếu cũ làm current. Góp ý nội dung G01 sau resume nằm trong hồ sơ gói, chưa được giải quyết bởi ma trận này.

**Hiện hành FB036:** xem [ma trận sửa lỗi mới](doi_sanh_FB036.md) và
`_audit/zo_web_pair_refinement_2026-10-08/README.md`. Chủ trì đã mở lại cả
G01/G02; nguồn và HTML đã sửa/kiểm, chờ xem. Giới hạn không sửa QMD của
FB029 bên dưới là lịch sử của nhiệm vụ cũ, không phủ nhận quyền FB036.

Phạm vi **của lượt FB029**: kit thử nghiệm web 2027, chưa là chuẩn toàn repository hoặc 0.5. Nhiệm vụ lúc đó: đối sánh G01/G02, liệt kê/sửa lỗi cũ trong prototype; giới hạn không sửa production/toán thuộc lượt ấy. FB036 có quyền sửa nguồn riêng, không bị prompt FB029 phủ nhận.

## Vì sao chưa nhất quán tại FB029

G01 đã chuyển kiến trúc và được duyệt thiết kế; G02 mới thay shell/CSS quanh nguồn học cũ. Kiểm FB028 bảo toàn nguồn và hình học cục bộ, chưa kiểm tương đương theo vai trò giữa hai gói. Không thể dùng 1089 PASS ấy làm bằng chứng đồng bộ. Hồ sơ G02 đã báo thiếu Nền/Nhật kí/CP nhưng chưa chuyển thành cổng chặn kết luận “nhân bản hoàn chỉnh”. Đây là thiếu sót triển khai/kiểm của agent.

## Hợp đồng kiểm trong kit này

1. Cùng chức năng → cùng component/vai trò; không yêu cầu cùng đề toán, số bài, số hình hoặc chiều cao hộp.
2. Bản đồ nhịp riêng phải nêu công việc và lý do ghép/tách; không ánh xạ tất cả section bằng nhãn chương hoặc `Nhiệm vụ · <tên view>`.
3. Giấy nhiệm vụ, guidance và solution kiểm riêng. Không so “phần tử đầu tiên” khác chức năng, không bỏ nhiệm vụ khi nó là `section` hoặc chính nó là giấy.
4. Mọi nhãn/heading/nội dung/link thuộc một vùng; header rỗng đi cùng nhiệm vụ đầu. Không thay trục chữ bằng trục mép hộp.
5. Nội dung giới thiệu chỉ ở điểm vào và Toàn văn; no-JS vẫn đọc đủ. Không di chuyển ID/DOM lớn bằng JavaScript.
6. Kiểm nguồn → bản dựng từng gói, rồi kiểm liên gói. Mất MathML/ID, lệch inset, đổi typography cùng vai trò phải bị phát hiện bằng ca âm.
7. Khuyết kiến trúc bắt buộc phải ghi CÒN THIẾU, không ghi GIỮ vì “nguồn không có”. Không tạo tab rỗng, bịa câu nền/CP/nhật kí để làm PASS.
8. Kiểm đạt / chủ trì duyệt / production / PDF / phát hành là các trạng thái riêng.

## Lỗi mới xác minh và xử lí

| Mã | Triệu chứng / nguyên nhân | Nguồn sửa / guard |
|---|---|---|
| PAIR-WEB-001 | G02 gọi nhiệm vụ bằng tên view, lý thuyết bằng tên chương; không cùng taxonomy G01 | `scripts/zo_web_2027_g02.py`: nhãn Nhiệm vụ, Khái niệm/Định nghĩa/Định lí/Ví dụ/Đối chứng; kiểm danh mục nhãn và taskpapers không rỗng |
| PAIR-WEB-002 | Bảy câu dừng G02 không có nhãn chức năng cùng hệ | Builder thêm Tự kiểm tra dạng metadata, không đổi đề/ID/disclosure; inventory bảo toàn và guard trục |
| PAIR-WEB-003 | Một vùng G02 chỉ chứa header, lỗi cũ tái diễn vì thiếu guard G01 | Ghép header vào nhiệm vụ kế tiếp đúng thứ tự; 112 → 111 vùng, không mất nội dung |
| PAIR-WEB-004 | Giới thiệu G02 lặp cả ở Kiểm tra/Bài học do nằm ngoài section do controller quản | Adapter đánh dấu vùng, CSS theo view hiện hữu; kiểm 10 view/3 viewport; Toàn văn/no-JS giữ đủ |
| PAIR-WEB-005 | Footer có ở G02 nhưng không ở G01 vì mốc footer trước chỉ áp dụng Nhà | Bản đối sánh G01 mới thêm footer chung ngoài main; snapshot đã duyệt bất biến, mọi vùng G01 giữ nguyên |
| PAIR-WEB-006 | Danh sách tải G02 mang class khác selector kit | Alias `.r1-section-download-list`; giữ mọi href/download, responsive kiểm lại |
| PAIR-CHECK-001 | JSON đã chuyển tuple thành list làm đối chiếu báo sai | Serialize hai phía cùng schema; không nới bảo vệ text/math/ID |
| PAIR-CHECK-002 | Selector `div` bỏ nhiệm vụ G01 `section`; tìm ancestor bỏ chính paper | Kiểm cả section/div và self-or-ancestor; inventory bắt buộc không rỗng; không biến ca rỗng thành PASS |
| PAIR-CHECK-003 | So summary đầu tiên (mục lục với guidance) tạo sai khác giả | Selector chức năng guidance/solution riêng; ca âm đổi typography phải bị bắt |

Lỗi build CLI đầu: kiểu chuỗi thay Path, thư mục audit chưa tạo, key `details` thay `disclosures`; đã sửa và dựng lại. Không cài phụ thuộc hoặc sửa production để xử lí.

## Khoảng cách kiến trúc G02 tại FB029 — không là trạng thái sau FB036

Bắt đầu riêng; C1/C2/C3 và checkpoint có tiêu chí–hỗ trợ–xác nhận–quay về; Nền theo nhu cầu; Nhật kí 14 trường; ba bài Ôn lại có ID/lời giải/CP riêng; P01/P02 không chặn lõi; wording mã máy và ngữ cảnh hỗ trợ. Ma trận 46 tiêu chí không đánh đồng các thiếu hụt này với khác biệt đúng của hai chủ đề toán.

Không tự sửa QMD hoặc tạo ngân hàng mới trong lượt prototype. Nhiệm vụ tiếp theo cần được giao rõ là chuyển kiến trúc G02 ở nguồn sau khi chốt phạm vi/ID; không mở thêm vòng thiết kế.

## Tái hiện

```text
python scripts/zo_python.py scripts/zo_web_2027_preview.py --compare --output _audit/zo_web_2027_g01_g02_doi_sanh_2026-10-08
python scripts/zo_python.py scripts/zo_web_2027_check.py --compare --preview _audit/zo_web_2027_g01_g02_doi_sanh_2026-10-08
python scripts/zo_python.py scripts/zo_web_2027_check.py --preview _audit/zo_web_2027_g01_g02_doi_sanh_2026-10-08
```

Đầu ra: `index.html`, `ma_tran_doi_sanh.md`, `matrix.json`, inventory trước/sau toàn bộ task/table/heading/hình/route, `canonical-pointers.json`, đủ 28 bản ghi nguyên văn trong `old-defects.json`, manifest/hash, QA hai lớp và ảnh. Các báo cáo PASS chỉ chứng minh phạm vi guard, không thẩm định lại chân trị mọi đáp án, PDF, thiết bị thật, screen reader hoặc trình duyệt khác Edge.
