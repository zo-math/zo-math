# TRỜI SAO KIẾN TẠO HỌC THUẬT

## 1. Bản chất

**Trời sao kiến tạo học thuật** là phong cách hoạt ảnh của ZO Math.

Phong cách này xem màn hình như một không gian tư duy.
Trong không gian ấy, toán học không xuất hiện như một kết quả đã được bày sẵn.
Toán học xuất hiện dần dần, qua nhu cầu, qua quan hệ, qua biến đổi, qua cấu trúc.

Một đối tượng toán học không được đưa lên màn hình chỉ vì nó đẹp, quen, hay sẽ cần ở phần sau.
Nó xuất hiện khi tư duy đã cần đến nó.
Nó ở lại khi còn giữ vai trò trong cấu trúc.
Nó mờ đi hoặc biến mất khi vai trò ấy đã hoàn thành.

Tên gọi **Trời sao** không quy định một hình ảnh trang trí.
Nó chỉ một khí chất thị giác: nền sâu, không gian rộng, ít nhiễu, mỗi đối tượng hiện ra như một điểm chú ý có vị trí, có vai trò riêng, có quan hệ với những điểm khác.

Tên gọi **kiến tạo học thuật** xác định cách hình ảnh vận hành.
Không trình diễn.
Không minh họa hời hợt.
Không làm kỹ xảo để gây ấn tượng.
Hình ảnh dựng lại quá trình một ý niệm được hình thành.

Nguyên tắc nền:

**Cái gì chưa có lý do để xuất hiện thì chưa xuất hiện.**

## 2. Không gian thị giác

Không gian của phong cách này là một nền tối, tĩnh, sâu.

Nền tối không nhằm tạo cảm giác huyền bí.
Nền tối làm giảm nhiễu.
Nền tối để các đối tượng toán học hiện ra rõ hơn.
Nền tối làm cho mỗi đường, mỗi điểm, mỗi ký hiệu đều có trọng lượng.

Màn hình không phải bảng đen lớp học.
Không phải sân khấu trình diễn.
Không phải giao diện phần mềm.
Màn hình là một mặt phẳng suy nghĩ.

Trên mặt phẳng ấy, khoảng trống có vai trò.
Khoảng trống không phải phần chưa dùng đến.
Khoảng trống giúp người xem cảm được điều chưa xuất hiện, điều đang chờ được hình thành.

Bố cục vì vậy phải thoáng.
Ít đối tượng.
Ít chữ.
Ít chuyển động.
Không chen chúc.
Không lấp đầy màn hình chỉ vì còn chỗ trống.

## 3. Sự xuất hiện của đối tượng

Một đối tượng trong phong cách này không xuất hiện bằng sự áp đặt.
Nó xuất hiện như kết quả của một nhu cầu đã được chuẩn bị.

Ban đầu có thể chỉ là một dấu nhỏ.
Rồi dấu ấy được đặt vào vị trí.
Sau đó nó nhận quan hệ với đối tượng khác.
Từ quan hệ ấy, một cấu trúc lớn hơn bắt đầu hình thành.

Sự xuất hiện phải có thứ tự.

Cái nền xuất hiện trước cái phụ thuộc vào nền.
Cái riêng xuất hiện trước cái tổng quát.
Dấu hiệu xuất hiện trước tên gọi.
Quan hệ xuất hiện trước kết luận.
Cấu trúc xuất hiện trước công thức hóa.

Một hình ảnh hoàn chỉnh chỉ được phép xuất hiện khi những thành phần làm nên nó đã có lý do tồn tại.

## 4. Sự biến đổi

Chuyển động trong phong cách này không nhằm làm màn hình sinh động.
Chuyển động là cách làm lộ ra sự biến đổi của tư duy.

