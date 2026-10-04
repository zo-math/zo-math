from __future__ import annotations

import json
import re
import sys
from pathlib import Path

from pypdf import PdfReader


ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = ROOT.parents[4]
SOURCE = ROOT / "index.qmd"
BASELINE_CSS = REPO_ROOT / "assets/css/zo_on_thi_learning_package.css"
BASELINE_SCRIPT = REPO_ROOT / "assets/html/zo_on_thi_learning_package_script.html"
FILTER = ROOT / "cong_cu" / "r1_g02.lua"
MOBILE_CHECKER = ROOT / "cong_cu" / "kiem_chung_mobile.mjs"
CANONICAL_CONTRACT = (
    REPO_ROOT / "content/thpt/on_thi_toan_thpt/_quy_trinh/quy_chuan_goi_qmd.md"
)
SHARED_COMPONENT_CSS = REPO_ROOT / "assets/css/_zo_learning_components.scss"
SHARED_COMPONENT_LUA = REPO_ROOT / "assets/lua/zo_learning_components.lua"
PROJECT_CONFIG = ROOT / "_quy_trinh/cau_hinh_san_xuat_qmd.yml"
PDF_PROVENANCE = ROOT / "_quy_trinh/ho_so/pdf_provenance.json"
PDF_ACCENT = REPO_ROOT / "assets/logo/zo_math_accent_mark.png"
PACKAGE_README = ROOT / "_quy_trinh/README.md"
PACKAGE_PROFILE = ROOT / "_quy_trinh/ho_so/index.yml"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def count(pattern: str, text: str) -> int:
    return len(re.findall(pattern, text, flags=re.MULTILINE))


