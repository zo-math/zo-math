# R2-G01 — Rà diễn đạt trong bản thảo 0.2

Ngày 22/10/2026. Yêu cầu của chủ trì: rà bản thảo, thay cách diễn đạt kỹ thuật bằng lời dễ hiểu với người học; chưa dựng HTML/PDF hoặc commit. [Mở bản thảo hiện hành](../ban_thao/noi_dung.md).

## Phạm vi và kết quả biên tập

Đã đọc toàn bộ Bắt đầu, Bài học, Luyện tập, Kiểm tra, Ôn lại, Ôn nền, Sửa lỗi, Nhật kí, Lời giải và Nguồn. Đối chiếu 07/6.1.6 và 02/Rà thuật ngữ: câu cũ — chỗ khó hiểu — câu mới — điều kiện và đích cần giữ. Bảng dưới ghi 134 vị trí thay đổi (gồm dòng phiên bản); một đoạn có thể có nhiều chỉnh sửa nhỏ. Đây là kết quả rà của người biên tập, chưa phải xác nhận người học đã hiểu hoặc chủ trì đã duyệt.

Các nhóm sửa chính:

- Đọc bảng: dùng “dòng trong bảng”, giải thích đơn vị quan sát, biến, cỡ mẫu và mẫu gốc bằng dữ liệu chim cánh cụt.
- Khí tượng: dùng “ký hiệu T”, giải thích giáng thủy và vết giáng thủy; thay “mã hóa”, “lớp điểm”, “khối giá trị” bằng mô tả những gì bảng ghi.
- Phép tính: giữ thuật ngữ toán cần học, giải thích trọng số và nội suy ngay khi xuất hiện; dùng đầy đủ “tần số tích lũy”.
- Học và tự kiểm tra: thay “bằng chứng độc lập”, “xác nhận mới”, “còn mới”, “gọi hỗ trợ” bằng việc tự làm, việc đã xem lời giải và bài cần quay lại. Giữ điều kiện Kiểm tra liền mạch, giữ riêng kết quả trước/sau trợ giúp và không dùng trước bài Ôn lại.
- Đề và lời giải: làm rõ “chia đều tổng lượt thuê cho mỗi ngày”, “cùng có tần số lớn nhất”, cách gộp trung bình và giới hạn kết luận. Tên đề và lời giải được đổi đồng thời.
- Nhật kí và nguồn: dùng “mục cần ghi”, “hướng dẫn hoặc giúp đỡ đã nhận”, “ôn lại sau một thời gian”; bỏ mô tả API khỏi lời dành cho người học, giữ tên cột và nguồn gốc cần tra cứu.

Các số đo gốc, phần trích dữ liệu, bài tập và phép tính được giữ nguyên. Không đổi 27 số nhiệm vụ, 27 cặp đề–lời giải, 9 Ví dụ, 5 Gợi mở, 7 Điểm dừng, lịch và thời lượng. Các URL nguồn, địa chỉ đích trong bản thảo và nơi quay lại không đổi. Những thuật ngữ toán như trung vị, tứ phân vị, mốt, tần số tích lũy, trọng số và nội suy vẫn được dùng đúng nghĩa; không thay bằng từ thông thường làm sai khái niệm. Tên cột “Nút thắt nhận thức” được giữ theo quy chuẩn bảng Sửa lỗi dùng chung; lời trong các hàng đã được viết cụ thể hơn.

[Kiểm bản thảo 0.1](ket_qua_kiem_tra.json) được giữ nguyên làm bằng chứng của lượt trước; không coi hash cũ là hash bản 0.2. Kết quả kiểm lượt này ghi ở cuối báo cáo.

## Đối chiếu đầy đủ các vị trí đã sửa

Số dòng dẫn tới bản thảo 0.2; số dòng trước/sau không đổi. Liên kết trong phần trích dẫn được dẫn về đúng mục của bản thảo để tiện đối chiếu. Các trích dẫn dưới đây dùng để duyệt biên tập, không phải một bản nội dung thứ hai để sửa. Điều kiện toán, dữ kiện và đường đi cụ thể được đối chiếu trong ngữ cảnh cả đoạn.

### 001. Dòng 3 — Biên tập phiên bản

**Trước:**

> **R2-G01 · Bản thảo nội dung 0.1 · 22/10/2026**

**Sau:**

> **R2-G01 · Bản thảo nội dung 0.2 · 22/10/2026**

**Lý do:** Đánh dấu lượt sửa diễn đạt; chưa duyệt nội dung.

### 002. Dòng 11 — Đọc dữ liệu

**Trước:**

> Một bảng số có thể nói về chiều dài chân chèo của chim cánh cụt, số lượt thuê xe trong ngày hoặc lượng giáng thủy tại một trạm khí tượng. Trước khi tìm một con số đại diện, ta cần biết mỗi số được ghi cho ai, vào lúc nào và bằng đơn vị gì. Sau đó mới có thể hỏi: con số ấy giữ lại điều gì, và làm mờ điều gì?

**Sau:**

> Một bảng số có thể nói về chiều dài chân chèo của chim cánh cụt, số lượt thuê xe trong ngày hoặc lượng giáng thủy (nước từ mưa, tuyết…) tại một trạm khí tượng. Trước khi tìm một con số đại diện, ta cần biết mỗi số được ghi cho ai, vào lúc nào và bằng đơn vị gì. Sau đó mới có thể hỏi: con số ấy giữ lại điều gì, và làm mờ điều gì?

**Lý do:** Giải thích từ chuyên ngành khí tượng ở lần xuất hiện đầu.

### 003. Dòng 17 — Đọc dữ liệu

**Trước:**

> | Đọc đúng dữ liệu | Xác định đơn vị quan sát, biến, đơn vị đo, cỡ mẫu và dữ liệu thiếu. |

**Sau:**

> | Đọc đúng dữ liệu | Nêu mỗi dòng ghi về đối tượng nào, ghi đại lượng gì, dùng đơn vị nào; đếm số giá trị dùng để tính và nhận ra ô thiếu. |

**Lý do:** Viết mục tiêu thành những việc người học cần làm; thuật ngữ được giải thích trong bài.

### 004. Dòng 24 — Hướng dẫn học

**Trước:**

