# ZO Math — Quy trình sản xuất video giới thiệu / video voice-over

**Phiên bản:** 1.0  
**Ngày kết tinh:** 2026-09-29  
**Nguồn kinh nghiệm:** quy trình thực tế đã dùng để sản xuất video giới thiệu **ZO Math — Ôn thi Toán Trung học Phổ thông 2027**.  
**Mục đích:** dùng lại cho các video giới thiệu, video voice-over, video học liệu và các video truyền thông có cấu trúc tương tự.

---

## 0. Tư tưởng điều hành

Quy trình này ưu tiên ba điều:

1. **Nội dung phải được khóa trước khi dựng.**
2. **Tài nguyên phải được tổ chức trước khi mở DaVinci.**
3. **Một việc chỉ làm một lần và phải tái sử dụng được cho các định dạng khác.**

Không nên vừa dựng vừa nghĩ nội dung, vừa tạo ảnh vừa sửa voice, hoặc vừa làm bản ngang vừa làm bản dọc. Cách đó làm timeline rối, khó kiểm soát và dễ sửa đi sửa lại.

Luồng chuẩn:

> **Kịch bản → Voice → Bản đồ cảnh → Tài nguyên → Dựng 16:9 → Subtitle → Sonic logo → Export master → Nhân timeline → Thay tài nguyên 9:16 → Export bản dọc**

---

# 1. Xác định loại video và đầu ra cần có

Trước khi bắt đầu, ghi rõ video này dùng để làm gì.

Ví dụ:

- Video giới thiệu chương trình.
- Video giải thích một ý toán học.
- Video voice-over từ podcast.
- Video ngắn cho Shorts / Reels / TikTok.
- Video ngang cho YouTube hoặc website.

Với một video có cả bản ngang và bản dọc, nên xác định ngay từ đầu:

- **Bản ngang:** 16:9, 1920 × 1080.
- **Bản dọc:** 9:16, 1080 × 1920.
- **Frame rate:** 30 fps.
- **Bản có phụ đề burn-in.**
- **Bản không phụ đề.**

Như vậy, một video có thể có bốn file master:

```text
..._16x9_sub_v01.mp4
..._16x9_no_sub_v01.mp4
..._9x16_sub_v01.mp4
..._9x16_no_sub_v01.mp4
```

---

# 2. Tạo cây thư mục trước khi làm nội dung

Không để file tải về nằm rải rác trong Downloads rồi dựng trực tiếp.

Ví dụ chuẩn đã dùng:

```text
E:\zo_media\
└── on_thi_toan_thpt_2027\
    └── 01_video_gioi_thieu_khoa_hoc\
        ├── 00_nguon\
        │   ├── kich_ban\
        │   └── voice\
        │
        ├── 01_tai_nguyen\
        │   ├── thuong_hieu\
        │   ├── hoc_lieu_that\
        │   ├── do_hoa\
        │   │   ├── canh_01\
        │   │   ├── canh_02\
        │   │   ├── canh_03\
        │   │   ├── ...
        │   │   └── canh_12\
        │   └── am_thanh\
        │
        ├── 02_davinci\
        │   └── xuat_project\
        │
        └── 03_thanh_pham\
            ├── master\
            └── youtube\
```

## 2.1. Ý nghĩa từng thư mục

### `00_nguon\kich_ban`

Lưu:

- kịch bản voice-over đã duyệt;
- bản sửa theo phiên bản;
- ghi chú nội dung gốc nếu cần.

Ví dụ:

```text
kich_ban_voice_v01.txt
kich_ban_voice_v02.txt
```

### `00_nguon\voice`

Lưu voice đã khóa.

Ví dụ:

```text
voice_gioi_thieu_2027_v01.mp3
```

Không để nguyên tên tải xuống rất dài của ElevenLabs.

### `01_tai_nguyen\thuong_hieu`

Lưu:

- logo;
- end card;
- dấu nhấn ZO;
- tài nguyên nhận diện dùng chung.

Ví dụ:

```text
logo_zo_math.png
end_card_16x9.png
end_card_9x16.png
```

### `01_tai_nguyen\hoc_lieu_that`

Lưu:

- ảnh trích từ D0;
- ảnh trích từ gói học liệu;
- bảng, đồ thị, bài tập thật;
- screenshot học liệu ZO Math cần dùng trong video.

