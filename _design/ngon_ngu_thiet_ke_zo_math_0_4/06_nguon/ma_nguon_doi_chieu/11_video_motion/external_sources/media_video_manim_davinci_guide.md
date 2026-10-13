# Hướng dẫn tạo video toán học bằng Manim và DaVinci Resolve

Tài liệu này chốt một quy trình sản xuất video toán học phù hợp với ZO Math: **viết kịch bản bằng VS Code, tạo hoạt hình toán học bằng Manim, thu voice-over riêng, rồi dựng hậu kì bằng DaVinci Resolve**.

CapCut chỉ được xem như giải pháp phụ khi cần dựng nhanh, làm bản nháp hoặc chưa kịp làm quen với DaVinci Resolve.

## 1. Quy trình tổng thể

Quy trình chính nên dùng lâu dài:

```text
Viết kịch bản
→ Thu voice-over
→ Tạo hoạt hình toán học bằng Manim
→ Dựng hậu kì bằng DaVinci Resolve
→ Xuất video hoàn chỉnh
```

Trong quy trình này, **VS Code không phải là một công đoạn sản xuất video**. VS Code chỉ là không gian làm việc dùng để viết kịch bản, quản lí thư mục, viết code Manim và chạy lệnh render trong terminal. Vì vậy, VS Code nên được xếp vào nhóm công cụ hỗ trợ, không đặt ngang hàng với Manim, voice-over và DaVinci Resolve trong dòng công việc chính.

Diễn giải theo công đoạn:

```text
1. Viết kịch bản video toán học.
2. Chia kịch bản thành từng cảnh nhỏ.
3. Thu voice-over theo kịch bản.
4. Viết code Manim để tạo hoạt hình toán học tương ứng.
5. Render video Manim không âm thanh.
6. Đưa voice-over và video Manim vào DaVinci Resolve.
7. Căn nhịp hình theo lời đọc.
8. Xử lí âm thanh, thêm phụ đề, thêm nhạc nền nếu cần.
9. Xuất video hoàn chỉnh để đăng YouTube.
```

Nguyên tắc quan trọng:

> **Voice-over là xương sống. Manim tạo hình toán học. DaVinci Resolve hoàn thiện video.**

Không nên làm hình trước rồi cố đọc theo hình. Với video toán học, nhịp giải thích quan trọng hơn hiệu ứng. Vì vậy, cần thu hoặc ít nhất là viết xong kịch bản đọc trước, sau đó mới căn hoạt hình theo lời đọc.

## 2. Công cụ cần thiết

### 2.1. VS Code

Dùng để:

```text
viết kịch bản Markdown;
quản lí thư mục dự án;
viết code Manim;
chạy lệnh render trong terminal.
```

### 2.2. Manim

Dùng để tạo:

```text
công thức toán học;
biến đổi đại số;
đồ thị hàm số;
hình học;
sơ đồ;
timeline;
chuyển động minh họa ý tưởng toán học.
```

Manim nên giữ vai trò sản xuất **hình toán học chính xác, sạch và có thể tái sử dụng**.

### 2.3. DaVinci Resolve

Dùng để:

```text
cắt ghép video;
đưa voice-over vào timeline;
căn nhịp hình theo lời đọc;
xử lí âm thanh bằng Fairlight;
thêm phụ đề;
thêm nhạc nền;
chỉnh màu nếu cần;
xuất video cuối cùng.
```

DaVinci Resolve là phần mềm dựng chính cho ZO Math vì phù hợp với mục tiêu dài hạn: làm nhiều video, giữ chuẩn hậu kì ổn định, có khả năng sửa lại dự án sau nhiều tháng.

### 2.4. CapCut

CapCut chỉ nên dùng như giải pháp phụ khi:

```text
cần dựng nhanh một bản thử;
cần làm video ngắn;
chưa kịp học DaVinci Resolve;
cần auto caption nhanh;
cần dựng bản demo để kiểm tra ý tưởng.
```

Không nên lấy CapCut làm quy trình chính cho ZO Math nếu mục tiêu là xây dựng hệ thống video toán học nghiêm túc, dài hạn và có thể chuẩn hóa.

## 3. Chốt lựa chọn công cụ dựng video