> **Tiên quyết.** Cần biết sắp thứ tự số, tính trung bình cộng và tỉ lệ, đọc khoảng. Không cần dùng đạo hàm. Nếu thiếu thao tác nào, mở đúng phần [Ôn nền](../ban_thao/noi_dung.md#on-nen), rồi trở về bài đang làm.

**Sau:**

> **Kiến thức cần có.** Cần biết sắp thứ tự số, tính trung bình cộng và tỉ lệ, đọc khoảng. Không cần dùng đạo hàm. Nếu thiếu thao tác nào, mở đúng phần [Ôn nền](../ban_thao/noi_dung.md#on-nen), rồi trở về bài đang làm.

**Lý do:** Thay nhãn điều hành bằng lời quen thuộc.

### 005. Dòng 26 — Hướng dẫn học

**Trước:**

> **Phạm vi.** Gói này tập trung vào vị trí trung tâm và tứ phân vị. Khoảng biến thiên, khoảng tứ phân vị, phương sai và độ lệch chuẩn sẽ được học riêng. Các dữ liệu thực tế giúp luyện cách đọc và suy nghĩ, không dùng để xây mô hình dự báo hoặc chứng minh quan hệ nhân quả.

**Sau:**

> **Phạm vi.** Gói này tập trung vào vị trí trung tâm và tứ phân vị. Khoảng biến thiên, khoảng tứ phân vị, phương sai và độ lệch chuẩn sẽ được học riêng. Các dữ liệu thực tế giúp luyện cách đọc và suy nghĩ, không dùng để dự báo hoặc khẳng định một yếu tố là nguyên nhân gây ra yếu tố khác.

**Lý do:** Nói rõ ý nghĩa quan hệ nhân quả, giữ giới hạn nội dung.

### 006. Dòng 40 — Hướng dẫn học

**Trước:**

> | Sửa thao tác tính hoặc đọc khoảng | [Ôn nền](../ban_thao/noi_dung.md#on-nen) | Tự làm câu xác nhận rồi trở về |

**Sau:**

> | Sửa thao tác tính hoặc đọc khoảng | [Ôn nền](../ban_thao/noi_dung.md#on-nen) | Tự làm bài ngắn ở cuối phần ôn rồi trở về |

**Lý do:** Chỉ đúng hoạt động cần làm.

### 007. Dòng 44 — Hướng dẫn học

**Trước:**

> Trong lúc Kiểm tra, em tự lực trong một lượt, không chia thành nhiều đợt. Nếu cần mở trợ giúp, hãy kết thúc lượt ấy và giữ bài làm ban đầu trước. Bài sau hỗ trợ được ghi riêng.

**Sau:**

> Trong lúc Kiểm tra, em tự lực trong một lượt, không chia thành nhiều đợt. Nếu cần mở trợ giúp, hãy kết thúc lượt ấy và giữ bài làm ban đầu trước. Phần làm sau khi xem hướng dẫn hoặc được giúp đỡ cần ghi riêng với phần em đã tự làm.

**Lý do:** Giải thích hỗ trợ và điều cần giữ riêng.

### 008. Dòng 50 — Hướng dẫn học

**Trước:**

> Lượt chính hoàn tất khi bài làm độc lập cho thấy em thực hiện được các mục tiêu thiết yếu và đã xử lí những lỗi cản trở việc học tiếp. Không dùng tổng điểm để bù cho một khái niệm còn hiểu sai. Một phép tính nhầm được sửa không làm mất những phần lập luận đúng, nhưng kết quả trước và sau sửa cần phân biệt.

**Sau:**

> Em hoàn tất lượt học chính khi tự làm được những việc cần đạt ở đầu gói và đã sửa, tự kiểm tra lại những lỗi cản trở việc học tiếp. Không dùng tổng điểm để bù cho một khái niệm còn hiểu sai. Một phép tính nhầm được sửa không làm mất những phần lập luận đúng, nhưng kết quả trước và sau sửa cần phân biệt.

**Lý do:** Chuyển điều kiện công nhận thành hành động; giữ yêu cầu tự làm và tự kiểm tra.

### 009. Dòng 90 — Hướng dẫn học

**Trước:**

> Làm đúng Khởi động cho thấy một số thao tác nền đã sẵn sàng, chưa chứng nhận các mục tiêu của cả gói.

**Sau:**

> Làm đúng Khởi động cho thấy em đã làm được những thao tác mở đầu này. Các kiến thức còn lại sẽ được học và tự kiểm tra ở những phần sau.

**Lý do:** Bỏ giọng chứng nhận, giữ giới hạn của Khởi động.

### 010. Dòng 100 — Đọc dữ liệu

**Trước:**

> | Dòng nguồn | Loài | Năm | Chiều dài chân chèo, mm |

**Sau:**

> | Dòng trong bảng gốc | Loài | Năm | Chiều dài chân chèo, mm |

**Lý do:** Nêu rõ nơi đánh số dòng.

### 011. Dòng 110 — Đọc dữ liệu

**Trước:**

> Số $0$ sẽ nói rằng chiều dài được ghi là $0$ mm. Trong khi đó, ô thiếu chỉ cho biết bản ghi không có giá trị chiều dài để dùng. Hai điều này khác nhau. Khi tính trên biến chiều dài, ta giữ lại thông tin rằng có một bản ghi thiếu, nhưng không đưa bản ghi ấy vào tổng hoặc mẫu số.

**Sau:**

> Số $0$ sẽ nói rằng chiều dài được ghi là $0$ mm. Trong khi đó, ô thiếu cho biết chưa có số đo chiều dài ở dòng ấy. Hai điều này khác nhau. Khi tính trung bình chiều dài, ta vẫn ghi nhận có một ô thiếu, nhưng chỉ cộng các số đo có sẵn và chia cho số giá trị đã cộng.

**Lý do:** Thay bản ghi, biến, mẫu số bằng việc đọc và tính cụ thể; giữ ô thiếu khác số 0.

### 012. Dòng 112 — Đọc dữ liệu

**Trước:**

> Một **đơn vị quan sát** ở đây là một cá thể chim trong dữ liệu. **Biến** đang xét là chiều dài chân chèo. Giá trị của biến được ghi bằng mm. Số dòng nguồn giúp truy lại bản ghi, không phải một phép đo khác và không phải mã cá thể do nhà nghiên cứu cấp.

**Sau:**

> Mỗi dòng trong bảng này ghi thông tin của một cá thể chim. Cá thể ấy là **đơn vị quan sát**. Đại lượng được ghi là chiều dài chân chèo; trong thống kê, đại lượng này gọi là **biến**, có đơn vị đo là mm. Số thứ tự dòng giúp tìm lại thông tin trong bảng gốc; nó không phải số đo hoặc mã nhận diện cá thể do nhà nghiên cứu cấp.

**Lý do:** Giải thích đối tượng trước khi đặt tên thuật ngữ.

### 013. Dòng 114 — Đọc dữ liệu

**Trước:**

> Phần Adélie 2007 có $50$ bản ghi, trong đó $49$ giá trị chiều dài hợp lệ. Khi tính trung bình chiều dài trên những giá trị có sẵn, cỡ mẫu là $n=49$. Không cần loại một giá trị chiều dài hợp lệ chỉ vì một biến khác, chẳng hạn giới tính, bị thiếu.

**Sau:**

> Phần Adélie 2007 có $50$ dòng, trong đó có $49$ số đo chiều dài dùng được. Số giá trị được đưa vào phép tính gọi là **cỡ mẫu**; ở đây $n=49$. Nếu một dòng có số đo chiều dài nhưng thiếu thông tin giới tính, số đo chiều dài ấy vẫn được dùng. Trong bài này, **mẫu gốc** là danh sách các giá trị trước khi ghép nhóm.

**Lý do:** Làm rõ cỡ mẫu, dữ liệu dùng được và mẫu gốc, giữ nguyên việc chọn dữ liệu.

### 014. Dòng 126 — Đọc dữ liệu

**Trước:**

> Trong $17$ bản ghi đầu của phần Adélie 2007, có đúng một ô thiếu chiều dài. Một bạn cộng các giá trị có sẵn được $3021$ mm rồi chia cho $17$.

**Sau:**

> Trong $17$ dòng đầu của phần Adélie 2007, có đúng một ô thiếu chiều dài. Một bạn cộng các giá trị có sẵn được $3021$ mm rồi chia cho $17$.

**Lý do:** Dòng dữ liệu dễ hình dung hơn bản ghi.

### 015. Dòng 162 — Đọc dữ liệu

**Trước:**

> Bỏ ô thiếu khỏi $17$ bản ghi đầu, ta có mẫu chiều dài chân chèo, đơn vị mm:

**Sau:**

> Chỉ lấy các số đo có sẵn trong $17$ dòng đầu, ta có mẫu chiều dài chân chèo, đơn vị mm:

**Lý do:** Không gợi ý xóa dòng khỏi nguồn.

### 016. Dòng 222 — Hướng dẫn học

**Trước:**

> Đây là một phần nhỏ của mẫu đã học, dùng để hiểu quy tắc; không phải một mẫu mới để xác nhận làm độc lập.

**Sau:**

> Ví dụ này dùng lại một phần dữ liệu vừa học để giải thích quy tắc khi số giá trị là số lẻ. Đọc hiểu lời giải giúp em nắm cách làm; để biết có tự làm được hay không, em cần thử một bài khác chưa xem lời giải.

**Lý do:** Nói rõ mục đích dùng lại dữ liệu và giới hạn của ví dụ.

### 017. Dòng 256 — Giải thích toán

**Trước:**

> Ta chia trục thành các khoảng không chồng lấn và bao phủ mọi giá trị của mẫu. Với quy ước đóng trái–mở phải, $190$ thuộc $[190;195)$, không thuộc $[185;190)$.

**Sau:**

> Ta chia trục thành các khoảng không chồng lấn và bao phủ mọi giá trị của mẫu. Ta dùng các khoảng lấy đầu mút trái và không lấy đầu mút phải (gọi là đóng trái–mở phải). Vì thế $190$ thuộc $[190;195)$, không thuộc $[185;190)$.

**Lý do:** Giải thích cách đọc khoảng trước thuật ngữ.

### 018. Dòng 299 — Giải thích toán

**Trước:**

> Trong một nhóm có nhiều quan sát, ta có thể dùng trung điểm để tính mức trung bình gần đúng. Với trung vị và tứ phân vị, tần số tích lũy cho biết cần đi đến nhóm nào; sau đó ta ước lượng vị trí bên trong nhóm bằng nội suy.

**Sau:**

> Trong một nhóm có nhiều quan sát, ta có thể dùng trung điểm để tính mức trung bình gần đúng. Với trung vị và tứ phân vị, tần số tích lũy cho biết cần đi đến nhóm nào; sau đó ta ước lượng vị trí bên trong nhóm. Cách tính này gọi là **nội suy**: coi các giá trị trải đều trong nhóm để tìm một giá trị gần đúng.

**Lý do:** Giải thích nội suy tại lần xuất hiện đầu, giữ ý nghĩa ước lượng.

### 019. Dòng 303 — Giải thích toán

**Trước:**

> | Khoảng, mm | Tần số $f_i$ | Trung điểm $c_i$, mm | Tích lũy |

**Sau:**

> | Khoảng, mm | Tần số $f_i$ | Trung điểm $c_i$, mm | Tần số tích lũy |

**Lý do:** Dùng đầy đủ tên đại lượng đã giải thích.

### 020. Dòng 324 — Giải thích toán

**Trước:**

> Mỗi trung điểm được tính với trọng số là số quan sát thuộc nhóm ấy. Lấy trung bình không trọng số của các trung điểm sẽ coi các nhóm đông và ít quan sát như nhau.

**Sau:**

> Ta nhân trung điểm của mỗi nhóm với số quan sát thuộc nhóm ấy, cộng các tích rồi chia cho tổng số quan sát. Số quan sát của nhóm được gọi là **trọng số** trong phép tính này. Nếu chỉ cộng các trung điểm rồi chia cho số nhóm, ta đã coi các nhóm có số quan sát như nhau, dù thực tế có nhóm nhiều, nhóm ít.

**Lý do:** Giải thích phép làm trước thuật ngữ trọng số.

### 021. Dòng 371 — Giải thích toán

**Trước:**

> Với $n=49$, vị trí trung vị là $r=24{,}5$. Tích lũy đến nhóm $[180;185)$ là $20$, đến nhóm $[185;190)$ là $30$. Vì vậy dùng nhóm $[185;190)$, với $a=185$, $F=20$, $f=10$, $h=5$:

**Sau:**

> Với $n=49$, vị trí trung vị là $r=24{,}5$. Tần số tích lũy đến nhóm $[180;185)$ là $20$, đến nhóm $[185;190)$ là $30$. Vì vậy dùng nhóm $[185;190)$, với $a=185$, $F=20$, $f=10$, $h=5$:

**Lý do:** Nêu đầy đủ tên đại lượng.

### 022. Dòng 418 — Giải thích toán

**Trước:**

> #### Nhiệm vụ 05 — Tự nội suy và kiểm ý nghĩa

**Sau:**

> #### Nhiệm vụ 05 — Tự nội suy và giải thích kết quả

**Lý do:** Nêu rõ yêu cầu thay cho nhãn kiểm ý nghĩa.

### 023. Dòng 434 — Khí tượng

**Trước:**

> Một con số có thể được tính đúng nhưng trả lời nhầm câu hỏi. Trung bình của một mẫu gộp hai loài không tự mô tả tốt từng loài; trung bình lượt thuê mỗi ngày không phải số người dùng khác nhau; số $0$ trong dữ liệu quan trắc cần được đọc cùng cờ ghi nhận.

**Sau:**

> Một con số có thể được tính đúng nhưng trả lời nhầm câu hỏi. Trung bình của một mẫu gộp hai loài không tự mô tả tốt từng loài; trung bình lượt thuê mỗi ngày không phải số người dùng khác nhau; số $0$ trong dữ liệu quan trắc cần được đọc cùng ký hiệu ghi nhận.

**Lý do:** Đã đọc từng ngữ cảnh: cờ ở đây là dấu ghi kèm dữ liệu, không phải khái niệm toán.

### 024. Dòng 451 — Giải thích toán

**Trước:**

> Con số này mô tả mẫu gộp theo đúng cơ cấu $49$ và $34$ quan sát. Nó nằm giữa hai trung bình riêng. Nếu câu hỏi quan tâm từng loài, bảng theo loài giữ được sự khác biệt mà một số chung che đi. Không lấy trung bình cộng đơn giản của hai trung bình khi cỡ mẫu hai nhóm khác nhau.

**Sau:**

> Con số này được tính từ $49$ cá thể Adélie và $34$ cá thể Gentoo đã ghi trong hai phần dữ liệu. Nó nằm giữa hai trung bình riêng. Nếu câu hỏi quan tâm từng loài, bảng theo loài giữ được sự khác biệt mà một số chung che đi. Không lấy trung bình cộng đơn giản của hai trung bình khi cỡ mẫu hai nhóm khác nhau.

**Lý do:** Giải thích cơ cấu mẫu bằng đối tượng cụ thể.

### 025. Dòng 463 — Giải thích toán

**Trước:**

> Nếu muốn phân bổ tổng lượt thuê của tháng theo ngày, số trung bình phù hợp vì $n\overline{x}$ khôi phục tổng trước khi làm tròn. Nếu muốn mô tả vị trí giữa các ngày khi xếp theo lượng thuê, dùng trung vị. Trung vị không cho biết tổng tháng bằng tích của nó với số ngày.

**Sau:**

> Nếu muốn biết tổng lượt thuê trong tháng chia đều cho mỗi ngày là bao nhiêu, số trung bình phù hợp vì $n\overline{x}$ khôi phục tổng trước khi làm tròn. Nếu muốn mô tả vị trí giữa các ngày khi xếp theo lượng thuê, dùng trung vị. Trung vị không cho biết tổng tháng bằng tích của nó với số ngày.

**Lý do:** Làm rõ phân bổ tổng theo ngày.

### 026. Dòng 470 — Nguồn và chú thích

**Trước:**

> Nguồn: Hadi Fanaee-T và João Gama, Bike Sharing, UCI Machine Learning Repository, tệp day.csv, các trường dteday và cnt, phần trích tháng 01/2012. Dữ liệu CC BY 4.0; ZO Math chọn phần trích và tính bảng tóm tắt, không thay giá trị gốc.

**Sau:**

> Nguồn: Hadi Fanaee-T và João Gama, Bike Sharing, UCI Machine Learning Repository, tệp day.csv, cột ngày (dteday) và cột số lượt thuê (cnt), phần trích tháng 01/2012. Dữ liệu CC BY 4.0; ZO Math chọn phần trích và tính bảng tóm tắt, không thay giá trị gốc.

**Lý do:** Giải thích tên cột gốc thay vì trường.

### 027. Dòng 473 — Khí tượng

**Trước:**

> #### Ví dụ 09 — Đọc số 0 cùng cờ quan trắc

**Sau:**

> #### Ví dụ 09 — Đọc số 0 cùng ký hiệu quan trắc

**Lý do:** Đã đọc từng ngữ cảnh: cờ ở đây là dấu ghi kèm dữ liệu, không phải khái niệm toán.

### 028. Dòng 477 — Khí tượng

**Trước:**

> | Ngày | PRCP, mm | Cờ vết giáng thủy |

**Sau:**

> | Ngày | PRCP, mm | Ký hiệu vết giáng thủy |

**Lý do:** Đồng bộ đầu câu và đầu cột.

### 029. Dòng 479 — Khí tượng

**Trước:**

> | 01/01/2023 | $0{,}3$ | Không có cờ T |

**Sau:**

> | 01/01/2023 | $0{,}3$ | Không có ký hiệu T |

**Lý do:** Đã đọc từng ngữ cảnh: cờ ở đây là dấu ghi kèm dữ liệu, không phải khái niệm toán.

### 030. Dòng 480 — Khí tượng

**Trước:**

> | 02/01/2023 | $0{,}0$ | Không có cờ T |

**Sau:**

> | 02/01/2023 | $0{,}0$ | Không có ký hiệu T |

**Lý do:** Đã đọc từng ngữ cảnh: cờ ở đây là dấu ghi kèm dữ liệu, không phải khái niệm toán.

### 031. Dòng 482 — Khí tượng

**Trước:**

> | 04/01/2023 | $0{,}5$ | Không có cờ T |

**Sau:**

> | 04/01/2023 | $0{,}5$ | Không có ký hiệu T |

**Lý do:** Đã đọc từng ngữ cảnh: cờ ở đây là dấu ghi kèm dữ liệu, không phải khái niệm toán.

### 032. Dòng 484 — Khí tượng

**Trước:**

> | 06/01/2023 | $3{,}0$ | Không có cờ T |

**Sau:**

> | 06/01/2023 | $3{,}0$ | Không có ký hiệu T |

**Lý do:** Đã đọc từng ngữ cảnh: cờ ở đây là dấu ghi kèm dữ liệu, không phải khái niệm toán.

### 033. Dòng 485 — Khí tượng

**Trước:**

> | 07/01/2023 | $7{,}1$ | Không có cờ T |

**Sau:**

> | 07/01/2023 | $7{,}1$ | Không có ký hiệu T |

**Lý do:** Đã đọc từng ngữ cảnh: cờ ở đây là dấu ghi kèm dữ liệu, không phải khái niệm toán.

### 034. Dòng 487 — Khí tượng

**Trước:**

> PRCP là lượng giáng thủy quy đổi nước. Cờ T cho biết có vết giáng thủy; số $0{,}0$ đi kèm cờ này không có nghĩa đã xác nhận hoàn toàn không có giáng thủy.

**Sau:**

> PRCP là tên cột ghi lượng giáng thủy: nước từ mưa, tuyết… được quy đổi thành lượng nước tương đương, đo bằng mm. Ký hiệu T ghi bên cạnh cho biết có một lượng giáng thủy rất nhỏ, thường gọi là **vết giáng thủy**, chưa đủ để ghi thành một số đo lớn hơn $0{,}0$ mm. Vì vậy, số $0{,}0$ kèm T không có nghĩa là hoàn toàn không có giáng thủy.

**Lý do:** Đã đọc từng ngữ cảnh: cờ ở đây là dấu ghi kèm dữ liệu, không phải khái niệm toán. Đồng bộ đầu câu và đầu cột. Giải thích tên cột, ký hiệu và vết giáng thủy trong chính đoạn học.

### 035. Dòng 489 — Khí tượng

**Trước:**

> Cả tháng có $31$ giá trị hợp lệ. Tổng các giá trị số được ghi là $78{,}5$ mm; trung bình khoảng $2{,}53$ mm/ngày, trung vị $0{,}8$ mm. Có $13$ ngày được ghi bằng $0$, trong đó $6$ ngày có cờ T. Tổng và trung bình ở đây được tính từ các giá trị đã mã hóa trong tệp, không tự bổ sung một lượng nước giả định cho các ngày có vết.

**Sau:**

> Cả tháng có $31$ giá trị hợp lệ. Tổng các giá trị số được ghi là $78{,}5$ mm; trung bình khoảng $2{,}53$ mm/ngày, trung vị $0{,}8$ mm. Có $13$ ngày được ghi bằng $0$, trong đó $6$ ngày có ký hiệu T. Tổng và trung bình ở đây được tính từ các con số được ghi trong dữ liệu, không tự bổ sung một lượng nước giả định cho các ngày có vết.

**Lý do:** Đã đọc từng ngữ cảnh: cờ ở đây là dấu ghi kèm dữ liệu, không phải khái niệm toán. Bỏ mô tả kỹ thuật về cách lưu dữ liệu.

### 036. Dòng 495 — Khí tượng

**Trước:**

> | $\{0\}$ | $13$, trong đó $6$ ngày có cờ T |

**Sau:**

> | $\{0\}$ | $13$, trong đó $6$ ngày có ký hiệu T |

**Lý do:** Đã đọc từng ngữ cảnh: cờ ở đây là dấu ghi kèm dữ liệu, không phải khái niệm toán.

### 037. Dòng 502 — Khí tượng

**Trước:**

> Đây là bảng mô tả có một lớp điểm và các khoảng không đều. Không áp dụng công thức mốt với các nhóm rộng bằng nhau của mục 4 cho bảng này. Khi cần trung vị hoặc tứ phân vị, dùng các giá trị gốc; không coi khối giá trị $0$ như phân bố đều trong một khoảng có độ rộng dương.

**Sau:**

> Bảng này để riêng các ngày có giá trị $0$ vào một hàng; những hàng còn lại dùng các khoảng có độ rộng khác nhau. Vì vậy, không áp dụng công thức mốt dành cho các nhóm rộng bằng nhau ở mục 4. Khi cần trung vị hoặc tứ phân vị, hãy tính từ các giá trị gốc; không thay các số $0$ bằng những giá trị trải đều trong một khoảng.

**Lý do:** Thay lớp điểm, khối giá trị và độ rộng dương bằng mô tả bảng cụ thể.

### 038. Dòng 505 — Khí tượng; Nguồn và chú thích

**Trước:**

> Nguồn: NOAA/NCEI, GHCN-Daily, trạm USW00024233, tháng 01/2023, biến PRCP và cờ đo kèm theo. Dữ liệu API đã được yêu cầu theo hệ mét; giá trị PRCP trong phần trích này có đơn vị mm.

**Sau:**

> Nguồn: NOAA/NCEI, GHCN-Daily, trạm USW00024233, tháng 01/2023, biến PRCP và ký hiệu đo kèm theo. Phần dữ liệu được lấy từ NCEI theo hệ mét; PRCP trong phần trích này đã có đơn vị mm.

**Lý do:** Đã đọc từng ngữ cảnh: cờ ở đây là dấu ghi kèm dữ liệu, không phải khái niệm toán. Bỏ cơ chế API khỏi lời dành cho người học, giữ đơn vị.

### 039. Dòng 530 — Luyện tập

**Trước:**

> Tự làm từng chặng trước khi mở lời giải. Phần này dùng Adélie 2008, Bike Sharing tháng 02/2012 và NOAA tháng 07/2023; các quan sát khác với phần Bài học. Trong cùng một chặng, có bài dùng lại mẫu nhỏ để chuyển biểu diễn: đó là bước học tiếp trên cùng dữ liệu, không phải một phép xác nhận mới.

**Sau:**

> Tự làm từng chặng trước khi mở lời giải. Phần này dùng Adélie 2008, Bike Sharing tháng 02/2012 và NOAA tháng 07/2023. Các dòng dữ liệu ở đây chưa được dùng trong Bài học, dù một vài con số có thể trùng nhau. Trong cùng một chặng, em có thể gặp lại một mẫu để tập chuyển từ danh sách số sang bảng nhóm. Làm tiếp trên mẫu đã gặp giúp luyện cách trình bày khác; việc đó chưa cho biết em có tự làm được với một mẫu chưa gặp hay không.

**Lý do:** Thay lời điều hành bằng hướng dẫn cụ thể; giữ điều kiện tự làm và đích quay lại.

### 040. Dòng 537 — Luyện tập; Giải thích toán

**Trước:**

> | Chuyển biểu diễn và ghép nhóm | Đếm, tích lũy, ước lượng, thay độ rộng | Nhiệm vụ 09–11; Điểm dừng 02 |

**Sau:**

> | Từ danh sách số sang bảng nhóm | Đếm số giá trị, cộng dồn tần số, tính gần đúng và thay độ rộng nhóm | Nhiệm vụ 09–11; Điểm dừng 02 |

**Lý do:** Tên chặng chỉ rõ hai cách trình bày dữ liệu. Giải thích các thao tác trong bản đồ Luyện tập.

### 041. Dòng 538 — Luyện tập

**Trước:**

> | Chọn và giải thích | Mục đích, trọng số và giới hạn dữ liệu | Nhiệm vụ 12–14; Điểm dừng 03 |

**Sau:**

> | Chọn và giải thích | Chọn số theo câu hỏi, tính trung bình các nhóm và nêu giới hạn kết luận | Nhiệm vụ 12–14; Điểm dừng 03 |

**Lý do:** Nêu việc cần luyện thay cho chuỗi thuật ngữ.

### 042. Dòng 576 — Luyện tập

**Trước:**

> | Dùng đúng cỡ mẫu và giữ đủ số quan sát | Nhiệm vụ 07a–b | Xem [đọc dữ liệu](../ban_thao/noi_dung.md#hoc-doc); nếu cần xác nhận mới, dùng Nhiệm vụ 24a hoặc 26a |

**Sau:**

> | Dùng đúng cỡ mẫu và giữ đủ số quan sát | Nhiệm vụ 07a–b | Xem [đọc dữ liệu](../ban_thao/noi_dung.md#hoc-doc); tự kiểm tra thêm bằng Nhiệm vụ 24a hoặc 26a nếu chưa làm và chưa xem lời giải |

**Lý do:** Thay lời điều hành bằng hướng dẫn cụ thể; giữ điều kiện tự làm và đích quay lại.

### 043. Dòng 577 — Luyện tập

**Trước:**

> | Sắp trước khi tìm trung vị, chọn đúng hai vị trí ở giữa | Nhiệm vụ 07b | Xem [mẫu gốc](../ban_thao/noi_dung.md#hoc-goc), rồi Nhiệm vụ 24b nếu chưa dùng |

**Sau:**

> | Sắp trước khi tìm trung vị, chọn đúng hai vị trí ở giữa | Nhiệm vụ 07b | Xem [mẫu gốc](../ban_thao/noi_dung.md#hoc-goc), rồi tự làm Nhiệm vụ 24b nếu chưa làm và chưa xem lời giải |

**Lý do:** Thay lời điều hành bằng hướng dẫn cụ thể; giữ điều kiện tự làm và đích quay lại.

### 044. Dòng 578 — Luyện tập

**Trước:**

> | Chia hai nửa đúng khi cỡ mẫu chẵn và lẻ | Nhiệm vụ 08a–b | Xem Ví dụ 01–02, rồi Nhiệm vụ 24b–c nếu chưa dùng |

**Sau:**

> | Chia hai nửa đúng khi cỡ mẫu chẵn và lẻ | Nhiệm vụ 08a–b | Xem Ví dụ 01–02, rồi tự làm Nhiệm vụ 24b–c nếu chưa làm và chưa xem lời giải |

**Lý do:** Thay lời điều hành bằng hướng dẫn cụ thể; giữ điều kiện tự làm và đích quay lại.

### 045. Dòng 579 — Luyện tập

**Trước:**

> | Nêu đúng một mốt hoặc nhiều mốt và phạm vi mẫu | Nhiệm vụ 07b–c, 08c | Đếm lại tần số; Nhiệm vụ 24b xác nhận một mốt, Nhiệm vụ 25a xác nhận nhiều mốt nếu còn mới |

**Sau:**

> | Nêu đúng một mốt hoặc nhiều mốt và phạm vi mẫu | Nhiệm vụ 07b–c, 08c | Đếm lại tần số; tự làm Nhiệm vụ 24b về một mốt hoặc 25a về nhiều mốt nếu chưa làm và chưa xem lời giải |

**Lý do:** Thay lời điều hành bằng hướng dẫn cụ thể; giữ điều kiện tự làm và đích quay lại.

### 046. Dòng 583 — Luyện tập

**Trước:**

> ### Chặng 2 — Chuyển biểu diễn và ghép nhóm

**Sau:**

> ### Chặng 2 — Từ danh sách số sang bảng nhóm

**Lý do:** Tên chặng chỉ rõ hai cách trình bày dữ liệu.

### 047. Dòng 650 — Luyện tập; Giải thích toán

**Trước:**

> #### Điểm dừng 02 — Kiểm đường đi từ dữ liệu đến ước lượng

**Sau:**

> #### Điểm dừng 02 — Kiểm lại cách lập bảng và tính gần đúng

**Lý do:** Tên mục hỏi trực tiếp việc người học vừa làm. Tránh lặp từ, giữ câu chỉ việc cần kiểm.

### 048. Dòng 654 — Luyện tập

**Trước:**

> | Không bỏ sót hoặc đếm hai lần ở biên | Nhiệm vụ 09a–b | Xem [ghép nhóm](../ban_thao/noi_dung.md#hoc-ghep); Nhiệm vụ 25a nếu còn mới |

**Sau:**

> | Không bỏ sót hoặc đếm hai lần ở biên | Nhiệm vụ 09a–b | Xem [ghép nhóm](../ban_thao/noi_dung.md#hoc-ghep); tự làm Nhiệm vụ 25a nếu chưa làm và chưa xem lời giải |

**Lý do:** Thay lời điều hành bằng hướng dẫn cụ thể; giữ điều kiện tự làm và đích quay lại.

### 049. Dòng 655 — Luyện tập

**Trước:**

> | Dùng trọng số và chia cho đúng tổng tần số | Nhiệm vụ 10a | Xem Ví dụ 04; Nhiệm vụ 25c nếu còn mới |

**Sau:**

> | Nhân từng trung điểm với tần số rồi chia tổng các tích cho tổng tần số | Nhiệm vụ 10a | Xem Ví dụ 04; tự làm Nhiệm vụ 25c nếu chưa làm và chưa xem lời giải |

**Lý do:** Mô tả phép tính trọng số. Thay lời điều hành bằng hướng dẫn cụ thể; giữ điều kiện tự làm và đích quay lại.

### 050. Dòng 656 — Luyện tập

**Trước:**

> | Chọn đúng nhóm, đúng $F$, đúng $f$ | Nhiệm vụ 10b | Xem Ví dụ 05; Nhiệm vụ 25c nếu còn mới |

**Sau:**

> | Chọn đúng nhóm, đúng $F$, đúng $f$ | Nhiệm vụ 10b | Xem Ví dụ 05; tự làm Nhiệm vụ 25c nếu chưa làm và chưa xem lời giải |

**Lý do:** Thay lời điều hành bằng hướng dẫn cụ thể; giữ điều kiện tự làm và đích quay lại.

### 051. Dòng 657 — Luyện tập

**Trước:**

> | Dùng mốt trong điều kiện nhóm rộng bằng nhau | Nhiệm vụ 10c | Xem Ví dụ 06; Nhiệm vụ 25d nếu còn mới |

**Sau:**

> | Dùng mốt trong điều kiện nhóm rộng bằng nhau | Nhiệm vụ 10c | Xem Ví dụ 06; tự làm Nhiệm vụ 25d nếu chưa làm và chưa xem lời giải |

**Lý do:** Thay lời điều hành bằng hướng dẫn cụ thể; giữ điều kiện tự làm và đích quay lại.

### 052. Dòng 660 — Luyện tập

**Trước:**

> Nếu còn một phép tính sai, sửa đúng phép tính đó và kiểm xem nó có làm đổi kết luận không. Nếu đã xem lời giải trước khi tự làm, chưa dùng bài ấy làm bằng chứng độc lập.

**Sau:**

> Nếu còn một phép tính sai, sửa đúng phép tính đó và kiểm xem nó có làm đổi kết luận không. Nếu đã xem lời giải, bài làm sau đó giúp em luyện lại cách giải, nhưng chưa cho biết em có tự giải được khi không có hướng dẫn hay không.

**Lý do:** Thay lời điều hành bằng hướng dẫn cụ thể; giữ điều kiện tự làm và đích quay lại.

### 053. Dòng 670 — Luyện tập

**Trước:**

> a) Tính số trung bình. Nếu báo cáo cần một số để phân bổ tổng lượt thuê của tháng theo ngày, em chọn số nào?

**Sau:**

> a) Tính số trung bình. Nếu báo cáo cần cho biết tổng lượt thuê trong tháng chia đều cho mỗi ngày là bao nhiêu, em chọn số nào?

**Lý do:** Nói rõ mục đích của số trung bình.

### 054. Dòng 701 — Khí tượng

**Trước:**

> Tại trạm Seattle–Tacoma, tháng 07/2023 có $31$ giá trị PRCP hợp lệ: $30$ ngày ghi $0$ mm, ngày 24/07 ghi $2{,}3$ mm. Không ngày nào trong phần trích có cờ T.

**Sau:**

> Tại trạm Seattle–Tacoma, tháng 07/2023 có $31$ giá trị PRCP hợp lệ: $30$ ngày ghi $0$ mm, ngày 24/07 ghi $2{,}3$ mm. Không ngày nào trong phần trích có ký hiệu T.

**Lý do:** Đã đọc từng ngữ cảnh: cờ ở đây là dấu ghi kèm dữ liệu, không phải khái niệm toán.

### 055. Dòng 715 — Luyện tập

**Trước:**

> Đối chiếu Nhiệm vụ 12a–b: lý do chọn số phải gắn với tổng hoặc vị trí giữa, không chỉ nói “số này tốt hơn”. Ở Nhiệm vụ 13, cần giữ trọng số và không chuyển quan hệ quan sát được thành nguyên nhân. Ở Nhiệm vụ 14, cần phân biệt trung vị, tổng và tần số của số $0$.

**Sau:**

> Đối chiếu Nhiệm vụ 12a–b: lý do chọn số phải gắn với tổng hoặc vị trí giữa, không chỉ nói “số này tốt hơn”. Ở Nhiệm vụ 13, cần tính trung bình theo đúng số ngày của mỗi nhóm. Số liệu cho thấy hai nhóm khác nhau, nhưng chưa giải thích được nguyên nhân của sự khác nhau ấy. Ở Nhiệm vụ 14, cần phân biệt trung vị, tổng và tần số của số $0$.

**Lý do:** Làm rõ trọng số và giới hạn suy luận.

### 056. Dòng 717 — Khí tượng; Luyện tập

**Trước:**

> Nếu còn vướng, xem [chọn số đại diện](../ban_thao/noi_dung.md#hoc-chon). Nhiệm vụ 26 hỗ trợ kiểm lại trung bình có trọng số và giới hạn mẫu; Nhiệm vụ 27 kiểm cách đọc số $0$ và cờ T. Chỉ làm các ý đúng với điều cần sửa và còn chưa dùng. Khi đã sẵn sàng, em có thể thực hiện Kiểm tra.

**Sau:**

> Nếu còn vướng, xem [chọn số đại diện](../ban_thao/noi_dung.md#hoc-chon). Nhiệm vụ 26 giúp em tự kiểm tra cách tính trung bình khi gộp hai nhóm và cách kết luận đúng với phần dữ liệu đã xét; Nhiệm vụ 27 giúp kiểm cách đọc số $0$ và ký hiệu T. Chọn ý đúng với điều cần sửa, chưa làm và chưa xem lời giải. Khi đã sẵn sàng, em có thể thực hiện Kiểm tra.

**Lý do:** Đã đọc từng ngữ cảnh: cờ ở đây là dấu ghi kèm dữ liệu, không phải khái niệm toán. Thay lời điều hành bằng hướng dẫn cụ thể; giữ điều kiện tự làm và đích quay lại.

### 057. Dòng 779 — Kiểm tra

**Trước:**

> a) Tính trung bình và chọn số để mô tả tổng lượt thuê phân bổ theo ngày.

**Sau:**

> a) Tính trung bình và chọn số cho biết tổng lượt thuê trong tháng chia đều cho mỗi ngày là bao nhiêu.

**Lý do:** Giữ yêu cầu chọn số, làm rõ ý chia đều.

### 058. Dòng 783 — Kiểm tra

**Trước:**

> c) Xác định tình trạng mốt và nêu một kết luận mà dữ liệu này chưa cho phép về người sử dụng hoặc tương lai.

**Sau:**

> c) Cho biết mẫu có mốt hay không và nêu một kết luận mà dữ liệu này chưa cho phép về người sử dụng hoặc tương lai.

**Lý do:** Bỏ cách nói hành chính tình trạng.

### 059. Dòng 791 — Khí tượng

**Trước:**

> Tháng 11/2023 tại trạm Seattle–Tacoma có $30$ giá trị PRCP hợp lệ, tổng các giá trị số là $147$ mm. Có $15$ giá trị bằng $0$; trong số đó, ngày 07/11 có cờ T. Giá trị dương nhỏ nhất là $1{,}3$ mm.

**Sau:**

> Tháng 11/2023 tại trạm Seattle–Tacoma có $30$ giá trị PRCP hợp lệ, tổng các giá trị số là $147$ mm. Có $15$ giá trị bằng $0$; trong số đó, ngày 07/11 có ký hiệu T. Giá trị dương nhỏ nhất là $1{,}3$ mm.

**Lý do:** Đã đọc từng ngữ cảnh: cờ ở đây là dấu ghi kèm dữ liệu, không phải khái niệm toán.

### 060. Dòng 809 — Kiểm tra

**Trước:**

> | Đọc đúng mẫu | Nhiệm vụ 15a, 16a, 18 | Đúng đối tượng, biến, đơn vị, cỡ mẫu; phân biệt bản ghi với giá trị |

**Sau:**

> | Đọc đúng mẫu | Nhiệm vụ 15a, 16a, 18 | Nêu đúng đối tượng, đại lượng và đơn vị đo; đếm đúng số giá trị dùng để tính |

**Lý do:** Giữ tiêu chí đọc dữ liệu, diễn đạt bằng thao tác.

### 061. Dòng 811 — Kiểm tra

**Trước:**

> | Ghép nhóm | Nhiệm vụ 15c, 16a và 16d | Đúng đầu mút, đủ tần số, giữ nhóm rỗng và tích lũy đúng |

**Sau:**

> | Ghép nhóm | Nhiệm vụ 15c, 16a và 16d | Xếp mỗi giá trị vào đúng một nhóm; đếm đủ, giữ nhóm có tần số bằng không và cộng dồn đúng |

**Lý do:** Làm rõ nhóm rỗng và tích lũy.

### 062. Dòng 812 — Kiểm tra

**Trước:**

> | Ước lượng từ bảng | Nhiệm vụ 16a–c | Trung điểm có trọng số; chọn đúng nhóm, $F,f,h$; mốt áp dụng đúng điều kiện |

**Sau:**

> | Ước lượng từ bảng | Nhiệm vụ 16a–c | Nhân trung điểm với tần số; chọn đúng nhóm, $F,f,h$; dùng công thức mốt đúng điều kiện |

**Lý do:** Làm rõ trọng số, giữ ký hiệu toán.

### 063. Dòng 814 — Khí tượng

**Trước:**

> | Giới hạn kết luận | Nhiệm vụ 16d, 17c, 18b–c | Không gọi ước lượng là số gốc; giữ ý nghĩa lượt thuê, cờ T và phạm vi thời gian |

**Sau:**

> | Giới hạn kết luận | Nhiệm vụ 16d, 17c, 18b–c | Không gọi ước lượng là số gốc; giữ ý nghĩa lượt thuê, ký hiệu T và phạm vi thời gian |

**Lý do:** Đã đọc từng ngữ cảnh: cờ ở đây là dấu ghi kèm dữ liệu, không phải khái niệm toán.

### 064. Dòng 816 — Kiểm tra

**Trước:**

> Lượt này trực tiếp kiểm tứ phân vị trên mẫu gốc chẵn, chưa kiểm lại trường hợp lẻ. Bằng chứng về trường hợp lẻ ở Nhiệm vụ 08b, nhiều mốt ở Nhiệm vụ 07c và Ôn lại, dữ liệu thiếu ở Nhiệm vụ 02 được ghi đúng mức hỗ trợ, không tự nhập thành kết quả độc lập của Kiểm tra.

**Sau:**

> Bài Kiểm tra này hỏi tứ phân vị khi mẫu gốc có số giá trị chẵn, chưa hỏi lại trường hợp lẻ. Em đã gặp trường hợp lẻ ở Nhiệm vụ 08b, nhiều mốt ở Nhiệm vụ 07c và sẽ gặp lại khi Ôn lại; dữ liệu thiếu đã được học ở Nhiệm vụ 02. Khi ghi kết quả của những bài ấy, hãy nói rõ em đã tự làm hay cần xem hướng dẫn. Kết quả của chúng được giữ riêng với bài Kiểm tra này.

**Lý do:** Thay lời điều hành bằng hướng dẫn cụ thể; giữ điều kiện tự làm và đích quay lại.

### 065. Dòng 818 — Kiểm tra

**Trước:**

> Nếu cần sửa, dùng [bảng Sửa lỗi](../ban_thao/noi_dung.md#sua-loi) để chọn đúng ý. Nhiệm vụ 24–27 chỉ xác nhận những thao tác được hỏi, không thay toàn bộ lượt Kiểm tra. Nếu bài xác nhận phù hợp đã dùng, ghi nội dung chưa được xác nhận bằng bài mới; không lấy đề ôn tương lai để lấp chỗ trống.

**Sau:**

> Nếu cần sửa, dùng [bảng Sửa lỗi](../ban_thao/noi_dung.md#sua-loi) để chọn đúng ý. Nhiệm vụ 24–27 giúp em tự kiểm tra từng chỗ còn vướng; làm đúng một ý chưa có nghĩa là đã làm được toàn bộ bài Kiểm tra. Nếu ý phù hợp đã được làm hoặc xem lời giải, ghi lại chỗ còn cần tự kiểm tra bằng bài khác. Giữ các bài Ôn lại cho đúng ngày đã hẹn.

**Lý do:** Thay lời điều hành bằng hướng dẫn cụ thể; giữ điều kiện tự làm và đích quay lại.

### 066. Dòng 852 — Ôn lại

**Trước:**

> Đối chiếu việc sắp thứ tự, vị trí và tần số. Lượt này kiểm đọc mẫu, các số đặc trưng mẫu gốc và trường hợp nhiều mốt; chưa kiểm công thức ghép nhóm. Nếu còn nhầm, xem mục 2; Nhiệm vụ 24 hoặc 25a chỉ dùng khi đúng thao tác cần xác nhận và còn mới. Ghi ngày thực hiện rồi tiếp tục lịch ôn đã hẹn.

**Sau:**

> Đối chiếu việc sắp thứ tự, vị trí và tần số. Lượt này giúp em biết còn nhớ cách đọc mẫu, tính các số đặc trưng từ dữ liệu gốc và tìm nhiều mốt hay không; chưa hỏi công thức ghép nhóm. Nếu còn nhầm, xem mục 2, rồi chọn ý phù hợp trong Nhiệm vụ 24 hoặc 25a để tự làm, với điều kiện chưa làm và chưa xem lời giải. Ghi ngày thực hiện rồi tiếp tục lịch ôn đã hẹn.

**Lý do:** Thay lời điều hành bằng hướng dẫn cụ thể; giữ điều kiện tự làm và đích quay lại.

### 067. Dòng 871 — Giải thích toán

**Trước:**

> a) Xác định cỡ mẫu, lập tích lũy và tính trung bình của mẫu ghép nhóm.

**Sau:**

> a) Xác định cỡ mẫu, lập tần số tích lũy và tính trung bình của mẫu ghép nhóm.

**Lý do:** Không dùng tên viết tắt chưa rõ đối tượng.

### 068. Dòng 883 — Ôn lại

**Trước:**

> Kiểm riêng trung điểm có trọng số, nhóm nội suy, tần số trước nhóm và điều kiện công thức mốt. Nếu đúng số nhưng chưa giải thích được $F$, xem mục 4 rồi dùng đúng ý của Nhiệm vụ 25 nếu còn mới. Lượt này không kiểm lại toàn bộ cách chọn số đại diện trong bối cảnh lượt thuê hoặc khí tượng.

**Sau:**

> Kiểm lại phép nhân từng trung điểm với tần số, cách chọn nhóm để nội suy, tần số tích lũy trước nhóm và điều kiện dùng công thức mốt. Nếu đúng số nhưng chưa giải thích được $F$, xem mục 4 rồi tự làm ý phù hợp của Nhiệm vụ 25 nếu chưa làm và chưa xem lời giải. Lượt này không hỏi lại toàn bộ cách chọn số đại diện trong dữ liệu lượt thuê xe hoặc khí tượng.

**Lý do:** Thay lời điều hành bằng hướng dẫn cụ thể; giữ điều kiện tự làm và đích quay lại.

### 069. Dòng 899 — Ôn lại

**Trước:**

> c) Nêu hai nhóm đông nhất. Có đủ căn cứ để khẳng định một nhóm chứa mốt duy nhất không? Không cần nội suy mốt trong trường hợp đồng hạng này.

**Sau:**

> c) Nêu hai nhóm đông nhất. Có đủ căn cứ để khẳng định một nhóm chứa mốt duy nhất không? Không cần nội suy mốt khi hai nhóm cùng có tần số lớn nhất.

**Lý do:** Thay đồng hạng bằng tình huống thống kê cụ thể.

### 070. Dòng 909 — Ôn lại

**Trước:**

> Đối chiếu tính toán, lý do chọn trung vị, cách xử lí đồng hạng và phạm vi kết luận. Lượt này kiểm một phần các mục tiêu về mẫu gốc, lựa chọn và giới hạn; không chứng nhận mọi tình huống của chủ đề. Nếu vừa phải sửa một nội dung, ghi ngày kiểm lại gần hơn cho nội dung ấy, giữ nguyên lịch sử lần ôn này.

**Sau:**

> Đối chiếu phép tính, lý do chọn trung vị, cách nhận ra các giá trị hoặc nhóm cùng có tần số lớn nhất và phạm vi kết luận. Làm đúng lượt này cho thấy em làm được những việc vừa hỏi; các tình huống khác của chủ đề vẫn cần được luyện thêm. Nếu vừa phải sửa một nội dung, hẹn tự kiểm tra lại nội dung ấy sớm hơn; vẫn giữ ngày và bài làm của lần ôn này.

**Lý do:** Thay lời điều hành bằng hướng dẫn cụ thể; giữ điều kiện tự làm và đích quay lại.

### 071. Dòng 917 — Ôn nền

**Trước:**

> Chỉ mở phần phù hợp với thao tác còn vướng. Các dãy số ngắn trong mục này là ví dụ số học được tạo để giải thích, không phải dữ liệu thực địa.

**Sau:**

> Chỉ mở phần phù hợp với thao tác còn vướng. Các dãy số ngắn trong mục này là ví dụ số học được tạo để giải thích, không phải số liệu thu thập ngoài thực tế.

**Lý do:** Giải thích nguồn của các ví dụ số học.

### 072. Dòng 929 — Ôn nền

**Trước:**

> #### Nhiệm vụ 22 — Xác nhận phép tính nền

**Sau:**

> #### Nhiệm vụ 22 — Tự kiểm tra phép tính cơ bản

**Lý do:** Đổi tên ở cả đề và lời giải, giữ số nhiệm vụ.

### 073. Dòng 941 — Ôn nền

**Trước:**

> **Tiêu chí và nơi trở lại.** Cần chia đúng số giá trị, giữ đúng mẫu số của tỉ lệ và phân biệt thiếu với $0$. Nếu đáp ứng, trở lại ý đã gọi hỗ trợ ở Nhiệm vụ 01 hoặc bài đang làm. Đây là xác nhận thao tác nền, chưa xác nhận khả năng tính mọi số đặc trưng của gói.

**Sau:**

> **Đọc kết quả và học tiếp.** Kiểm lại xem em đã chia cho đúng số giá trị, tính tỉ lệ với đúng mẫu số và phân biệt ô thiếu với $0$ chưa. Nếu đã làm đúng, trở lại ý còn vướng ở Nhiệm vụ 01 hoặc bài đang làm. Bài ngắn này chỉ hỏi những phép tính cơ bản vừa ôn; các số đặc trưng khác còn cần tự kiểm tra ở bài tương ứng.

**Lý do:** Viết rõ việc cần làm, giữ phạm vi tự kiểm tra và nơi quay lại.

### 074. Dòng 953 — Ôn nền

**Trước:**

> #### Nhiệm vụ 23 — Xác nhận đọc khoảng

**Sau:**

> #### Nhiệm vụ 23 — Tự kiểm tra cách đọc khoảng

**Lý do:** Đổi tên ở cả đề và lời giải, giữ số nhiệm vụ.

### 075. Dòng 963 — Ôn nền

**Trước:**

> **Tiêu chí và nơi trở lại.** Phải giữ cả hai giá trị $15$, không đếm chúng vào khoảng trước, tổng tần số bằng số phần tử ban đầu. Sau đó trở về ý đang vướng ở Nhiệm vụ 01, 09 hoặc hoạt động đã gọi hỗ trợ.

**Sau:**

> **Đọc kết quả và học tiếp.** Kiểm lại xem em đã giữ cả hai giá trị $15$, xếp chúng vào đúng khoảng và có tổng tần số bằng số phần tử ban đầu chưa. Sau đó trở về ý đang vướng ở Nhiệm vụ 01, 09 hoặc bài em đang làm.

**Lý do:** Viết rõ việc cần làm, giữ phạm vi tự kiểm tra và nơi quay lại.

### 076. Dòng 969 — Sửa lỗi

**Trước:**

> Trước hết giữ bài đã làm và xác định bước còn vướng. Dùng giải thích hoặc ví dụ của đúng mục để hiểu lại, rồi chọn ý xác nhận phù hợp bên dưới. Các dữ liệu Gentoo 2008–2009 và NOAA tháng 02/2023 chỉ dành cho phần hỗ trợ này.

**Sau:**

> Trước hết giữ bài đã làm và tìm bước em còn vướng. Đọc lại giải thích hoặc ví dụ của đúng mục, rồi chọn một ý bên dưới hỏi đúng việc ấy để tự làm. Chọn ý em chưa làm và chưa xem lời giải; như vậy, kết quả mới cho biết em có tự giải được sau khi ôn hay không. Các dữ liệu Gentoo 2008–2009 và NOAA tháng 02/2023 được dành riêng cho phần Sửa lỗi.

**Lý do:** Viết rõ việc cần làm, giữ phạm vi tự kiểm tra và nơi quay lại.

### 077. Dòng 971 — Sửa lỗi

**Trước:**

> Một bài đã xem đáp án hoặc đã làm trước đó không trở thành bài mới khi đổi tên hay đổi thứ tự. Ngay cả khi gặp lại bài ở một Điểm dừng khác, em vẫn cần ghi đã dùng. Nếu không còn ý mới phù hợp, ghi “chưa có bài mới để xác nhận nội dung này”, tiếp tục học đúng phần còn vướng và những phần độc lập đã đủ điều kiện; không dùng sớm đề của lượt Ôn lại sau.

**Sau:**

> Nếu một Điểm dừng khác dẫn đến bài em đã làm hoặc đã xem lời giải, hãy ghi rõ điều đó. Em vẫn có thể làm lại để luyện, nhưng kết quả chưa cho biết em có tự giải được một bài chưa gặp hay không. Nếu không còn bài phù hợp, ghi “cần một bài khác để tự kiểm tra phần này”, tiếp tục ôn chỗ còn vướng. Em có thể học tiếp những phần không cần đến kiến thức ấy và đã có đủ kiến thức để học. Giữ các bài Ôn lại cho đúng ngày đã hẹn.

**Lý do:** Viết rõ việc cần làm, giữ phạm vi tự kiểm tra và nơi quay lại.

### 078. Dòng 975 — Sửa lỗi

**Trước:**

> | Bản ghi và giá trị dùng được | Chia cho số dòng kể cả ô thiếu; thay thiếu bằng $0$ | Ô đó có thực sự chứa phép đo không? Xem [đọc dữ liệu](../ban_thao/noi_dung.md#hoc-doc), tách số dòng và số giá trị hợp lệ | Nhiệm vụ 26a |

**Sau:**

> | Số dòng và số giá trị dùng được | Chia cho số dòng kể cả ô thiếu; thay thiếu bằng $0$ | Ô đó có thực sự chứa phép đo không? Xem [đọc dữ liệu](../ban_thao/noi_dung.md#hoc-doc), tách số dòng và số giá trị hợp lệ | Nhiệm vụ 26a |

**Lý do:** Phân biệt bằng những gì thấy trong bảng.

### 079. Dòng 982 — Sửa lỗi

**Trước:**

> | Điều kiện công thức mốt ghép nhóm | Thay số dù độ rộng khác nhau hoặc đồng hạng mà kết luận duy nhất | Có một nhóm cao nhất rõ ràng và các nhóm rộng bằng nhau không? Xem Ví dụ 06 | Nhiệm vụ 25d; bài này chỉ xác nhận trường hợp một nhóm cao nhất |

**Sau:**

> | Điều kiện công thức mốt ghép nhóm | Dùng công thức khi các nhóm rộng khác nhau; thấy nhiều nhóm có cùng tần số lớn nhất nhưng vẫn kết luận chỉ có một mốt | Có đúng một nhóm có tần số lớn nhất và các nhóm rộng bằng nhau không? Xem Ví dụ 06 | Nhiệm vụ 25d; bài này chỉ hỏi trường hợp có đúng một nhóm có tần số lớn nhất |

**Lý do:** Làm rõ biểu hiện dễ nhầm. Đổi cao nhất thành tần số lớn nhất. Viết rõ việc cần làm, giữ phạm vi tự kiểm tra và nơi quay lại.

### 080. Dòng 983 — Sửa lỗi

**Trước:**

> | Trọng số khi gộp nhóm | Lấy trung bình cộng của hai trung bình có cỡ mẫu khác nhau | Hai nhóm có bao nhiêu giá trị hợp lệ? Xem Ví dụ 07 | Nhiệm vụ 26b |

**Sau:**

> | Số giá trị của từng nhóm khi tính trung bình chung | Lấy trung bình cộng của hai trung bình có cỡ mẫu khác nhau | Hai nhóm có bao nhiêu giá trị hợp lệ? Xem Ví dụ 07 | Nhiệm vụ 26b |

**Lý do:** Nêu ý nghĩa trọng số trong dòng hướng dẫn.

### 081. Dòng 984 — Khí tượng; Sửa lỗi

**Trước:**

> | Số 0 và cờ đo | Đồng nhất số $0$ với không có hiện tượng; đồng nhất trung vị với tổng | Tệp đang ghi gì, cờ bổ sung điều gì? Xem Ví dụ 09 | Nhiệm vụ 27 |

**Sau:**

> | Số 0 và ký hiệu ghi kèm | Đồng nhất số $0$ với không có hiện tượng; đồng nhất trung vị với tổng | Con số đang ghi là gì, ký hiệu bên cạnh cho biết thêm điều gì? Xem Ví dụ 09 | Nhiệm vụ 27 |

**Lý do:** Đã đọc từng ngữ cảnh: cờ ở đây là dấu ghi kèm dữ liệu, không phải khái niệm toán. Nêu rõ ký hiệu đi kèm số đo. Không bắt người học nghĩ theo cấu trúc tệp.

### 082. Dòng 987 — Sửa lỗi

**Trước:**

> Các bài sau dùng chung cho nhu cầu phát hiện sau Bài học, Luyện tập, Kiểm tra đã kết thúc hoặc Ôn lại. Chọn đúng ý còn mới; không phải làm toàn bộ mỗi khi có một lỗi.

**Sau:**

> Em có thể dùng các bài sau khi gặp khó ở Bài học, Luyện tập, sau khi kết thúc Kiểm tra hoặc khi Ôn lại. Chỉ chọn ý đúng với chỗ cần sửa theo hướng dẫn trên; không cần làm toàn bộ.

**Lý do:** Viết rõ việc cần làm, giữ phạm vi tự kiểm tra và nơi quay lại.

### 083. Dòng 991 — Sửa lỗi

**Trước:**

> ### Nhiệm vụ 24 — Xác nhận trên mẫu Gentoo nhỏ

**Sau:**

> ### Nhiệm vụ 24 — Tự làm với mẫu Gentoo nhỏ

**Lý do:** Đổi tên ở cả đề và lời giải.

### 084. Dòng 993 — Sửa lỗi

**Trước:**

> Mười hai giá trị chiều dài chân chèo trong phần dự phòng Gentoo 2008, đơn vị mm:

**Sau:**

> Mười hai giá trị chiều dài chân chèo trong phần dữ liệu Gentoo 2008 dành cho Sửa lỗi, đơn vị mm:

**Lý do:** Giải thích dự phòng là dành cho hoạt động nào.

### 085. Dòng 1005 — Sửa lỗi

**Trước:**

> **Đọc kết quả.** Chỉ ghi đã sửa những thao tác em tự làm đúng ở các ý được chọn. Trở về đúng Điểm dừng 01, 04, 05 hoặc nhiệm vụ đã gọi hỗ trợ. Nếu bài này đã được dùng, không tính lại là xác nhận mới.

**Sau:**

> **Đọc kết quả.** Ghi rõ những ý em đã tự làm đúng và những ý còn cần giúp đỡ. Trở về Điểm dừng 01, 04, 05 hoặc bài em đang làm trước khi mở Sửa lỗi. Nếu đã làm bài này hoặc xem lời giải từ trước, ghi đây là lần luyện lại.

**Lý do:** Viết rõ việc cần làm, giữ phạm vi tự kiểm tra và nơi quay lại.

### 086. Dòng 1009 — Sửa lỗi

**Trước:**

> ### Nhiệm vụ 25 — Xác nhận ghép nhóm và nội suy

**Sau:**

> ### Nhiệm vụ 25 — Tự kiểm tra ghép nhóm và nội suy

**Lý do:** Đổi tên ở cả đề và lời giải.

### 087. Dòng 1037 — Sửa lỗi

**Trước:**

> **Đọc kết quả.** Ý a kiểm lập bảng và nhiều mốt trên mẫu gốc; ý b kiểm trung điểm; ý c kiểm trọng số và nội suy; ý d kiểm mốt ghép nhóm. Kết quả đúng một ý không tự xác nhận các ý còn lại. Trở về Điểm dừng 02, 04, 05, 06 hoặc nơi đã gọi hỗ trợ.

**Sau:**

> **Đọc kết quả.** Ý a hỏi cách lập bảng và tìm nhiều mốt của mẫu gốc; ý b hỏi trung điểm; ý c hỏi cách tính trung bình theo tần số và nội suy; ý d hỏi mốt ghép nhóm. Làm đúng một ý chưa cho biết em đã làm được các ý còn lại. Trở về Điểm dừng 02, 04, 05, 06 hoặc bài em đang làm trước khi mở Sửa lỗi.

**Lý do:** Viết rõ việc cần làm, giữ phạm vi tự kiểm tra và nơi quay lại.

### 088. Dòng 1041 — Sửa lỗi

**Trước:**

> ### Nhiệm vụ 26 — Xác nhận dữ liệu thiếu, trọng số và phạm vi

**Sau:**

> ### Nhiệm vụ 26 — Đếm giá trị, tính trung bình và giới hạn kết luận

**Lý do:** Đổi tên ở cả đề và lời giải.

### 089. Dòng 1043 — Đọc dữ liệu

**Trước:**

> Phần Gentoo 2009 được chia theo thứ tự bản ghi thành hai phần:

**Sau:**

> Phần dữ liệu Gentoo 2009 được chia theo thứ tự dòng trong bảng gốc thành hai phần:

**Lý do:** Chỉ rõ thứ tự chia dữ liệu.

### 090. Dòng 1045 — Đọc dữ liệu

**Trước:**

> | Phần | Số bản ghi | Số chiều dài hợp lệ | Tổng chiều dài hợp lệ, mm |

**Sau:**

> | Phần | Số dòng | Số chiều dài hợp lệ | Tổng chiều dài hợp lệ, mm |

**Lý do:** Thay thuật ngữ trong bảng bằng đối tượng cụ thể.

### 091. Dòng 1047 — Đọc dữ liệu

**Trước:**

> | 20 bản ghi đầu | $20$ | $20$ | $4375$ |

**Sau:**

> | 20 dòng đầu | $20$ | $20$ | $4375$ |

**Lý do:** Nêu rõ số dòng của bảng.

### 092. Dòng 1048 — Đọc dữ liệu

**Trước:**

> | 24 bản ghi còn lại | $24$ | $23$ | $5017$ |

**Sau:**

> | 24 dòng còn lại | $24$ | $23$ | $5017$ |

**Lý do:** Nêu rõ số dòng của bảng.

### 093. Dòng 1050 — Đọc dữ liệu

**Trước:**

> a) Toàn bộ phần trích có bao nhiêu bản ghi và bao nhiêu giá trị dùng được? Một ô thiếu có được coi là chiều dài $0$ mm không?

**Sau:**

> a) Toàn bộ phần trích có bao nhiêu dòng và bao nhiêu số đo chiều dài dùng được? Một ô thiếu có được coi là chiều dài $0$ mm không?

**Lý do:** Giữ phân biệt dòng với số đo dùng được.

### 094. Dòng 1052 — Sửa lỗi

**Trước:**

> b) Tính trung bình mỗi phần và trung bình chung. Nêu trọng số đúng; giữ đủ chữ số trung gian.

**Sau:**

> b) Tính trung bình mỗi phần và trung bình chung. Nêu số giá trị dùng để tính ở mỗi phần; giữ đủ chữ số trung gian.

**Lý do:** Hỏi ý nghĩa trọng số bằng thao tác.

### 095. Dòng 1060 — Sửa lỗi

**Trước:**

> **Đọc kết quả.** Ý a xác nhận xử lí thiếu, ý b xác nhận trọng số, ý c xác nhận phạm vi và ý d xác nhận trường hợp không có mốt. Trở về Điểm dừng 01, 03, 04, 07 hoặc nhiệm vụ đã gọi hỗ trợ. Bốn giá trị ở ý d được chọn để kiểm một quy tắc, không được mô tả là một mẫu ngẫu nhiên đại diện cho loài.

**Sau:**

> **Đọc kết quả.** Ý a hỏi cách đếm khi có ô thiếu; ý b hỏi cách tính trung bình chung; ý c hỏi có thể kết luận về những cá thể nào; ý d hỏi trường hợp không có mốt. Trở về Điểm dừng 01, 03, 04, 07 hoặc bài em đang làm trước khi mở Sửa lỗi. Bốn giá trị ở ý d được chọn để luyện quy tắc tìm mốt, không được chọn ngẫu nhiên để đại diện cho cả loài.

**Lý do:** Viết rõ việc cần làm, giữ phạm vi tự kiểm tra và nơi quay lại.

### 096. Dòng 1064 — Khí tượng; Sửa lỗi

**Trước:**

> ### Nhiệm vụ 27 — Xác nhận cách đọc cờ T

**Sau:**

> ### Nhiệm vụ 27 — Đọc ký hiệu T

**Lý do:** Đã đọc từng ngữ cảnh: cờ ở đây là dấu ghi kèm dữ liệu, không phải khái niệm toán. Đổi tên ở cả đề và lời giải.

### 097. Dòng 1068 — Khí tượng

**Trước:**

> | Ngày | PRCP, mm | Cờ T |

**Sau:**

> | Ngày | PRCP, mm | Ký hiệu T |

**Lý do:** Đồng bộ đầu câu và đầu cột.

### 098. Dòng 1082 — Khí tượng; Sửa lỗi

**Trước:**

> **Đọc kết quả.** Cần phân biệt dữ liệu số với cờ đo, trung vị với tổng và ba ngày với cả năm. Trở về Điểm dừng 03, 04 hoặc nơi đã gọi hỗ trợ. Bài này không kiểm lại toàn bộ nội dung về thống kê ghép nhóm.

**Sau:**

> **Đọc kết quả.** Cần đọc cả con số và ký hiệu ghi kèm, phân biệt trung vị với tổng, giới hạn kết luận trong ba ngày đã xét. Trở về Điểm dừng 03, 04 hoặc bài em đang làm trước khi mở Sửa lỗi. Bài này không hỏi lại toàn bộ nội dung về thống kê ghép nhóm.

**Lý do:** Đã đọc từng ngữ cảnh: cờ ở đây là dấu ghi kèm dữ liệu, không phải khái niệm toán. Viết rõ việc cần làm, giữ phạm vi tự kiểm tra và nơi quay lại.

### 099. Dòng 1088 — Nhật kí

**Trước:**

> [Mở mẫu Nhật kí học tập dùng chung, đủ 14 trường](../../../_dung_chung/nhat_ki_hoc_tap.qmd).

**Sau:**

> [Mở mẫu Nhật kí học tập dùng chung, gồm 14 mục cần ghi](../../../_dung_chung/nhat_ki_hoc_tap.qmd).

**Lý do:** Giải thích trường của biểu mẫu.

### 100. Dòng 1090 — Nhật kí

**Trước:**

> Ghi khi cần lưu một quyết định, nơi tiếp tục hoặc khi kết thúc buổi học. Chỉ điền thông tin đã có. Giữ bài làm ban đầu, mức hỗ trợ, việc đã sửa và kết quả sau khoảng trễ thành các thông tin riêng. Không bắt buộc ghi sau mọi câu.

**Sau:**

> Ghi khi cần lưu một quyết định, nơi tiếp tục hoặc khi kết thúc buổi học. Chỉ điền thông tin đã có. Ghi riêng bài làm ban đầu, hướng dẫn hoặc giúp đỡ đã nhận, chỗ đã sửa và kết quả tự làm khi ôn lại sau một thời gian. Không bắt buộc ghi sau mọi câu.

**Lý do:** Thay mức hỗ trợ và khoảng trễ bằng sự việc cụ thể.

### 101. Dòng 1092 — Nhật kí

**Trước:**

> Trong trường “Bài khắc phục mới”, ghi đúng tên nhiệm vụ và ý đã dùng; nếu đã xem trước lời giải, ghi rõ điều đó. Mẫu chung có ví dụ giả lập thuộc một gói khác để minh họa cách ghi; em không phải làm thêm bài trong ví dụ ấy.

**Sau:**

> Ở mục “Bài khắc phục mới”, ghi đúng tên nhiệm vụ và ý đã dùng; nếu đã xem trước lời giải, ghi rõ điều đó. Mẫu chung có ví dụ về một tình huống học được đặt ra ở gói khác để minh họa cách ghi; em không phải làm thêm bài trong ví dụ ấy.

**Lý do:** Giữ nguyên tên mục chung, thay từ trường. Giải thích ví dụ giả lập, giữ giới hạn minh họa.

### 102. Dòng 1125 — Lời giải

**Trước:**

> b) Có $16$ giá trị hợp lệ nên phải chia cho $16$: $\overline{x}=\frac{3021}{16}=188{,}8125$ mm. Số $17$ đếm bản ghi, gồm cả ô không có phép đo để tính.

**Sau:**

> b) Có $16$ giá trị hợp lệ nên phải chia cho $16$: $\overline{x}=\frac{3021}{16}=188{,}8125$ mm. Số $17$ là số dòng trong bảng, gồm cả dòng thiếu số đo chiều dài.

