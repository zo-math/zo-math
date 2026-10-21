# Quy trình xuất bản website ZO Math

## 1. Mục đích và phạm vi

Quy trình này điều hành các nhiệm vụ kiểm tra, chuẩn bị và xuất bản website ZO Math. Đây là tài liệu nội bộ, không phải nội dung dành cho người đọc website.

Nhánh `master` chứa nguồn xây dựng website. Nhánh `gh-pages` chỉ chứa cây đầu ra công khai. Commit nguồn và commit xuất bản phải luôn tách biệt.

## 2. Cấu hình công khai

`publish_public.yml` là nguồn cấu hình chính thức xác định cây đầu ra được phép xuất bản. Cơ chế lựa chọn chính là allowlist; denylist chỉ là lớp phòng vệ bổ sung.

Không mặc định công khai toàn bộ `content/`, `assets/`, `figures/` hoặc toàn bộ thư mục đầu ra Quarto. Mọi nhóm mới phải được khảo sát và thêm tường minh vào allowlist.

## 3. Công cụ chính thức

Mọi lệnh của công cụ xuất bản phải chạy qua trình khởi chạy Python repository-local:

```text
python scripts/zo_python.py scripts/zo_publish.py check
python scripts/zo_python.py scripts/zo_publish.py prepare
python scripts/zo_python.py scripts/zo_publish.py publish
```

`check` chỉ đọc: kiểm tra Git, worktree, cấu hình và cây đầu ra hiện có; từ đó dựng một candidate công khai trong thư mục hệ thống tạm nằm ngoài repository và worktree xuất bản. Candidate được lọc, bổ sung tệp đặc biệt, chuẩn hóa chỉ mục và kiểm định bằng cùng builder với `prepare`; diff dự kiến được tính từ byte cuối của candidate. Thư mục tạm luôn được dọn, còn repository, `docs`, Git index và worktree `gh-pages` không bị thay đổi.

`prepare` không có `--page`, hoặc có `--full-render`, render toàn website qua `scripts/zo_quarto.py` vào staging sạch trong `_audit/`, dùng lại đúng candidate builder của `check`, tạo báo cáo chuẩn bị rồi đồng bộ có kiểm soát sang worktree `gh-pages`. Để tách thay đổi nguồn khỏi drift của toolchain, công cụ đọc trailer `Source-Master` của commit `gh-pages` hiện hành, render commit nguồn đã xuất bản và HEAD bằng cùng toolchain, rồi chỉ phủ những đầu ra thực sự khác nhau giữa hai render lên cây đang xuất bản. Tập đầu ra được phép phủ còn phải bắt nguồn từ diff Git của source, quan hệ include/dependency hoặc nhóm sidebar thực sự thay đổi; khác biệt render nằm ngoài tập này được giữ nguyên byte từ `gh-pages`. Baseline tạm được bổ sung cùng các dependency và cache render đang bị Git ignore, nhưng tuyệt đối không lấy lại `docs`, `tmp` hoặc `_audit`. Chỉ mục toàn site vẫn được lấy từ render mới khi nội dung nguồn làm chúng thay đổi. `prepare` toàn phần không tái sử dụng candidate tạm của lần `check`: mỗi lần chạy đều render, dựng và xác thực lại candidate từ trạng thái hiện hành. Đường `prepare --page` dùng cơ chế artifact riêng mô tả bên dưới. Lệnh này không stage, commit hoặc push. Chỉ chạy khi người dùng yêu cầu rõ và worktree đích hoàn toàn sạch; báo cáo chuẩn bị là căn cứ cho bước xuất bản tiếp theo.

Candidate phải đạt kiểm tra trailing whitespace tương đương `git diff --check`. JSON và XML do công cụ chuẩn hóa phải dùng LF độc lập hệ điều hành. Với HTML, công cụ chỉ được bỏ khoảng trắng cuối dòng trên các dòng tag độc lập vừa thêm hoặc thay đổi và không nằm trong `pre`, `script`, `style` hoặc `textarea`; khoảng trắng có thể mang nghĩa phải được giữ nguyên và làm cổng kiểm tra thất bại thay vì bị sửa mù quáng.

