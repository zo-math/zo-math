"""Authored orientation for the six topics in the canonical course site.

Copy is based on the approved canonical learning material, not selected by paragraph or
heading position. The complete learning goals remain owned by the source and
are rendered separately by reader_overview.py. This module adds no exercises,
mathematical claims, prerequisites or completion requirements to that source.
"""


# Internal provenance only; these references are not learner-facing links.
SOURCE_ANCHORS = {
    key: {
        "file": f"content/thpt/on_thi_toan_thpt/hoc_lieu/{key}/index.qmd",
        "intro": ["bat-dau", "bai-hoc"],
        "prerequisites": ["bat-dau"],
        "choices": ["bat-dau", "bai-hoc", "phieu-luyen", "tu-kiem-tra", "on-lai"],
    }
    for key in ("r1_g01", "r1_g02", "r1_g03", "r1_g04", "r1_g05", "r2_g01")
}


OVERVIEWS = {
    "r1_g01": {
        "intro": [
            "Chuyên đề này giúp em xác định khoảng đồng biến, nghịch biến và cực trị "
            "của hàm số từ công thức, dấu đạo hàm, bảng biến thiên hoặc đồ thị. "
            "Trọng tâm là giải thích được vì sao dữ kiện cho phép kết luận như vậy "
            "và nhận ra những điều chưa thể kết luận.",
            "Các phần học đi từ ý nghĩa của đơn điệu và cực trị đến việc kết nối "
            "các biểu diễn, đọc dữ kiện và sửa lập luận sai. Giá trị lớn nhất, "
            "giá trị nhỏ nhất, tiệm cận và quy trình khảo sát đầy đủ được học "
            "ở những chuyên đề khác.",
        ],
        "prerequisites": [
            "Em cần biết tính đạo hàm đa thức, xét dấu biểu thức và đọc giá trị "
            "hàm số. Khởi động giúp em nhận ra một số thao tác còn vướng để ôn "
            "đúng phần cần dùng.",
            "Riêng các bài về điểm ghép cần thêm giới hạn một phía đơn giản "
            "và cách dùng thương sai phân một phía để kiểm tra đạo hàm tại "
            "điểm đó. Hướng dẫn Ôn nền được đặt tại những bài cần dùng.",
        ],
        "choices": {
            "bai-hoc": "Khi cần học hoặc học lại, tìm hiểu điều kiện dùng dấu đạo hàm "
            "và cách đọc công thức, bảng biến thiên, đồ thị.",
            "phieu-luyen": "Khi đã nắm kiến thức, tự làm các bài nối biểu diễn, "
            "đọc dữ kiện và sửa lập luận; đối chiếu bài làm tại Điểm dừng.",
            "tu-kiem-tra": "Khi đã chuẩn bị kĩ hoặc đủ tự tin, làm một lượt tự lực "
            "để kiểm tra các mục tiêu của chuyên đề. Đây không phải đề thi thử.",
            "on-lai": "Đến ngày đã hẹn, tự làm lượt ôn về đơn điệu và cực trị "
            "trước khi đối chiếu để biết phần còn nhớ và phần cần học lại.",
        },
    },
    "r1_g02": {
        "intro": [
            "Tìm giá trị lớn nhất hoặc nhỏ nhất đòi hỏi xác định đúng tập đang xét, "
            "so sánh các giá trị và kiểm tra xem giá trị được chọn có thực sự đạt "
            "được trên tập ấy hay không. Chuyên đề giúp em giải thích từng việc "
            "này từ công thức, bảng biến thiên và đồ thị, đồng thời phân biệt "
            "giá trị lớn nhất, nhỏ nhất với cực trị.",
            "Phạm vi học gồm cách tìm trên đoạn đóng, xét sự tồn tại trên các tập "
            "khác đoạn đóng và giải bài toán có điều kiện thực tế. Khi lập mô hình, "
            "em phải giữ đúng đại lượng, đơn vị và các giá trị được phép chọn, "
            "kể cả khi biến chỉ nhận giá trị nguyên.",
        ],
        "prerequisites": [
            "Em cần biết tập xác định, khoảng đơn điệu, cực trị và dấu đạo hàm; "
            "tính được đạo hàm, giá trị của các hàm số quen thuộc và đọc được "
            "bảng biến thiên. Cần phân biệt đồ thị hàm số với đồ thị đạo hàm. "
            "Khởi động và các hướng dẫn Ôn nền giúp em tìm đúng thao tác cần ôn.",
            "Nhánh Chuyển giao dành cho những em đã học phần lượng giác, mũ "
            "hoặc lôgarit tương ứng. Đây là phần lựa chọn thêm, không phải "
            "điều kiện để hoàn tất các mục tiêu cốt lõi của chuyên đề.",
        ],
        "choices": {
            "bai-hoc": "Khi cần làm rõ tập đang xét, sự đạt được hoặc cách tìm "
            "giá trị lớn nhất, nhỏ nhất, đọc giải thích và tự làm nhiệm vụ trong bài.",
            "phieu-luyen": "Khi đã nắm kiến thức, luyện chọn và kiểm tra cách giải "
            "trên các tập khác nhau, từ bài hàm số đến bài có ràng buộc thực tế.",
            "tu-kiem-tra": "Khi đã chuẩn bị kĩ hoặc đủ tự tin, tự làm một lượt "
            "rồi đối chiếu các mục tiêu, nhất là điều kiện so sánh và sự đạt được.",
            "on-lai": "Đến ngày đã hẹn, làm lượt ôn trước khi đọc lại bài "
            "để kiểm tra cách xét tập, điểm đạt và các điều kiện còn nhớ được.",
        },
    },
    "r1_g03": {
        "intro": [
            "Chuyên đề này giúp em dùng giới hạn để xác định tiệm cận đứng, "
            "ngang và xiên của đồ thị hàm số. Với mỗi kết luận, em cần chỉ rõ "
            "biến đang tiến về đâu, từ phía nào và vì sao giới hạn cho phép "
            "xác định đường thẳng ấy.",
            "Em sẽ nối công thức và dữ kiện giới hạn với từng nhánh đồ thị, "
            "phân biệt giới hạn với giá trị tại một điểm và giải thích kết quả "
            "trong mô hình thực tế. Phần học chính chưa thực hiện toàn bộ "
            "quy trình khảo sát hàm số và không yêu cầu biện luận tham số.",
        ],
        "prerequisites": [
            "Em cần biến đổi được phân thức, xét dấu đơn giản và đọc kí hiệu "
            "giới hạn. Đạo hàm không bắt buộc trong các nhiệm vụ chính. "
            "Các câu Khởi động giúp chọn thao tác cần ôn trước khi học tiếp.",
            "Hai nhánh Phối hợp và Chuyển giao là lựa chọn thêm. Phối hợp cần "
            "kiến thức về giá trị lớn nhất, nhỏ nhất trên tập đang xét; "
            "Chuyển giao cần đọc được giới hạn chứa căn và trị tuyệt đối.",
        ],
        "choices": {
            "bai-hoc": "Khi cần học hoặc nhớ lại, bắt đầu từ ý nghĩa của giới hạn "
            "rồi tìm hiểu cách xác định và giải thích từng loại tiệm cận.",
            "phieu-luyen": "Khi đã hiểu kiến thức, tự xác định tiệm cận, nối kết quả "
            "với hình và kiểm tra những kết luận có thể rút ra từ dữ kiện.",
            "tu-kiem-tra": "Khi đã chuẩn bị kĩ hoặc đủ tự tin, làm một lượt tự lực; "
            "giữ cả phép tính, hướng xét giới hạn và lí do kết luận để đối chiếu.",
            "on-lai": "Đến ngày đã hẹn, tự làm lượt ôn rồi kiểm lại cách xét "
            "tập xác định, các phía tiến tới và phương trình tiệm cận.",
        },
    },
    "r1_g04": {
        "intro": [
            "Khảo sát hàm số cần đưa các kết quả tính toán thành một hình vẽ "
            "phù hợp với công thức. Chuyên đề này giúp em tổ chức tập xác định, "
            "đạo hàm, biến thiên, cực trị, giới hạn và tiệm cận thành một bản "
            "khảo sát, rồi dùng những dữ kiện ấy để vẽ và kiểm tra đồ thị.",
            "Phần khảo sát đầy đủ tập trung vào ba họ: hàm số bậc ba, phân thức "
            "bậc nhất trên bậc nhất và phân thức bậc hai trên bậc nhất. Hai họ "
            "phân thức được xét với tử không chia hết cho mẫu; điều kiện mẫu "
            "số khác không luôn được giữ. Em cũng học cách nhận biết đối xứng "
            "và giải thích kết quả khảo sát trong mô hình được cho.",
        ],
        "prerequisites": [
            "Em cần biết tìm tập xác định, tính đạo hàm, xét dấu và xác định "
            "cực trị từ dấu đạo hàm; đọc được giới hạn và tìm tiệm cận trong "
            "những trường hợp đơn giản.",
            "Các kiến thức trong Đơn điệu và cực trị, Giá trị lớn nhất và giá trị "
            "nhỏ nhất, Đường tiệm cận được kết nối ở đây. Nếu đã có nền phù hợp, "
            "em không cần học lại toàn bộ ba chuyên đề. Dùng Khởi động và "
            "hướng dẫn Ôn nền để bổ sung đúng thao tác còn thiếu.",
        ],
        "choices": {
            "bai-hoc": "Khi cần học hoặc nhớ lại cách khảo sát, đi từ sơ đồ chung "
            "đến từng họ hàm và cách dùng dữ kiện để kiểm tra hình vẽ.",
            "phieu-luyen": "Khi đã nắm phương pháp, tự lập bản khảo sát và vẽ "
            "đồ thị; kiểm sự phù hợp giữa công thức, bảng biến thiên và từng nhánh.",
            "tu-kiem-tra": "Khi đã chuẩn bị kĩ hoặc đủ tự tin, thực hiện một lượt "
            "tự lực để đối chiếu cả kết quả khảo sát, hình vẽ và cách giải thích.",
            "on-lai": "Đến ngày đã hẹn, tự làm lượt ôn trước khi tra lại phương pháp "
            "để kiểm tra những bước khảo sát và dữ kiện đồ thị còn nhớ được.",
        },
    },
    "r1_g05": {
        "intro": [
            "Chuyên đề này giúp em chuyển một tình huống thực tế thành bài toán "
            "hàm số một biến, dùng đạo hàm để giải rồi kiểm tra câu trả lời "
            "trong bối cảnh ban đầu. Trước khi tính, em cần xác định đại lượng, "
            "đơn vị, điều kiện của biến và những lựa chọn thực sự được phép.",
            "Phần học gồm ý nghĩa của tốc độ thay đổi, cách lập mô hình và chứng "
            "minh phương án tối ưu, kể cả khi phải chọn giá trị nguyên hoặc theo "
            "một bước cho trước. Các bài dùng số liệu giả định phục vụ học toán. "
            "Hình phối cảnh giúp hình dung; số đo dùng để "
            "tính phải lấy từ đề và nhãn kích thước.",
        ],
        "prerequisites": [
            "Em cần biến đổi được biểu thức đơn giản, tính đạo hàm và đọc dấu "
            "đạo hàm. Phương pháp tìm giá trị lớn nhất, nhỏ nhất được dùng "
            "để giải bài tối ưu; nếu còn vướng, xem lại phần tương ứng của "
            "chuyên đề Giá trị lớn nhất và giá trị nhỏ nhất. Công thức hình học "
            "cần thiết được nhắc ngay tại bài.",
        ],
        "choices": {
            "bai-hoc": "Khi cần học hoặc làm rõ cách lập mô hình, tìm hiểu cách "
            "chọn đại lượng, đặt điều kiện, dùng đạo hàm và trả lời trong bối cảnh.",
            "phieu-luyen": "Khi đã nắm kiến thức, tự lập và giải mô hình; "
            "kiểm phương án được phép, đơn vị và căn cứ cho kết luận tối ưu.",
            "tu-kiem-tra": "Khi đã chuẩn bị kĩ hoặc đủ tự tin, làm một lượt tự lực "
            "từ việc hiểu tình huống đến kết luận, rồi đối chiếu các mục tiêu.",
            "on-lai": "Đến ngày đã hẹn, tự giải lượt ôn để kiểm tra cách lập mô hình "
            "và lựa chọn phương án trước khi xem lại lời giải.",
        },
    },
    "r2_g01": {
        "intro": [
            "Khi dùng một con số để mô tả nhiều quan sát, em cần biết con số ấy "
            "trả lời câu hỏi nào. Chuyên đề này giúp em đọc dữ liệu và sử dụng "
            "số trung bình, trung vị, tứ phân vị, mốt; giải thích lựa chọn "
            "thay vì chỉ tính ra kết quả.",
            "Em sẽ làm việc với mẫu số liệu gốc và bảng ghép nhóm, nhận ra "
            "thông tin bị mất khi ghép nhóm và phân biệt kết quả tính từ mẫu gốc "
            "với kết quả ước lượng. Các bài dùng cả mẫu giả định và số liệu "
            "quan trắc có nguồn, đơn vị và bối cảnh cụ thể. Khoảng biến thiên, "
            "khoảng tứ phân vị, phương sai và độ lệch chuẩn được học riêng.",
        ],
        "prerequisites": [
            "Em cần biết sắp thứ tự các số, tính trung bình cộng và tỉ lệ, "
            "đọc khoảng để xác định một giá trị thuộc nhóm nào. Khởi động "
            "giúp em tự kiểm các thao tác này; nếu còn vướng, hướng dẫn "
            "Ôn nền được đặt ngay sau câu hỏi tương ứng.",
        ],
        "choices": {
            "bai-hoc": "Khi cần học hoặc học lại, tìm hiểu ý nghĩa từng số đặc trưng, "
            "cách tính trên mẫu gốc và cách ước lượng từ bảng ghép nhóm.",
            "phieu-luyen": "Khi đã hiểu kiến thức, tự đọc bảng số liệu, tính và chọn "
            "số đại diện; giải thích kết quả trong đúng đơn vị và bối cảnh.",
            "tu-kiem-tra": "Khi đã chuẩn bị kĩ hoặc đủ tự tin, tự làm một lượt "
            "rồi đối chiếu cách đọc dữ liệu, tính toán và giải thích kết quả.",
            "on-lai": "Sau khi hoàn tất lượt học chính và đến ngày đã hẹn, "
            "tự làm lượt ôn trước khi đối chiếu để nhận ra kiến thức cần củng cố.",
        },
    },
}
