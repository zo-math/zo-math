# Cách dùng, quản lý và cập nhật trong VS Code

Phiên bản: 0.8 · Ngày biên tập: 10/10/2026 · Tiếp quản theo QD_021–025.

Hướng dẫn dành cho người chủ trì. Bộ này dùng được với Codex và Copilot trên cùng repo. [Điểm vào](README.md).


## 1. Tiếp quản bộ đã có trong repo

Không giải nén hoặc nhập lại bộ điều hành đã hiện diện. Mở [README](README.md), đọc mục A của [03](03_dieu_hanh_chuong_trinh.md) và [08](08_danh_muc_tham_quyen_dieu_hanh.md). Agent tự tìm/đối chiếu nguồn, trạng thái và các chỉ dẫn theo nhiệm vụ; người chủ trì không phải biết tên script hoặc dò hàng loạt tài liệu.

Chỉ cần giao bằng tên bước và phạm vi. Ví dụ: “Thực hiện bước đang đề xuất ở mục A; chỉ lập phương án biên tập, chưa sửa nguồn.” Nếu giao sửa, nêu rõ nhận phương án nào; agent lập danh sách tác động và kiểm phần dùng chung. Không diễn giải câu đồng ý với khảo sát thành quyền biên tập, PDF hoặc phát hành.

Các bước nhập và prompt lần đầu ở dưới **chỉ dành cho một bộ bàn giao chưa tích hợp**, không chạy lại để tiếp tục FB036/DH_009. Quyết định mới phải được cập nhật đủ các lớp theo 02 trước khi biên tập tiếp. Chỉ 03 sở hữu công việc hiện hành; sau mỗi bàn giao đặt tên bước tiếp theo rõ ràng.

### Tiếp quản sau một quyết định mới

QD_024 áp dụng hai quy tắc Kiểm tra cho toàn bộ các gói của chương trình tại 01/2.3.1, không chỉ R1. Đọc 07/4.4 để áp dụng lời dẫn, 02 để kiểm và 03 để biết sản phẩm nào chưa sửa. Không yêu cầu chứng minh bài làm độc lập trước khi được vào Kiểm tra, không cho chia cùng một lượt Kiểm tra thành nhiều đợt; quyền vào khác bằng chứng đạt mục tiêu. Bản biên tập G01 do chủ trì sửa đã được nhận làm chỉ dẫn triển khai, không yêu cầu duyệt lại cùng bản; chưa có nghĩa đã áp dụng nguồn hoặc nghiệm thu HTML.

Hệ nhãn QD_025 toàn chương trình kế thừa QD_023 và bổ sung Gợi mở; không cần người chủ trì học cú pháp CLI. Agent nạp từ điển duy nhất, kiểm bảng áp dụng từ nguồn hiện tại và trình phần riêng còn cần chốt. Duyệt hệ thống khác duyệt tên/số/câu chữ cụ thể và khác nghiệm thu bản HTML. Bảng G01 ở `_quy_trinh/ap_dung_he_nhan.json` đã áp dụng nguồn/binding; G02 đã áp dụng binding riêng `giao_dien/he_nhan.json` tại DH_016; kiểm bằng `zo_r1_g02_labels_check.py`, không áp số lượng G01. Lệnh kiểm `zo_learning_architecture.py labels --self-test --output <audit_mới>` qua launcher. Chỉ bảng 03 ghi việc tiếp theo; kết quả kiểm hợp đồng không tự cấp quyền sửa nguồn hoặc nghiệm thu.

Đọc quyết định hiện hành và phần bị thay, không dùng chat hoặc checkpoint cũ làm quy tắc. Trước biên tập, agent chạy cổng `scripts/zo_2027_governance_check.py` qua `scripts/zo_python.py`; cổng tài liệu sai bản phải dừng để đồng bộ đúng phạm vi. QD_022: không tái dùng kết quả chịu ảnh hưởng của quy tắc đã bị thay; giữ kết quả không liên quan khi đầu vào và phép kiểm tương ứng không đổi. Hash tài liệu đổi không hủy toàn bộ QA, không cấm sửa chữa trong phạm vi đã giao. Sản phẩm còn lỗi được phép sửa theo nhiệm vụ, không được trình như đã đạt. Mô hình nội bộ giúp biên tập, không là câu chữ xuất bản. Quy trình thay thế tức thời tại 02/1.2; 03 chỉ ghi một bước tiếp.

### Nhập một bộ bàn giao mới — không phải thao tác tiếp quản hiện tại