### 3.1. So sánh DaVinci Resolve và CapCut

| Tiêu chí                          | DaVinci Resolve                                    | CapCut                                 |
| --------------------------------- | -------------------------------------------------- | -------------------------------------- |
| Vai trò nên dùng                  | Công cụ dựng chính                                 | Công cụ phụ, dựng nhanh                |
| Phù hợp với                       | Video toán học dài hạn, nghiêm túc, cần hậu kì tốt | Shorts, bản nháp, video nhanh          |
| Quản lí dự án lớn                 | Tốt                                                | Cơ bản                                 |
| Xử lí âm thanh                    | Mạnh, có Fairlight                                 | Dễ dùng nhưng không sâu bằng           |
| Chỉnh màu                         | Rất mạnh                                           | Cơ bản, thiên về filter nhanh          |
| Phụ đề                            | Làm được chuyên nghiệp, kiểm soát cao              | Nhanh, tiện, đặc biệt với auto caption |
| Độ khó ban đầu                    | Cao hơn                                            | Dễ hơn                                 |
| Khả năng dùng lâu dài cho ZO Math | Rất phù hợp                                        | Chỉ phù hợp như công cụ phụ            |

### 3.2. Lựa chọn chính

```text
Pipeline chính:  Manim + DaVinci Resolve
Pipeline phụ:    Manim + CapCut
```

Lí do chọn DaVinci Resolve làm chính: video toán học sống bằng lời giải thích rõ, âm thanh sạch, nhịp hình chính xác, phụ đề nghiêm túc và khả năng lưu trữ dự án lâu dài. Đây là những điểm DaVinci Resolve phù hợp hơn CapCut.

## 4. Cấu trúc thư mục chuẩn cho xưởng video ZO Math

Nên đặt xưởng video tại:

```text
E:\zo_media\zo_video
```

Cấu trúc thư mục:

```text
E:\zo_media\zo_video
│
├─ scripts
│  └─ vi_sao_can_chu_x.md
│
├─ manim
│  └─ vi_sao_can_chu_x.py
│
├─ audio
│  └─ vi_sao_can_chu_x_voice.wav
│
├─ resolve
│  └─ vi_sao_can_chu_x
│
├─ exports
│  ├─ preview
│  └─ final
│     └─ vi_sao_can_chu_x_final.mp4
│
└─ assets
   ├─ logo
   ├─ music
   └─ fonts
```

Ý nghĩa từng thư mục:

```text
scripts     chứa kịch bản video;
manim       chứa code Manim;
audio       chứa voice-over;
resolve     chứa ghi chú dựng, bản export project hoặc tài nguyên riêng của DaVinci Resolve;
exports     chứa video xuất ra;
assets      chứa logo, nhạc nền, font, hình phụ trợ.
```

Lưu ý: Manim sẽ tự sinh thư mục `media` bên trong thư mục dự án khi render. Nếu chạy Manim từ thư mục gốc `E:\zo_media\zo_video`, video render sẽ nằm trong:

```text
E:\zo_media\zo_video\media\videos\...
```

## 5. Chuẩn bị môi trường Manim

Mở VS Code, chọn:

```text
File → Open Folder → E:\zo_media\zo_video
```

Mở terminal trong VS Code:

```text
Terminal → New Terminal
```

Chạy:

```powershell
cd E:\zo_media\zo_video
```

Nếu chưa tạo thư mục dự án, chạy:

```powershell
mkdir scripts
mkdir manim
mkdir audio
mkdir resolve
mkdir exports
mkdir exports\preview
mkdir exports\final
mkdir assets
mkdir assets\logo
mkdir assets\music
mkdir assets\fonts
```

Nếu chưa cài Manim cho dự án này, chạy một lần:

```powershell
uv init
uv python install
uv add manim
```

Sau này quay lại dự án này thì không cần chạy lại các lệnh trên. Mỗi lần làm việc chỉ cần:

```powershell
cd E:\zo_media\zo_video
```

rồi render video bằng `uv run manim`.

## 6. Ví dụ video đầu tiên: Vì sao toán học cần chữ x?

### 6.1. Mục tiêu video

Video đầu tiên có mục tiêu rất nhỏ:

```text
Giải thích rằng chữ x không chỉ là một kí hiệu để tìm đáp án,
mà là cách con người đặt tên cho cái chưa biết để có thể suy nghĩ bằng kí hiệu.
```

Video minh họa quá trình:

```text
Một số cộng với 3 thì bằng 7
→ x + 3 = 7
→ x = 4
```

## 7. Công đoạn 1: Viết kịch bản

Tạo file:

```text
E:\zo_media\zo_video\scripts\vi_sao_can_chu_x.md
```

Nội dung kịch bản:

```markdown
# Vì sao toán học cần chữ x?

Ngày nay, ta viết phương trình x cộng 3 bằng 7 rất tự nhiên.

Nhưng trước khi có chữ x, người ta phải nói bài toán bằng lời:

Một số cộng với 3 thì bằng 7.

Khi đặt tên cho cái chưa biết là x,
ta biến một câu nói dài thành một biểu thức gọn.

Và khi cái chưa biết đã có tên,
ta có thể biến đổi nó như một đối tượng toán học.

Trừ 3 ở cả hai vế,
ta nhận được x bằng 4.

Vì vậy, chữ x không chỉ giúp ta tìm đáp án.

Nó giúp ta suy nghĩ bằng kí hiệu.
```

Khi đọc, cần ngắt nhịp rõ. Không đọc quá nhanh. Với video toán học, mỗi công thức quan trọng nên có khoảng nghỉ để người xem kịp nhìn.

## 8. Công đoạn 2: Thu voice-over

Thu âm bằng điện thoại, Audacity hoặc công cụ ghi âm khác. Ưu tiên thu trong phòng yên tĩnh.

Tên file voice-over:

```text
vi_sao_can_chu_x_voice.wav
```

Lưu đúng đường dẫn:

```text
E:\zo_media\zo_video\audio\vi_sao_can_chu_x_voice.wav
```

Chuẩn thu âm:

```text
đọc chậm hơn bình thường một chút;
giữ giọng rõ;
nghỉ ngắn sau mỗi ý;
tránh để nhạc nền hoặc tiếng quạt lọt vào bản thu;
ưu tiên WAV khi dựng hậu kì.
```

Nếu bản thu ban đầu là `.m4a`, có thể chuyển sang `.wav` bằng lệnh:

```powershell
ffmpeg -i audio\vi_sao_can_chu_x_voice.m4a -ar 48000 -ac 1 audio\vi_sao_can_chu_x_voice.wav
```

Ghi chú: `.wav` không tự làm bản thu hay hơn nếu nguồn ban đầu đã kém, nhưng đây là định dạng dễ dựng, ổn định và phù hợp cho hậu kì âm thanh hơn `.m4a`.

## 9. Công đoạn 3: Tạo code Manim

Tạo file:

```text
E:\zo_media\zo_video\manim\vi_sao_can_chu_x.py
```

Dán code sau:

```python
from manim import *

FONT = "Arial"


class ViSaoCanChuX(Scene):
    def clear_screen(self, *objects):
        self.play(*[FadeOut(obj) for obj in objects])

    def construct(self):
        self.camera.background_color = "#101014"

        # Cảnh 1: Mở đầu
        title = Text(
            "Vì sao toán học cần chữ x?",
            font=FONT,
            font_size=48,
        )

        subtitle = Text(
            "Một video Manim đầu tiên của ZO Math",
            font=FONT,
            font_size=26,
        ).next_to(title, DOWN, buff=0.4)

        self.play(Write(title), run_time=1.6)
        self.play(FadeIn(subtitle, shift=UP * 0.2), run_time=1)
        self.wait(1.2)
        self.clear_screen(title, subtitle)

        # Cảnh 2: Ngày nay, ta viết phương trình rất tự nhiên
        intro = Text(
            "Ngày nay, ta viết rất tự nhiên:",
            font=FONT,
            font_size=34,
        ).to_edge(UP)

        equation = MathTex("x", "+", "3", "=", "7", font_size=86)

        self.play(FadeIn(intro), run_time=1)
        self.play(Write(equation), run_time=1.5)
        self.wait(1.2)

        box = SurroundingRectangle(equation[0], color=YELLOW, buff=0.15)

        label = Text(
            "cái chưa biết",
            font=FONT,
            font_size=28,
            color=YELLOW,
        ).next_to(box, DOWN)

        self.play(Create(box), FadeIn(label), run_time=1)
        self.wait(1.5)
        self.clear_screen(intro, equation, box, label)

        # Cảnh 3: Trước khi có chữ x
        before = Text(
            "Nhưng trước khi có chữ x,\nngười ta nói bài toán bằng lời.",
            font=FONT,
            font_size=38,
            line_spacing=0.9,
        )

        sentence = Text(
            "Một số cộng với 3 thì bằng 7.",
            font=FONT,
            font_size=34,
            color=YELLOW,
        ).next_to(before, DOWN, buff=0.8)

        self.play(Write(before), run_time=2)
        self.wait(0.4)
        self.play(FadeIn(sentence, shift=UP * 0.2), run_time=1)
        self.wait(2)
        self.clear_screen(before, sentence)

        # Cảnh 4: Từ lời nói sang kí hiệu
        left_text = Text(
            "Một số cộng với 3\nthì bằng 7",
            font=FONT,
            font_size=32,
            line_spacing=0.9,
        ).shift(LEFT * 3.2)

        right_equation = MathTex("x", "+", "3", "=", "7", font_size=76).shift(RIGHT * 3.2)

        arrow = Arrow(
            start=LEFT * 1.3,
            end=RIGHT * 1.3,
            buff=0.1,
        )

        arrow_label = Text(
            "đặt tên cho cái chưa biết",
            font=FONT,
            font_size=24,
            color=YELLOW,
        ).next_to(arrow, UP, buff=0.25)

        self.play(FadeIn(left_text), run_time=1)
        self.play(Create(arrow), FadeIn(arrow_label), run_time=1.2)
        self.play(Write(right_equation), run_time=1.2)
        self.wait(2)
        self.clear_screen(left_text, arrow, arrow_label, right_equation)

        # Cảnh 5: Biến đổi phương trình
        note = Text(
            "Khi cái chưa biết có tên,\nta có thể biến đổi nó.",
            font=FONT,
            font_size=34,
            line_spacing=0.9,
        ).to_edge(UP)

        eq1 = MathTex("x", "+", "3", "=", "7", font_size=78)

        self.play(FadeIn(note), run_time=1.2)
        self.play(Write(eq1), run_time=1.2)
        self.wait(1.4)

        minus = MathTex("-3", r"\qquad", "-3", font_size=48)
        minus.next_to(eq1, DOWN, buff=0.35)

        self.play(Write(minus), run_time=1)
        self.wait(0.8)

        eq2 = MathTex("x", "+", "3", "-", "3", "=", "7", "-", "3", font_size=68)

        self.play(
            ReplacementTransform(eq1, eq2),
            FadeOut(minus),
            run_time=1.2,
        )
        self.wait(1)

        eq3 = MathTex("x", "=", "4", font_size=90)

        self.play(ReplacementTransform(eq2, eq3), run_time=1.2)
        self.wait(0.8)

        result_box = SurroundingRectangle(eq3, color=YELLOW, buff=0.2)

        self.play(Create(result_box), run_time=0.8)
        self.wait(1.8)

        self.clear_screen(note, eq3, result_box)

        # Cảnh 6: Kết luận
        conclusion_1 = Text(
            "Chữ x không chỉ giúp ta tìm đáp án.",
            font=FONT,
            font_size=38,
        )

        conclusion_2 = Text(
            "Nó giúp ta suy nghĩ bằng kí hiệu.",
            font=FONT,
            font_size=38,
            color=YELLOW,
        ).next_to(conclusion_1, DOWN, buff=0.45)

        self.play(Write(conclusion_1), run_time=1.5)
        self.wait(0.5)
        self.play(Write(conclusion_2), run_time=1.5)
        self.wait(3)

        self.play(FadeOut(conclusion_1), FadeOut(conclusion_2), run_time=1)
```

## 10. Công đoạn 4: Render video Manim

Trong terminal VS Code, chạy:

```powershell
cd E:\zo_media\zo_video
```

Render bản nháp:

```powershell
uv run manim -pql manim\vi_sao_can_chu_x.py ViSaoCanChuX
```

Video nháp sẽ nằm ở:

```text
E:\zo_media\zo_video\media\videos\vi_sao_can_chu_x\480p15\ViSaoCanChuX.mp4
```

Render bản đẹp để dựng:

```powershell
uv run manim -pqh manim\vi_sao_can_chu_x.py ViSaoCanChuX
```

Video đẹp thường nằm ở:

```text
E:\zo_media\zo_video\media\videos\vi_sao_can_chu_x\1080p60\ViSaoCanChuX.mp4
```

File này là video hình ảnh, chưa có voice-over.

## 11. Công đoạn 5: Dựng trong DaVinci Resolve

Ở công đoạn này, ta đã có hai tệp cần ghép:

```text
Video Manim không âm thanh:
E:\zo_media\zo_video\media\videos\vi_sao_can_chu_x\1080p60\ViSaoCanChuX.mp4

Voice-over:
E:\zo_media\zo_video\audio\vi_sao_can_chu_x_voice.wav
```

Mục tiêu của DaVinci Resolve trong video đầu tiên rất đơn giản:

```text
1. Đưa video Manim vào timeline.
2. Đưa voice-over vào timeline.
3. Cho hình và tiếng bắt đầu cùng lúc.
4. Nghe thử để kiểm tra nhịp.
5. Xuất thành file MP4 hoàn chỉnh.
```

Chưa cần thêm nhạc nền, chưa cần làm phụ đề, chưa cần chỉnh màu. Video đầu tiên chỉ cần hoàn thành đúng vòng sản xuất: **có hình, có tiếng, xuất được file cuối**.

### 11.1. Mở DaVinci Resolve và tạo project mới

Mở DaVinci Resolve.

Ở màn hình `Project Manager`, bấm:

```text
New Project
```

Đặt tên:

```text
vi_sao_can_chu_x
```

Bấm:

```text
Create
```

Ghi chú: DaVinci Resolve thường lưu project trong database riêng của phần mềm, không nhất thiết tạo một file project nằm trực tiếp trong thư mục Windows. Vì vậy, thư mục sau chỉ dùng để lưu ghi chú dựng, tài nguyên phụ hoặc bản export project nếu sau này cần:

```text
E:\zo_media\zo_video\resolve\vi_sao_can_chu_x
```

### 11.2. Thiết lập project trước khi dựng

Sau khi project mở ra, bấm biểu tượng bánh răng ở góc dưới bên phải để mở:

```text
Project Settings
```

Trong mục `Master Settings`, đặt:

```text
Timeline resolution: 1920 x 1080 HD
Timeline frame rate: 60
Playback frame rate: 60
```

Sau đó bấm:

```text
Save
```

Nếu DaVinci Resolve hỏi có thay đổi frame rate hay không, chọn:

```text
Change
```

Vì video Manim đang nằm trong thư mục `1080p60`, timeline nên để `60 fps` để khớp với file nguồn.

### 11.3. Đưa hai tệp vào Media Pool

Chuyển sang trang `Edit` ở thanh dưới cùng.

Ở góc trên bên trái, tìm vùng `Media Pool`.

Kéo file video Manim từ File Explorer vào `Media Pool`:

```text
E:\zo_media\zo_video\media\videos\vi_sao_can_chu_x\1080p60\ViSaoCanChuX.mp4
```

Tiếp tục kéo file voice-over vào `Media Pool`:

```text
E:\zo_media\zo_video\audio\vi_sao_can_chu_x_voice.wav
```

Nếu DaVinci Resolve hỏi có đổi project settings để khớp với clip hay không, có thể chọn `Change`, miễn là timeline cuối cùng vẫn là:

```text
1920 x 1080
60 fps
```

### 11.4. Tạo timeline

Trong `Media Pool`, bấm chuột phải vào vùng trống, chọn:

```text
Create New Timeline
```

Đặt tên timeline:

```text
vi_sao_can_chu_x_timeline
```

Bấm:

```text
Create
```

Sau khi tạo, timeline ở phía dưới màn hình sẽ có các track như:

```text
V1: track hình ảnh
A1: track âm thanh
```

### 11.5. Kéo voice-over và video vào timeline

