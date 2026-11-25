# Hướng dẫn biên tập học liệu Ôn thi Toán THPT 2027

Dùng bản HTML đã biên tập của R1-G01 làm mẫu đối chiếu. Áp dụng bảng kiểm chung và hướng dẫn theo từng thẻ cho R1-G02 và các chuyên đề tiếp theo. Các số liệu và ví dụ ở mục 4 chỉ thuộc R1-G01.

Đối chiếu với [Quy trình và nghiệm thu](02_quy_trinh_va_nghiem_thu.md), [Quy chuẩn trang người học](07_quy_chuan_cau_truc_trang_nguoi_hoc.md) và [QMD hiện hành của R1-G01](../../../hoc_lieu/r1_g01/index.qmd).

## 1. Trình tự mỗi lượt

1. **Lượt đầu — rà các điểm đã chốt.** Đọc QMD và HTML hiện hành, xác định phần đang biên tập phục vụ việc học gì, rồi đi qua bảng kiểm chung và hướng dẫn riêng của phần đó. Giữ nhịp học của từng phần, chẳng hạn tự làm rồi đối chiếu ở Luyện tập và tự lực ở Kiểm tra.
2. **Lượt góp ý — xử lý các điểm riêng.** Sau khi chủ trì đọc, đối chiếu từng góp ý với đoạn liền trước, đoạn liền sau và phần học liên quan. Với thay đổi về nội dung toán hoặc cách tổ chức việc học chưa được chốt, trình phương án để chủ trì quyết định.
3. **Cập nhật và kiểm lại.** Sửa câu chữ ở QMD và giao diện ở nguồn của thành phần tương ứng. Khi được giao cập nhật HTML, dựng đúng vùng bị ảnh hưởng bằng [bộ dựng hiện hành](../../../../../../scripts/zo_course_site_sources/README.md). Giữ điều kiện toán, số nhiệm vụ, điểm neo, đích đề–lời giải và nội dung ngoài phạm vi. Báo ngắn phần đã sửa, phần đã xem trực tiếp và phần còn chưa kiểm.

## 2. Bảng kiểm dùng chung

Dùng ngay ở lượt đầu. Đối chiếu với phần đã chốt có thành phần cùng vai trò. Sau khi sửa, làm lại các phép kiểm liên quan ở vùng bị ảnh hưởng.

### Câu chữ, dữ kiện và nhiệm vụ