Một đối tượng có thể di chuyển khi vị trí của nó đang được hiểu lại.
Một đối tượng có thể đổi màu khi vai trò của nó thay đổi.
Một nhóm đối tượng có thể gom lại khi người xem cần thấy chúng như một toàn thể.
Một hình có thể tách ra khi người xem cần phân biệt các thành phần bên trong.

Mọi chuyển động phải đọc được bằng mắt.

Không chuyển động quá nhanh.
Không xoay lật không cần thiết.
Không nảy, rung, phóng đại kiểu biểu diễn.
Không dùng hiệu ứng chỉ để tạo cảm giác hấp dẫn.

Chuyển động tốt là chuyển động làm cho người xem hiểu thêm một quan hệ.

## 5. Màu sắc

Màu sắc trong phong cách này có chức năng ngữ nghĩa.

Màu không dùng để trang trí.
Màu không dùng để làm vui mắt.
Màu không gắn vĩnh viễn với một biến, một khái niệm hay một dạng toán cụ thể.
Màu chỉ nhận vai trò trong từng cấu trúc đang được dựng.

Hệ màu nền tảng:

```python
# Nền và thang hiện diện
COLOR_BACKGROUND = "#050507" # nền sâu toàn cảnh
COLOR_SURFACE = "#111114" # bề mặt hộp, thẻ, panel, vùng chứa nhẹ

# Nội dung
COLOR_PRIMARY = "#F5F5F5" # nội dung chính, công thức chính, đường chính
COLOR_SECONDARY = "#C8C8C8" # nội dung phụ nhưng còn rõ
COLOR_MUTED = "#9A9A9A" # ghi chú, nhãn phụ, thông tin lùi

# Đường dẫn và hình mờ
COLOR_GUIDE = "#5F5F5F" # đường dẫn, khung, trục phụ, lưới phụ
COLOR_FAINT = "#303030" # hình mờ, đối tượng nền, phần đã lùi

# Màu nhấn ZO Math: chỉ khi được chỉ định trực tiếp mới đem ra sử dụng, không được tự quyết định
COLOR_ZO_RED = "#ef5350"
COLOR_ZO_YELLOW = "#ffca28"
COLOR_ZO_TEAL = "#1de8b5"
```

Màu nhấn xuất hiện ít.
Mỗi lần xuất hiện phải có vai trò rõ.
Một màu nhấn có thể biểu thị một đối tượng, một trạng thái, một lựa chọn, một điểm cần chú ý, hoặc một quan hệ đang được phân biệt.

Trong cùng một cảnh, một màu chỉ nên giữ một nghĩa.
Nếu nghĩa thay đổi, sự thay đổi ấy phải được thể hiện bằng chuyển động hoặc chuyển cảnh rõ ràng.

## 6. Ánh sáng và độ nổi

Phong cách này không dùng ánh sáng như hiệu ứng sân khấu.
Ánh sáng được hiểu là mức độ hiện diện của một ý niệm.

Đối tượng chính sáng hơn.
Đối tượng phụ mờ hơn.
Đối tượng đã hoàn thành vai trò thì lùi xuống.
Đối tượng đang được xét thì tiến lên.

Độ mờ là một thao tác tư duy.
Làm mờ không có nghĩa là xóa bỏ.
Làm mờ có nghĩa là: đối tượng vẫn còn trong cấu trúc, nhưng không còn là điểm chú ý hiện tại.

Đường phụ, khung phụ, mốc phụ và lưới phụ phải đủ thấy nhưng không được tranh vai với nội dung chính.

## 7. Chữ trên màn hình

Phong cách **Trời sao kiến tạo học thuật** dùng một hệ cỡ chữ ít bậc.

Cỡ chữ không dùng để trang trí.
Cỡ chữ dùng để phân tầng sự chú ý.

Tất cả chữ văn bản trên màn hình được viết in hoa.
Sự nhấn mạnh hoặc làm nhẹ không dựa vào kiểu chữ phức tạp, mà dựa vào ba yếu tố:

```text
cỡ chữ
màu sắc
vị trí trong bố cục
```