1. Giải nén bộ bàn giao. Mở repo ZO Math bằng VS Code.
2. Tìm gốc điều hành `tot_nghiep_thpt/2027/_quy_trinh/`. Kế hoạch 0.6 và bộ điều hành cùng nằm trực tiếp tại gốc này. Giữ nguyên nguồn QMD và các URL; không đặt bộ điều hành vào `docs/`.
3. Nếu đã có thư mục hoặc tệp điều hành cùng tên, không ghi đè ngay. Cho Codex đối chiếu và hợp nhất phần còn hiệu lực; giữ lịch sử trong Git. Tài liệu cũ được đánh dấu vai trò tại tệp 06, không xóa hàng loạt.
4. Mở `README.md`, dùng prompt lần đầu bên dưới. Codex tìm các đường dẫn thật, cập nhật ô chưa xác minh và báo cáo G01.
5. Đọc báo cáo. Giao phạm vi sửa cụ thể bằng prompt triển khai. Chỉ sau bước này mới sửa học liệu.

Không cần tạo AGENTS.md mới để dùng bộ này. Nếu repo đã có chỉ dẫn chung, chỉ bổ sung liên kết đến điểm vào khi bạn giao rõ việc đó; tránh biến toàn bộ repo ZO Math thành dự án chỉ chuyên ôn thi 2027.

## 2. Ai làm việc gì?

**Codex là công cụ thực hiện chính; Copilot là người rà độc lập theo từng đợt.** Bạn quyết định phạm vi và chấp nhận sản phẩm.

| Chủ thể | Trách nhiệm |
|---|---|
| Bạn | Chọn việc, đọc phạm vi sửa, xem bản thực chạy và chốt nghiệm thu |
| Codex | Đối chiếu nguồn, sửa trong phạm vi được giao, kiểm, báo cáo và cập nhật hồ sơ |
| Copilot | Đọc diff và bằng chứng, tìm lỗi/sót/mâu thuẫn; mặc định chỉ báo cáo trong lượt rà |

Không để hai công cụ sửa cùng tệp đồng thời. Khi chuyển sang Copilot, để Codex kết thúc lượt ghi; khi quay lại Codex, chỉ chuyển các phát hiện cụ thể đã xác nhận. Không coi việc một AI đồng ý với AI khác là phép kiểm toán học.

## 3. Prompt dùng lần đầu: nhập bộ điều hành và kiểm G01

Mở `README.md` trong VS Code và đính kèm tệp đó vào cuộc trò chuyện của công cụ. Dán nguyên khối sau:

```text
Hãy đọc README.md đang được đính kèm và các tệp mà nó chỉ dẫn cho nhiệm vụ R1-G01. Đọc hướng dẫn repo áp dụng trước khi thao tác.

Nhiệm vụ lần này: đưa bộ điều hành vào sử dụng và đối chiếu R1-G01 hiện hành trong repo. Kiểm nhánh, trạng thái Git và diff sẵn có. Tìm Kế hoạch 0.6, nguồn QMD, các thành phần dùng chung và các bản xuất có liên quan. Được cập nhật đường dẫn đã xác minh và kết quả kiểm trong bộ điều hành; chưa sửa học liệu, CSS, script, checker hoặc cấu hình. Chưa commit, push hay phát hành.

Đối chiếu từng yêu cầu trong hồ sơ R1_G01.md với repo thật. Báo cáo: đã đáp ứng; còn thiếu; phát hiện cũ không còn áp dụng; phần chưa kiểm được. Mỗi phát hiện phải có đường dẫn/vị trí, bằng chứng, mức ảnh hưởng, sửa đề xuất và phép kiểm. Không tự tính một mã bài khác là bằng chứng mới nếu nội dung đã lộ.

Lưu báo cáo dưới _audit/ theo quy ước repo. Cập nhật tóm tắt vào hồ sơ G01 và bảng điều hành, giữ phần đề xuất khác với phần đã chốt. Kết thúc bằng một phạm vi sửa cụ thể để tôi xem xét; không thực hiện phạm vi sửa đó trong lượt này.
```

## 4. Prompt triển khai sau khi đã xem báo cáo

Đính kèm báo cáo vừa đọc cùng điểm vào. Chọn rõ các ID phát hiện được chấp nhận nếu không nhận toàn bộ. Dán khối sau và thay dòng phạm vi bằng quyết định thực của bạn:

```text
Tôi chốt phạm vi sửa được ghi dưới đây trong báo cáo đang đính kèm:
[Điền các ID phát hiện và nội dung đã chấp nhận; không để nguyên dòng này.]

Hãy đọc điểm vào của bộ điều hành, trạng thái hiện hành và hồ sơ R1-G01. Thực hiện phạm vi vừa chốt trên nguồn repo, bảo toàn diff sẵn có và nội dung còn đúng. Nếu repo đã thay đổi từ báo cáo, đối chiếu lại phần bị ảnh hưởng trước khi sửa.

Kiểm nội dung toán, đường học, nguồn bằng chứng và các tình huống nghiệm thu liên quan; dựng HTML để tôi xem. Nếu thay thành phần dùng chung, kiểm ảnh hưởng lên G02 và trang liên quan. Tệp tạm/báo cáo để dưới _audit/. Không sửa PDF, không commit/push hoặc phát hành trong lượt này.

Cuối lượt, báo cáo những gì đã sửa, bằng chứng kiểm, việc chưa kiểm được và các tệp thay đổi; cập nhật hồ sơ G01 và bảng điều hành. Ghi trạng thái đúng, chưa tự đánh dấu tôi đã duyệt HTML.
```

## 5. Prompt cho Copilot rà kết quả

Đính kèm điểm vào, hồ sơ G01 và báo cáo triển khai; chỉ dẫn phạm vi diff hoặc commit thực nếu có.

```text
Hãy rà độc lập kết quả tinh chỉnh R1-G01 theo hồ sơ gói, kiến trúc và quy trình trong bộ điều hành đang đính kèm. Đây là lượt rà, không sửa nguồn hoặc cập nhật trạng thái nghiệm thu.

Đọc diff thuộc nhiệm vụ và kiểm các vị trí nguồn liên quan. Ưu tiên tính đúng của toán, phạm vi bắt buộc, bài mới có thật sự chưa lộ, các tuyến sửa/Nền và đích quay về. Đối chiếu các kết quả kiểm đã báo cáo; phân biệt kiểm mã với kiểm bản thực chạy. Không phát sinh một cuộc tái thiết kế ngoài phạm vi.

Với mỗi vấn đề, nêu vị trí, cách tái hiện hoặc lập luận, mức ảnh hưởng và sửa tối thiểu. Nếu không thấy lỗi, nói rõ phạm vi đã kiểm cùng phần còn chưa kiểm. Không coi không phát hiện lỗi là bằng chứng đã nghiệm thu toàn gói.
```

Codex xử lý các phát hiện được xác nhận; nếu có tranh luận toán học, đối chiếu định nghĩa và tự giải bài, không bỏ phiếu giữa hai công cụ.

## 6. Khi bạn đã duyệt HTML

Giao rõ: “Tôi chấp nhận bản HTML tại [vị trí/bản/commit thực]. Hãy ghi việc chấp nhận, đồng bộ các PDF bị ảnh hưởng từ cùng nguồn và kiểm tính nhất quán; chưa phát hành.” Sau khi xem kết quả, giao phát hành bằng quy trình repo đang dùng. Không cần viết lại kiến trúc ở bước này.

Phát hành có thể gồm commit/push theo quy trình đã được bạn giao. Luôn stage tệp rõ ràng, không `git add .`. Ghi bản hoặc commit thật đã phát hành vào hồ sơ. Nếu chưa phát hành, giữ trạng thái đó dù PDF đã xong.

## 7. Chuyển sang G02 và gói mới

Khi G01 đạt, cập nhật các quyết định chung có hiệu lực trước. Sau đó mở hồ sơ G02 và giao Codex đối chiếu như G01, thay mục tiêu bằng G02; không chạy lại prompt tích hợp Pha 2 cũ.

Với gói mới, dùng mẫu `mau/ho_so_goi.md`. Chốt phạm vi và ma trận trước, rồi mới biên soạn và tạo giao diện. Chưa cấp mã R1-G03 cho một phạm vi chưa xác định. R2, R3… là mạch; mỗi mạch có thể có nhiều gói.

## 8. Cập nhật ở đâu?