**Lý do:** Làm rõ diễn đạt trong lời giải, giữ nguyên dữ kiện, phép tính và kết luận.

### 103. Dòng 1127 — Lời giải

**Trước:**

> c) Sửa thành: “Bản ghi ở dòng 4 thiếu giá trị chiều dài chân chèo.” Không có căn cứ gán chiều dài bằng $0$.

**Sau:**

> c) Sửa thành: “Dòng 4 chưa có số đo chiều dài chân chèo.” Không có căn cứ gán chiều dài bằng $0$.

**Lý do:** Làm rõ diễn đạt trong lời giải, giữ nguyên dữ kiện, phép tính và kết luận.

### 104. Dòng 1161 — Giải thích toán

**Trước:**

> <summary>Lời giải Nhiệm vụ 05 — Tự nội suy và kiểm ý nghĩa</summary>

**Sau:**

> <summary>Lời giải Nhiệm vụ 05 — Tự nội suy và giải thích kết quả</summary>

**Lý do:** Đồng bộ tên đề và lời giải.

### 105. Dòng 1163 — Giải thích toán

**Trước:**

> a) $r=\frac{3\cdot49}{4}=36{,}75$. Tích lũy trước nhóm $[190;195)$ là $30$, đến hết nhóm là $40$, nên dùng $a=190$, $F=30$, $f=10$, $h=5$:

**Sau:**

> a) $r=\frac{3\cdot49}{4}=36{,}75$. Tần số tích lũy trước nhóm $[190;195)$ là $30$, đến hết nhóm là $40$, nên dùng $a=190$, $F=30$, $f=10$, $h=5$:

**Lý do:** Nêu đầy đủ tên đại lượng.

### 106. Dòng 1181 — Khí tượng

**Trước:**

> b) “Tháng 01/2023 có $13$ ngày được ghi PRCP bằng $0$; trong đó $6$ ngày có cờ vết giáng thủy.” Cờ T bác bỏ cách hiểu rằng mọi số $0$ đều xác nhận hoàn toàn không có giáng thủy.

**Sau:**

> b) “Tháng 01/2023 có $13$ ngày được ghi PRCP bằng $0$; trong đó $6$ ngày có ký hiệu vết giáng thủy.” Ký hiệu T bác bỏ cách hiểu rằng mọi số $0$ đều xác nhận hoàn toàn không có giáng thủy.

**Lý do:** Đã đọc từng ngữ cảnh: cờ ở đây là dấu ghi kèm dữ liệu, không phải khái niệm toán. Đồng bộ đầu câu và đầu cột.

### 107. Dòng 1183 — Lời giải

**Trước:**

> c) Chưa đủ căn cứ. Một tháng tại một trạm chỉ mô tả đúng phạm vi đó. Kết luận dài hạn cần chuỗi thời gian dài hơn cùng việc kiểm tính so sánh của phép đo và phạm vi không gian; không thể suy từ riêng bảng này.