### `01_tai_nguyen\do_hoa\canh_xx`

Mỗi cảnh có thư mục riêng.

Ví dụ:

```text
canh_01_16x9.png
canh_01_9x16.png
```

Không dùng tên chung chung như:

```text
imagegen.png
final.png
new.png
```

### `01_tai_nguyen\am_thanh`

Lưu:

- sonic logo;
- nhạc nền nếu có;
- sound effect nếu có;
- file subtitle nếu muốn để cùng phần audio/video hỗ trợ.

Ví dụ:

```text
zo_math_sonic_logo_v01.mp3
phu_de_gioi_thieu_2027_v01.srt
```

### `02_davinci\xuat_project`

Dùng để xuất:

- project backup;
- project archive;
- file `.drp` khi cần.

Không phải nơi DaVinci lưu project mặc định.

### `03_thanh_pham\master`

Lưu các file xuất cuối cùng chất lượng đầy đủ.

### `03_thanh_pham\youtube`

Chỉ dùng khi cần một bản riêng phục vụ upload hoặc một preset khác master.

---

# 3. Lệnh PowerShell tạo cây thư mục

Có thể dùng mẫu sau:

```powershell
$base = "E:\zo_media\on_thi_toan_thpt_2027\01_video_gioi_thieu_khoa_hoc"

$folders = @(
    "$base\00_nguon\kich_ban",
    "$base\00_nguon\voice",
    "$base\01_tai_nguyen\thuong_hieu",
    "$base\01_tai_nguyen\hoc_lieu_that",
    "$base\01_tai_nguyen\am_thanh",
    "$base\02_davinci\xuat_project",
    "$base\03_thanh_pham\master",
    "$base\03_thanh_pham\youtube"
)

1..12 | ForEach-Object {
    $folders += "$base\01_tai_nguyen\do_hoa\canh_{0:D2}" -f $_
}

$folders | ForEach-Object {
    New-Item -ItemType Directory -Path $_ -Force | Out-Null
}

tree $base /F
```

Nếu số cảnh khác 12, thay `1..12`.

---

# 4. Khóa kịch bản trước khi tạo voice

Không đưa một bản nháp chưa duyệt vào ElevenLabs.

Quy trình:

1. Viết kịch bản.
2. Đọc lại bằng mắt.
3. Rút gọn các câu khó đọc thành tiếng.
4. Không dùng mã quản lí nội bộ trong lời nói.
5. Viết tên gọi theo cách người nghe hiểu được.
6. Khóa bản voice-over.

Ví dụ:

Không đọc:

```text
R1-G01
D0
R1–R8
B16–B18
```

nếu đây chỉ là mã quản lí nội bộ.

Nên nói:

```text
bài khảo sát đầu vào
gói học liệu
các mạch ôn
kiến thức lớp 10, 11 và 12
```

---

# 5. Chuẩn hóa văn bản cho Text-to-Speech

Text-to-Speech không phải lúc nào cũng đọc đúng chữ viết tắt.

Ví dụ:

Không nên đưa:

```text
THPT
```

nếu engine đọc thành từng chữ cái.

Nên đưa:

```text
Trung học Phổ thông
```

Tương tự:

- tránh chữ viết tắt không cần thiết;
- tránh ký hiệu khó đọc;
- tránh dấu câu quá dày;
- ưu tiên câu nói tự nhiên.

---

# 6. Tạo voice trong ElevenLabs

## 6.1. Chọn model

Không mặc định model nhanh nhất là tốt nhất.

Trong quá trình thực tế:

- Flash v2.5 có thể nhanh nhưng một số từ tiếng Việt phát âm chưa tốt.
- v3 cho kết quả tiếng Việt chính xác hơn trong trường hợp đã thử.

Do đó:

> **Ưu tiên model phát âm đúng và tự nhiên hơn tốc độ sinh.**

## 6.2. Chọn voice

Tiêu chí cho ZO Math:

- rõ chữ;
- điềm tĩnh;
- không mang giọng quảng cáo;
- không lên giọng quá cao;
- không quá kịch;
- nghe được lâu mà không mệt.

## 6.3. Cách thử

Không generate toàn bộ kịch bản ngay.

Lấy một đoạn 2–3 câu có:

- tên thương hiệu;
- cụm “Trung học Phổ thông”;
- vài từ dễ sai;
- câu hỏi có nhịp.

