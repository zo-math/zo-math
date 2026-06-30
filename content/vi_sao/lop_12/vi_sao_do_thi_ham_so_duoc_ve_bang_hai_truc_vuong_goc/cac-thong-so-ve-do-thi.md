Dưới đây là bản bảng `.md` để theo dõi và tái dùng.

## 1. Thiết lập chung

| Thành phần  |     Thông số | Ghi chú                                    |
| ----------- | -----------: | ------------------------------------------ |
| `border`    |        `6pt` | Giữ lề ngoài vừa đủ khi xuất PDF/SVG       |
| Tỉ lệ ngang |   `x=1.75cm` | Kéo giãn trục $x$, giúp nhãn không quá sát |
| Tỉ lệ dọc   |    `y=.75cm` | Làm hình cao hơn, dễ đặt nhãn $y$          |
| Mũi tên     |  `>=Stealth` | Dùng thống nhất kiểu mũi tên               |
| Cỡ chữ      | `font=\tiny` | Phù hợp khi nhiều nhãn nhỏ                 |

## 2. Thứ tự các tầng

| Tầng | Nội dung                       | Vai trò                   |
| ---: | ------------------------------ | ------------------------- |
|    1 | Đoạn tham chiếu mờ về hai trục | Nền phụ trợ               |
|    2 | Đường cong chính               | Đối tượng nổi bật nhất    |
|    3 | Hai trục tọa độ có mũi tên     | Khung đọc                 |
|    4 | Vạch trên trục $x$             | Đánh dấu vị trí ngang     |
|    5 | Vạch trên trục $y$             | Đánh dấu độ cao           |
|    6 | Nhãn thủ công trên trục $x$    | Đọc giá trị $x$           |
|    7 | Nhãn thủ công trên trục $y$    | Đọc giá trị $y$           |
|    8 | Điểm mẫu trên đường cong       | Nhấn mạnh dữ liệu rời rạc |

## 3. Độ nổi bật của nét

| Thành phần       | Thông số                                   | Mức nổi bật                    |
| ---------------- | ------------------------------------------ | ------------------------------ |
| Đường cong chính | `line width=1pt, draw=black`               | Rõ nhất                        |
| Điểm mẫu         | `circle (1.45pt)`                          | Rõ, nhưng không lấn đường cong |
| Trục tọa độ      | `line width=.5pt`                          | Mảnh hơn đường cong            |
| Vạch chia        | `line width=0.35pt`                        | Nhẹ                            |
| Đoạn tham chiếu  | `dashed, line width=0.35pt, draw=black!15` | Mờ nhất                        |

## 4. Đoạn tham chiếu

| Thuộc tính | Giá trị                |
| ---------- | ---------------------- |
| Kiểu nét   | `dashed`               |
| Độ dày     | `line width=0.35pt`    |
| Màu        | `draw=black!15`        |
| Đoạn đứng  | `(\xx,0) -- (\xx,\yy)` |
| Đoạn ngang | `(\xx,\yy) -- (0,\yy)` |

## 5. Đường cong

| Thuộc tính | Giá trị                  |
| ---------- | ------------------------ |
| Độ dày     | `line width=1pt`         |
| Màu        | `draw=black`             |
| Miền vẽ    | `domain=-2.5:2.5`        |
| Số mẫu     | `samples=180`            |
| Làm mượt   | `smooth`                 |
| Biến chạy  | `variable=\t`            |
| Công thức  | `({\t},{\t*\t*\t-3*\t})` |

## 6. Trục tọa độ

| Thành phần  | Thông số                              |
| ----------- | ------------------------------------- |
| Mũi tên     | `-{Stealth[length=4pt,width=5pt]}`    |
| Độ dày trục | `line width=.5pt`                     |
| Trục $x$    | `(-2.85,0) -- (2.85,0)`               |
| Nhãn $x$    | `\node[right=1pt] at (2.85,0) {$x$};` |
| Trục $y$    | `(0,-8.8) -- (0,8.8)`                 |
| Nhãn $y$    | `\node[above=1pt] at (0,8.8) {$y$};`  |

## 7. Vạch chia

| Trục     | Thông số                    | Ghi chú              |
| -------- | --------------------------- | -------------------- |
| Trục $x$ | `(\xx,0.09) -- (\xx,-0.09)` | Vạch dọc nhỏ         |
| Trục $y$ | `(-0.05,\yy) -- (0.05,\yy)` | Vạch ngang nhỏ       |
| Độ dày   | `line width=0.35pt`         | Mảnh, không lấn nhãn |

## 8. Nhãn thủ công

| Loại nhãn       | Mẫu thông số                        | Ghi chú                            |
| --------------- | ----------------------------------- | ---------------------------------- |
| Nhãn thường     | `fill=white, inner sep=1pt`         | Giữ nền trắng để tránh lẫn với nét |
| Khoảng cách gần | `above=2pt`, `below=2pt`            | Dùng nhiều nhất                    |
| Lệch trái       | `left=2pt`, `left=4pt`              | Dùng cho nhãn $y$                  |
| Lệch phải       | `right=2pt`                         | Tránh chồng bên trái               |
| Chéo            | `below left=2pt`, `above right=2pt` | Dùng khi nhãn dễ đè lên trục/điểm  |
| Gốc tọa độ      | `below left=2pt`                    | Chỉ ghi một số $0$                 |

## 9. Quy tắc ghi nhãn số

| Tình huống      | Cách ghi                                      |
| --------------- | --------------------------------------------- |
| Gốc tọa độ      | Chỉ ghi `$0$` một lần                         |
| Không ghi ở gốc | Không ghi `$0.0$` trên trục $x$               |
| Không ghi ở gốc | Không ghi `$0.000$` trên trục $y$             |
| Số nguyên       | Ghi gọn: `$-2$`, `$-1$`, `$1$`, `$2$`         |
| Số không nguyên | Giữ cần thiết: `$-2.5$`, `$1.375$`, `$8.125$` |
| Nhãn dễ đè      | Đặt thủ công từng `\node`                     |

## 10. Điểm mẫu

| Thuộc tính  | Giá trị                                   |
| ----------- | ----------------------------------------- |
| Màu         | `black`                                   |
| Kiểu        | `\fill[black]`                            |
| Bán kính    | `circle (1.45pt)`                         |
| Vị trí tầng | Sau cùng                                  |
| Vai trò     | Nổi rõ trên đường cong và đoạn tham chiếu |
