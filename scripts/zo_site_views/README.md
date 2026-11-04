# Tổng lượt xem ZO Math

`config.json` là cấu hình công khai duy nhất. Nguồn số liệu là Cloudflare Web
Analytics, tài khoản/site/hostname được giới hạn trong cấu hình; lọc bot bằng
`bot: 0`. Không dùng số request HTTP, lượt ghé hoặc bộ đếm trong trình duyệt
để thay lượt xem. Mốc bắt đầu 03/11/2026 là ngày bắt đầu ghi nhận, không tuyên
bố phục hồi lịch sử trước khi cài beacon.

Chân trang chỉ hiển thị hai dòng: lượt xem trong ngày và tổng từ 3/11/2026.
Lượt trong ngày được truy vấn riêng từ 00:00 giờ Việt Nam (UTC+7), không lấy
ngày UTC hoặc 24 giờ trượt. Qua nửa đêm, không hiển thị số ngày trước như
số hôm nay trong lúc chờ lần cập nhật mới. Nguồn và trạng thái cập nhật nằm
trong chú giải khi trỏ vào thống kê.

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

Worker công khai `zo-math-site-views` chạy tại
`https://zo-math-site-views.khongvamot2024.workers.dev/api/site-views`.
Chân trang trên zomath.vn đọc endpoint này qua CORS; không cần đổi DNS.
Worker dùng KV `SITE_VIEWS`, secret `CF_ANALYTICS_API_TOKEN`, biến `SITE_CONFIG`
và cron `*/5 * * * *`. Public GET chỉ đọc bản tổng hợp, không truy vấn Analytics
theo mỗi khách. Khóa Analytics chỉ đọc được giữ trong Secret phía Cloudflare.

Đường triển khai chính thức, chỉ chạy sau khi được giao quyền triển khai:
`python scripts/zo_python.py scripts/zo_site_views_deploy.py --worker zo-math-site-views --subdomain khongvamot2024 --report _audit/<ten-luot>/cloudflare-deployment.json`.
Công cụ đọc khóa triển khai tạm đã mã hóa ở `.local/site-views/deploy.dpapi`,
chỉ ghi Worker/KV/lịch của dịch vụ này, giữ sổ đã có; lần đầu cần sổ Cloudflare
thật vừa cập nhật. Không đọc token qua tham số hay ghi vào báo cáo. Thu hồi
khóa triển khai sau khi xong; quyền Analytics của Worker không phụ thuộc khóa
triển khai tạm. Báo cáo triển khai và GET công khai là bằng chứng riêng;
phải xác nhận timestamp tiến lên sau một lượt cron thực tế trước bàn giao.

Sửa JS/CSS dùng chung mà không sửa chính văn: `zo_course_site.py assets`
qua launcher. Cổng này từ chối thay QMD/cấu hình/nội dung hay HTML đã lệch,
chỉ cập nhật đúng các tài sản được liệt kê, rồi giữ hồ sơ nguồn và bảo vệ.