Hệ cỡ chữ chuẩn:

```python
FONT_SIZE_DETAIL = 16
FONT_SIZE_LABEL = 18
FONT_SIZE_MAIN = 24
FONT_SIZE_TITLE = 32
FONT_SIZE_EMPHASIS = 48
FONT_SIZE_HERO = 72
```

Ý nghĩa của từng cỡ:

```text
DETAIL   = chi tiết nhỏ, mốc phụ, số nhỏ, thông tin nền
LABEL    = nhãn đối tượng, nhãn nhóm, nhãn trục, ghi chú ngắn
MAIN     = nội dung chính trên màn hình
TITLE    = tiêu đề cảnh, câu hỏi chính, mệnh đề dẫn
EMPHASIS = số lớn, từ khóa, kết luận tạm, điểm cần nhấn
HERO     = kết quả trung tâm, ký hiệu lớn, khoảnh khắc kết tinh
```

Không tạo thêm cỡ chữ mới nếu chưa thật sự cần.
Nếu cần ngoại lệ cục bộ, ưu tiên dùng phép nhân từ hệ chuẩn, chẳng hạn:

```python
FONT_SIZE_HERO * 0.75
FONT_SIZE_MAIN + 4
```

Nhưng ngoại lệ không được trở thành một cỡ chữ mới của phong cách.

Chữ trên màn hình phải ngắn.
Vì toàn bộ chữ được viết in hoa, mỗi dòng không nên quá dài.
Một dòng chữ càng dài thì càng nên dùng cỡ nhỏ hơn và màu nhẹ hơn.

Công thức toán học không bị ép vào hệ chữ văn bản.
Công thức dùng `MathTex` hoặc đối tượng toán học tương ứng.
Kích thước công thức vẫn nên quy chiếu về hệ cỡ chữ chuẩn để giữ nhịp thị giác thống nhất.

## 8. Công thức

Công thức không phải vật trang sức.

Một công thức xuất hiện khi người xem đã có nhu cầu nén một quan hệ vào ký hiệu.
Công thức không nên xuất hiện quá sớm.
Công thức không nên đứng một mình như kết luận từ trên rơi xuống.

Công thức có thể được dựng từng phần.
Một vế xuất hiện trước.
Một đại lượng được thay vào.
Một quan hệ được biến đổi.
Một kết quả được rút ra.

Khi công thức biến đổi, hình ảnh phải cho thấy điều gì được giữ lại và điều gì đang thay đổi.

Công thức lớn chỉ dành cho khoảnh khắc kết tinh.
Công thức nhỏ dùng cho nhãn, mốc, giá trị, hoặc quan hệ cục bộ.

## 9. Đường, điểm, khung và mũi tên

Đường là quan hệ.
Điểm là vị trí chú ý.
Khung là phạm vi xét.
Mũi tên là hướng phụ thuộc, hướng biến đổi, hoặc hướng đọc.

Không dùng đường chỉ để trang trí.
Không dùng khung chỉ để làm đẹp bố cục.
Không dùng mũi tên nếu quan hệ đã đủ rõ bằng vị trí.

Mũi tên phải ít.
Một mũi tên xuất hiện thì nó phải trả lời được câu hỏi: từ đâu sang đâu, theo nghĩa nào.

Khung không nên quá dày.
Khung không nên chiếm vai trò chính.
Khung chỉ giúp người xem biết: phần nào đang được xét như một đơn vị.

Điểm nhấn không nên kéo dài quá lâu.
Một đối tượng được nhấn, người xem nhận ra, rồi sự nhấn lùi xuống để cấu trúc tiếp tục vận động.

## 10. Nhịp

Nhịp của phong cách này chậm, nhưng không ì.

Chậm để người xem kịp thấy.
Chậm để một quan hệ có thời gian hình thành.
Chậm để khoảng trống có nghĩa.