**Sau:**

> c) Chưa đủ căn cứ. Một tháng tại một trạm chỉ mô tả đúng phạm vi đó. Muốn kết luận về khí hậu lâu dài, cần dữ liệu của nhiều năm, kiểm tra xem cách đo qua các năm có so sánh được với nhau hay không và các trạm đo có đủ để nói về khu vực muốn xét hay không. Riêng bảng này chưa đủ.

**Lý do:** Làm rõ diễn đạt trong lời giải, giữ nguyên dữ kiện, phép tính và kết luận.

### 108. Dòng 1241 — Giải thích toán

**Trước:**

> | Khoảng, mm | Tần số | Trung điểm, mm | Tích lũy |

**Sau:**

> | Khoảng, mm | Tần số | Trung điểm, mm | Tần số tích lũy |

**Lý do:** Dùng đầy đủ tên đại lượng đã giải thích.

### 109. Dòng 1251 — Lời giải

**Trước:**

> Trung điểm chỉ là đại diện của khoảng. Biết khoảng không đủ để thay lời mô tả từng quan sát bằng một giá trị đo chính xác.

**Sau:**

> Trung điểm chỉ là đại diện của khoảng. Chỉ biết khoảng chứa một số đo thì chưa biết số đo ấy chính xác là bao nhiêu.