Kéo file voice-over xuống track `A1` trước:

```text
A1: vi_sao_can_chu_x_voice.wav
```

Sau đó kéo file video Manim xuống track `V1`:

```text
V1: ViSaoCanChuX.mp4
```

Kéo đầu của cả hai clip sát về mốc đầu timeline:

```text
00:00:00:00
```

Sau bước này, timeline nên có dạng:

```text
V1: ViSaoCanChuX.mp4
A1: vi_sao_can_chu_x_voice.wav
```

Điểm cần nhớ: **voice-over nằm ở A1, video Manim nằm ở V1**.

### 11.6. Nghe thử để kiểm tra hình và tiếng

Bấm phím cách hoặc nút `Play` để xem từ đầu.

Kiểm tra ba điều:

```text
1. Video có hình.
2. Video có tiếng.
3. Hình và lời đọc bắt đầu tương đối đúng nhịp.
```

Nếu hình và lời đã khớp tương đối, có thể chuyển sang bước xuất video.

Nếu video Manim đi nhanh hơn voice-over, không nên vội kéo giãn clip trong DaVinci Resolve. Với video toán học làm bằng Manim, cách sạch hơn là quay lại file code:

```text
E:\zo_media\zo_video\manim\vi_sao_can_chu_x.py
```

Tăng thời gian chờ, ví dụ đổi:

```python
self.wait(1)
```

thành:

```python
self.wait(2)
```

hoặc tăng thời lượng chuyển động, ví dụ đổi:

```python
self.play(Write(eq1), run_time=1.2)
```

thành:

```python
self.play(Write(eq1), run_time=1.8)
```

Sau đó render lại:

```powershell
cd E:\zo_media\zo_video
uv run manim -pqh manim\vi_sao_can_chu_x.py ViSaoCanChuX
```

Rồi đưa bản video Manim mới vào DaVinci Resolve để kiểm tra lại với voice-over.

Vòng chỉnh sửa nên là:

```text
nghe voice-over
→ phát hiện đoạn hình nhanh hoặc chậm
→ sửa self.wait() hoặc run_time trong Manim
→ render lại video Manim
→ thay video trong DaVinci Resolve
→ kiểm tra lại
```

### 11.7. Chỉnh âm lượng voice-over cơ bản

Chọn clip âm thanh trên track `A1`.

Mở `Inspector` ở góc trên bên phải.

Nếu tiếng hơi nhỏ, tăng nhẹ mục `Volume`, chẳng hạn:

```text
Volume: +3 dB
```

Không nên tăng quá mạnh vì âm thanh có thể bị rè hoặc vỡ tiếng.

Với video đầu tiên, chỉ cần đạt ba yêu cầu:

```text
giọng đọc nghe rõ;
không bị quá nhỏ;
không bị rè hoặc méo tiếng.
```

Nếu sau này thêm nhạc nền, đặt nhạc ở track `A2` và giảm âm lượng rất thấp để không lấn giọng đọc.

### 11.8. Xuất video hoàn chỉnh

Chuyển sang trang `Deliver` ở thanh dưới cùng.

Thiết lập xuất video như sau:

```text
File name: vi_sao_can_chu_x_final
Location: E:\zo_media\zo_video\exports\final
Format: MP4
Codec: H.264
Resolution: 1920 x 1080 HD
Frame rate: 60
Audio codec: AAC
```

Sau đó bấm:

```text
Add to Render Queue
```

Ở bảng `Render Queue` bên phải, bấm:

```text
Render All
```

File hoàn chỉnh sẽ được xuất ra:

```text
E:\zo_media\zo_video\exports\final\vi_sao_can_chu_x_final.mp4
```

### 11.9. Kiểm tra file cuối

Sau khi render xong, mở file:

```text
E:\zo_media\zo_video\exports\final\vi_sao_can_chu_x_final.mp4
```

Kiểm tra lần cuối:

```text
[ ] Video có hình.
[ ] Video có tiếng.
[ ] Voice-over nghe rõ.
[ ] Hình và lời tương đối khớp nhau.
[ ] File xuất đúng 1920 x 1080.
[ ] File final nằm đúng thư mục exports\final.
```