`publish` không render và không tự chạy `prepare`. Lệnh chỉ dùng báo cáo cùng cây công khai do một lần `prepare` thành công tạo ra; kiểm tra lại SHA nguồn, remote, manifest, validator và diff trước khi stage từng đường dẫn tường minh, commit riêng trên `gh-pages` rồi push không force. Nguồn phải được push lên `origin/master` trước, `origin/gh-pages` không được thay đổi sau `prepare`, và người dùng phải yêu cầu rõ việc xuất bản.

Nếu push bị từ chối, công cụ giữ commit `gh-pages` cục bộ và báo lỗi; không tự merge, rebase, sửa lịch sử hoặc force push. Sau khi push thành công hoặc xác nhận không có thay đổi, dữ liệu tạm và báo cáo của lần `prepare` được dọn. Commit nguồn trên `master` và commit website trên `gh-pages` luôn tách biệt.

Không dùng `scripts/publish_public.sh` cho quy trình mới, trừ khi yêu cầu hiện tại của người dùng chỉ định rõ việc khảo sát script cũ. Không dùng `git add -A`, force push hoặc thao tác xóa diện rộng.

Khi chỉ cập nhật một số trang HTML, mặc định dùng `prepare --page <duong_dan_HTML>` và lặp lại `--page` cho từng trang đã được giao. Đường này dùng `scripts/zo_publish_pages.py`: chỉ render các nguồn QMD/Rmd được chọn, không render baseline lịch sử và không render toàn website. Cây public hiện hành là baseline; HTML khác cùng các PDF giữ nguyên byte. Muốn dùng cơ chế đối chiếu hai render toàn site cũ cho một phạm vi HTML, thêm `--full-render` một cách tường minh.

### Cập nhật riêng trang: plan → prepare → validate → publish

```text
python scripts/zo_python.py scripts/zo_publish.py plan --page content/thpt/on_thi_toan_thpt/tot_nghiep_thpt/2027/index.html
python scripts/zo_python.py scripts/zo_publish.py prepare --committed-source --page content/thpt/on_thi_toan_thpt/tot_nghiep_thpt/2027/index.html
python scripts/zo_python.py scripts/zo_publish.py validate
```

`plan` chỉ khảo sát nguồn đang làm việc: nhận diện QMD/Rmd, kiểm phạm vi công khai, đường dẫn và tài nguyên khai báo trực tiếp. Không render, fetch, stage hay sửa worktree public; chỉ ghi báo cáo nếu chỉ định `--report`. Đây là kiểm tra sớm, chưa thay thế validator sau dựng.

`prepare --page` kiểm Git, cấu hình toàn cục và tài nguyên trước khi dựng. Khi `_quarto*.yml/yaml`, theme SCSS, filter hoặc extension toàn cục đã đổi, mặc định phải dùng `--full-render`. Nếu chủ trì chỉ giao một danh sách trang HTML cụ thể, có thể dùng thêm `--allow-global-inputs-for-pages`: công cụ ghi các đầu vào chung đã đổi vào biên nhận, dựng lại từng trang được chọn, giữ nguyên byte mọi trang và PDF khác, đồng thời vẫn chặn tài nguyên dùng chung ảnh hưởng trang ngoài phạm vi. Sau một lượt render mỗi trang, công cụ lần theo HTML/CSS để gom đúng JS, ảnh, phông và giấy phép liên quan, kiểm allowlist/denylist, kích thước, nội dung nhạy cảm, liên kết và trailing whitespace. Tài nguyên thay đổi đang được trang khác dùng sẽ chặn phát hành, kèm danh sách trang bị ảnh hưởng; chủ nhiệm vụ phải mở rộng danh sách trang phù hợp hoặc chọn phát hành toàn phần.