Nếu đoạn thử tốt mới generate toàn bộ.

## 6.4. Chốt voice

Sau khi chọn bản tốt:

1. tải MP3;
2. đổi tên;
3. đưa vào `00_nguon\voice`;
4. không sửa voice tiếp nếu không có lỗi cụ thể.

Nguyên tắc:

> **Voice đã nghe tốt thì không tiếp tục EQ/compress chỉ vì “có thể chỉnh”.**

---

# 7. Phân tích voice trước khi tạo hình

Sau khi voice được khóa, mới chia video thành cảnh.

Không chia cảnh bằng ước lượng cảm tính.

Mỗi cảnh phải tương ứng với:

- một ý;
- một đoạn lời nói;
- một hình ảnh chính.

Ví dụ:

```text
Cảnh 1 — Câu hỏi mở đầu
Cảnh 2 — Xác định đang vững / đang hổng / học tiếp gì
Cảnh 3 — Giới thiệu ZO Math
Cảnh 4 — Kết nối kiến thức lớp 10–11–12
Cảnh 5 — Khảo sát đầu vào
Cảnh 6 — Học → Luyện tập → Kiểm tra → Sửa lỗi → Ôn lại
...
```

Không tạo hình trước rồi cố ép kịch bản vào hình.

---

# 8. Ba cơ sở bắt buộc khi tạo hình ZO Math

Mỗi ảnh phải dựa đồng thời trên ba cơ sở:

## 8.1. Nội dung cảnh

Ảnh phải phản ánh đúng đoạn voice.

Không tạo một poster đẹp nhưng nội dung không đúng đoạn lời đọc.

## 8.2. Nguồn nội dung thật của dự án

Khi cảnh nói về:

- khảo sát đầu vào;
- sửa lỗi;
- chu trình học;
- bảng biến thiên;
- đồ thị;
- học liệu;

thì hình nên bám vào các học liệu thật đang có.

Không tự thêm nội dung toán đã lỗi thời.

Ví dụ đã phát hiện:

> **Không còn dùng Số phức trong phạm vi hiện tại.**

Nếu hình AI tự sinh sách “Số phức”, phải thay bằng nội dung phù hợp như **Xác suất**.

## 8.3. Phong cách ZO Math

Nguồn phong cách đã dùng:

- `Phong_cach_ZO_Math.md`
- `Dau_nhan_ZO_Quy_cach.md`
- màu và đồ thị từ hệ ZO Math hiện có.

Các điểm cốt lõi:

- nền trắng ấm `#FBFAF8`;
- đỏ chính `#EF5350`;
- vàng đồng hành;
- chữ xám đậm;
- bố cục thoáng;
- mỗi cảnh một trọng tâm;
- không nhấn cùng một đối tượng bằng quá nhiều cách;
- ưu tiên hình, sơ đồ, đồ thị có ý nghĩa;
- không nhồi chữ;
- không dùng màu neon;
- không biến video thành quảng cáo rực rỡ.

---

# 9. Dấu nhấn ZO

Dấu nhấn phụ trợ:

- một vạch đỏ dài;
- một vạch vàng ngắn;
- hai vạch bo tròn;
- không phải logo.

Dùng:

- chân khung;
- điểm phân tách;
- phần kết;
- vị trí nhận diện phụ.

Không dùng:

- làm dấu bằng;
- làm dấu trừ;
- làm đường dữ liệu;
- làm gạch chân cho chữ đã được tô màu.

---

# 10. Tạo hai phiên bản hình ngay từ khâu tài nguyên

Mỗi cảnh nên có:

```text
canh_01_16x9.png
canh_01_9x16.png
```

Không nên dựng xong bản ngang rồi crop ảnh ngang thành dọc.

Hai phiên bản phải được **bố trí lại**, không kéo giãn.

## 10.1. 16:9

Dùng cho:

- YouTube video;
- website;
- trình chiếu;
- màn hình desktop.

## 10.2. 9:16

Dùng cho:

- YouTube Shorts;
- TikTok;
- Instagram Reels;
- xem trên điện thoại.

---

# 11. Kiểm ảnh trước khi đưa vào DaVinci

Mỗi ảnh cần kiểm:

1. Đúng nội dung cảnh chưa?
2. Có chữ sai không?
3. Có kiến thức lỗi thời không?
4. Có logo giả hoặc logo AI tự chế không?
5. Có đúng màu ZO Math không?
6. Có quá nhiều chữ không?
7. Có phù hợp 16:9 / 9:16 không?
8. Có vật thể thừa làm phân tán chú ý không?
9. Có lỗi toán học không?

Nếu sai, sửa ảnh ngay trước khi dựng.

Không chờ đến DaVinci mới sửa lỗi hình.

---

# 12. Tạo project DaVinci Resolve

Trong Project Manager:

```text
ZO_Math_Gioi_thieu_2027
```

Project được lưu trong Project Library của DaVinci.

Không cần tự đặt file project vào thư mục media.

---

# 13. Thiết lập project

Vào:

```text
File → Project Settings → Master Settings
```

Bản ngang:

```text
Timeline resolution: 1920 × 1080
Timeline frame rate: 30 fps
Playback frame rate: 30 fps
```

---

# 14. Import tài nguyên

Ban đầu chỉ import:

- voice;
- bộ ảnh 16:9.

Không import tất cả mọi thứ nếu chưa cần.

Sau này mới thêm:

- sonic logo;
- subtitle;
- ảnh 9:16;
- end card.

---

# 15. Tạo timeline 16:9

Đặt tên:

```text
ZO_Math_Gioi_thieu_2027_16x9
```

Track gợi ý:

```text
V1 — ảnh / video chính
A1 — voice
A2 — sonic logo / sound effect
Subtitle Track — phụ đề
```

---

# 16. Dàn ảnh theo voice

Đặt voice vào A1 trước.

Sau đó:

1. kéo Cảnh 1 vào V1;
2. đặt đúng thời lượng;
3. nối Cảnh 2;
4. tiếp tục đến hết.

Nguyên tắc:

> **Lời đọc quyết định thời lượng ảnh, không phải ngược lại.**

Nếu voice có nhịp dừng tự nhiên, nên để ảnh giữ thêm một chút thay vì đổi quá gấp.

---

# 17. Chuyển động ảnh tĩnh

Với ảnh poster / infographic, có thể dùng zoom rất nhẹ.

Ví dụ:

```text
Đầu clip: Zoom X = 1.000
Cuối clip: Zoom X = 1.040 hoặc 1.050
```

Nếu X và Y đang khóa bằng biểu tượng mắt xích:

- chỉ chỉnh Zoom X;
- Zoom Y tự đổi theo.

Không nên zoom mạnh.

## 17.1. Copy chuyển động hàng loạt

Sau khi chỉnh Cảnh 1:

1. `Ctrl + C`;
2. chọn các clip còn lại;
3. `Alt + V`;
4. chọn Transform / Zoom;
5. chọn **Stretch to Fit**;
6. Apply.

`Stretch to Fit` giúp keyframe đầu–cuối co giãn theo đúng thời lượng từng clip.

---

# 18. Chuyển cảnh

Dùng nhẹ.

Phương án đã dùng:

```text
Cross Dissolve
Duration: khoảng 8 frame
```

Với timeline 30 fps:

```text
00:00:00:08
```

Có thể:

1. Set Cross Dissolve làm Standard Transition;
2. chọn các clip;
3. `Ctrl + T`.

Không nên dùng transition phức tạp cho video ZO Math nếu không có mục đích rõ.

---

# 19. Nhạc nền

Không bắt buộc.

Trong video đã thử:

- nhiều nhạc nền làm video ồn;
- voice và hình đã đủ đẹp;
- bỏ nhạc nền cho kết quả sạch hơn.

Nguyên tắc:

> **Không thêm nhạc chỉ vì video “thường phải có nhạc”.**

Nếu voice đã đủ nhịp và hình đủ đẹp, có thể dùng:

> **voice + hình + sonic logo**

---

# 20. Sonic logo ZO Math

Có thể tạo một âm thanh nhận diện rất ngắn.

Bản đã thử:

- khoảng 1 giây;
- ba nốt đi lên;
- mềm;
- sáng;
- không giống thông báo điện thoại;
- không hoành tráng.

Lưu:

```text
01_tai_nguyen\am_thanh\
zo_math_sonic_logo_v01.mp3
```

Đặt:

- một bản ở đầu video;
- một bản ở đầu end card.

Nếu quá to:

- chọn riêng clip sonic logo;
- Inspector → Audio → Volume;
- giảm riêng clip.