- [ ] **Rõ nghĩa, có ngữ cảnh.** Câu hỏi và lời dẫn gọi rõ đối tượng toán, việc cần làm và điều kiện áp dụng. Đọc trong cả đoạn, rồi đọc riêng tiêu đề hoặc câu hỏi xem người học có hiểu mà không cần đoán ngữ cảnh. Bài thuần toán có thể mở bằng một câu hỏi toán cụ thể. [Quy chuẩn giọng văn](07_quy_chuan_cau_truc_trang_nguoi_hoc.md#giong-van-ro-nghia-co-ngu-canh)
- [ ] **Chỉ dẫn đặt đúng chỗ.** Nêu cách làm việc chung một lần ở đầu nhóm. Đặt quy ước dữ kiện và yêu cầu riêng ngay ở nhiệm vụ cần dùng. Đặt hướng dẫn sửa lỗi ở Điểm dừng hoặc phần hỗ trợ, nơi học sinh cần quyết định bước tiếp theo.
- [ ] **Đề, hình, tiêu chí và lời giải khớp nhau.** Đọc cả đề lẫn lời giải khi sửa một nhiệm vụ. Khi thay hình, đối chiếu lại dữ kiện, văn bản thay thế, đáp số và lập luận. Tiêu chí tự kiểm, nếu phần học có dùng, nêu việc học sinh cần giải thích mà chưa tiết lộ kết quả.
- [ ] **Mỗi nhãn đường nằm gần đường mà nó gọi tên.** Ưu tiên đặt nhãn gần một đầu nhìn thấy của đường tương ứng, ở phía đủ thoáng và cách mép hình. Với nhiều đường hoặc nhiều hình ghép, kiểm từng nhãn để tránh nhầm sang đường bên cạnh. Dùng $x$, $y$ cho các trục tọa độ thông thường. Với bài đọc đồ thị, ghi tên như $y=f(x)$ hoặc $y=f'(x)$ và chỉ cho công thức cụ thể khi đó là dữ kiện của đề. [Quy chuẩn sản xuất đồ thị](../../../../../../quy_trinh_xay_dung/quy_chuan_san_xuat_do_thi_ham_so_zo_math_v0.2.md)
- [ ] **Đường phụ đúng vai trò và dễ nhận ra.** Dùng màu và kiểu nét theo quy chuẩn đồ thị. Khi đường tiếp tuyến kéo ngang để học sinh đối chiếu với đường cong như ở hình $y=2$ của R1-G01, vẽ nét dài ít nhất bằng bề ngang phần đường cong đang hiển thị. Đặt nhãn phương trình gần đầu mút thoáng, ưu tiên đầu phải nếu đủ chỗ. Bỏ chữ “Tiếp tuyến” nếu lời dẫn và nhãn phương trình đã đủ để nhận biết.
- [ ] **Nhãn điểm, nhãn trục và số trên trục đủ thoáng.** Đặt nhãn điểm sát điểm tương ứng, chừa khoảng hở với dấu điểm, trục và nét cong. Kiểm cả hộp chữ của từng nhãn, kể cả dấu âm, dấu ngoặc và dấu phẩy. Nếu số trên trục quá sát nét, dịch phần chữ và giữ vạch chia đúng tọa độ.
- [ ] **Kiểm từng hình sau khi dựng.** Mở từng ảnh đã sửa ở kích thước sử dụng thực tế, kể cả từng ô của hình ghép. So vị trí nhãn, độ rõ của các nét và dữ kiện trước–sau. Sửa vị trí tại nguồn dựng hình, giữ nguyên đường cong, tọa độ và dữ kiện khi chỉ chỉnh trình bày. Đối chiếu hình được dùng trong mỗi đầu ra thuộc phạm vi cập nhật với hình vừa dựng.
- [ ] **Mô tả kí hiệu đồ thị chính xác.** Khi thay hình bằng lời, gọi rõ đồ thị của hàm số hay của đạo hàm. Phân biệt điểm thuộc đồ thị, được đánh dấu bằng chấm kín, với vị trí đánh dấu bằng vòng tròn rỗng. Khi đọc dấu, viết rõ đường biểu diễn nằm phía trên, phía dưới hay trên trục hoành.
- [ ] **Kiểm giả thiết và phạm vi kết luận.** Xác định đủ giả thiết trước khi dùng định lí. Khi xét dấu, kiểm cả hai khoảng ngoài cùng do các mốc chia ra. Khi dùng dấu đạo hàm để kết luận đồng biến qua một mốc đạo hàm bằng $0$, nêu rõ điều kiện cho phép áp dụng trong tình huống đó. Khi dữ kiện chưa đủ, chỉ ra cụ thể điều gì còn thiếu. Chẳng hạn, tính đồng biến trên một khoảng chỉ cho phép so sánh các giá trị tại những hoành độ thuộc khoảng ấy.
- [ ] **Số lượng và thứ tự khớp bản hiện hành.** Đếm từ các nhiệm vụ thực tế, kể cả bài xác nhận sau sửa nếu bài ấy nằm trong chặng. So số bài, số chặng và số lượt ôn được nhắc ở đầu trang với nội dung bên dưới.

### Bố cục và điều hướng

- [ ] **Nhãn và cấp đề mục có vai trò rõ.** Giữ nhãn giúp định vị khi cuộn. Bỏ nhãn lặp tên khu vực trên từng nhiệm vụ hay ví dụ. Giữ tên và số hoạt động dùng để tra cứu. Chỉ đánh số cấp con khi mục cha có từ hai phần kiến thức riêng đáng tra cứu. Với một đề mục con duy nhất, cân nhắc chuyển thành câu dẫn hoặc cụm in đậm đầu đoạn và giữ điểm neo tương ứng.
- [ ] **Gộp hoặc bỏ khối có đối chiếu trước–sau.** Đọc từng đoạn hoặc từng hàng của khối cũ. Xác định ý cần giữ nằm ở đâu và liên kết cũ sẽ dẫn tới đâu. Sau khi sửa, kiểm ngược từ bản mới về khối cũ để phát hiện phần sót. Khi bỏ bảng lộ trình, đối chiếu từng chặng và từng đích liên kết.
- [ ] **Một mẫu mục lục cho các thẻ học liệu.** Dùng nhãn theo mẫu **Mục lục + tên thẻ**, chẳng hạn **Mục lục bài học**. Cả hai bố cục lấy cùng tên mục, cấp mục, thứ tự và đích liên kết từ cấu trúc nội dung. Mục lục ghi tên đề mục hoặc số và tên nhiệm vụ, bỏ các nhãn khu vực lặp lại. Trên màn hình rộng, mục lục nằm ở cột phải. Trên màn hình hẹp, mục lục là một khung mặc định đóng ngay sau phần mở đầu. Khi mở khung, các mục chính hiện trước và học sinh có thể mở mục con của từng nhóm.
- [ ] **Thứ tự nhóm Tra cứu trên thanh điều hướng.** Xếp **Đọc toàn văn → Tải PDF → Nguồn tài liệu**. Với chuyên đề chưa có PDF, hiện **Đọc toàn văn → Nguồn tài liệu**. Kiểm thứ tự và đích liên kết trên thanh bên máy tính và trong menu **Nội dung** ở màn hình hẹp.
- [ ] **Lối về danh sách chuyên đề.** Dùng liên kết **Chuyên đề** trên thanh điều hướng chung. Bỏ dòng điều hướng lặp ngay trên tên bài. Kiểm liên kết vẫn dễ tìm và mở đúng danh sách trên màn hình rộng và hẹp. Nếu bố cục hẹp đưa thanh điều hướng vào menu, đặt lối về danh sách trong menu đó.
- [ ] **Kích thước mục lục nhất quán.** Trên màn hình rộng, giữ cùng bề rộng cột và chừa sẵn chỗ cho thanh cuộn. Trên màn hình hẹp, khung bám bề rộng cột đọc, có cùng khoảng đệm và hàng tiêu đề cao tối thiểu 44 px với chữ 14 px. Trong mỗi bố cục, các mục cùng cấp dùng cùng cỡ chữ, khoảng dòng và độ thụt lề. Dùng kiểu chung trong [CSS trang học](../../../../../../scripts/zo_course_site_sources/learning-format.css).
- [ ] **Kiểm mục lục ở cả hai bố cục.** So một mục lục ngắn với một mục lục phải cuộn, ở cả hai phía của ngưỡng đổi bố cục. Ở mỗi độ rộng, chỉ một mục lục hiển thị. Thử mở mục lục bằng bàn phím và chọn một đích nằm trong khung nội dung đang đóng. Liên kết phải tự mở đúng khung và đưa đích vào vùng đọc ngay dưới thanh đọc. Thử cả hai chiều giữa đề và lời giải khi đường đi này bị ảnh hưởng.

### Hiển thị và thao tác

- [ ] **Cỡ chữ cho thấy thứ bậc.** So các tiêu đề cùng vai trò ngay trong trang và với phần đã chốt. Chặng hoặc mục chính nổi rõ hơn các mục bên trong. Nhiệm vụ và Điểm dừng cùng cấp trong Luyện tập dùng cỡ nhất quán. So cả chế độ chữ thường và chữ lớn trên màn hình rộng, hẹp.
- [ ] **Hộp thu gọn cân đối theo chức năng.** Căn giữa tiêu đề và dấu mở hoặc đóng theo chiều dọc. Dùng khoảng đệm trên dưới bằng nhau khi hộp đóng và để hộp tự giãn khi tiêu đề xuống dòng. Khung lượt Ôn lại, thẻ Ôn nền và khung nhóm Sửa lỗi dùng cùng cỡ chữ và khoảng đệm. Hộp đọc thêm, đối chiếu và lời giải dùng cỡ chữ theo vai trò. Khung video dùng biểu tượng phát. Kiểm một tiêu đề một dòng và một tiêu đề nhiều dòng trên màn hình hẹp, rồi thử đóng mở bằng bàn phím.
- [ ] **Khoảng cách nhãn–tiêu đề khớp phần đã chốt.** Ngay lượt đầu, đo các cặp còn hiển thị từ mép dưới hộp nhãn đến mép trên hộp tiêu đề. Đối chiếu với cặp cùng cấp ở phần trước tại cả hai cỡ chữ và độ rộng.
- [ ] **Các thành phần cùng chức năng phản hồi giống nhau.** So khoảng cách icon–chữ và điểm căn của các liên kết tương đương. Rê chuột và dùng Tab để so liên kết chữ trong đoạn văn, danh sách và bảng, chẳng hạn “Ôn nền” và “Xem lời giải”. Kiểm dấu hiệu chọn bằng bàn phím và thử mở đúng đích.
- [ ] **Lời mời cạnh mã QR trên thanh đếm ngược.** Dùng **Mời ZO Math một ly trà sữa 🧋**. Nếu thanh đếm ngược ở màn hình hẹp chỉ đủ chỗ cho một dòng dưới mã QR, dùng **Mời trà sữa**. Tên dành cho trình đọc màn hình dùng lời mời đầy đủ và cho biết nút mở mã QR bảo trợ. Kiểm mã QR và nút mở hộp thông tin trên cả hai bố cục.
- [ ] **Nội dung đọc liền mạch ở màn hình hẹp.** Kiểm tiêu đề và phần thân của cùng một nhiệm vụ có đủ gần để nhìn thành một khối. Soát đường kẻ lặp, dấu câu rơi dòng và khung bảng hoặc hình che mất dữ kiện quan trọng. Với bảng hoặc hình cuộn ngang, thử cuộn tới phần nằm ngoài khung ban đầu.

## 3. Hướng dẫn theo phần học

### Tổng quan

1. Mở bằng câu hỏi trọng tâm của chuyên đề. Nếu có hai câu hỏi, có thể đặt ở hai dòng. Tiếp theo dùng một đoạn ngắn nêu học sinh sẽ làm việc với dữ kiện nào và học cách kết luận ra sao.
2. Đặt **Chọn phần học** gần đầu trang làm điều hướng của Tổng quan. Dưới mỗi liên kết, dùng một cụm mô tả ngắn theo nội dung của gói. **Bài học** nêu kiến thức và ví dụ. **Luyện tập** nêu dạng bài hoặc thao tác chính. **Kiểm tra** nêu việc tự kiểm tra. **Ôn lại** ghi số lượt và mốc thực tế. Tránh lặp tên chuyên đề hoặc dùng mẫu “Em muốn…” cho các mô tả.
3. Viết mục tiêu thành việc học sinh làm được. Chỉ đánh số khi thứ tự mang ý nghĩa. Dùng cùng cấp chữ cho **Chọn phần học**, **Học xong, em cần làm được gì?** và **Kiến thức cần dùng**. Nêu tên các kĩ năng nền và đặt liên kết **Ôn nền** tại chỗ phù hợp.

### Bài học

1. Mở bằng câu hỏi dẫn đường có thể theo dõi xuyên bài và một lời dẫn ngắn. Bỏ tiêu đề lớn “Bài học” khi tên phần đã hiện rõ. Giữ nhãn định vị trên thanh đọc khi cuộn.
2. Với **Khởi động**, đặt một lời hướng dẫn ngay dưới tiêu đề. Nếu có lời giải chung, đặt một liên kết **Xem lời giải** sau nhóm nhiệm vụ. Bỏ đề mục chỉ để chứa liên kết đó.
3. Đưa lời gợi mở vào mạch văn bằng câu hỏi hoặc tình huống toán cụ thể. Đặt video cạnh phần mà nó giúp giải thích. Khung video cần tên video và biểu tượng phát dễ nhận biết.
4. Ở **Khép lại bài học**, dùng câu tự kiểm cụ thể. Nếu hai tình huống có điều kiện khác nhau, gọi rõ từng tình huống trong câu hỏi.

### Luyện tập

1. Dùng một đoạn mở đầu ngắn để nêu số bài, cách tự làm và giữ bài trước khi xem lời giải. Giải thích ngay **Điểm dừng** giúp học sinh đối chiếu bài làm, nhận ra chỗ còn vướng và quyết định đi tiếp hay ôn lại.
2. Khi mục lục và bảng lộ trình dẫn tới cùng nhiệm vụ, đối chiếu từng hàng trước khi gộp điều hướng vào mục lục. Nếu tên chặng chưa nói đủ việc học sinh sẽ làm, đặt một câu dẫn ngay dưới tiêu đề.
3. Ở mỗi Điểm dừng, nêu tiêu chí của chính chặng đó, đường dẫn hỗ trợ phù hợp và việc học sinh làm tiếp. Nếu có bài xác nhận sau sửa, chỉ rõ bài nào cần đối chiếu trước và lời giải nào mở sau khi tự làm bài xác nhận.

### Kiểm tra

1. **Trước khi vào đề.** Dùng một đoạn ngắn nêu số nhiệm vụ, cách tự làm cả đề trong một lần, yêu cầu trình bày lập luận và điều kiện tự lực. Đặt thời lượng đề xuất và tổng điểm ngay trước nhiệm vụ đầu tiên. Lấy các số này từ đề và thang điểm của chính chuyên đề.
2. **Trong đề.** Viết từng ý sao cho học sinh biết cần xác định, giải thích hay sửa điều gì. Giữ câu hỏi dùng lại kết quả của ý trước khi nó yêu cầu thêm một thao tác riêng, chẳng hạn chỉ ra vế đúng và sửa vế sai. Với câu hỏi đọc hình, kiểm cả nhãn, chú thích và văn bản thay thế. Mô tả ảnh cung cấp dữ kiện tương đương với hình để học sinh dùng trình đọc màn hình tự suy ra kết quả. Chỉ giữ chú thích khi nó bổ sung thông tin cần dùng hoặc giúp tham chiếu đến hình.
3. **Sau bài cuối.** Đặt một liên kết chung **Xem lời giải**. Nhắc học sinh giữ bài làm ban đầu, mở nhiệm vụ cần xem, đối chiếu cách làm và tự chấm từng ý. Chỉ rõ nơi xem cách tính điểm, chẳng hạn cột **Căn cứ cho điểm** hoặc phần ghi điểm kèm lời giải. Hướng dẫn ghi riêng điểm ban đầu và kết quả sau khi sửa. Mỗi khoản điểm phải ứng với một yêu cầu trong đề. Khi đề hỏi một kết luận có suy ra từ giả thiết hay không, dùng **Suy ra / Không suy ra** nhất quán trong lời giải.
4. **Điểm dừng sau Kiểm tra.** Hướng dẫn ngắn cách chọn **Ôn nền** khi thiếu kiến thức nền, chọn **Sửa lỗi** theo lỗi đã gặp và tự làm một bài chưa gặp để kiểm tra lại. Nêu điều kiện ghi ngày hoàn tất và hẹn **Ôn lại**. Khi nhắc tới các kĩ năng cần đạt, dẫn về danh sách mục tiêu của chuyên đề. Nếu cần giúp học sinh đọc kết quả chi tiết, dùng khung thu gọn **Xem lại những ý em còn vướng**. Sắp câu tự hỏi theo thứ tự nhiệm vụ, ghi rõ ý nào và bước nào cần xem lại. Giữ hướng dẫn sử dụng khung ở một chỗ.
5. **Cấp đề mục.** Đặt **Đề bài** và **Sau khi hoàn thành bài kiểm tra** cùng cấp. Các **Nhiệm vụ** thuộc **Đề bài**. **Điểm dừng** thuộc **Sau khi hoàn thành bài kiểm tra**. Đối chiếu cấp tiêu đề trong QMD, cấp hiển thị trong HTML và độ lồng trong mục lục. Các tiêu đề cùng cấp dùng cùng cỡ chữ ở mỗi chế độ đọc.
6. **Kiểm trước khi chốt.**
   - Đọc theo thứ tự học sinh sử dụng. Đối chiếu từng ý với lời giải, khoản điểm và câu tự hỏi tương ứng. Cộng điểm từng ý để kiểm điểm nhiệm vụ, rồi cộng điểm các nhiệm vụ để kiểm tổng điểm ghi ở đầu đề.
   - Trên màn hình rộng và hẹp, dùng mục lục để tới một nhiệm vụ và Điểm dừng. Kiểm điều kiện kết thúc lượt tự làm trước khi mở lời giải, cả ở thẻ riêng và trong Đọc toàn văn. Với hộp xác nhận, thử tiếp tục tự làm và xác nhận đã kết thúc. Sau khi mở lời giải, thử mũi tên **Quay lại chỗ vừa đọc** trong các khung nhiệm vụ. Các mũi tên phải đưa học sinh về đúng chỗ đã bấm liên kết chung.
   - Mở khung tự hỏi, thử liên kết về nhiệm vụ và kiểm đích tới mục tiêu hoặc phần hỗ trợ. Khi gộp, bỏ hoặc đổi cấp đề mục, giữ các điểm neo còn được dùng và kiểm lại liên kết từ **Ôn lại** về Điểm dừng.

### Ôn lại

1. **Ngày hẹn.** Nêu rõ ngày bắt đầu tính lịch, chỗ học sinh ghi ngày đó và nơi ghi các ngày hẹn. Nếu cần minh họa, dùng một ngày cụ thể và tính tất cả mốc theo lịch của chính chuyên đề. Đặt mốc thời gian ngay trong tên lượt để học sinh biết mở khung nào.
2. **Cấu trúc mỗi lượt.** Đặt lượt ôn làm đề mục cha. Đặt **Nhiệm vụ** và **Điểm dừng** làm hai mục con cùng cấp và cùng cỡ chữ. Khung lượt ôn mặc định thu gọn. Liên kết từ mục lục phải mở đúng lượt và đưa học sinh đến nhiệm vụ hoặc Điểm dừng được chọn trên cả màn hình rộng và hẹp.
3. **Trước khi tự làm.** Nêu một lần cách làm bài vào ngày hẹn. Đề cung cấp đủ dữ kiện, kí hiệu và phạm vi để học sinh hiểu nhiệm vụ. Đặt gợi ý giải, đáp án, tiêu chí đối chiếu và video giải thích sau phần tự làm. Với đề đọc hình, mô tả ảnh diễn đạt hình thể hiện gì để học sinh tự kết luận.
4. **Sau mỗi lượt.** Đặt **Xem lời giải** sau nhiệm vụ của lượt đó. Trong Điểm dừng, gọi tên bước cần đối chiếu, chỉ bài sửa hoặc kiến thức nền phù hợp và nhắc ghi riêng kết quả tự làm. Nếu cần kiểm tra lại sớm một lỗi vừa sửa, hẹn riêng cho lỗi đó và giữ lịch các lượt ôn. Nêu rõ phần ôn thêm và điều kiện để làm nếu có.
5. **Kiểm trước khi chốt.** Đọc mỗi đề cùng lời giải và Điểm dừng. Kiểm các tiêu đề cùng cấp ở chế độ chữ thường và chữ lớn. Từ từng lượt, mở lời giải rồi dùng mũi tên ở cuối lời giải để về đúng vị trí. Thử thêm đường đi qua mục hỗ trợ, tải lại trang và dùng nút quay lại của phần đó. Xác nhận đúng lượt và điểm neo trên màn hình rộng và hẹp.

### Ôn nền

1. **Chọn đúng thẻ.** Đầu mỗi thẻ, dùng **Dùng thẻ này khi…** để nêu một dấu hiệu mà học sinh nhận ra từ bài đang làm. Gọi rõ thao tác hoặc chỗ dễ nhầm. Cuối thẻ, chỉ ra bước cần kiểm lại khi quay về bài hoặc Điểm dừng.
2. **Từ ví dụ đến tự làm.** Nhắc ngắn kiến thức cần dùng, giải một ví dụ rồi cho học sinh **Làm tiếp một bước**. Nêu tình huống toán, dữ kiện đã biết và thao tác cần thực hiện. Viết yêu cầu thành câu đầy đủ và giữ đủ các ý toán khi bỏ dạng điền chỗ trống. Trong **Đối chiếu bước vừa làm**, trả lời từng ý và giải thích vì sao kết quả giúp quyết định bước kế tiếp. Tiếp theo là nhiệm vụ tự làm với dữ kiện phù hợp để kiểm lại đúng kĩ năng. Đặt lời giải trong khung thu gọn mang cùng tên nhiệm vụ. Nếu có thêm nhiệm vụ dành cho một lỗi cụ thể, nêu ngay trong đề khi nào cần làm.
3. **Hướng dẫn tự kiểm tra một lần ở đầu trang.** Dùng một câu phù hợp mà học sinh chưa từng làm và chưa xem đáp án. Dành đề **Kiểm tra** và bài **Ôn lại** cho đúng lượt. Nếu học sinh vẫn làm sai, hướng em xem lại bước còn vướng. Chỉ dùng câu “Chưa có bài mới để xác nhận thêm ở mục tiêu này” khi đã hết câu mới phù hợp.
4. **Kiểm lời văn và đích quay về.** Đọc đề và lời giải cùng nhau. Gọi đúng đối tượng trong câu hỏi và tiêu chí, chẳng hạn dấu của đạo hàm trên một khoảng hoặc giá trị hàm số tại một điểm. Nếu đề cho mô tả đồ thị bằng chữ, lời giải phải đối chiếu với chính mô tả đó. Trên màn hình rộng và hẹp, thử mở thẻ từ mục lục, kiểm lời giải mặc định đóng và thử quay lại đúng chỗ đang làm.

### Sửa lỗi

1. **Mở đầu và tra bảng.** Nêu ngắn cách giữ bài làm ban đầu, tìm và sửa bước sai, rồi tự làm một bài chưa gặp về cùng lỗi trước khi xem lời giải. Để bảng **Chọn bài sửa lỗi** hiển thị sẵn. Trong bảng, dùng dấu hiệu học sinh nhận ra được từ bài làm, một câu hỏi giúp tìm nguyên nhân, cách tháo gỡ và đường dẫn đến bài phù hợp. Ghi rõ khi chưa có bài tự kiểm tương ứng. Nếu học sinh đã làm hoặc đã xem lời giải của mọi bài phù hợp, hướng dẫn xem lại dòng tương ứng trong bảng và ghi lỗi cần thử lại vào **Nhật kí** nếu cần.
2. **Nhóm theo nơi phát hiện lỗi.** Dùng các khung mặc định đóng theo mẫu **Ôn lại**, mỗi khung chứa lời dẫn ngắn và các nhiệm vụ của nhóm. Với R1-G01, ba khung là **Sau Luyện tập**, **Sau Kiểm tra** và **Sau Ôn lại**. Lỗi phát hiện trong **Bài học** dùng nhóm **Sau Luyện tập**. Nhóm **Sau Kiểm tra** dùng sau khi đã kết thúc bài kiểm tra. Giữ nhiệm vụ dưới đúng cấp nhóm và giữ các điểm neo đang được dùng.
3. **Đề gọn và đủ yêu cầu.** Bỏ đoạn **Dùng bài này khi…** nếu dấu hiệu đã có trong bảng. Bỏ mục **Tự đối chiếu** ở từng nhiệm vụ Sửa lỗi. Trước khi bỏ, chuyển yêu cầu còn thiếu vào đề, chẳng hạn nêu lí do, xét đủ trường hợp hoặc trình bày hai cách giải cụ thể. Giữ giả thiết và phạm vi kết luận. Tiêu đề và câu hỏi để học sinh tự xác định kết quả, số bước sai hoặc phương án phù hợp.
4. **Lời giải và hỗ trợ.** Đặt **Xem lời giải** ngay sau yêu cầu cuối của từng đề. Lời giải trả lời đủ từng ý và nêu căn cứ cho các kết luận. Khi đề yêu cầu kiểm tra một lập luận, giải thích cả các bước đúng cần giữ lẫn bước sai cần sửa. Chọn lọc liên kết ôn tập theo quy tắc **Chỉ dẫn cuối lời giải**.
5. **Dữ kiện mới cho bài tự kiểm.** Khi mục tiêu là kiểm tra khả năng tự làm sau khi sửa lỗi, dùng dữ kiện khác với ví dụ đã được hướng dẫn. Với bài đọc hình, dùng hình mới cùng kĩ năng, rà các nhãn và mô tả ảnh rồi tính lại kết quả trong lời giải. Mô tả ảnh cung cấp dữ kiện nhìn thấy được để học sinh tự kết luận.
6. **Kiểm đường đi trước khi chốt.** Ở màn hình rộng và hẹp, xác nhận bảng tra luôn thấy được và các nhóm mặc định đóng. Thử mở khung bằng bàn phím, chọn bài trong mỗi nhóm từ bảng hoặc mục lục, mở **Xem lời giải** rồi dùng mũi tên ở cuối lời giải. Trang phải mở đúng nhóm và khôi phục vị trí đã bấm **Xem lời giải**. Thử cả liên kết trực tiếp tới một nhiệm vụ đang nằm trong khung đóng.

### Lời giải

1. **Nhóm theo phần học.** Dùng tên phần học làm tiêu đề, mỗi nhiệm vụ là một khung mặc định đóng. Mục lục xếp các nhiệm vụ trực tiếp dưới nhóm tương ứng và dùng số, tên nhiệm vụ. Bỏ nhãn lặp như **Hỗ trợ · Lời giải** và các tiêu đề trung gian chỉ để chia danh sách. Giữ những điểm neo còn được dùng.
2. **Đọc lại đề tại chỗ.** Lấy đề từ cùng nguồn với nhiệm vụ gốc, kèm hình, bảng và dữ kiện cần thiết. Đặt dòng **Hiện đề bài** trước lời giải và mặc định thu gọn đề. Khi mở, đổi nhãn thành **Ẩn đề bài**. Trình bày đề thụt nhẹ, chữ nhỏ hơn lời giải và cùng nền với khung nhiệm vụ. Dùng dòng chữ gọn, bỏ nền riêng và mũi tên. Khi rê chuột, dùng đổi màu. Khi chọn bằng bàn phím, có dấu hiệu focus rõ. Không dùng gạch chân ở bất kì trạng thái nào. Bỏ tiêu đề **Lời giải** lặp trong từng khung.
3. **Trả lời đủ yêu cầu của đề.** Đối chiếu từng ý với lời giải. Thể hiện bảng hoặc hình khi đề yêu cầu lập bảng hoặc phác hình. Khi sửa một lập luận, nêu bước đúng, bước sai và viết thành lời giải hoàn chỉnh nếu đề yêu cầu. Nêu điều kiện áp dụng ngay ở bước kết luận và chỉ rõ dữ kiện còn thiếu khi chưa thể kết luận. Với bài Kiểm tra, đối chiếu lời giải với từng khoản điểm.
4. **Chỉ dẫn cuối lời giải.** Giữ chỉ dẫn khi nó giúp học sinh tự chấm, nhận ra một lỗi cụ thể hoặc biết cần làm gì tiếp theo. Bỏ lời nhắc lặp lại kết luận hoặc cách học đã nêu ở đầu thẻ hay Điểm dừng. Khi dẫn sang bài ôn, gọi rõ ý hoặc bước học sinh có thể làm sai và chọn bài giúp kiểm lại đúng bước đó. Nếu có nhiều lỗi cần dẫn, viết mỗi lỗi một dòng để dễ tra. Giữ lưu ý tự chấm khi học sinh có thể dùng cách giải khác và nêu căn cứ để tính điểm. Kiểm cả nội dung ở đích liên kết.
5. **Mũi tên trong khung lời giải.** Trên HTML, đặt mũi tên sang trái trong vòng tròn nhỏ, căn trái ở cuối khung nhiệm vụ. Mũi tên hiện khi mở khung. Nếu cả nhóm dùng chung một liên kết **Xem lời giải**, mỗi khung có một mũi tên và tất cả dùng chung đích quay lại. Khi học sinh vừa bấm **Xem lời giải**, mũi tên khôi phục đúng vị trí đã bấm và có nhãn **Quay lại chỗ vừa đọc**. Khi mở từ mục lục hoặc liên kết trực tiếp, mũi tên dẫn đến đề gốc hoặc phần đề của cả nhóm và có nhãn **Quay lại đề bài**. Dùng cùng nhãn khi rê chuột, chọn bằng bàn phím hoặc dùng trình đọc màn hình. Giữ mũi tên trên thanh đọc khi hệ thống còn ghi nhớ chỗ xuất phát.
6. **Kiểm trước khi chốt.** Trên màn hình rộng và hẹp, thử mở một lời giải riêng và một nhóm lời giải từ **Xem lời giải**. Kiểm mũi tên ở từng khung trong nhóm và mũi tên trên thanh đọc. Thử mở từ mục lục và liên kết trực tiếp để xác nhận đích về đề gốc. Thử bằng bàn phím và kiểm nhãn khi rê chuột hoặc nhận focus. Đối chiếu đề mở tại chỗ với đề gốc và kiểm đề vẫn thu gọn khi vừa mở lời giải.

### Nhật kí

1. **Ghi khi có việc cần nhớ.** Mở đầu bằng một câu ngắn nêu khi nào cần ghi, chẳng hạn khi còn vướng, cần hẹn ngày ôn hoặc cần nhớ nơi học tiếp. Dùng bốn câu hỏi để học sinh chọn điều cần ghi về bài đã làm và hỗ trợ đã dùng, chỗ còn vướng, cách sửa và thử lại, việc làm lần tới. Chỉ nhắc ghi kết quả của bài mới nếu đã thử. Nếu còn vướng, ghi rõ chỗ cần gợi ý.
2. **Đặt ví dụ ngay sau phần ghi nhanh.** Dùng nhãn **Ví dụ.** Nêu một tình huống cụ thể của chuyên đề, gồm lỗi đã mắc, cách sửa, kết quả tự làm bài mới nếu có và việc dự định làm tiếp. Ghi riêng kết quả ngay sau khi sửa và kết quả vào ngày hẹn. Nếu chưa kiểm vào ngày hẹn, ghi **Chưa kiểm lại**. Phân biệt ngày hẹn kiểm một lỗi với lịch **Ôn lại** toàn chuyên đề.
3. **Để mẫu đầy đủ trong khung thu gọn.** Dùng tên **Mẫu nhật kí chi tiết**, mặc định đóng. Giữ tên và thứ tự 14 trường theo mục 2.8 của tài liệu Kiến trúc học tập trong cả mẫu trống và bảng ví dụ. Học sinh điền những ô đã có thông tin. Bảng ví dụ có thể dùng lại tình huống ghi nhanh để minh họa cách điền. Viết ngắn, mỗi ô ghi thông tin đúng với tên trường. Bỏ câu dẫn chỉ nói lại điều bảng đã thể hiện. [Kiến trúc học tập](01_kien_truc_hoc_tap.md)
4. **Kiểm trên màn hình rộng và hẹp.** Phần ghi nhanh và ví dụ hiện ngay khi mở thẻ. Bỏ mục lục nếu chỉ có một liên kết trỏ về chính thẻ. Thử mở khung chi tiết bằng bàn phím, kiểm đủ 14 trường ở cả hai bảng và đọc thử các dòng dài trên màn hình hẹp.

### Tải PDF

1. **Đưa danh sách tải lên đầu thẻ.** Đặt các bản dùng cho cả chuyên đề ngay dưới thanh đọc. Các tệp riêng đặt dưới tiêu đề **Tải theo phần**. Bỏ lời dẫn chung chỉ nhắc chọn bản tải, thông báo chung về trạng thái PDF ở đầu danh sách và mục lục chỉ trỏ về chính thẻ. Bỏ nhãn khu vực lặp trên mỗi thẻ tải và dòng ghi tên chuyên đề, phiên bản ở cuối trang.
2. **Giúp học sinh chọn đúng bản.** Mỗi mục ghi tên bản, mô tả ngắn, số trang và nút **Tải PDF**. Với biến thể PDF `student`, dùng tên **Bản học sinh** trên thẻ tải ở mọi chuyên đề và nhãn truy cập **Tải PDF: Bản học sinh** trên nút. Mô tả ngắn bản nào dùng để tự làm và bản nào kèm lời giải hoặc hướng dẫn chấm. Khi trạng thái cập nhật khác nhau giữa các tệp, ghi trạng thái ngay ở mục tương ứng.
3. **Dùng chung khối lời mời với trang Khóa 2027.** Đặt khối sau danh sách tải, dùng nền vàng nhạt và logo xếp tầng. Trên màn hình rộng, đặt mã QR cạnh thông tin chuyển khoản. Trên màn hình hẹp, xếp dọc các phần. Lấy tiêu đề **Mời ZO Math một ly trà sữa 🧋**, đoạn lời mời và nhãn **Xem cách gửi trà sữa** từ QMD trang Khóa 2027. Viết lời mời thân tình, nói rõ sự ủng hộ giúp ZO Math soạn thêm bài và chia sẻ miễn phí. Liên kết dẫn đến trang thông tin bảo trợ. Các nhãn chuyển khoản dùng cách gọi chuẩn và thông tin lấy từ mẫu chung. [QMD trang Khóa 2027](../index.qmd) · [Mẫu Bảo trợ](../../../../../../_design/web_2027_mau_dung_chung/templates/support.html.tpl)
4. **Kiểm bản HTML và các đích tải.** Đối chiếu từng nút với tên tệp, số trang và nội dung của bản PDF liên kết. Kiểm trên màn hình rộng và hẹp, gồm cả việc tải ảnh logo, mã QR và mở đúng liên kết bảo trợ. Việc sửa giao diện thẻ Tải PDF chỉ cần cập nhật HTML. Dựng PDF khi nhiệm vụ yêu cầu cập nhật tệp PDF.
5. **Lời mời trong PDF.** Dùng cùng lời mời và nhãn **Xem cách gửi trà sữa** từ QMD trang Khóa 2027 cho khối Bảo trợ ở cuối PDF. Mẫu in dùng tiêu đề chữ thuần **Mời ZO Math một ly trà sữa** để phù hợp với phông in. Trước khi thay tệp, kiểm trang cuối, mã QR, thông tin chuyển khoản và đích liên kết. Nếu đồng bộ bản tải trên HTML cục bộ, đối chiếu tệp tải với PDF đã kiểm và cập nhật số trang trên thẻ.

### Nguồn tài liệu

1. **Mỗi tài liệu một mục.** Ghi tên tài liệu, cơ quan ban hành hoặc nhà xuất bản, năm và thông tin nhận diện bản đã dùng nếu cần. Nêu cụ thể phần chuyên đề đã đối chiếu với từng nguồn. Nếu dùng nhiều bài trong cùng một sách, đặt chúng thành các mục con dưới tên sách.
2. **Ghi số trang theo đúng bản đã đối chiếu.** Kiểm tên bài và số trang trực tiếp trong tài liệu. Khi số trang in khác số trang PDF, ghi trang in trước và số trang PDF trong ngoặc. Nếu dùng bản mẫu, ghi rõ phiên bản để người đọc tra đúng bản.
3. **Ghi rõ phần ZO Math biên soạn.** Dùng một câu ngắn để xác định phần do ZO Math biên soạn, chẳng hạn ví dụ, câu hỏi, phản ví dụ, lời giải và hướng dẫn chấm. Khi học liệu trích hoặc chuyển thể một nội dung cụ thể, ghi nguồn ngay ở nội dung đó.
4. **Trình bày gọn.** Bắt đầu bằng danh sách nguồn và dùng nhãn **Nguồn tài liệu** trên thanh đọc. Bỏ tiêu đề lặp và mục lục nếu nó chỉ trỏ về chính thẻ. Kiểm tên sách, số trang và các mục con trên màn hình rộng và hẹp.

### Đọc toàn văn

1. **Dùng chung nội dung với từng thẻ.** Trong **Bắt đầu**, dùng phần Tổng quan hiện hành rồi đến phần **Cách học** nếu có. Các phần tiếp theo lấy nội dung từ thẻ tương ứng theo thứ tự tra đọc của chuyên đề. Dùng chung nguồn và nội dung hiển thị để một lần sửa có hiệu lực ở cả hai chế độ. [Quy chuẩn trang người học](07_quy_chuan_cau_truc_trang_nguoi_hoc.md)
2. **Giữ tiêu đề và nhãn định vị.** Hiện tiêu đề của từng phần để người học nhận ra khi chuyển đoạn. Giữ nhãn **Đọc toàn văn** trên thanh đọc. Ẩn các nhãn khu vực lặp như **Mạch học · Bài học** và **Hỗ trợ · Lời giải** trong nội dung, kể cả bên trong khung thu gọn, và trong mục lục. Giữ tên, số hoạt động và cỡ tiêu đề theo cấp đã chốt ở từng thẻ.
3. **Dùng chung cấu trúc mục lục.** Đặt tên **Mục lục toàn văn**. Dùng các phần làm nhóm chính và lấy tên, thứ tự, cấp mục tương đối và đích của các mục con từ mục lục từng thẻ. Trên màn hình rộng, dùng cột phải. Trên màn hình hẹp, đặt khung mặc định đóng ở đầu cột đọc và cho mở mục con theo từng nhóm.
4. **Kiểm điều hướng ở cả hai chế độ.** Trên màn hình rộng và hẹp, đối chiếu từng phần với thẻ riêng, kể cả nhãn và nội dung trong khung thu gọn. Dùng mục lục và bàn phím để đến một mục đang đóng, rồi thử tải lại và quay lại bằng trình duyệt. Từ **Xem lời giải**, kiểm mũi tên khôi phục đúng vị trí và giữ chế độ **Đọc toàn văn**. Thử riêng liên kết lời giải của **Kiểm tra** để kiểm điều kiện kết thúc lượt tự làm.

## 4. Mốc đối chiếu riêng của R1-G01

- **Khoảng cách nhãn–tiêu đề** là 14 px ở các mục chính của Bài học và cả ba Chặng của Luyện tập. Đo giữa hai hộp ở cỡ chữ thường và chữ lớn.
- **Liên kết chữ** dùng chữ đỏ đậm trên nền hồng nhạt khi rê chuột hoặc nhận focus bằng bàn phím. Viền focus cho thấy liên kết đang được chọn bằng Tab.
- **Bài học** gộp nội dung của đề mục con duy nhất vào mục 1 và mục 7, vẫn giữ các điểm neo cũ. Tạm giữ cách trình bày các bảng Bài học trên điện thoại, kể cả khi cần cuộn ngang.
- **Mục lục** dùng cùng mẫu ở **Bài học, Luyện tập, Kiểm tra, Ôn lại, Ôn nền, Sửa lỗi, Lời giải và Đọc toàn văn**. Mốc đối chiếu là cột phải từ 1201 px và khung thu gọn từ 1200 px trở xuống. **Tổng quan** dùng khối **Chọn phần học**.
- **Luyện tập** có chín bài trong ba chặng, tính cả Nhiệm vụ 20 ở cuối Chặng 3. Cả ba Chặng có lời dẫn và các đích trong bảng lộ trình cũ vẫn có trong mục lục.
- **Nhiệm vụ 14** yêu cầu đọc dấu từ đồ thị $y=h'(x)$. Nhãn trên hình chỉ gọi tên đồ thị. Đường cong, các trục và hai tọa độ đánh dấu là dữ kiện của bài.
- **Kiểm tra** có năm nhiệm vụ (21–25), thời lượng đề xuất 45 phút và tổng điểm 20. Sau Nhiệm vụ 25 là liên kết **Xem lời giải** chung. **Điểm dừng 04** có khung thu gọn **Xem lại những ý em còn vướng**, với câu tự hỏi xếp theo năm nhiệm vụ. Nhiệm vụ 22 là mẫu đối chiếu cách viết mô tả đồ thị khi đề yêu cầu đọc dấu. Nhiệm vụ 25 là mẫu phân điểm theo từng ý.
- **Ôn lại** có ba lượt sau 2–3 ngày, 7 ngày và 3–4 tuần, cùng tính từ ngày hoàn tất ghi theo Điểm dừng 04. Ba lượt lần lượt chứa Nhiệm vụ 26–28 và Điểm dừng 05–07. Ví dụ hoàn tất ngày 1/3 minh họa cách tính các ngày hẹn.
- **Ôn nền** có bảy thẻ và tám nhiệm vụ (29–36). Phần **Làm tiếp một bước** của thẻ **Tập xác định và khoảng xét** là mẫu viết đủ ý trong một tình huống. Học sinh nêu điều kiện để mẫu khác $0$, tìm tập xác định rồi kiểm tra cả khoảng dự định xét. Thẻ **Liên tục và đạo hàm tại điểm ghép** có thêm Nhiệm vụ 35 để kiểm lại điều kiện liên tục.
- **Sửa lỗi** có 26 nhiệm vụ (37–62) trong ba nhóm thu gọn. Nhiệm vụ 57 dùng một cặp đồ thị mới để học sinh phân biệt hoành độ cực trị, giá trị cực trị và điểm cực trị trên đồ thị. Cặp hình dùng ở Ôn nền vẫn phục vụ ví dụ hướng dẫn. Khi đối chiếu Nhiệm vụ 57, kiểm đủ hai hình, mô tả ảnh và lời giải.
- **Lời giải** có 54 khung nhiệm vụ trong năm nhóm **Bài học**, **Luyện tập**, **Kiểm tra**, **Ôn lại** và **Sửa lỗi**. Với **Khởi động** và **Kiểm tra**, mỗi khung lời giải có một mũi tên. Các mũi tên trong cùng nhóm đều quay lại vị trí của liên kết **Xem lời giải** chung khi học sinh mở từ liên kết đó.
- **Nhật kí** dùng cùng một ví dụ về lỗi suy cực trị từ đạo hàm bằng 0 cho phần ghi nhanh và bảng mẫu chi tiết. Ngày 3/11 là ngày hẹn kiểm riêng lỗi này.
- **Tải PDF** có hai bản cho cả chuyên đề là **Bản học sinh** và **Bản đầy đủ**. Sáu bản tải theo phần là **Bài học**, **Luyện tập**, **Kiểm tra**, **Sửa lỗi**, **Ôn lại** và **Lời giải**.
- **Nguồn tài liệu** nêu vai trò của Chương trình giáo dục phổ thông môn Toán 2018 và sách *Toán 12, tập một — Kết nối tri thức với cuộc sống*. Với sách giáo khoa, ghi riêng nội dung đối chiếu và hai cách đánh số trang của **Bài 1** và **Bài 4** theo bản mẫu tháng 1/2024.
- **Đọc toàn văn** có 11 phần theo thứ tự **Bắt đầu → Bài học → Luyện tập → Kiểm tra → Ôn lại → Ôn nền → Sửa lỗi → Nhật kí → Lời giải → Nguồn tài liệu → Tải PDF**. Đã kiểm trên màn hình rộng và hẹp về nhãn lặp, đích trong mục lục và mũi tên quay lại vị trí đọc. Liên kết **Xem lời giải** của **Kiểm tra** hiện cùng hộp xác nhận trong thẻ riêng và trong **Đọc toàn văn**. **Tiếp tục tự làm** giữ vị trí hiện tại. **Đã kết thúc** mở lời giải và mũi tên quay lại đúng nơi đã bấm. Liên kết giữa các mục trong **Kiểm tra** hoạt động trực tiếp.
- **Khoảng trống cần theo dõi của R1-G01.** Ngân hàng Sửa lỗi hiện chưa có bài kiểm trực tiếp lỗi bảng biến thiên hoặc đồ thị không khớp với công thức, như tình huống ở Nhiệm vụ 12. Khi bổ sung bài, yêu cầu học sinh chỉ ra dữ kiện không khớp và giải thích cách sửa.

## 5. Cập nhật hướng dẫn

Sau mỗi phần được chủ trì chốt, ghi ngay cách làm mới vào mục liên quan, cùng **phạm vi áp dụng** và **cách kiểm**. Đặt quyết định chỉ phù hợp với R1-G01 ở mục mốc đối chiếu. Các đề xuất đang trao đổi giữ trạng thái chờ chốt. Khi cách làm đã chốt thay một cách cũ, sửa ngay dòng đang áp dụng để các lượt sau có một hướng dẫn nhất quán.

Khi khép R1-G01, rà lại các điểm có thể áp dụng cho R1-G02. Ưu tiên tự động hóa những phép kiểm có tiêu chí rõ như đếm nhiệm vụ, đo khoảng cách, kiểm điểm neo và dựng đúng vùng. Tiếp tục đọc trong ngữ cảnh khi sửa lời văn và mạch học.
