"""Sinh lưới thẻ dự án ZO Math từ _data/cards.yml.

Script này chỉ sinh _partials/card_grid.qmd.
CSS dùng chung nằm riêng ở assets/css/zo_card_grid.css.
Không sửa trực tiếp partial đã sinh; hãy sửa dữ liệu rồi chạy lại script.
"""

from pathlib import Path
import ast
import html
import re
import sys

CSS = Path("assets/css/zo_card_grid.css")


def parse_value(raw: str):
    raw = raw.strip()
    if raw == "":
        return ""
    if raw in {"true", "false"}:
        return raw == "true"
    if raw.startswith("[") and raw.endswith("]"):
        return ast.literal_eval(raw)
    if raw.startswith('"') and raw.endswith('"'):
        return ast.literal_eval(raw)
    if re.fullmatch(r"-?\d+", raw):
        return int(raw)
    return raw


def read_cards(data_path: Path):
    lines = data_path.read_text(encoding="utf-8").splitlines()

    special = []
    groups = []
    mode = None
    current_group = None
    current_item = None

    for line in lines:
        if not line.strip() or line.lstrip().startswith("#"):
            continue

        if line == "special:":
            mode = "special"
            current_group = None
            current_item = None
            continue

        if line == "groups:":
            mode = "groups"
            current_group = None
            current_item = None
            continue

        if mode == "special":
            m_new = re.match(r"^  - ([^:]+):\s*(.*)$", line)
            if m_new:
                current_item = {m_new.group(1): parse_value(m_new.group(2))}
                special.append(current_item)
                continue

            m_field = re.match(r"^    ([^:]+):\s*(.*)$", line)
            if m_field and current_item is not None:
                current_item[m_field.group(1)] = parse_value(m_field.group(2))
                continue

        if mode == "groups":
            m_group = re.match(r"^  - title:\s*(.*)$", line)
            if m_group:
                current_group = {"title": parse_value(m_group.group(1)), "items": []}
                groups.append(current_group)
                current_item = None
                continue

            if re.match(r"^    items:\s*$", line):
                continue

            m_item = re.match(r"^      - ([^:]+):\s*(.*)$", line)
            if m_item and current_group is not None:
                current_item = {m_item.group(1): parse_value(m_item.group(2))}
                current_group["items"].append(current_item)
                continue

            m_field = re.match(r"^        ([^:]+):\s*(.*)$", line)
            if m_field and current_item is not None:
                current_item[m_field.group(1)] = parse_value(m_field.group(2))
                continue

    return special, groups


def make_svg(path: Path, title: str, number=None):
    if path.exists():
        return

    path.parent.mkdir(parents=True, exist_ok=True)
    safe_title = html.escape(str(title))
    label = f"#{number:03d}" if isinstance(number, int) else ""

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="640" height="360" viewBox="0 0 320 180" role="img" aria-label="{safe_title}">
  <rect width="320" height="180" rx="18" fill="#f8fafc"/>
  <path d="M34 90 H286" stroke="#cbd5e1" stroke-width="2"/>
  <path d="M160 28 V142" stroke="#cbd5e1" stroke-width="2"/>
  <path d="M52 118 C98 66, 133 78, 164 92 C197 107, 226 92, 268 54" fill="none" stroke="#111827" stroke-width="4" stroke-linecap="round"/>
  <text x="24" y="30" font-family="Arial, sans-serif" font-size="13" fill="#64748b">{label}</text>
  <text x="160" y="164" text-anchor="middle" font-family="Arial, sans-serif" font-size="18" fill="#111827">{safe_title}</text>