Không giảm track hoặc Bus nếu không muốn ảnh hưởng voice.

---

# 21. End card

Bản ngang và bản dọc phải có end card riêng:

```text
end_card_16x9.png
end_card_9x16.png
```

Lưu:

```text
01_tai_nguyen\thuong_hieu\
```

Thời lượng gợi ý:

```text
3 giây
```

Có thể:

- sonic logo chạy ở giây đầu;
- 2 giây còn lại giữ sạch.

Không cần zoom end card.

---

# 22. Subtitle trong DaVinci Resolve Free

Nếu không có AI Tools / Create Subtitles from Audio, không phải lỗi.

DaVinci Resolve Free có thể không có tính năng AI transcription tương ứng.

Cách thay thế:

1. tạo file `.srt`;
2. import vào DaVinci;
3. kéo vào timeline;
4. DaVinci tạo Subtitle Track.

Tên:

```text
phu_de_gioi_thieu_2027_v01.srt
```

---

# 23. Quy chuẩn subtitle ZO Math

Theo phong cách đã dùng:

- chữ vàng ZO;
- nền xám ấm đậm;
- font Be Vietnam Pro SemiBold nếu có;
- nằm phía dưới;
- tối đa hai dòng;
- không chạm mép;
- không che công thức hoặc hình quan trọng.

Màu đã dùng:

```text
Text: #FFCF3D
Background: #25221F
```

Quan trọng:

> **Không giảm chữ quá nhỏ chỉ để nhét một câu dài vào một dòng.**

Tốt hơn:

- chia thành hai dòng;
- giữ cỡ chữ đọc được trên điện thoại.

---

# 24. Burn subtitle

Đây là bước rất dễ quên.

Khi xuất bản có sub:

```text
Subtitle Settings
→ Export Subtitle
→ Burn into video
```

Phải kiểm tra riêng trước khi render.

Có thể xem đây là một mục bắt buộc trong checklist xuất video.

---

# 25. Export bản 16:9

Trang Deliver:

```text
Format: MP4
Codec: H.264
Resolution: 1920 × 1080
Frame rate: 30 fps
Network Optimization: Off
Subtitle: Burn into video
```

Tên:

```text
ZO_Math_Gioi_thieu_On_thi_2027_16x9_sub_v01.mp4
```

Bản không sub:

- giữ nguyên các thông số;
- tắt Export Subtitle / Burn into video.

Tên:

```text
ZO_Math_Gioi_thieu_On_thi_2027_16x9_no_sub_v01.mp4
```

---

# 26. Tạo bản 9:16 nhanh nhất

Không dựng lại từ đầu.

## 26.1. Duplicate timeline

Từ timeline ngang:

```text
ZO_Math_Gioi_thieu_2027_16x9
```

duplicate thành:

```text
ZO_Math_Gioi_thieu_2027_9x16
```

## 26.2. Timeline Settings

Nhấp phải timeline 9:16 trong Media Pool:

```text
Timeline Settings
```

Bỏ:

```text
Use Project Settings
```

Đặt:

```text
1080 × 1920
30 fps
```

---

# 27. Không nên dùng F11 Replace Edit cho trường hợp này

Trong quá trình thử:

- playhead nằm giữa clip;
- F11 làm clip cũ bị chia;
- ảnh mới chỉ thay một phần.

Do đó với bộ ảnh tĩnh này:

> **Không dùng F11 Replace Edit.**

---

# 28. Cách an toàn để dựng bản dọc

Có thể dùng một track video mới:

```text
V1 — giữ bản 16:9 làm dự phòng
V2 — đặt ảnh 9:16
```

Sau đó:

1. đặt các ảnh 9:16 lên V2;
2. khớp đúng timing với V1;
3. copy Transform từ V1 sang V2 bằng Paste Attributes;
4. thêm transition;
5. disable V1 khi xem bản dọc.

Cách này tránh phá timeline ngang.

---

# 29. Subtitle trên 9:16

Subtitle bản ngang thường quá rộng khi chuyển sang dọc.

Không giảm font theo “%” mơ hồ.

Trong DaVinci:

- Font Size là số cụ thể;
- giảm từng ít;
- xem trực tiếp trên khung 9:16.

Nếu câu dài:

> **ưu tiên xuống 2 dòng trước khi giảm chữ quá nhỏ.**