Công cụ ghép các mục search/sitemap của đúng trang được chọn vào chỉ mục public hiện hành. Không thay nội dung tìm kiếm hoặc metadata sitemap của trang ngoài phạm vi. Không tự xóa tài nguyên cũ còn có thể được trang khác dùng.

PDF chỉ được kế thừa nếu SHA-256 và kích thước giống hệt bản public. Thêm, thay hoặc xóa PDF trên đường theo trang đều bị chặn; phải dùng quy trình đầy đủ với kiểm provenance PDF. Chỉ nội dung HTML/chỉ mục có byte thay đổi được phân tích lại; manifest, hash của phần giữ nguyên và ranh giới public vẫn được kiểm toàn cây. Đây là kế thừa bản đã phát hành, không phải miễn kiểm cho một PDF mới.

Riêng khi chủ trì yêu cầu cập nhật cùng lúc trang D0 và PDF toàn văn của chính D0, dùng `prepare --page content/thpt/on_thi_toan_thpt/hoc_lieu/d0/index.html --d0-pdf`. Cổng chỉ nhận đúng một trang này và `content/thpt/on_thi_toan_thpt/hoc_lieu/d0/index.pdf`, kiểm biên nhận dựng, toàn bộ hash đầu vào hiện hành, byte PDF canonical/ứng viên và số trang. Mọi PDF khác phải giữ nguyên byte; `validate` và `publish` kiểm lại cùng điều kiện từ biên nhận prepare.

`validate` dùng lại bản prepare, kiểm nguồn, HEAD public, manifest, backup, chính sách và validator cuối giống nhánh publish. Không render, fetch, stage, commit hay push. Nó không xác nhận remote mới nhất; `publish` vẫn fetch và kiểm remote ngay trước hành động thật. Nên chạy `validate` trước khi xin quyền phát hành để phát hiện lỗi môi trường/dependency sớm.

### Artifact và điều kiện tái sử dụng

Artifact ở `.quarto/zo_publish_cache/<fingerprint>/`; không nằm trong `_audit/`, không đưa vào Git hay cây public. Mỗi mục chỉ giữ trang đã chọn, chuỗi tài nguyên tham chiếu, search/sitemap cần ghép và receipt hash. Cache chỉ được tạo sau render thành công, nguồn không đổi trong khi dựng; khi dùng lại phải kiểm hash toàn bộ artifact. Cache hỏng bị chặn, không âm thầm dùng bản cũ hay sửa receipt.

Fingerprint bao gồm trang được chọn, nội dung nguồn tracked (blob Git cho tệp sạch; hash trực tiếp cho tệp đã đổi), dependency bị ignore được phép, mã công cụ, chính sách public, phiên bản Quarto/Python/các gói Python và các biến môi trường liên quan. Chỉ thay metadata commit mà cây nguồn không đổi không buộc dựng lại. Hiện việc ghi nhận phụ thuộc là **bảo thủ trên toàn bộ nguồn tracked**, vì hook Python/R có thể đọc động: một số thay đổi nguồn không ảnh hưởng trực tiếp trang vẫn có thể làm cache mất hiệu lực. Chưa tuyên bố đã có đồ thị phụ thuộc tối thiểu cho mọi hook.

Tài liệu có khối mã thực thi hoặc shortcode không xác định đầu vào không được tái sử dụng cache; vẫn render riêng trang mỗi lần. Khối HTML thô và include tĩnh được nhận diện riêng. Mỗi prepare vẫn xác thực và ghép candidate hiện hành, kể cả cache hit. `publish` phát hành đúng candidate đã duyệt, không render lại. Nguồn/công cụ/chính sách hoặc tệp phụ thuộc thay đổi sau prepare làm kiểm định dừng; không tự cập nhật SHA trong receipt. Nếu còn một prepare hợp lệ, không chạy đè: dùng `validate`/`publish` hoặc yêu cầu bỏ bản chuẩn bị cũ một cách có kiểm soát.