def main() -> int:
    text = SOURCE.read_text(encoding="utf-8")
    baseline_css = BASELINE_CSS.read_text(encoding="utf-8")
    baseline_script = BASELINE_SCRIPT.read_text(encoding="utf-8")
    filter_text = FILTER.read_text(encoding="utf-8")
    mobile_checker = MOBILE_CHECKER.read_text(encoding="utf-8")
    canonical_contract = CANONICAL_CONTRACT.read_text(encoding="utf-8")
    shared_component_css = SHARED_COMPONENT_CSS.read_text(encoding="utf-8")
    shared_component_lua = SHARED_COMPONENT_LUA.read_text(encoding="utf-8")
    project_config = PROJECT_CONFIG.read_text(encoding="utf-8")
    package_readme = PACKAGE_README.read_text(encoding="utf-8")
    package_profile = PACKAGE_PROFILE.read_text(encoding="utf-8")

    require(
        all(
            fragment in canonical_contract
            for fragment in (
                "Định danh baseline: `on-thi-learning-components/1.0`.",
                "### Khung trang và điều hướng",
                "### Khối thu gọn và bề mặt",
                "### Nhiệm vụ, ví dụ và liên kết",
                "### Bảng, bảng biến thiên và hình",
                "### Công thức và nguồn đối chiếu",
                "### Hàng rào kiểm định",
                "desktop, 430 px và 390 px",
            )
        ),
        "the canonical baseline 1.0 contract is missing or incomplete",
    )
    require(
        all(
            fragment in shared_component_css
            for fragment in (
                ".zo-learning-task {",
                ".zo-learning-task--pause {",
                ".zo-learning-task--item {",
                ".zo-learning-example,",
                ".zo-learning-guidance {",
                ".zo-learning-solution {",
                ".zo-source-note {",
            )
        ),
        "the shared canonical component CSS contract changed",
    )
    require(
        all(
            fragment in shared_component_lua
            for fragment in (
                "div.classes:includes('zo-learning-guidance')",
                "div.classes:includes('zo-learning-hint')",
                "div.classes:includes('zo-learning-solution')",
                "div.classes:includes('zo-learning-task--pause')",
                "add_class(div.classes, 'zo-learning-task--item')",
            )
        ),
        "the shared canonical component Lua mapping changed",
    )
    require(
        "../../../../../assets/css/zo_on_thi_learning_package.css" in text
        and "../../../../../assets/html/zo_on_thi_learning_package_script.html" in text
        and "../r1_g01/giao_dien/" not in text
        and ".zo-on-thi-package" in baseline_css
        and "body.zo-on-thi-package-page" in baseline_css
        and ".r1-g01" not in baseline_css
        and "document.querySelector('.zo-on-thi-package')" in baseline_script
        and "root.dataset.r1Code" in baseline_script
        and "document.querySelector('.r1-g01')" not in baseline_script,
        "R1-G02 must consume the independent canonical package assets",
    )
    require(
        text.count("::: r1-downloads\n:::") == 1
        and text.count("::: r1-section-downloads\n:::") == 1
        and text.count("::: r1-download-support\n:::") == 1
        and text.count("::: r1-footer\n") == 1,
        "the R1-G02 PDF download view must retain all canonical render placeholders",
    )
    require(
        'src="/assets/logo/zo_math_accent_mark.png"' in filter_text
        and 'src="hinh/dau_nhan_zo.svg"' not in filter_text,
        "the R1-G02 download support must use the published canonical accent asset",
    )

    expected = {
        "guidance summaries": (r"^Cách thực hiện$", 12),
        "hint summaries": (r"^Cần một gợi ý\?$", 4),
        "hint roles": (r"^:{4,} .*\.zo-learning-hint(?:[ .}])", 4),
        "legacy task inputs": (r"^:{3,} .*\.r1-task(?:[ .}])", 41),
        "pause task inputs": (r"^:{3,} .*\.r1-g02-pause(?:[ .}])", 6),
        "solution inputs": (r"^:{4,} .*\.r1-solution(?:[ .}])", 44),
        "content blocks": (r"^:{4,} .*\.zo-block(?:[ .}])", 3),
        "content-block titles": (r"^::: \{\.zo-block-title\}$", 3),
        "unboxed labels": (r"^\[\*\*.*\*\*\]\{[^}\n]*\.r1-unboxed-label[^}\n]*\}$", 5),
        "forward solution links": (r"\]\(#loi-giai", 44),
        "back links": (r"\[Xem đề bài\]\(#", 44),
    }

    guidance_blocks = re.findall(
        r"^:{4,} \{[^\n]*\.r1-guidance[^\n]*\}$", text, flags=re.MULTILINE
    )
    solution_blocks = re.findall(
        r"^:{4,} \{[^\n]*\.r1-solution[^\n]*\}$", text, flags=re.MULTILINE
    )
    task_blocks = re.findall(
        r"^:{3,} \{[^\n]*\.r1-task[^\n]*\}$", text, flags=re.MULTILINE
    )
    summary_blocks = re.findall(
        r"^::: \{[^\n]*\.r1-summary[^\n]*\}$", text, flags=re.MULTILINE
    )
    require(
        len(guidance_blocks) == 16
        and sum(".zo-learning-guidance" in line for line in guidance_blocks) == 12
        and sum(".zo-learning-hint" in line for line in guidance_blocks) == 4,
        "all R1-G02 guidance and hint blocks must declare their canonical learning role",
    )
    require(
        len(solution_blocks) == 44
        and all(".zo-learning-solution" in line for line in solution_blocks),
        "all R1-G02 solution disclosures must declare the canonical solution role",
    )
    require(
        len(task_blocks) == 41
        and all(".zo-learning-task" in line for line in task_blocks)
        and sum(".zo-learning-task--pause" in line for line in task_blocks) == 6
        and sum(".zo-learning-task--item" in line for line in task_blocks) == 35,
        "all R1-G02 tasks must declare exactly one canonical task variant",
    )
    require(
        len(summary_blocks) == 60
        and all(".zo-learning-summary" in line for line in summary_blocks),
        "all R1-G02 disclosure summaries must declare the canonical summary role",
    )
    for label, (pattern, wanted) in expected.items():
        actual = count(pattern, text)
        require(actual == wanted, f"{label}: expected {wanted}, got {actual}")

    require(".zo-block-gray" not in text, "ordinary lesson prose must not use fixed gray content blocks")
    require(
        re.search(r"^:{3,} equation$", text, flags=re.MULTILINE) is None,
        "display equations must not be wrapped in decorative equation blocks",
    )
    require(
        re.findall(
            r"^\[\*\*(.*?)\*\*\]\{[^}\n]*\.r1-unboxed-label[^}\n]*\}$",
            text,
            flags=re.MULTILINE,
        )
        == [
            "Cần phân biệt ba việc: thay số vào biểu thức, tính giá trị hàm số và xét điểm đạt trên $K$.",
            "Không đạt một cận tùy ý chưa đủ để kết luận không có giá trị lớn nhất.",
            "Một điểm hở không loại luôn cả một giá trị.",
            "Chỗ dừng của gói.",
            "Tiêu chí xác nhận đã sửa lỗi.",
        ],
        "the approved unboxed lesson labels changed",
    )

    require(
        all(table_id in text for table_id in ("r1-g02-table-t09", "r1-g02-table-t10")),
        "the canonical opening tables are missing",
    )
    require(
        re.search(
            r'- id: r1-g02-table-t08\n'
            r'    label: "Cách học và kết quả cần giữ lại"\n'
            r'    family: R\n'
            r'    mode: scroll\n'
            r'    widths: \[18, 52, 30\]\n'
            r'    min_width: 42em\n'
            r'    row_header: true',
            text,
        ) is not None,
        "the three-column study table must retain its mobile scroll contract",
    )
    require(
        len(re.findall(r"== 10(?:\D|$)", filter_text)) == 3
        and "must contain 10 entries" in filter_text
        and "expected 10" in filter_text,
        "the Lua ordinary-table inventory must contain exactly 10 entries",
    )
    require(
        "for(const width of [1440,430,390])" in mobile_checker
        and "state.pageOverflow<=1" in mobile_checker
        and "guidance uses the canonical white surface and muted title" in mobile_checker
        and "PDF view renders every canonical download component" in mobile_checker,
        "the responsive audit must check overflow and canonical guidance styling at desktop, 430 px and 390 px",
    )
    require(
        "document.querySelectorAll('.r1-table-scroll-x')" in mobile_checker
        and "table.overflowX==='auto'" in mobile_checker
        and "table.scrollWidth>=table.clientWidth" in mobile_checker,
        "the mobile audit must preserve and verify local horizontal table scrolling",
    )
    require(
        "'.r1-tablist,#quarto-sidebar,nav#TOC,.quarto-toc,.toc,.r1-table-scroll-x,.table-scroll'"
        in mobile_checker,
        "the mobile audit must distinguish intentional local or off-canvas overflow",
    )
    require(
        "const tabEdgePadding = 12;" in baseline_script
        and "selectedTab.offsetLeft - tabEdgePadding" in baseline_script
        and "selectedTab.offsetLeft + selectedTab.offsetWidth + tabEdgePadding" in baseline_script,
        "the shared tab strip must keep the selected mobile tab away from clipped edges",
    )
    require(
        "| Mục tiêu | Việc em cần làm được |" in text
        and "| Nếu còn vướng | Ôn nhanh điều này | Quay lại |" in text,
        "the opening objective or review-routing table changed",
    )
    require(
        re.search(r"\bM0[1-4]\b", text) is None,
        "internal objective codes M01-M04 must not be visible in learner content",
    )
    objective_names = [
        "Gọi đúng đối tượng",
        "Tìm trên đoạn",
        "Giải thích sự tồn tại",
        "Chọn và kiểm tra kết quả",
    ]
    require(
        all(text.count(name) == 2 for name in objective_names),
        "each full objective name must appear in the objective table and result guide",
    )
    require(
        re.search(
            r"^:{5} \{\.zo-learning-task \.zo-learning-task--pause\}\n"
            r".*?\*\*Câu hỏi khởi động 01\.\*\*.*?"
            r"\*\*Câu hỏi khởi động 02\.\*\*.*?"
            r"\*\*Câu hỏi khởi động 03\.\*\*.*?"
            r"^::: answer-link\n\[Xem lời giải\]\(#loi-giai-khoi-dong-01\)\n:::\n^:{5}$",
            text,
            flags=re.MULTILINE | re.DOTALL,
        )
        is not None,
        "the three kickoff questions do not use one canonical task block",
    )
    require(
        "Hãy thử trả lời trên giấy trước khi mở lời giải. Không cần tính điểm; câu nào còn vướng sẽ chỉ ra phần cần ôn."
        in text,
        "the kickoff questions need their approved local introduction",
    )
    lesson_subheadings = re.findall(r"^#### ([1-5]\.\d+\.) ", text, flags=re.MULTILINE)
    require(
        lesson_subheadings == ["1.1.", "2.1.", "2.2.", "2.3.", "3.1.", "3.2.", "4.1.", "4.2."],
        "lesson subsection numbering is not canonical",
    )
    answer_links = re.findall(
        r"^::: answer-link\n\[([^\]]+)\]\(#([^)]+)\)\n:::$",
        text,
        flags=re.MULTILINE,
    )
    require(len(answer_links) == 88, f"answer links: expected 88, got {len(answer_links)}")
    require(
        [label for label, _ in answer_links].count("Xem lời giải") == 44
        and [label for label, _ in answer_links].count("Xem đề bài") == 44,
        "answer-link labels must use the two canonical short forms",
    )
    require(
        ("Xem đề bài", "ba-câu-khởi-động") in answer_links,
        "the kickoff solution must return to the kickoff-question block",
    )
    phase2_task_anchors = (
        "l11",
        "s-k-e01", "s-k-e02", "s-k-e03", "s-k-e04", "s-k-e05", "s-k-e06",
        "s-o-e01", "s-o-e02", "s-o-e03", "s-o-e04", "s-o-e05", "s-o-e06",
        "s-p02",
    )
    for task_anchor in phase2_task_anchors:
        solution_anchor = f"loi-giai-{task_anchor}"
        require(
            text.count(f"{{#{task_anchor} ") == 1
            and text.count(f"{{#{solution_anchor} ") == 1
            and ("Xem lời giải", solution_anchor) in answer_links
            and ("Xem đề bài", task_anchor) in answer_links,
            f"Pha 2 task/solution pair is incomplete: {task_anchor}",
        )
    require(
        text.index("## Sửa lỗi {#sua-loi}")
        < text.index("{#thu-lai-chuyen-giao")
        < text.index("## Ôn lại {#on-lai}"),
        "the transfer retry task must belong to the correction section",
    )
    require(
        "### Chọn bài tập khắc phục lỗi {#chọn-bài-tập-khắc-phục-lỗi}" in text,
        "the correction-routing table needs its canonical heading",
    )
    require(
        count(r"^:{4,} \{\.zo-learning-example\}$", text) == 1
        and "#### 3.2. Ví dụ làm mẫu --- So sánh giá trị, không so sánh hoành độ {.r1-example-heading .zo-learning-example-heading}"
        in text,
        "the worked example must use the canonical example role",
    )
    require(
        all(
            fragment in text
            for fragment in (
                "{.r1-figure r1-id=\"fig-r1-g02-do-thi-01\"}",
                "Hình 01 — Đồ thị của $f$ trên $K=[-1;2)$.",
                "{.r1-figure r1-id=\"fig-r1-g02-do-thi-02\"}",
                "Hình 02 — Phần đồ thị của $g$ trên $K=(1;3]$;",
            )
        )
        and count(r"^::: r1-figcaption$", text) == 2,
        "the two graphs must use canonical figure wrappers and captions",
    )
    require(
        re.search(r"\[Bài [^\]]+\]\(#s\d\d\)", text) is None
        and "Bài tập khắc phục lỗi 01" in text
        and "Bài tập khắc phục lỗi 05" in text,
        "the correction-routing table must use static canonical cell content",
    )
    require(
        re.search(r"\b(?:SGK|SGV)\b|\btr\.", text) is None,
        "reference lines must use full names and words",
    )
    require(
        count(r"\]\{\.zo-source-note\}$", text) == 3
        and "Sách giáo khoa Toán 12, tập một" in text
        and "Sách giáo viên Toán 12" in text,
        "reference notes must use complete canonical sentences",
    )

    ids = re.findall(r"\{#([^ }]+)", text)
    duplicate_ids = sorted({value for value in ids if ids.count(value) > 1})
    require(not duplicate_ids, "duplicate ids: " + ", ".join(duplicate_ids))

    anchors = set(ids)
    targets = re.findall(r"\]\(#([^)]+)\)", text)
    missing = sorted({target for target in targets if target not in anchors})
    require(not missing, "missing local link targets: " + ", ".join(missing))

    hint_blocks = re.findall(
        r"^:{4,} \{[^\n]*\.zo-learning-hint[^\n]*\}\n(.*?)^:{4,}\s*$",
        text,
        flags=re.MULTILINE | re.DOTALL,
    )
    require(len(hint_blocks) == 4, "could not isolate all four hint blocks")
    require(
        all("Cần một gợi ý?" in block for block in hint_blocks),
        "a hint role does not use the approved summary",
    )
    require(
        all(fragment in baseline_css for fragment in (
            ".zo-on-thi-package .zo-variation-image {\n  margin-inline: auto;",
            ".zo-on-thi-package figure img {",
            "display: block;",
            "margin-inline: auto;",
        )),
        "the inherited R1-G01 baseline does not center graphs and variation assets",
    )
    require(
        all(fragment in baseline_css for fragment in (
            ".zo-on-thi-package details > summary {",
            "display: flex;",
            "align-items: center;",
            "min-height: 44px;",
            "box-sizing: border-box;",
            "padding: .4rem 3rem .4rem .85rem;",
        )),
        "the inherited R1-G01 baseline does not normalize every disclosure header",
    )
    require(
        ".zo-on-thi-package .r1-section-toc > summary," in baseline_css
        and ".zo-on-thi-package details.zo-learning-guidance > summary { color: var(--r1-muted); }"
        in baseline_css,
        "guidance titles must use the same muted color as the lesson contents title",
    )
    variation_captions = re.findall(r'\.r1-bbt\s+bbt="[^"]+"\s+caption="([^"]+)"', text)
    require(
        len(variation_captions) == 2 and all(value.endswith(".") for value in variation_captions),
        "all variation captions must end with a full stop",
    )

    pause_contract = {
        "cau-hoi-bai-hoc-01": ("Thử trước khi đọc tiếp.", "loi-giai-bai-hoc-01"),
        "cau-hoi-bai-hoc-02": ("Dừng để nghĩ.", "loi-giai-bai-hoc-02"),
        "cau-hoi-bai-hoc-03": ("Kiểm tra điều kiện.", "loi-giai-bai-hoc-03"),
        "cau-hoi-bai-hoc-04": ("Trước khi xem:", "loi-giai-bai-hoc-04"),
        "cau-hoi-bai-hoc-05": ("Thử kiểm tra cách làm tròn.", "loi-giai-bai-hoc-05"),
        "thu-lai-chuyen-giao": (
            "Sau khi sửa lỗi ở Bài luyện tập 07, thử một câu mới.",
            "loi-giai-thu-lai-chuyen-giao",
        ),
    }
    for block_id, (label, target) in pause_contract.items():
        pattern = (
            rf'^::: \{{#{re.escape(block_id)} [^\n]*\.r1-task [^\n]*\.r1-g02-pause[^\n]*\}}\n'
            rf'\[\*\*{re.escape(label)}\*\*\]\{{\.r1-task-label\}}.*?'
            rf'^::: answer-link\n\[[^\]]+\]\(#{re.escape(target)}\)\n:::\n:::$'
        )
        require(
            re.search(pattern, text, flags=re.MULTILINE | re.DOTALL) is not None,
            f"pause task {block_id} does not keep its canonical label and answer link inside the block",
        )

    pdf_variants = (
        "full", "student", "bai_hoc", "luyen_tap",
        "kiem_tra", "sua_loi", "on_lai", "loi_giai",
    )
    pdf_outputs = {
        "full": "index.pdf",
        "student": "index_hoc_sinh.pdf",
        "bai_hoc": "index_bai_hoc.pdf",
        "luyen_tap": "index_luyen_tap.pdf",
        "kiem_tra": "index_kiem_tra.pdf",
        "sua_loi": "index_sua_loi.pdf",
        "on_lai": "index_on_lai.pdf",
        "loi_giai": "index_loi_giai.pdf",
    }
    require(
        "pdf_provenance_manifest: _quy_trinh/ho_so/pdf_provenance.json" in project_config
        and all(re.search(rf"^    {variant}:$", project_config, flags=re.MULTILINE) for variant in pdf_variants),
        "the canonical eight-variant PDF registry is incomplete",
    )
    require(
        PDF_ACCENT.is_file()
        and "assets/logo/zo_math_accent_mark.png" in project_config
        and "Dau_nhan_ZO_Xem_truoc.png" not in project_config
        and filter_text.count(
            "\\includegraphics[width=46mm]{zo_math_accent_mark.png}"
        ) == 1
        and filter_text.count(
            "\\includegraphics[width=38mm]{zo_math_accent_mark.png}"
        ) == 1,
        "the PDF cover and ending must use the cropped canonical accent asset",
    )
    require(
        project_config.count(
            'subtitle: "Từ cực trị cục bộ đến so sánh trên toàn bộ tập đang xét —'
        ) == 8,
        "all PDF variants must use the approved thematic subtitle",
    )
    require(
        "or div.classes:includes('r1-guidance')" in filter_text
        and "block.identifier == 'loi-giai-kiem-tra'" in filter_text
        and "block.identifier == 'r1-g02-table-t01'" in filter_text,
        "the 6B1.1 guidance and page-break guards are incomplete",
    )
    require(
        "\\noindent\\begin{minipage}{\\linewidth}" in filter_text
        and "\\end{center}\n\\end{minipage}" in filter_text,
        "the PDF ending must remain an indivisible page-layout unit",
    )
    require(
        all(f"  - variant: {variant}" in text for variant in pdf_variants[2:]),
        "the six section projection contracts are incomplete",
    )
    require(PDF_PROVENANCE.is_file(), "the R1-G02 PDF provenance manifest is missing")
    provenance = json.loads(PDF_PROVENANCE.read_text(encoding="utf-8"))
    built = {item["name"]: item for item in provenance.get("variants", [])}
    expected_pdf_pages = {
        "full": 34,
        "student": 20,
        "bai_hoc": 10,
        "luyen_tap": 6,
        "kiem_tra": 4,
        "sua_loi": 7,
        "on_lai": 4,
        "loi_giai": 16,
    }
    require(
        all(text.count(f"  - {output}") == 1 for output in pdf_outputs.values()),
        "all eight canonical PDFs must be declared exactly once as page resources",
    )
    require(
        re.search(
            r"r1-download-files:\n"
            r"  - href: index_hoc_sinh\.pdf\n.*?    pages: 20\n"
            r"  - href: index\.pdf\n.*?    pages: 34\n",
            text,
            flags=re.DOTALL,
        ) is not None,
        "the two canonical download cards must lock the current 20/34 page metadata",
    )
    require(
        "Baseline PDF canonical của R1-G02" in package_readme
        and "`full` 26, `student` 17" in package_readme
        and "`loi_giai` 10" in package_readme,
        "the package README does not record the accepted R1-G02 PDF matrix",
    )
    require(
        "production: accepted" in package_profile
        and "publication: pending" in package_profile
        and "user_confirmed: true" in package_profile
        and "pdf_canonical: accepted_2026_09_30" in package_profile
        and "final: accepted" in package_profile,
        "the package acceptance profile is not closed while publication remains pending",
    )
    require(
        "R1-G02 đã được nghiệm thu thị giác và chốt ở Pha 6C" in canonical_contract
        and "`full` 26 trang, `student` 17 trang" in canonical_contract
        and "`loi_giai` 10 trang" in canonical_contract,
        "the shared canonical contract does not record the accepted R1-G02 PDF baseline",
    )
    require(
        tuple(item["name"] for item in provenance.get("variants", [])) == pdf_variants,
        "the PDF provenance variant order does not match the canonical registry",
    )
    for variant, expected_pages in expected_pdf_pages.items():
        require(variant in built, f"the {variant} variant is missing from PDF provenance")
        output = REPO_ROOT / built[variant]["output"]["path"]
        require(output.is_file() and output.stat().st_size > 1024, f"the {variant} PDF is missing")
        require(
            len(PdfReader(output).pages) == expected_pages,
            f"the {variant} PDF does not contain exactly {expected_pages} pages",
        )
        require(
            built[variant].get("inventory", {}).get("pages") == expected_pages,
            f"the {variant} page inventory is not locked at {expected_pages}",
        )

    print("R1-G02 canonical components: PASS")
    print("12 guidance | 4 hints | 42 tasks (7 pause, 35 item) | 44 solutions")
    print("3 titled theory blocks | 5 unboxed lesson labels | 44 forward links | 44 back links")
    print("8 PDF variants built | pages: 34, 20, 10, 6, 4, 7, 4, 16")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except AssertionError as error:
        print(f"R1-G02 canonical components: FAIL: {error}", file=sys.stderr)
        raise SystemExit(1)