Nhịp không đều một cách máy móc.
Đoạn phát hiện cần chậm hơn.
Đoạn chuyển nền cần gọn hơn.
Đoạn kết tinh cần giữ lại lâu hơn.
Đoạn phụ trợ cần nhẹ và ngắn.

Một cảnh tốt không chạy theo số lượng hiệu ứng.
Một cảnh tốt có một chuyển hóa chính.

## 11. Âm thanh

Âm thanh trong phong cách này là tín hiệu phụ.
Nó không dẫn dắt cảm xúc thay cho hình ảnh.
Nó không lấn lời đọc.
Nó không tạo cảm giác trò chơi.

Hệ âm thanh nền tảng:

```python
SFX = {
    "tick": "computer_mouse_click.wav",
    "hit": "menu_beep_accept_soft.wav",
    "whoosh": "simple_whoosh.wav",
    "typing": "keyboard_typing.wav",
}
```

Ý nghĩa thị giác của từng âm:

```text
tick   = chọn, đánh dấu, xác nhận nhỏ
hit    = nhấn, chốt, va vào một phát hiện
whoosh = chuyển trạng thái, đổi bố cục, dịch khung nhìn
typing = chữ đang được hình thành
```

Âm thanh phải nhỏ.
Âm thanh phải thưa.
Âm thanh phải có lý do.

Mức âm lượng gợi ý:

```python
SFX_GAIN = {
    "tick": -20,
    "hit": -16,
    "whoosh": -22,
    "typing": -12,
}
```

Có thể bổ sung một âm rất nhẹ cho khoảnh khắc kết tinh, nhưng âm ấy không được tạo cảm giác chiến thắng.
Nó chỉ đánh dấu việc một cấu trúc đã trở nên rõ.

## 12. Helper hình ảnh

Mã nguồn của phong cách này phải phản ánh cùng một tinh thần với hình ảnh: rõ, ít nhiễu, có phân vai.

Helper không chỉ là tiện ích kỹ thuật.
Helper là cách mã nguồn giữ lại ngữ pháp thị giác của phong cách.

Một helper tốt phải có ba đặc điểm:

```text
phổ quát
dễ đọc
không chứa nội dung riêng của một bài
```

Bộ helper nền tảng:

```python
clear_screen()
play_sfx()

make_text()
make_text_block()
make_math()
fit_to_width()

make_frame()
make_scan_band()

play_type_text()
play_scan_once()
play_focus()
play_dim()
```

Các helper này tạo thành lớp ngữ pháp chung.

`clear_screen()` làm sạch màn hình bằng một chuyển cảnh nhẹ, để cảnh mới bắt đầu từ một không gian rõ ràng.

`play_sfx()` phát âm thanh ngắn theo tên đã định nghĩa, giúp âm thanh được tách khỏi logic hình ảnh.

`make_text()` tạo một dòng chữ văn bản theo chuẩn chữ của phong cách: in hoa, rõ, tối giản, đúng màu và đúng cỡ.

`make_text_block()` tạo một khối chữ ngắn gồm nhiều dòng, dùng cho câu hỏi, mệnh đề, tiêu đề hoặc kết luận tạm.

`make_math()` tạo công thức toán học theo cùng hệ màu và hệ kích thước thị giác, nhưng vẫn giữ hình thức toán học riêng.

`fit_to_width()` giới hạn chiều rộng của một đối tượng để bảo vệ bố cục và tránh chữ hoặc công thức vượt khỏi vùng nhìn.

`make_frame()` tạo một khung thị giác để xác định phạm vi đang được xét. Khung không phải trang trí; khung cho biết phần nào đang tạm thời được xem như một đơn vị.

`make_scan_band()` tạo một vệt quét mờ dùng cho thao tác dò, kiểm tra, đọc lướt hoặc chuyển sự chú ý qua một vùng.

`play_type_text()` làm chữ xuất hiện theo nhịp gõ, dùng khi một câu hỏi, một mệnh đề hoặc một kết luận đang được hình thành.

