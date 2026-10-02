from __future__ import annotations

import json
from pathlib import Path

import yaml


PACKAGE_ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = PACKAGE_ROOT / "du_lieu" / "ngan_hang.json"
HISTORY_ROOT = PACKAGE_ROOT / "_quy_trinh" / "lich_su" / "v1_0"
PUBLIC_GUIDE_PATH = PACKAGE_ROOT / "du_lieu" / "huong_dan_cong_khai.md"
ANALYSIS_GUIDE_PATH = PACKAGE_ROOT / "du_lieu" / "huong_dan_phan_tich.md"
QMD_PATH = PACKAGE_ROOT / "index.qmd"
MANIFEST_PATH = PACKAGE_ROOT / "_quy_trinh" / "manifest_chuyen_doi.yml"

PUBLIC_FIELDS = ("id", "title", "prereq", "format", "minutes", "question")
PRIVATE_FIELDS = (
    "version", "r", "n", "objective", "clusters", "support", "ct", "source",
    "level", "capacity", "answer", "solution", "criteria", "error", "repair",
    "retest_id", "retest", "reanswer", "resolution", "check", "family",
    "history", "author", "scope",
)

def normalized(text: str) -> str:
    return text.replace("\r\n", "\n").replace("\r", "\n").rstrip() + "\n"


def strip_front_matter(text: str) -> str:
    lines = normalized(text).splitlines()
    if lines and lines[0] == "---":
        try:
            end = lines.index("---", 1)
        except ValueError as error:
            raise ValueError("front matter lịch sử chưa đóng") from error
        lines = lines[end + 1 :]
    return normalized("\n".join(line for line in lines if line.strip() != r"\clearpage"))


def canonical_resource_paths(text: str) -> str:
    return text.replace("(src/hinh_hop.pdf)", "(hinh/hinh_hop.pdf)")


def scalar(value: object) -> str:
    if isinstance(value, list):
        return "\n".join(f"- {entry}" for entry in value)
    return str(value)


def primary_block(item: dict) -> str:
    identifier = item["id"].lower()
    question = canonical_resource_paths(item["question"])
    if item["id"] == "D0-R1-03":
        sign_table = "\n".join(line for line in question.splitlines() if line.startswith("|"))
        if len(sign_table.splitlines()) != 3:
            raise ValueError("Bảng dấu nguồn R1-03 đã đổi cấu trúc; cần rà lại phép chiếu")
        question = question.replace(sign_table, '::: {.zo-variation bbt="BBT01"}\n:::')
    if item["id"] == "D0-R7-01":
        question = question.replace('; $F_', ';\n\n$F_')
    if item["id"] == "D0-R7-03":
        question = question.replace(': a)', ':\n\na)').replace('; b)', ';\n\nb)')
    return normalized(f'''<!-- D0_PRIMARY_START {item["id"]} -->
:::: {{#{identifier} .zo-learning-task .zo-learning-task--item .d0-primary-task d0-id="{item["id"]}" d0-family="{item["family"]}"}}
[Bài {item["n"]:02d}]{{.d0-task-number}} [{item["r"]}]{{.d0-task-code}}

#### {item["title"]}

::: {{.d0-task-meta}}
**Điều kiện học trước:** {item["prereq"]}

**Hình thức:** {item["format"]} · **Thời gian gợi ý:** {item["minutes"]} phút
:::

::: {{.d0-task-prompt}}
{question}
:::
::::
<!-- D0_PRIMARY_END {item["id"]} -->''')


def private_record(item: dict) -> str:
    fields = []
    for name in PRIVATE_FIELDS:
        fields.append(f"#### `{name}`\n\n{canonical_resource_paths(scalar(item[name]))}")
    identifier = item["id"].lower()
    retest_identifier = item["retest_id"].lower()
    return normalized(f'''<!-- D0_PRIVATE_RECORD_START {item["id"]} -->
:::: {{#ho-so-{identifier} .d0-item-record d0-id="{item["id"]}" d0-family="{item["family"]}"}}
### Hồ sơ {item["id"]} — {item["title"]}

**Các trường công khai đã chiếu:** {", ".join(PUBLIC_FIELDS)}

{chr(10).join(fields)}

:::: {{#{retest_identifier} .zo-learning-task .d0-retest-task d0-id="{item["retest_id"]}" d0-family="{item["family"]}"}}
### {item["retest_id"]} — Thử lại

{canonical_resource_paths(item["retest"])}
::::

:::: {{#loi-giai-{identifier} .zo-learning-solution .d0-primary-solution d0-id="{item["id"]}"}}
### Lời giải {item["id"]}

{item["solution"]}
::::

:::: {{#loi-giai-{retest_identifier} .zo-learning-solution .d0-retest-solution d0-id="{item["retest_id"]}"}}
### Đáp án thử lại {item["retest_id"]}

{item["resolution"]}
::::
::::
<!-- D0_PRIVATE_RECORD_END {item["id"]} -->''')