**Lý do:** Làm rõ diễn đạt trong lời giải, giữ nguyên dữ kiện, phép tính và kết luận.

### 110. Dòng 1261 — Giải thích toán

**Trước:**

> a) Tích lũy lần lượt là $0;1;4;19;37;46;48;50;50$. Tổng các tích tần số với trung điểm là $9600$, nên $\overline{x}_{\text{nhóm}}=\frac{9600}{50}=192$ mm.

**Sau:**

> a) Tần số tích lũy lần lượt là $0;1;4;19;37;46;48;50;50$. Tổng các tích tần số với trung điểm là $9600$, nên $\overline{x}_{\text{nhóm}}=\frac{9600}{50}=192$ mm.

**Lý do:** Nêu đầy đủ tên đại lượng.

### 111. Dòng 1311 — Lời giải

**Trước:**

> a) $\overline{x}=\frac{103137}{29}\approx3556{,}45$ lượt/ngày. Số trung bình phù hợp với yêu cầu phân bổ tổng theo ngày, vì tổng bằng số ngày nhân với trung bình chưa làm tròn.

**Sau:**

> a) $\overline{x}=\frac{103137}{29}\approx3556{,}45$ lượt/ngày. Số trung bình phù hợp với câu hỏi tổng lượt thuê chia đều cho mỗi ngày là bao nhiêu, vì tổng bằng số ngày nhân với trung bình chưa làm tròn.