`play_scan_once()` cho một vệt quét đi qua đối tượng đúng một lần, dùng để biểu thị thao tác kiểm tra hoặc quan sát có hướng.

`play_focus()` làm một đối tượng hoặc một nhóm đối tượng trở thành tâm điểm chú ý.

`play_dim()` làm một đối tượng hoặc một nhóm đối tượng lùi xuống thành bối cảnh mà không bị xóa khỏi cấu trúc.

Quy tắc đặt tên:

```text
make_  = tạo đối tượng hình ảnh và trả về mobject
play_  = phát một hoạt ảnh hoặc âm thanh
fit_   = điều chỉnh kích thước để bảo vệ bố cục
clear_ = dọn không gian hiển thị
```

Không đặt helper phổ quát theo nội dung riêng của một bài.

Không đặt tên helper theo cảm giác cá nhân.
Không đặt tên helper theo màu sắc nếu màu chỉ là biểu hiện của một vai trò.
Không đặt tên helper theo một cảnh cụ thể nếu helper có thể dùng lại.

Mã nguồn có ba lớp:

```text
lớp phong cách
lớp cấu trúc bài
lớp cảnh cụ thể
```

Lớp phong cách chứa màu, chữ, âm thanh, helper phổ quát.

Lớp cấu trúc bài chứa dữ liệu, đối tượng, hình tượng và tham số riêng của bài.

Lớp cảnh cụ thể chứa thứ tự xuất hiện, biến đổi và kết tinh.

Helper chung không chứa nội dung riêng của một bài.
Helper riêng của một bài không được lẫn vào lõi phong cách.
Helper riêng của một cảnh phải được đặt tên theo cảnh hoặc theo vai trò cục bộ của nó.

## 13. Đặt tên trong mã nguồn

Tên trong mã nguồn phải nói lên vai trò tư duy của đối tượng.

Tên tốt:

```python
main_question
source_group
target_structure
guide_line
focus_point
faint_context
current_relation
```

Tên chưa tốt:

```python
thing1
abc
text2
obj
temp
nice_box
cool_effect
```

Tên hàm nên bắt đầu bằng nhóm tiền tố có vai trò rõ:

```python
make_  = tạo đối tượng hình ảnh
build_ = dựng một cụm hình phức hợp
play_  = phát một hoạt ảnh hoặc âm thanh
fit_   = điều chỉnh kích thước
clear_ = dọn không gian hiển thị
```

Tên helper không nên mô tả hiệu ứng bề mặt nếu chức năng thật là tư duy.

Không đặt tên theo cảm giác cá nhân.
Không đặt tên theo vị trí tạm thời nếu đối tượng có vai trò khái niệm.
Không đặt tên theo màu nếu màu chỉ là biểu hiện của một vai trò.

## 14. Cấu trúc cảnh

Một cảnh là một đơn vị chuyển hóa.

Cảnh không chỉ là một đoạn thời gian.
Cảnh là nơi một điều gì đó trong tư duy thay đổi.

Mỗi cảnh có một chuyển hóa chính:

```text
từ rời rạc sang có trật tự
từ ví dụ sang cấu trúc
từ kết quả sang nguyên nhân
từ thao tác sang ý nghĩa
từ hình ảnh sang khái niệm
từ mơ hồ sang phân biệt
```

Các pha trong cảnh không phải các hiệu ứng nối nhau.
Chúng là các bước nhỏ của chuyển hóa ấy.

Một cảnh không nên có quá nhiều trung tâm chú ý.
Một cảnh không nên kết thúc bằng sự xuất hiện của một đối tượng chưa rõ vai trò.
Một cảnh kết thúc tốt khi người xem thấy được vì sao bước tiếp theo trở nên cần thiết.

Giữa hai cảnh cần có một khung hình định danh cảnh.