| Điều vừa thay đổi | Nơi cập nhật |
|---|---|
| Việc đang làm, thứ tự tiếp theo | 03_dieu_hanh_chuong_trinh.md |
| Phạm vi, nguồn, câu hỏi, tuyến hỗ trợ, kết quả kiểm của một gói | Hồ sơ tương ứng trong `goi/` |
| Quy tắc học tập dùng chung | 01_kien_truc_hoc_tap.md và nhật kí quyết định; liệt kê gói cần rà |
| Cấu trúc trang, điều hướng, responsive và nghiệm thu giao diện | 07_quy_chuan_cau_truc_trang_nguoi_hoc.md; chi tiết component ở quy_chuan_goi_qmd.md |
| Cách kiểm, cách dựng hoặc phát hành dùng chung | 02_quy_trinh_va_nghiem_thu.md; đối chiếu hướng dẫn repo |
| Một quyết định quan trọng hoặc đổi quyết định cũ | 04_nhat_ki_quyet_dinh.md |
| Phạm vi/định hướng toàn chương trình | Đề xuất sửa Kế hoạch; chỉ cập nhật phiên bản Kế hoạch khi bạn giao rõ |
| Đường dẫn hoặc vai trò tài liệu nguồn | `README.md` và `06_nguon_va_chuyen_tiep.md` |

Không cập nhật cả bộ mỗi lần sửa một câu. Không chép toàn bộ nội dung QMD sang hồ sơ gói. Riêng các đoạn thay thế G01 hiện nằm trong hồ sơ để triển khai: sau khi tích hợp, ghi nguồn chính và phiên bản đã tích hợp; ngừng sửa song song hai bản.

Khi tiếp nhận một bộ bàn giao cũ, dùng quy trình ở Mục 2.1 của `02_quy_trinh_va_nghiem_thu.md`. Prompt cũ chỉ là bằng chứng về một lượt giao việc; không tự cấp quyền commit, dựng PDF, xuất bản hoặc buộc worktree hiện tại phải quay về commit nền được ghi trong prompt.

### Tiếp tục một phiên đã tạm nghỉ

Bạn chỉ cần nói tên bước đã bàn giao. Agent đọc bảng 03, quyết định sau cùng và hồ sơ liên quan, rồi kiểm nguồn/checkpoint/diff; không yêu cầu bạn tự tìm tài liệu cũ hoặc biết thiết kế, CLI. Khi cùng vấn đề đã đổi nhiều lần, agent theo quyết định cuối có căn cứ và ghi phần cũ bị thay. Không tự restore toàn bộ checkpoint hoặc dùng prompt lịch sử cấp quyền mới.

Sau **mỗi câu trả lời**, agent kết thúc bằng **“Bước tiếp theo: [tên nhiệm vụ rõ ràng]”**, nêu ngắn đầu ra và giới hạn nếu cần. Tên ấy phải khớp bảng 03 khi thuộc công việc khóa; không chép nhiều roadmap vào các hồ sơ khác. Bước đề xuất không tự là nhiệm vụ đang được thực hiện.

## 9. Checklist kết thúc mỗi phiên

- [ ] Đã phân biệt việc hoàn thành với việc mới đề xuất.
- [ ] Hồ sơ gói có kết quả kiểm, vị trí nguồn, giới hạn và lỗi chặn còn lại.
- [ ] Bảng điều hành có đúng một việc hiện hành và bước tiếp theo rõ; câu trả lời kết thúc bằng tên bước ấy.
- [ ] Quyết định mới quan trọng có căn cứ và trạng thái đúng trong nhật kí.
- [ ] Diff được báo cáo; không mất thay đổi có sẵn; commit nếu đã được giao, ghi hash thật khi có.

Bạn có thể kết thúc một phiên dài ngay khi các thông tin trên đã lưu. Phiên sau chỉ cần đính kèm điểm vào và nói “tiếp tục công việc hiện hành”; công cụ vẫn phải kiểm lại trạng thái repo.

## 10. Phiên bản và lịch sử

Giữ tên tệp cố định. Khi thay đổi nội dung quy phạm, tăng phiên bản trong tệp (0.1 → 0.2…) và ghi quyết định liên quan. Sửa trạng thái hoặc kết quả kiểm: cập nhật ngày và bằng chứng, không nhất thiết tăng phiên bản chuẩn kiến trúc. Dùng Git để xem và khôi phục thay đổi có phạm vi; không tạo các bản sao “mới nhất”.

PDF ngày 06/10 giữ làm bản đọc tổng hợp theo thời điểm. Bộ Markdown sẽ tiếp tục phát triển; không cần xuất lại PDF mỗi phiên. Nếu cần bản PDF mới, xuất từ trạng thái Markdown đã chốt và ghi ngày mới.

Các prompt trên là hướng dẫn thao tác theo phạm vi bạn giao, không phải lệnh tự chạy mỗi khi công cụ đọc tệp. Prompt mẫu không tự cấp quyền thay đổi repo hay phát hành.