Kiểm tra trên màn hình điện thoại nếu có thể.

---

# 30. Export bản 9:16

Trước khi render phải nhìn đúng timeline.

Đây là lỗi đã xảy ra trong thực tế:

- đang chỉnh timeline dọc;
- nhưng Deliver lại dùng timeline ngang;
- Resolution hiện `1920 × 1080`.

Do đó checklist bắt buộc:

```text
1. Mở đúng timeline ZO_Math_Gioi_thieu_2027_9x16.
2. Viewer phải dọc.
3. Vào Deliver.
4. Resolution phải hiện 1080 × 1920.
```

Không render nếu Deliver vẫn là:

```text
1920 × 1080
```

Thiết lập:

```text
MP4
H.264
1080 × 1920
30 fps
Network Optimization: Off
Subtitle: Burn into video
```

Tên:

```text
ZO_Math_Gioi_thieu_On_thi_2027_9x16_sub_v01.mp4
```

Bản không sub:

```text
ZO_Math_Gioi_thieu_On_thi_2027_9x16_no_sub_v01.mp4
```

---

# 31. Kiểm tra file render thật

Không chỉ xem trong DaVinci.

Sau khi render:

## Bản ngang

Xem trên:

- desktop;
- trình duyệt;
- màn hình thường.

## Bản dọc

Xem trên:

- điện thoại;
- toàn màn hình;
- thử trong điều kiện giống Shorts / Reels.

Kiểm:

- subtitle có tràn không;
- hình có crop sai không;
- end card đủ lâu không;
- sonic logo có to quá không;
- âm thanh có bị nhỏ hoặc vỡ không;
- transition có gây giật không;
- có frame đen không.

---

# 32. Chốt phiên bản

Nếu video đã:

- đúng nội dung;
- voice tốt;
- hình khớp lời;
- subtitle dễ đọc;
- không lỗi kỹ thuật;

thì **chốt phiên bản**.

Không tiếp tục chỉnh vô hạn các chi tiết rất nhỏ.

Ví dụ:

```text
v01
```

Nếu sau này sửa nội dung hoặc hình đáng kể:

```text
v02
```

---

# 33. Bốn master nên giữ

Cuối quy trình, nên giữ:

```text
ZO_Math_Gioi_thieu_On_thi_2027_16x9_sub_v01.mp4
ZO_Math_Gioi_thieu_On_thi_2027_16x9_no_sub_v01.mp4
ZO_Math_Gioi_thieu_On_thi_2027_9x16_sub_v01.mp4
ZO_Math_Gioi_thieu_On_thi_2027_9x16_no_sub_v01.mp4
```

Bản `no_sub` đặc biệt quan trọng để:

- tái sử dụng;
- thay subtitle;
- làm ngôn ngữ khác;
- dùng trên nền tảng tự tạo caption;
- chỉnh sửa về sau.

---

# 34. Những lỗi đã gặp và bài học

## 34.1. Tạo tài nguyên quá sớm

Sai:

> vào DaVinci khi chưa có đủ ảnh.

Đúng:

> tạo đủ bộ tài nguyên trước, rồi mới dựng.

---

## 34.2. Không dựa sát nội dung cảnh

Sai:

> ảnh đẹp nhưng nói chung chung về “học hiệu quả”.

Đúng:

> cảnh nói “khảo sát đầu vào” thì ảnh phải thể hiện khảo sát đầu vào.

---

## 34.3. Dùng nội dung toán lỗi thời

Sai:

> AI tự đưa “Số phức” vào tài nguyên.

Đúng:

> đối chiếu phạm vi dự án hiện tại; thay bằng nội dung phù hợp như Xác suất.

---

## 34.4. Tính timing bằng ước lượng

Sai:

> chia cảnh bằng thời gian đoán.

Đúng:

> voice thật là chuẩn; cảnh theo đoạn nghĩa và khoảng nghỉ thật.

---

## 34.5. Chỉnh fade không cần thiết

Sai:

> kéo tay cầm fade làm clip khó kiểm soát.

Đúng:

> với phong cách này, Cross Dissolve nhẹ giữa cảnh đã đủ.

---

## 34.6. Dùng Replace Edit không đúng ngữ cảnh

Sai:

> F11 khi playhead ở giữa clip làm clip bị chia.

Đúng:

> không dùng F11 cho quy trình thay hàng loạt ảnh tĩnh này.