Sau khi một cảnh kết thúc, trước khi nội dung của cảnh tiếp theo bắt đầu, màn hình chuyển về một trạng thái sạch.
Trên nền ấy, tên cảnh tiếp theo xuất hiện ở giữa màn hình.
Phía trên tên cảnh là số thứ tự của cảnh, nhỏ hơn và nhạt hơn.
Số thứ tự nên viết bằng hai chữ số: 01, 02, 03...

```text
02
BIẾN ĐẦU VÀO X VÀ BIẾN PHỤ THUỘC Y
```

Không thêm chữ “cảnh” trước con số.

Tên cảnh lấy từ tên mục trong bài luận hoặc tên cảnh trong kịch bản lời dẫn.
Nhờ vậy, cấu trúc video, bài luận, kịch bản lời dẫn, kịch bản hoạt ảnh và mã Manim cùng quy chiếu về một hệ tên thống nhất.

Khung định danh cảnh có ba vai trò.

Thứ nhất, nó giúp người xem biết mình đang đi đến phần nào của mạch tư duy.

Thứ hai, nó tạo một khoảng nghỉ ngắn để cảnh trước khép lại và cảnh sau bắt đầu rõ ràng.

Thứ ba, nó giúp quá trình sản xuất dễ kiểm soát hơn: khi render, chỉnh sửa, đối chiếu âm thanh hoặc thay đổi hoạt ảnh, mỗi cảnh có một điểm mở đầu dễ nhận ra.

Khung định danh cảnh không phải là một hiệu ứng trang trí.
Nó là dấu ngắt cấu trúc.
Nó giúp video giữ nhịp tĩnh, rõ và có trật tự.

## 15. Render và bảo trì

Mã nguồn phải cho phép render từng cảnh độc lập.
Mỗi cảnh phải có thể kiểm tra riêng về bố cục, nhịp, chữ, màu, âm thanh và độ rõ.

Cấu trúc render phản ánh cấu trúc tư duy:

```python
def construct(self):
    self.scene_01()
    self.scene_02()
    self.scene_03()
```

Khi cần kiểm thử, có thể bật riêng từng cảnh mà không phá cấu trúc tổng thể.

Các hằng số nằm ở đầu tệp hoặc trong lớp cấu hình.
Dữ liệu riêng của bài nằm tách khỏi helper.
Không rải màu, cỡ chữ, đường dẫn âm thanh và tham số bố cục khắp nơi trong code.

Một thay đổi về phong cách phải sửa được ở một nơi.
Một thay đổi về nội dung chỉ ảnh hưởng đến cảnh hoặc bài liên quan.

## 16. Điều phong cách này tránh

Không hoạt náo.
Không giật mở.
Không nhồi chữ.
Không trình diễn kỹ xảo.
Không dùng màu tùy hứng.
Không để đối tượng xuất hiện trước lý do của nó.
Không biến màn hình thành slide bài giảng.
Không biến công thức thành vật trang trí.
Không dùng âm thanh như phần gây phấn khích.
Không để code trở thành chuỗi hiệu ứng khó bảo trì.

## 17. Tiêu chuẩn cuối cùng

Một hoạt ảnh theo phong cách **Trời sao kiến tạo học thuật** đạt chuẩn khi người xem có cảm giác:

```text
Mình không chỉ thấy một hình.
Mình thấy hình ấy được sinh ra.

Mình không chỉ thấy một công thức.
Mình thấy quan hệ khiến công thức ấy cần thiết.

Mình không chỉ thấy một kết quả.
Mình thấy con đường làm kết quả ấy trở nên tự nhiên.
```

Phong cách này không làm toán học dễ dãi hơn.
Nó làm toán học hiện ra rõ hơn.

Không thêm ồn ào vào tư duy.
Không che lấp sự khó bằng hiệu ứng.
Không làm thay phần suy nghĩ của người xem.

Nó tạo một không gian đủ tĩnh để ý niệm tự hiện ra.