**Lý do:** Làm rõ diễn đạt trong lời giải, giữ nguyên dữ kiện, phép tính và kết luận.

### 112. Dòng 1336 — Lời giải

**Trước:**

> Nếu viết theo trung bình nhóm, phải dùng trọng số $20$ và $9$. Trung bình cộng đơn giản của hai trung bình nhóm chỉ khoảng $3364{,}74$ lượt/ngày, vì nó cho hai nhóm trọng lượng bằng nhau dù số ngày khác nhau.

**Sau:**

> Nếu tính từ hai số trung bình nhóm, ta phải nhân chúng lần lượt với số ngày tương ứng là $20$ và $9$, cộng lại rồi chia cho tổng số ngày. Trung bình cộng đơn giản của hai trung bình nhóm chỉ khoảng $3364{,}74$ lượt/ngày, vì cách tính ấy coi hai nhóm có số ngày như nhau.

**Lý do:** Làm rõ diễn đạt trong lời giải, giữ nguyên dữ kiện, phép tính và kết luận.

### 113. Dòng 1338 — Lời giải

**Trước:**

> c) Có thể kết luận: “Trong phần dữ liệu tháng 02/2012, trung bình lượt thuê của nhóm ngày làm việc cao hơn nhóm còn lại.” Bảng mô tả chưa tách ảnh hưởng của thời tiết, sự kiện và các yếu tố khác, nên không chứng minh quan hệ nhân quả.

**Sau:**

> c) Có thể kết luận: “Trong phần dữ liệu tháng 02/2012, trung bình lượt thuê của nhóm ngày làm việc cao hơn nhóm còn lại.” Số lượt thuê còn có thể chịu ảnh hưởng của thời tiết, sự kiện và các yếu tố khác. Riêng bảng này chưa cho biết có phải vì là ngày làm việc mà số lượt thuê cao hơn hay không.

**Lý do:** Làm rõ diễn đạt trong lời giải, giữ nguyên dữ kiện, phép tính và kết luận.

### 114. Dòng 1392 — Giải thích toán

**Trước:**

> a) Tích lũy là $0;1;5;16;35;47;51;51;52$. Tổng các tích tần số với trung điểm là $10020$, nên

**Sau:**

> a) Tần số tích lũy là $0;1;5;16;35;47;51;51;52$. Tổng các tích tần số với trung điểm là $10020$, nên

**Lý do:** Nêu đầy đủ tên đại lượng.

### 115. Dòng 1424 — Lời giải

**Trước:**

> a) $\overline{x}=\frac{164875}{31}\approx5318{,}55$ lượt/ngày. Chọn số trung bình cho mục đích phân bổ tổng theo ngày.

**Sau:**

> a) $\overline{x}=\frac{164875}{31}\approx5318{,}55$ lượt/ngày. Chọn số trung bình để cho biết tổng lượt thuê chia đều cho mỗi ngày là bao nhiêu.

**Lý do:** Làm rõ diễn đạt trong lời giải, giữ nguyên dữ kiện, phép tính và kết luận.

### 116. Dòng 1428 — Lời giải

**Trước:**

> c) Mẫu không có mốt vì mọi giá trị có tần số bằng một. Chưa thể suy ra số người dùng khác nhau, hoặc khẳng định một ngày tương lai sẽ có đúng số lượt thuê bằng trung bình này. Chấp nhận một giới hạn đúng, được giải thích gắn với dữ liệu.

**Sau:**

> c) Mẫu không có mốt vì mọi giá trị có tần số bằng một. Chưa thể suy ra số người dùng khác nhau, hoặc khẳng định một ngày tương lai sẽ có đúng số lượt thuê bằng trung bình này. Em chỉ cần nêu một điều chưa thể kết luận và giải thích vì sao dữ liệu này chưa đủ.

**Lý do:** Đổi lời hướng dẫn chấm thành lời giải thích cho người học.

### 117. Dòng 1446 — Khí tượng; Lời giải

**Trước:**

> b) “Có 15 ngày được ghi PRCP bằng $0$; trong đó ngày 07/11 có cờ vết giáng thủy.” Không đồng nhất số được mã hóa với khẳng định hoàn toàn không có hiện tượng.

**Sau:**

> b) “Có 15 ngày được ghi PRCP bằng $0$; trong đó ngày 07/11 có ký hiệu vết giáng thủy.” Một số $0$ được ghi trong bảng chưa đủ để khẳng định hoàn toàn không có giáng thủy; cần đọc cả ký hiệu đi kèm.

**Lý do:** Đã đọc từng ngữ cảnh: cờ ở đây là dấu ghi kèm dữ liệu, không phải khái niệm toán. Làm rõ diễn đạt trong lời giải, giữ nguyên dữ kiện, phép tính và kết luận.

### 118. Dòng 1448 — Lời giải

**Trước:**

> c) Một tháng ở một trạm chưa đủ để suy ra xu thế dài hạn. Cần dữ liệu qua thời gian dài và kiểm tính nhất quán của quan trắc, cùng phạm vi không gian muốn kết luận.

**Sau:**

> c) Một tháng ở một trạm chưa đủ để suy ra xu thế dài hạn. Cần dữ liệu của nhiều năm, kiểm tra xem cách đo có so sánh được giữa các thời điểm hay không và các trạm đo có đủ để nói về khu vực muốn xét hay không.

**Lý do:** Làm rõ diễn đạt trong lời giải, giữ nguyên dữ kiện, phép tính và kết luận.

### 119. Dòng 1478 — Lời giải; Giải thích toán

**Trước:**

> a) $n=18$. Tích lũy là $0;0;3;5;10;14;16;18$. Tổng có trọng số theo trung điểm là $3585$, nên $\overline{x}_{\text{nhóm}}=\frac{3585}{18}\approx199{,}17$ mm.

**Sau:**

> a) $n=18$. Tần số tích lũy là $0;0;3;5;10;14;16;18$. Tổng các tích của tần số với trung điểm là $3585$, nên $\overline{x}_{\text{nhóm}}=\frac{3585}{18}\approx199{,}17$ mm.

**Lý do:** Làm rõ diễn đạt trong lời giải, giữ nguyên dữ kiện, phép tính và kết luận. Nêu đầy đủ tên đại lượng.

### 120. Dòng 1512 — Lời giải

**Trước:**