### Đo thời gian và kiểm thử

Receipt prepare theo trang ghi `timings` cho kiểm phạm vi, snapshot nguồn, preflight, fingerprint, artifact, backup, candidate/validator và đồng bộ; `page_release.cache_hit` cùng `render.source_count` phân biệt dựng mới với tái sử dụng. Full render cũng ghi thời gian baseline/head/tổng. `validate` báo thời gian kiểm không render; `publish` báo riêng validator, commit/đối chiếu Git, mạng và tổng. Không cộng thời gian chờ người duyệt vào tốc độ build.

```text
python scripts/zo_python.py scripts/zo_publish_selftest.py
python scripts/zo_python.py scripts/zo_publish_pages_selftest.py
```

Bộ theo trang kiểm vòng prepare → validate → dùng lại artifact trên Git fixture, cache bị sửa, nguồn/công cụ đổi, nguồn đổi khi đang dựng, tài nguyên thiếu/cấm/dùng chung, giữ nguyên HTML/PDF, ghép chỉ mục, cùng đọc Git blob nhị phân/Unicode. Benchmark thực phải dùng cùng commit và cùng sửa đổi mẫu, so byte HTML/search với đường đầy đủ, tạo snapshot mới cả lần cache hit, không phát hành dữ liệu mẫu. Số đo một máy/một lượt không phải cam kết thời gian cho mọi trang.



### Chuẩn bị một số trang từ nguồn đã commit

Khi checkout chính còn công việc khác chưa commit, dùng:

```text
python scripts/zo_python.py scripts/zo_publish.py prepare --committed-source --page content/thpt/on_thi_toan_thpt/tot_nghiep_thpt/2027/index.html
```

Chế độ này chỉ dùng với `prepare --page`. Trước đó phải commit đúng phần
nguồn cần phát hành và mã/config công cụ xuất bản, để vùng staged trống.
Công cụ dựng HEAD trong snapshot tạm `.quarto/_zph`, giữ nơi biên tập chính
và mọi sửa đổi khác nguyên trạng; snapshot được dọn cả khi có lỗi. Chỉ các
dependency/cache render bị ignore vốn được phép mới được bổ sung như đường
dựng baseline, không dùng docs hay audit lịch sử làm đầu vào.

Trong đường đầy đủ, PDF được kiểm bằng chính mã hợp đồng/provenance trong snapshot HEAD, không so với pipeline PDF đang được sửa ngoài commit. Trong đường theo trang, PDF phải giữ nguyên byte của bản public, mọi thay đổi PDF bị chặn như quy định ở trên.
Receipt ghi `committed_source`, SHA nguồn, fingerprint artifact và các thay đổi làm việc bị loại
khỏi render. Sai nhánh, vùng staged có dữ liệu, merge/rebase, source behind
remote hoặc public worktree bẩn vẫn bị chặn.

`publish` nhận receipt của chế độ này, kiểm lại HEAD/remote, manifest và
PDF từ đúng commit. Nguồn vẫn phải được push trước khi publish theo quyền
của chủ dự án; prepare không push. Không tự stash/restore hoặc commit phần
việc khác để làm sạch checkout. Lệnh check mặc định vẫn kiểm toàn trạng
thái làm việc hiện tại, không thay bằng kiểm một commit.

## 4. Nguyên tắc an toàn

- Không thay đổi `master` trong quá trình chuẩn bị hoặc xuất bản website.
- Không ghi vào worktree `gh-pages` nếu trạng thái ban đầu không sạch.
- Không xuất bản tệp ngoài allowlist hoặc tệp bị denylist chặn.
- Không commit nếu HTML, tài nguyên, đường dẫn hoặc kiểm tra nội dung riêng tư chưa đạt.
- Mọi render phải đi qua `scripts/zo_quarto.py`.
- Phải xem diff xuất bản trước khi stage và commit.
- Không push nếu remote `gh-pages` đã thay đổi sau lần kiểm tra gần nhất.
- Chỉ xuất bản khi yêu cầu hiện tại của người dùng cho phép rõ việc xuất bản website.

