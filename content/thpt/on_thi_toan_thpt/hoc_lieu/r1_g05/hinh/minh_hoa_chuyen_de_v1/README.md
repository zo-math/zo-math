# Ứng dụng đạo hàm trong thực tiễn — bộ minh họa v1

Thư viện chính thức của gói R1-G05. Dựa trên Ví dụ 05: hộp từ tấm bìa vuông 30 cm, cao 2/5/10 cm, đáy 26/20/10 cm; hộp 5 cm có thể tích lớn nhất.

- originals/: giữ nguyên ảnh gốc, không ghi đè.
- candidates/: bốn nguồn bố trí lại bằng công cụ image_gen; bố cục mới chờ chủ trì duyệt riêng.
- r1_g05-minh-hoa-*.png: đủ 1:1 (1200×1200), 3:4 (960×1280), 4:3 (1280×960), 9:16 (864×1536), 16:9 (1600×900), nền trong suốt.
- manifest.json: nguồn bài, mô hình, kích thước, hash, prompt đầy đủ và trạng thái từng bố cục.

Lưu trữ chính thức không đồng nghĩa duyệt bố cục mới hoặc phát hành. Website dùng bản gốc từ thư viện chính thức; không tự thay bằng biến thể. Không đổi bìa bài học/PDF.

Dựng/kiểm lại qua scripts/zo_topic_art.py build/check --package r1_g05, gọi bằng scripts/zo_python.py.