---

## 34.7. Làm bản dọc bằng cách phá bản ngang

Sai:

> sửa trực tiếp V1 bản 16:9.

Đúng:

> duplicate timeline; hoặc giữ V1 và dựng ảnh dọc trên V2.

---

## 34.8. Quên Burn Subtitle

Sai:

> render xong mới phát hiện video không có sub.

Đúng:

> xem `Subtitle → Burn into video` là một mục bắt buộc trước render.

---

## 34.9. Tin rằng Deliver đang dùng đúng timeline

Sai:

> timeline dọc đã có nhưng Deliver vẫn xuất 1920 × 1080.

Đúng:

> trước render luôn kiểm tra:
>
> - tên timeline;
> - hình dạng Viewer;
> - Resolution trong Deliver.

---

# 35. Checklist sản xuất rút gọn

## Trước DaVinci

- [ ] Kịch bản đã duyệt.
- [ ] Voice đã chốt.
- [ ] Voice đã đổi tên và lưu đúng thư mục.
- [ ] Đã chia cảnh theo voice.
- [ ] Mỗi cảnh có nội dung rõ.
- [ ] Ảnh 16:9 đã đủ.
- [ ] Ảnh 9:16 đã đủ.
- [ ] Ảnh đúng phong cách ZO Math.
- [ ] Ảnh không có kiến thức lỗi thời.
- [ ] End card 16:9 và 9:16 đã có.
- [ ] Sonic logo đã có nếu sử dụng.

## Dựng 16:9

- [ ] Timeline 1920 × 1080, 30 fps.
- [ ] Voice ở A1.
- [ ] Ảnh đúng timing trên V1.
- [ ] Zoom nhẹ.
- [ ] Cross Dissolve nhẹ.
- [ ] Sonic logo đầu / cuối.
- [ ] End card.
- [ ] Subtitle.
- [ ] Subtitle dễ đọc.
- [ ] Burn subtitle khi xuất bản có sub.

## Dựng 9:16

- [ ] Duplicate timeline.
- [ ] Timeline 1080 × 1920.
- [ ] Ảnh 9:16 thay đúng cảnh.
- [ ] Không phá bản 16:9.
- [ ] Subtitle không tràn.
- [ ] Viewer dọc.
- [ ] Deliver = 1080 × 1920.
- [ ] Burn subtitle nếu xuất bản có sub.

## Sau render

- [ ] Xem lại bản ngang.
- [ ] Xem lại bản dọc trên điện thoại.
- [ ] Không frame đen.
- [ ] Không sub bị cắt.
- [ ] Âm lượng voice ổn.
- [ ] Sonic logo vừa phải.
- [ ] End card đủ thời gian.
- [ ] Lưu đủ master sub / no-sub.

---

# 36. Quy trình đề xuất cho những video sau

Để nhanh hơn lần đầu, với video tương tự chỉ cần:

```text
1. Tạo thư mục dự án.
2. Viết và khóa kịch bản.
3. Tạo voice.
4. Chia cảnh theo voice.
5. Tạo đủ ảnh 16:9 và 9:16 theo đúng phong cách.
6. Tạo end card.
7. Chuẩn bị sonic logo.
8. Dựng bản 16:9.
9. Import SRT và chỉnh subtitle.
10. Render 16:9 sub + no-sub.
11. Duplicate timeline.
12. Chuyển sang 1080 × 1920.
13. Thay bộ ảnh dọc.
14. Chỉnh subtitle bản dọc.
15. Render 9:16 sub + no-sub.
16. Kiểm tra file thật.
17. Chốt phiên bản.
```

Đây là chuỗi nên dùng làm mặc định cho các video ZO Math tương tự.

---

# 37. Nguyên tắc cuối cùng

Một video ZO Math hoàn chỉnh không cần có thật nhiều hiệu ứng.

Ưu tiên:

> **Nội dung đúng → Voice rõ → Hình đúng ý → Nhịp dựng sạch → Phụ đề dễ đọc → Nhận diện nhất quán.**

Hiệu ứng chỉ được thêm nếu giúp người xem hiểu tốt hơn hoặc giúp chuyển cảnh tự nhiên hơn.

**Đơn giản mà sâu sắc** không chỉ là phong cách hình ảnh; nó cũng nên là nguyên tắc tổ chức toàn bộ quy trình sản xuất.
