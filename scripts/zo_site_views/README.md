# Tổng lượt xem ZO Math

`config.json` là cấu hình công khai duy nhất. Nguồn số liệu là Cloudflare Web
Analytics, tài khoản/site/hostname được giới hạn trong cấu hình; lọc bot bằng
`bot: 0`. Không dùng số request HTTP, lượt ghé hoặc bộ đếm trong trình duyệt
để thay lượt xem. Mốc bắt đầu 03/11/2026 là ngày bắt đầu ghi nhận, không tuyên
bố phục hồi lịch sử trước khi cài beacon.

`worker.mjs` giữ sổ tổng hợp từng ngày UTC, thay số theo ngày khi cập nhật,
không cộng trùng. Mỗi lần cập nhật chỉ công bố sau khi tất cả truy vấn thành
công; kiểm lại bảy ngày gần nhất để nhận hiệu chỉnh. Giữ ngày cũ vượt cửa sổ
lưu dữ liệu Cloudflare; nếu bỏ lỡ quá 170 ngày thì dừng để đối soát, không
đổi tổng lịch sử thành một cửa sổ trượt. Dữ liệu có thể được Cloudflare lấy
mẫu/hiệu chỉnh; không cam kết đếm chính xác từng lượt thực tế.

Chạy kiểm với `node --test scripts/zo_site_views/worker.test.mjs`.
Chạy API cục bộ bằng `node scripts/zo_site_views/serve.mjs`; chỉ lắng nghe
127.0.0.1:8878, cập nhật mỗi năm phút. Chân trang truy vấn mỗi phút khi tab
hiện. Chưa có số thật thì báo chưa lấy được; dữ liệu quá 20 phút mang trạng
thái chưa cập nhật, không trình bày như số mới.

Khóa chỉ cần quyền Account / Account Analytics / Read, giới hạn đúng tài
khoản. Dùng biến tiến trình `CF_ANALYTICS_API_TOKEN`, hoặc kho Windows DPAPI
do `zo_site_views_secret.py` quản lý trong `.local/site-views/analytics.dpapi`.
Thư mục này chứa trạng thái vận hành riêng, không phải cache biên dịch; giữ
khóa mã hóa và sổ tổng hợp khi dọn `.quarto/`. Nó được bỏ qua có chủ đích bởi
Git, không phải nguồn sinh nội dung học liệu.
Không lưu khóa vào cấu hình, Git, HTML, báo cáo hoặc clipboard. Không in khóa
ra hội thoại. Lệnh Python luôn qua `scripts/zo_python.py`.

`worker.mjs` cũng là handler dành cho Cloudflare Worker sau này: cần binding
KV `SITE_VIEWS`, secret `CF_ANALYTICS_API_TOKEN`, biến `SITE_CONFIG` đúng nội
dung cấu hình và cron `*/5 * * * *`; route GET `/api/site-views`. Public GET
chỉ đọc bản tổng hợp, không thực hiện truy vấn Cloudflare theo mỗi khách.
Việc tạo KV, gán secret/route, cấu hình cron và triển khai là bước xuất bản
riêng, chưa được thực hiện bởi lệnh thử cục bộ.

Sửa JS/CSS dùng chung mà không sửa chính văn: `zo_course_site.py assets`
qua launcher. Cổng này từ chối thay QMD/cấu hình/nội dung hay HTML đã lệch,
chỉ cập nhật đúng các tài sản được liệt kê, rồi giữ hồ sơ nguồn và bảo vệ.