> c) Hai nhóm đông nhất là $[195;200)$ và $[200;205)$, cùng có sáu quan sát. Không có một nhóm cao nhất duy nhất; không tùy ý bỏ một nhóm đồng hạng. Ý này không yêu cầu tính mốt ghép nhóm trong trường hợp đồng hạng.

**Sau:**

> c) Hai nhóm đông nhất là $[195;200)$ và $[200;205)$, cùng có sáu quan sát. Cả hai nhóm cùng có tần số lớn nhất, nên không tùy ý bỏ qua một nhóm. Ý này không yêu cầu tính mốt ghép nhóm khi hai nhóm cùng có tần số lớn nhất.

**Lý do:** Làm rõ diễn đạt trong lời giải, giữ nguyên dữ kiện, phép tính và kết luận.

### 121. Dòng 1524 — Ôn nền

**Trước:**

> <summary>Lời giải Nhiệm vụ 22 — Xác nhận phép tính nền</summary>

**Sau:**

> <summary>Lời giải Nhiệm vụ 22 — Tự kiểm tra phép tính cơ bản</summary>

**Lý do:** Đổi tên ở cả đề và lời giải, giữ số nhiệm vụ.

### 122. Dòng 1538 — Ôn nền

**Trước:**

> <summary>Lời giải Nhiệm vụ 23 — Xác nhận đọc khoảng</summary>

**Sau:**

> <summary>Lời giải Nhiệm vụ 23 — Tự kiểm tra cách đọc khoảng</summary>

**Lý do:** Đổi tên ở cả đề và lời giải, giữ số nhiệm vụ.

### 123. Dòng 1552 — Sửa lỗi

**Trước:**

> <summary>Lời giải Nhiệm vụ 24 — Xác nhận trên mẫu Gentoo nhỏ</summary>

**Sau:**

> <summary>Lời giải Nhiệm vụ 24 — Tự làm với mẫu Gentoo nhỏ</summary>

**Lý do:** Đổi tên ở cả đề và lời giải.

### 124. Dòng 1576 — Sửa lỗi

**Trước:**

> <summary>Lời giải Nhiệm vụ 25 — Xác nhận ghép nhóm và nội suy</summary>

**Sau:**

> <summary>Lời giải Nhiệm vụ 25 — Tự kiểm tra ghép nhóm và nội suy</summary>

**Lý do:** Đổi tên ở cả đề và lời giải.

### 125. Dòng 1582 — Giải thích toán

**Trước:**

> c) Với toàn bộ 34 giá trị, tích lũy là $0;4;10;17;28;31;34$. Tổng các tích tần số với trung điểm là $7455$:

**Sau:**

> c) Với toàn bộ 34 giá trị, tần số tích lũy là $0;4;10;17;28;31;34$. Tổng các tích tần số với trung điểm là $7455$:

**Lý do:** Nêu đầy đủ tên đại lượng.

### 126. Dòng 1598 — Giải thích toán

**Trước:**

> Vị trí trung vị $17$ trùng tích lũy đến hết nhóm $[215;220)$. Nội suy từ nhóm kế tiếp cũng cho $220+\frac{17-17}{11}\cdot5=220$. Đây là biên chung, không phải lý do để đếm một quan sát vào hai nhóm.

**Sau:**

> Vị trí trung vị $17$ bằng tần số tích lũy đến hết nhóm $[215;220)$. Nội suy từ nhóm kế tiếp cũng cho $220+\frac{17-17}{11}\cdot5=220$. Đây là biên chung, không phải lý do để đếm một quan sát vào hai nhóm.

**Lý do:** Diễn đạt phép so sánh rõ đối tượng.

### 127. Dòng 1614 — Sửa lỗi

**Trước:**

> <summary>Lời giải Nhiệm vụ 26 — Xác nhận dữ liệu thiếu, trọng số và phạm vi</summary>

**Sau:**

> <summary>Lời giải Nhiệm vụ 26 — Đếm giá trị, tính trung bình và giới hạn kết luận</summary>

**Lý do:** Đổi tên ở cả đề và lời giải.

### 128. Dòng 1616 — Lời giải

**Trước:**

> a) Có $44$ bản ghi, $43$ chiều dài hợp lệ và một ô thiếu. Ô thiếu không phải một phép đo bằng $0$.

**Sau:**

> a) Có $44$ dòng, với $43$ số đo chiều dài dùng được và một ô thiếu. Ô thiếu không phải một phép đo bằng $0$.

**Lý do:** Làm rõ diễn đạt trong lời giải, giữ nguyên dữ kiện, phép tính và kết luận.

### 129. Dòng 1624 — Lời giải

**Trước:**

> Trọng số là $20$ và $23$, số giá trị hợp lệ của từng phần; không dùng $20$ và $24$, cũng không lấy trung bình cộng không trọng số của hai trung bình.

**Sau:**

> Nếu tính từ hai số trung bình riêng, cần nhân chúng với số giá trị dùng được của từng phần là $20$ và $23$, cộng lại rồi chia cho tổng số giá trị. Không dùng $20$ và $24$, vì phần sau có một ô thiếu; cũng không chỉ cộng hai số trung bình rồi chia đôi.

**Lý do:** Làm rõ diễn đạt trong lời giải, giữ nguyên dữ kiện, phép tính và kết luận.

### 130. Dòng 1636 — Khí tượng; Sửa lỗi

**Trước:**

> <summary>Lời giải Nhiệm vụ 27 — Xác nhận cách đọc cờ T</summary>

**Sau:**

> <summary>Lời giải Nhiệm vụ 27 — Đọc ký hiệu T</summary>

**Lý do:** Đã đọc từng ngữ cảnh: cờ ở đây là dấu ghi kèm dữ liệu, không phải khái niệm toán. Đổi tên ở cả đề và lời giải.

### 131. Dòng 1640 — Khí tượng

**Trước:**

> b) Không. Ngày 10/02 có cờ T, cho biết vết giáng thủy. Có thể viết: “Hai ngày có giá trị PRCP ghi bằng $0$; riêng ngày 10/02 được gắn cờ vết giáng thủy.” Không xóa cờ khi diễn giải.

**Sau:**

> b) Không. Ngày 10/02 có ký hiệu T, cho biết vết giáng thủy. Có thể viết: “Hai ngày có giá trị PRCP ghi bằng $0$; riêng ngày 10/02 được gắn ký hiệu vết giáng thủy.” Không xóa ký hiệu khi diễn giải.

**Lý do:** Đã đọc từng ngữ cảnh: cờ ở đây là dấu ghi kèm dữ liệu, không phải khái niệm toán.

### 132. Dòng 1671 — Khí tượng; Nguồn và chú thích

**Trước:**

> ZO Math dùng day.csv, chọn ngày, số lượt thuê và cờ ngày làm việc; trích theo tháng, tính tổng và các số đặc trưng, dịch nhãn sang tiếng Việt. Không thay các giá trị quan sát. Việc ghi công không hàm ý tác giả hoặc UCI bảo trợ học liệu.

**Sau:**

> ZO Math dùng day.csv, chọn các cột ngày, số lượt thuê và thông tin cho biết ngày đó có phải ngày làm việc hay không; trích theo tháng, tính tổng và các số đặc trưng, dịch nhãn sang tiếng Việt. Không thay các giá trị quan sát. Việc ghi công không hàm ý tác giả hoặc UCI bảo trợ học liệu.

**Lý do:** Đã đọc từng ngữ cảnh: cờ ở đây là dấu ghi kèm dữ liệu, không phải khái niệm toán. Giải thích thông tin ngày làm việc.

### 133. Dòng 1677 — Khí tượng; Nguồn và chú thích

**Trước:**

> Menne và cộng sự, [GHCN-Daily, Version 3](https://doi.org/10.7289/V5D21VHZ), [tài liệu trường và cờ dữ liệu](https://www.ncei.noaa.gov/pub/data/ghcn/daily/readme.txt), [thông tin trạm USW00024233](https://www.ncei.noaa.gov/cdo-web/datasets/GHCND/stations/GHCND%3AUSW00024233/detail).

**Sau:**

> Menne và cộng sự, [GHCN-Daily, Version 3](https://doi.org/10.7289/V5D21VHZ), [giải thích các cột và ký hiệu trong dữ liệu](https://www.ncei.noaa.gov/pub/data/ghcn/daily/readme.txt), [thông tin trạm USW00024233](https://www.ncei.noaa.gov/cdo-web/datasets/GHCND/stations/GHCND%3AUSW00024233/detail).

**Lý do:** Đã đọc từng ngữ cảnh: cờ ở đây là dấu ghi kèm dữ liệu, không phải khái niệm toán. Nhãn liên kết rõ nghĩa, URL giữ nguyên.

### 134. Dòng 1679 — Khí tượng; Nguồn và chú thích

**Trước:**

> Phần dùng trong gói là PRCP năm 2023 của trạm Hoa Kỳ này. Dữ liệu được đọc qua API NCEI theo hệ mét, giữ cờ quan trắc. Các số trung bình và tổng tính trên giá trị đã ghi; không tự gán lượng nước cho cờ T.

**Sau:**

> Phần dùng trong gói là PRCP năm 2023 của trạm Hoa Kỳ này. Dữ liệu được lấy từ NCEI theo hệ mét, giữ nguyên các ký hiệu ghi kèm số đo. Các số trung bình và tổng tính trên giá trị đã ghi; không tự gán lượng nước cho ký hiệu T.

**Lý do:** Đã đọc từng ngữ cảnh: cờ ở đây là dấu ghi kèm dữ liệu, không phải khái niệm toán. Bỏ mô tả giao tiếp kỹ thuật, giữ cách lấy đơn vị và ký hiệu.

## Kiểm tra và bảo toàn

- Bản thảo 0.1 trước sửa: SHA-256 `37a766a6645d583d664bfccab00278eb3155141b1d729e988bf8507bae280962`.
- Bản thảo 0.2 sau sửa: SHA-256 `9de582583024dff638010e261c0af4dece7c5c212ba447f37ee78c84cf737d56`.
- Chạy lại các phép kiểm của bản thảo trong bộ nhớ, tắt bước ghi đè báo cáo 0.1: **153/153 đạt**, không có lỗi. Phạm vi gồm dữ liệu tách riêng theo hoạt động, số liệu và đáp số, đánh số, cặp đề–lời giải, liên kết, dấu ngoặc toán và giới hạn không dựng sản phẩm.
- Cổng quản trị tài liệu: **192/192 đạt**. `git diff --check` không báo lỗi. Các kết quả này kiểm phần có thể đối chiếu bằng công cụ, không thay việc đọc và duyệt cách diễn đạt.
- Đối chiếu toàn bộ biểu thức toán trước/sau: các công thức, giá trị tính toán và thứ tự của chúng giữ nguyên. Chỉ thêm ba lần nhắc số không trong lời giải thích (hai lần `$0$`, một lần `$0{,}0$`); không thay số đo hay đáp số.
- Toàn bộ địa chỉ đích của liên kết trong bản thảo, ID, số dòng và cặp đề–lời giải giữ nguyên. **20 liên kết cục bộ trong báo cáo này** trỏ tới tệp/mục tồn tại.
- **3146 tệp ngoài bốn tệp hiện có cần cập nhật được giữ nguyên từng byte**, gồm năm tệp dữ liệu học–luyện–kiểm tra–ôn lại–sửa lỗi và báo cáo kiểm 0.1. Dấu đối chiếu tổng hợp trước/sau: `b0d70768dee362ae0c039e4f46d447f7371322701415529e0c359a7d4200da42`. Vùng Git staging giữ nguyên.
- Bốn tệp hiện có được sửa: bản thảo `ban_thao/noi_dung.md`, README của gói, phần dẫn tới lượt rà mới trong `ho_so/doi_chieu_noi_dung.md`, và đúng đoạn R2-G01 trong tài liệu điều hành 03. Một tệp mới: báo cáo trước–sau này. Không sửa quy chuẩn dùng chung, dữ liệu hoặc công cụ.
- Không tạo tệp tạm hoặc script mới trong lượt này; chỉ đọc lại script và bằng chứng kiểm bản 0.1. Không dựng QMD/HTML/PDF, không stage, commit, push hoặc phát hành. Các giới hạn của checker kiến trúc G01 đã ghi ở hồ sơ 0.1 vẫn nằm ngoài phạm vi lượt sửa lời văn này.

**Trạng thái:** chờ chủ trì duyệt nội dung và cách diễn đạt của bản 0.2; chưa chuyển sang bước dựng học liệu.