## 5. Trình tự dự kiến

1. Chọn phạm vi: cập nhật riêng HTML dùng `plan --page`; thay cấu hình/toàn site/PDF dùng đường đầy đủ. Không mặc định render toàn website.
2. Kiểm sớm nguồn, Git, dependency, chính sách và phạm vi; xử lí điểm chặn trước render. `check` vẫn phục vụ kiểm cây đầu ra hiện có, không phải bước bắt buộc dựng lại toàn site trước một cập nhật trang.
3. Chủ dự án duyệt kết quả kiểm tra. `check` đạt không tự động cho phép `prepare` hoặc `publish`.
4. Khi người dùng yêu cầu rõ, chạy `prepare --page` hoặc prepare đầy đủ phù hợp; dựng/tái sử dụng artifact, xác thực và đồng bộ candidate có kiểm soát sang worktree xuất bản.
5. Chạy `validate` không phát hành; chủ dự án duyệt candidate và diff do `prepare` tạo.
6. Chỉ khi người dùng cho phép xuất bản, chạy `publish` để kiểm định lại remote, manifest và diff, sau đó commit riêng trên `gh-pages` và push thường.

## 6. Bản nháp và ranh giới nội bộ

`draft: true` trong Quarto không thay thế chính sách public. Các trang và tài sản đã duyệt của chuyên mục `content/thpt/on_thi_toan_thpt` chỉ được chọn qua allowlist trong `publish_public.yml`; `_quy_trinh` tiếp tục bị chặn. Mọi mở rộng ngoài phạm vi đã duyệt vẫn cần người dùng phê duyệt riêng.

Profile `on-thi-preview` chỉ phục vụ preview trên `127.0.0.1`. Công cụ xuất bản từ chối profile này khi có trong `QUARTO_PROFILE` hoặc profile mặc định của dự án, trước khi fetch, render hoặc tác động worktree public. Không dùng `prepare` như một lệnh preview.

`check` và validator của quy trình hiện hành kiểm tra đường dẫn bị cấm sau giải mã và chuẩn hóa trong manifest, HTML (kể cả chuỗi đường dẫn không phải liên kết), `search.json` và sitemap. Chỉ loại tệp khỏi manifest là chưa đủ nếu chỉ mục hoặc HTML vẫn tham chiếu tới vùng bị cấm. Chỉ mục JSON/XML không đọc được phải làm kiểm tra thất bại.

Kiểm thử mục tiêu của hàng rào:

```text
python scripts/zo_python.py scripts/zo_publish_selftest.py
```

Fixture của bộ kiểm thử nằm trong `_audit/` và được tự dọn. Khi mở rộng validator, phải phân biệt phát hiện mới trên đầu ra cũ với hồi quy do thay đổi nguồn; không tự dọn các vấn đề ngoài nhiệm vụ.

### Benchmark tái lập (chỉ khi được giao đo hiệu năng)

Dùng `python scripts/zo_python.py scripts/zo_publish_benchmark.py --page <trang.html> --old-text <chuoi-cu> --new-text <chuoi-moi> --report _audit/<ten-phep-do>.json`. Công cụ chỉ dựng sửa đổi mẫu trong snapshot tạm, không commit nguồn mẫu, không stage hay push, không sửa cây public. Cả lần đầu và lần cache dùng snapshot nguồn mới. Tất cả snapshot và sản phẩm lớn được dọn khi xong; chỉ giữ báo cáo. Đây là phép đo dài, không chạy trong mỗi lần cập nhật trang.

### Phát hành bộ sáu trang đã duyệt từ đầu ra canonical