Với video đầu tiên, mục tiêu không phải dựng thật phức tạp. Mục tiêu quan trọng nhất là hoàn thành trọn vẹn một vòng sản xuất:

```text
Manim render hình
→ voice-over có sẵn
→ DaVinci Resolve ghép hình và tiếng
→ xuất video final
```

Khi vòng này chạy được, những video sau chỉ cần lặp lại cùng quy trình và tinh chỉnh dần chất lượng.

## 12. Quy trình phụ nếu dùng CapCut

CapCut chỉ dùng khi cần dựng nhanh bản nháp.

Import video Manim:

```text
E:\zo_media\zo_video\media\videos\vi_sao_can_chu_x\1080p60\ViSaoCanChuX.mp4
```

Import voice-over:

```text
E:\zo_media\zo_video\audio\vi_sao_can_chu_x_voice.wav
```

Trong timeline CapCut:

```text
1. Đặt voice-over xuống audio track trước.
2. Đặt video Manim lên video track.
3. Căn hình theo giọng đọc.
4. Thêm phụ đề nếu cần.
5. Export bản nháp hoặc bản phụ.
```

Nếu export từ CapCut, lưu tại:

```text
E:\zo_media\zo_video\exports\preview\vi_sao_can_chu_x_capcut_preview.mp4
```

Không nên để bản CapCut ghi đè lên bản chính từ DaVinci Resolve.

## 13. Vòng lặp chỉnh sửa

Khi video chưa khớp, chỉnh theo vòng này:

```text
1. Nghe lại voice-over.
2. Xác định đoạn hình nhanh, chậm hoặc lệch ý.
3. Sửa `self.wait()` hoặc `run_time` trong file Manim.
4. Render lại video Manim.
5. Thay video Manim trong DaVinci Resolve.
6. Kiểm tra lại với voice-over.
7. Chỉ export final khi nhịp đã ổn.
```

Đường dẫn cần nhớ:

```text
Kịch bản:
E:\zo_media\zo_video\scripts\vi_sao_can_chu_x.md

Code Manim:
E:\zo_media\zo_video\manim\vi_sao_can_chu_x.py

Voice-over:
E:\zo_media\zo_video\audio\vi_sao_can_chu_x_voice.wav

Video Manim bản đẹp:
E:\zo_media\zo_video\media\videos\vi_sao_can_chu_x\1080p60\ViSaoCanChuX.mp4

Video hoàn chỉnh:
E:\zo_media\zo_video\exports\final\vi_sao_can_chu_x_final.mp4
```

## 14. Checklist trước khi xuất bản

Trước khi xem video là hoàn chỉnh, kiểm tra:

```text
[ ] Voice-over rõ, không bị nhỏ.
[ ] Nhạc nền nếu có không lấn giọng.
[ ] Công thức xuất hiện đúng lúc lời đọc nhắc đến.
[ ] Mỗi công thức quan trọng có đủ thời gian để nhìn.
[ ] Phụ đề nếu có không che công thức.
[ ] Video xuất đúng 1920 x 1080.
[ ] File final nằm đúng thư mục exports\final.
[ ] Tên file rõ ràng, không dùng tên chung chung như final_final.mp4.
```

## 15. Nguyên tắc sản xuất lâu dài cho ZO Math

Nên giữ một phong cách ổn định:

```text
nền tối hoặc nền sáng tối giản;
một màu nhấn chính;
công thức lớn;
ít hiệu ứng trang trí;
chuyển động chậm, rõ, có lí do;
giọng đọc là trung tâm;
phụ đề sạch và ít gây nhiễu.
```

Mỗi video nên được xem như một bài học nhỏ có mạch kể chuyện:

```text
câu hỏi mở đầu
→ tình huống hoặc vấn đề
→ ý tưởng toán học
→ minh họa bằng Manim
→ kết luận nhận thức
```

Với video đầu tiên, mục tiêu không phải làm thật hoành tráng. Mục tiêu là hoàn thành trọn vẹn một quy trình:

```text
kịch bản
→ voice-over
→ Manim
→ DaVinci Resolve
→ video final
```

Khi quy trình này chạy được, các video sau chỉ là mở rộng cùng một xưởng sản xuất.