def build_qmd() -> str:
    data = json.loads(DATA_PATH.read_text(encoding="utf-8"))
    manifest = yaml.safe_load(MANIFEST_PATH.read_text(encoding="utf-8"))
    strand_specs = manifest["strand_contract"]["strands"]
    public_text = normalized(PUBLIC_GUIDE_PATH.read_text(encoding="utf-8"))
    public_parts = public_text.split("\n## ")
    public_sections = {}
    for index, part in enumerate(public_parts):
        section = part if index == 0 else "## " + part
        heading, body = section.split("\n", 1)
        identifier = heading.rsplit("{#", 1)[1].rstrip("}")
        if identifier in public_sections:
            raise ValueError(f"trùng section hướng dẫn: {identifier}")
        public_sections[identifier] = normalized(body).strip()
    if list(public_sections) != ["bat-dau", "khai-bao-pham-vi", "doc-ket-qua", "thu-lai", "tai-pdf"]:
        raise ValueError("hướng dẫn công khai phải có đúng năm section theo hợp đồng")
    analysis = strip_front_matter(ANALYSIS_GUIDE_PATH.read_text(encoding="utf-8"))

    strands = []
    for strand, spec in strand_specs.items():
        title = spec["title"]
        tasks = "\n".join(primary_block(item) for item in data["items"] if item["r"] == strand)
        strands.append(f"### {strand} — {title} {{#mach-{strand.lower()}}}\n\n{tasks}")

    records = "\n".join(private_record(item) for item in data["items"])
    return normalized(f'''---
title: "Khảo sát và định vị đầu vào"
lang: vi
draft: false
toc: true
toc-depth: 2
sidebar: on-thi
number-sections: false
page-layout: article
body-classes: zo-page-article zo-meta-hidden zo-on-thi-package-page d0-page
filters:
  - cong_cu/d0.lua
format:
  html:
    subtitle: "Xác định việc cần ôn trước"
    title-block-style: default
    title-block-banner: false
    html-math-method: mathml
    anchor-sections: false
    fig-responsive: false
    css:
      - ../../../../../assets/css/zo_on_thi_learning_package.css
      - giao_dien/d0.css
    include-after-body:
      - giao_dien/d0_script.html
---

<!-- D0_QMD_GENERATED_BY cong_cu/tao_qmd_chuyen_doi.py -->

::::: {{.zo-on-thi-package .d0-package data-d0-title="Khảo sát và định vị đầu vào"}}

## Bắt đầu {{#bat-dau}}

{public_sections["bat-dau"]}

## Khai báo phạm vi {{#khai-bao-pham-vi}}

{public_sections["khai-bao-pham-vi"]}

## Khảo sát {{#khao-sat}}

{chr(10).join(strands)}

## Đọc kết quả {{#doc-ket-qua}}

{public_sections["doc-ket-qua"]}

## Khảo sát bổ sung {{#thu-lai}}

{public_sections["thu-lai"]}

:::: {{.d0-private .d0-facilitator-material}}
## Dành cho người hướng dẫn {{#danh-cho-nguoi-huong-dan}}

{analysis}

## Hồ sơ nội dung và câu thử lại {{#ho-so-noi-dung}}

{records}
::::

## Tải PDF {{#tai-pdf}}

{public_sections["tai-pdf"]}
:::::
''')


def main() -> int:
    if (PACKAGE_ROOT / '_quy_trinh' / 'noi_dung_da_duyet.json').exists():
        raise RuntimeError('Nguồn hiện hành là index.qmd đã tích hợp nội dung được duyệt; không tái sinh từ hướng dẫn lịch sử 6B.')
    QMD_PATH.write_text(build_qmd(), encoding="utf-8", newline="\n")
    print(f"Đã tạo ứng viên chuyển đổi: {QMD_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