Với bộ Khóa 2027, D0 và G01–G04 đã được chủ trì duyệt, dùng
`python scripts/zo_python.py scripts/zo_publish.py prepare --approved-course`,
sau đó `validate` và `publish` như quy trình chung. Không dựng lại bản lịch sử
chỉ để phát hành bộ hiện hành: phụ thuộc công cụ đồ thị bên ngoài đã đổi có
thể khiến baseline lịch sử không còn tái tạo được bằng bộ công cụ hiện tại.

Đường này chỉ nhận đúng sáu HTML trong `docs/`, có biên nhận dựng còn đúng
nguồn, hash đầy đủ và manifest `owner_approved`. Kiểm provenance riêng D0
và đủ 32 PDF R1, so byte 33 PDF tải với PDF trong gói. Ứng viên giữ nguyên
byte HTML/PDF đã duyệt, chỉ lấy tài nguyên phụ thuộc đã kiểm, ghép mục tìm
kiếm/sitemap của sáu trang; trang ngoài phạm vi giữ nguyên. Tài nguyên dùng
chung làm ảnh hưởng trang ngoài phạm vi vẫn bị chặn. Cổng `validate`/`publish`
kiểm lại nguồn, duyệt, hash, phụ thuộc, chính sách công khai và PDF; có backup
và rollback trước commit. Không đọc HTML cũ từ audit, không sửa receipt để
chấp nhận nguồn cũ và không tự cấp nghiệm thu.

Nếu nguồn thực sự đổi, phải sửa nguồn → bộ dựng canonical → kiểm → đối chiếu
bản đã duyệt trước prepare. Chỉ sửa công cụ phát hành cũng làm fingerprint
bảo thủ hiện hành hết hạn: dựng lại sáu HTML bằng bộ dựng, xác nhận byte
không đổi; không dựng lại hình hoặc PDF không chịu ảnh hưởng.
Kiểm hồi quy: `python scripts/zo_python.py scripts/zo_publish_course_selftest.py`.

### Phát hành bộ tích hợp R1-G05 ngày 21/10/2026

Yêu cầu phát hành hiện hành cho phép push và đưa đúng bảy HTML đã nghiệm thu
cùng tám PDF G05 lên zomath.vn, giữ nguyên 33 PDF cũ. Đường `prepare
--approved-course` đọc `r1_g05/_quy_trinh/ho_so/uy_quyen_phat_hanh_20261021.json`
và các biên nhận nghiệm thu canonical được chỉ rõ trong đó. Không ghi đè biên
nhận cũ hoặc dùng audit làm nguồn. Danh sách trang lấy từ binding điều hướng;
kiểm kê PDF lấy từ cấu hình biến thể của từng gói và phải bằng tập đã duyệt.

Tám PDF mới vẫn phải đạt provenance hiện hành. Chỉ 33 PDF được chủ trì yêu
cầu giữ nguyên mới dùng cơ chế kế thừa: SHA-256 phải trùng biên nhận duyệt,
blob Git của commit public trước, PDF canonical, bản tải trong docs và ứng
viên. Chúng giữ trạng thái lịch sử, không được coi là CURRENT. Cổng mặc định
và các chế độ phát hành khác tiếp tục yêu cầu provenance hiện hành. Validate
và publish kiểm lại toàn bộ ràng buộc, backup và nguồn đã push.

Với thay đổi chỉ ở công cụ phát hành, dùng chính biên nhận nghiệm thu khóa
hash bảy QMD, bảy HTML và toàn bộ phụ thuộc, cùng manifest bảo vệ nguồn để
chứng minh sản phẩm không đổi; không gia hạn fingerprint dựng của bộ cũ.
Không dựng lại HTML, hình hoặc PDF đã duyệt chỉ để làm mới fingerprint bảo
thủ của công cụ phát hành. Khi đầu vào sản phẩm thật sự đổi, vẫn bắt buộc
sửa nguồn → dựng canonical → kiểm → trình duyệt lại phần chịu ảnh hưởng.