</svg>
'''
    path.write_text(svg, encoding="utf-8")


def card_markdown(item: dict, project_dir: Path, special=False):
    if item.get("visible", True) is False:
        return ""

    status_value = item.get("status", "pending")
    is_published = status_value == "published" and bool(item.get("href"))
    cls = ".is-published" if is_published else ".is-pending"

    title = item.get("title") or item.get("formula") or "Thẻ"
    formula = item.get("formula", "")
    href = item.get("href", "")
    image = item.get("image", "")
    note = item.get("note") or ("Mở bài đã biên soạn." if is_published else "Đang biên soạn.")
    labels = item.get("labels", [])

    if image:
        make_svg(project_dir / image, formula or title, item.get("number"))

    label_text = " ".join(f"[{x}]" for x in labels)
    eyebrow = item.get("eyebrow") or label_text
    badges = "".join(f'<span class="zo-card-badge">[{x}]</span>' for x in labels)
    status = (
        '<span class="zo-card-status is-ready">Đã có bài</span>'
        if is_published
        else '<span class="zo-card-status is-waiting">Đang chờ</span>'
    )

    alt = html.escape(str(title))

    if image and is_published:
        image_md = f"[![{alt}]({image}){{.zo-card-image}}]({href})"
    elif image:
        image_md = f"![{alt}]({image}){{.zo-card-image}}"
    else:
        image_md = ""

    if is_published:
        title_md = f"[{title}]({href})"
    else:
        title_md = str(title)

    if formula and formula != title:
        display_title = f"{title_md}<br><span class=\"zo-card-formula\">{formula}</span>"
    else:
        display_title = title_md

    special_cls = " .is-special" if special else ""

    return f'''::: {{.zo-card {cls}{special_cls}}}
{image_md}

::: {{.zo-card-body}}
::: {{.zo-card-eyebrow}}
{label_text}
:::

::: {{.zo-card-title}}
{display_title}
:::

::: {{.zo-card-note}}
{note}
:::

::: {{.zo-card-meta}}
{badges}{status}
:::
:::
:::
'''


def build(project_dir: Path):
    data_path = project_dir / "_data" / "cards.yml"
    partial_path = project_dir / "_partials" / "card_grid.qmd"

    if not CSS.exists():
        raise SystemExit(f"Thiếu CSS dùng chung: {CSS}")

    if not data_path.exists():
        raise SystemExit(f"Không tìm thấy dữ liệu thẻ: {data_path}")

    special, groups = read_cards(data_path)

    partial_path.parent.mkdir(parents=True, exist_ok=True)

    out = [
        "<!-- Generated by scripts/zo_build_card_grid.py from _data/cards.yml. Do not edit directly. -->",
        "",
    ]
    out.append("::: {.zo-card-grid .zo-card-grid-featured}")
    for item in special:
        out.append(card_markdown(item, project_dir, special=True))
    out.append(":::\n")

    out.append("### Bản đồ các thẻ trong dự án\n")
    out.append("Thẻ đã sáng là nội dung đã có thể đọc. Thẻ mờ là nội dung đang chờ biên soạn.\n")

    for group in groups:
        visible_items = [x for x in group.get("items", []) if x.get("visible", True) is not False]
        if not visible_items:
            continue

        out.append(f"### {group['title']}\n")
        out.append("::: {.zo-card-grid}")
        for item in visible_items:
            out.append(card_markdown(item, project_dir))
        out.append(":::\n")

    partial_path.write_text("\n".join(out), encoding="utf-8")
    all_items = [x for g in groups for x in g.get("items", []) if x.get("visible", True) is not False]
    published = [x for x in all_items if x.get("status") == "published" and x.get("href")]
    pending = [x for x in all_items if not (x.get("status") == "published" and x.get("href"))]

    audit_dir = Path("_audit")
    audit_dir.mkdir(exist_ok=True)
    slug = project_dir.name
    audit = audit_dir / f"{slug}_card_grid_summary.txt"
    audit.write_text(
        "\n".join([
            "Tổng kết lưới thẻ",
            "",
            f"Dự án: {project_dir}",
            f"Số nhóm: {len(groups)}",
            f"Số thẻ đang hiển thị: {len(all_items)}",
            f"Đã có bài: {len(published)}",
            f"Đang chờ: {len(pending)}",
            "",
            "Các thẻ đã có bài:",
            *[f"- {x.get('title') or x.get('formula')} -> {x.get('href')}" for x in published],
        ]) + "\n",
        encoding="utf-8",
    )

    print(f"Đã sinh partial: {partial_path}")
    print(f"Đã ghi audit: {audit}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("Cách dùng: python scripts/zo_build_card_grid.py <thu_muc_du_an>")
    build(Path(sys.argv[1]))
