# Khảo sát sự biến thiên và vẽ đồ thị — bộ minh họa v1

Ảnh gốc đã được chủ trì duyệt ngày 04/11/2026, giữ nguyên byte tại `originals/r1_g04-approved.png`. Ý tưởng từ Ví dụ 05: u(x)=x²/(x−1), cực đại 0 thấp hơn cực tiểu 4 trên hai nhánh rời.

| Tỉ lệ | Kích thước PNG | Trạng thái |
|---|---|---|
| 1:1 | 1200 × 1200 | Dựng lại đúng công thức — chờ duyệt bố cục |
| 3:4 | 960 × 1280 | Dựng lại đúng công thức — chờ duyệt bố cục |
| 4:3 | 1280 × 960 | Dựng lại đúng công thức — chờ duyệt bố cục |
| 9:16 | 864 × 1536 | Dựng lại đúng công thức — chờ duyệt bố cục |
| 16:9 | 1600 × 900 | Giữ bố cục đã chốt |

Sau khi chủ trì phát hiện bản AI vuông vẽ nhánh cắt sai tiệm cận xiên, bốn bố cục mới được dựng trực tiếp bằng `scripts/zo_topic_art_g04.py`. Đặt t=x−1, v=u−2=t+1/t. Mỗi bố cục dùng cùng một ánh xạ x/y cho cả nhánh đồ thị và hai tiệm cận. Nhánh t>0 luôn trên đường v=t; t<0 luôn dưới. Kiểm đủ 2002 điểm mỗi bố cục; các đoạn nối cũng giữ cùng phía vì đường tiệm cận là đường thẳng. Điểm cực trị t=−1,v=−2 và t=1,v=2 được đặt chính xác. Không dùng các bản AI sinh sai làm nguồn.

`candidates/` giữ PNG và SVG tự chứa phông Be Vietnam Pro của bốn bố cục dựng theo công thức. Màu vector dùng đúng #EF5350, #FFCA28, #3E3A35. Nền trong suốt, không có điểm ở giao hai tiệm cận. `manifest.json` lưu nguồn/hash/recipe/kiểm toán và trạng thái từng bản. Bốn bố cục chờ chủ trì duyệt riêng; đúng toán không tự là duyệt thẩm mĩ.

```text
python -B scripts/zo_python.py -B scripts/zo_topic_art_g04.py
python -B scripts/zo_python.py -B scripts/zo_topic_art.py build --package r1_g04
python -B scripts/zo_python.py -B scripts/zo_topic_art.py check --package r1_g04
```

Danh mục chung của khóa 2027 vẫn chọn ảnh gốc đã chốt cho website; không tự đổi ảnh hiển thị. Ảnh gốc và HTML/PDF không đổi trong lượt tạo bộ ảnh. Không commit, push hoặc phát hành.
