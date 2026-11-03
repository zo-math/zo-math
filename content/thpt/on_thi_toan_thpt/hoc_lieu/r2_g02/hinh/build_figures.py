"""Ba hình bản thảo R2-G02; dùng khung thống kê native đang có của ZO Math."""
from pathlib import Path
import argparse
import json
import runpy

parser = argparse.ArgumentParser()
parser.add_argument("--repo", type=Path)
args = parser.parse_args()
HERE = Path(__file__).resolve().parent
REPO = args.repo or next(p for p in HERE.parents if (p / "scripts/zo_python.py").is_file())
helper = REPO / "content/thpt/on_thi_toan_thpt/hoc_lieu/r2_g01/hinh/y_tuong_v01/build_figures.py"
native = runpy.run_path(str(helper))
plt, palette = native["plt"], native["style"]()
plt.rcParams.update({"font.size": 14})
axis, dots = native["axis"], native["dots"]

def save(fig, name, title):
    fig.savefig(HERE / (name + ".svg"), bbox_inches="tight", metadata={"Date": None, "Title": title})
    fig.savefig(HERE / (name + ".png"), dpi=150, bbox_inches="tight", facecolor="white")
    plt.close(fig)

data = {
    "cung_trung_tam": {"A": [8, 9, 10, 11, 12], "B": [2, 6, 10, 14, 18]},
    "gia_tri_bat_thuong": {"values": [2, 4, 4, 5, 5, 6, 8, 14], "Q1": 4, "median": 5, "Q3": 7, "lower": -0.5, "upper": 11.5},
    "cung_bang_nhom": {"A": [1, 1, 19, 19], "B": [9, 9, 11, 11], "edges": [0, 10, 20], "midpoints": [5, 15]},
}
(HERE / "data.json").write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

fig, axs = plt.subplots(2, 1, figsize=(5.2, 5.4))
for ax, (name, values) in zip(axs, data["cung_trung_tam"].items()):
    axis(ax, palette)
    dots(ax, values, palette)
    ax.set_xlim(0, 20); ax.set_ylim(0, 1.0)
    ax.set_xticks([0, 5, 10, 15, 20])
    ax.vlines(10, 0, .65, color=palette["red-5"], lw=1.2, linestyles="dashed")
    ax.text(10, .78, "Trung bình = 10", ha="center", color=palette["red-5"])
    ax.set_title("Mẫu " + name + " · năm quan sát", loc="left", fontsize=15, pad=12)
    ax.set_xlabel("Giá trị quan sát")
fig.tight_layout(h_pad=2)
save(fig, "cung_trung_tam", "Cùng trung tâm, khác độ trải")

fig, ax = plt.subplots(figsize=(5.2, 5.0))
axis(ax, palette)
ax.set_xlim(-2, 16); ax.set_ylim(0, 2.0)
ax.set_xticks([0, 2, 4, 6, 8, 10, 12, 14])
dots(ax, data["gia_tri_bat_thuong"]["values"], palette)
from matplotlib.patches import Rectangle
ax.add_patch(Rectangle((4, 1.04), 3, .32, facecolor=palette["yellow-1"], edgecolor=palette["gray-7"], lw=1))
ax.vlines(5, 1.04, 1.36, color=palette["red-5"], lw=1.6)
ax.text(4, 1.46, "Q₁ = 4", ha="right")
ax.text(7, 1.46, "Q₃ = 7", ha="left")
ax.annotate("Trung vị = 5", (5, 1.2), (5, 1.78), ha="center",
            arrowprops={"arrowstyle": "-", "lw": .7, "color": palette["gray-6"]})
for x, text in [(-.5, "Ngưỡng dưới\n−0,5"), (11.5, "Ngưỡng trên\n11,5")]:
    ax.vlines(x, 0, .95, color=palette["gray-6"], lw=1, linestyles="dashed")
    ax.text(x, 1.0, text, ha="center", fontsize=13)
ax.annotate("14 vượt\nngưỡng", (14, .24), (14, .60), ha="center", color=palette["red-5"],
            arrowprops={"arrowstyle": "-", "lw": .8, "color": palette["red-5"]})
ax.set_xlabel("Giá trị quan sát")
fig.tight_layout()
save(fig, "gia_tri_bat_thuong", "Ngưỡng phát hiện và giá trị quan sát")

fig, axs = plt.subplots(2, 1, figsize=(5.2, 7.2))
for ax, name in zip(axs, ["A", "B"]):
    axis(ax, palette)
    values = data["cung_bang_nhom"][name]
    ax.set_xlim(-1, 21); ax.set_ylim(0, 1.65)
    for lo, hi in [(0, 10), (10, 20)]:
        ax.axvspan(lo, hi, color=palette["yellow-1"], ec=palette["gray-3"], lw=.8, zorder=0)
        ax.text((lo+hi)/2, 1.32, f"[{lo}; {hi})\n2 quan sát", ha="center", fontsize=13)
    dots(ax, values, palette)
    for x in [5, 15]:
        ax.plot(x, .95, marker="D", color=palette["red-5"], ms=6)
        ax.text(x, .61, f"Đại diện {x}", ha="center", color=palette["red-5"], fontsize=13)
    variance = 81 if name == "A" else 1
    ax.set_title(f"Mẫu {name}: " + "; ".join(map(str, values)) + f"\nPhương sai thật = {variance}", loc="left", fontsize=15, pad=12)
    ax.set_xticks([0, 5, 10, 15, 20])
    ax.set_xlabel("Giá trị quan sát")
fig.tight_layout(h_pad=2)
save(fig, "cung_bang_nhom", "Cùng bảng nhóm, khác phương sai thật")
