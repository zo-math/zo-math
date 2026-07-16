#!/usr/bin/env python3
"""Sinh lưới thẻ dự án ZO Math từ _data/cards.yml.

Phiên bản này dùng MỘT renderer SVG thống nhất cho tất cả các thẻ hàm số.
- Đọc YAML thật bằng yaml.safe_load.
- Vẽ đồ thị bằng lấy mẫu số học từ công thức/biểu thức.
- Không dùng draw_kind để quyết định kiểu vẽ riêng lẻ.
- Có thể tinh chỉnh riêng từng thẻ qua plot_expr / plot / breaks trong cards.yml.
"""
from __future__ import annotations

import html
import math
import re
import sys
import warnings
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple

import yaml

SVG_W = 320
SVG_H = 180
PAD_X = 24
PAD_Y = 22
STROKE = "#5F6B7A"
STROKE_WIDTH = 2.5
BG = "none"
SPECIAL_STROKE = "#1F2937"


def _cbrt(x: float) -> float:
    return math.copysign(abs(x) ** (1.0 / 3.0), x)


def _sgn(x: float) -> float:
    return -1.0 if x < 0 else (1.0 if x > 0 else 0.0)


def _H(x: float) -> float:
    return 0.0 if x < 0 else 1.0


def _tri(x: float) -> float:
    ax = abs(x)
    return 1.0 - ax if ax <= 1.0 else 0.0


def _sinc(x: float) -> float:
    return 1.0 if abs(x) < 1e-8 else math.sin(x) / x


def _softplus(x: float) -> float:
    if x > 20:
        return x
    if x < -20:
        return math.exp(x)
    return math.log1p(math.exp(x))


def _elu(x: float) -> float:
    return x if x >= 0 else math.exp(x) - 1.0


def _gelu(x: float) -> float:
    return 0.5 * x * (1.0 + math.tanh(math.sqrt(2.0 / math.pi) * (x + 0.044715 * x**3)))


def _mish(x: float) -> float:
    return x * math.tanh(_softplus(x))


def _j0(x: float) -> float:
    # Bessel J_0(x) by its convergent Maclaurin series, enough for thumbnail range.
    term = 1.0
    total = 1.0
    xx = (x * x) / 4.0
    for k in range(1, 32):
        term *= -xx / (k * k)
        total += term
        if abs(term) < 1e-12:
            break
    return total


SAFE_FUNCS = {
    "sin": math.sin,
    "cos": math.cos,
    "tan": math.tan,
    "asin": math.asin,
    "acos": math.acos,
    "atan": math.atan,
    "arcsin": math.asin,
    "arccos": math.acos,
    "arctan": math.atan,
    "sinh": math.sinh,
    "cosh": math.cosh,
    "tanh": math.tanh,
    "asinh": math.asinh,
    "acosh": math.acosh,
    "atanh": math.atanh,
    "exp": math.exp,
    "sqrt": math.sqrt,
    "cbrt": _cbrt,
    "log": math.log,
    "ln": math.log,
    "floor": math.floor,
    "ceil": math.ceil,
    "gamma": math.gamma,
    "erf": math.erf,
    "abs": abs,
    "max": max,
    "min": min,
    "sgn": _sgn,
    "H": _H,
    "tri": _tri,
    "sinc": _sinc,
    "softplus": _softplus,
    "elu": _elu,
    "gelu": _gelu,
    "mish": _mish,
    "j0": _j0,
    "pi": math.pi,
    "e": math.e,
}

PARAM_DEFAULTS = {
    "a": 1.0,
    "b": 0.6,
    "c": 0.8,
    "d": -0.5,
    "e": 0.3,
    "h": 0.8,
    "k": -0.4,
    "n": 5.0,
}

# Các công thức có tham số/ý nghĩa họ hàm cần ánh xạ mẫu điển hình.
SPEC_OVERRIDES: Dict[str, Dict[str, Any]] = {
    "y=ax+b": {"expr": "1.0*x+0.6", "xlim": (-3, 3), "ylim": (-3, 3)},
    "y=a(x-h)^2+k": {"expr": "1.0*(x-0.8)**2-0.4", "xlim": (-3, 3), "ylim": (-2.5, 3.5)},
    "y=ax^2+bx+c": {"expr": "1.0*x**2-0.8*x-0.4", "xlim": (-3, 3), "ylim": (-2.5, 5.5)},
    "y=ax^3+bx^2+cx+d": {"expr": "1.0*x**3-1.0*x+0.2", "xlim": (-2.4, 2.4), "ylim": (-5.5, 5.5)},
    "y=ax^4+bx^3+cx^2+dx+e": {"expr": "1.0*x**4-1.8*x**2+0.2*x+0.4", "xlim": (-2.2, 2.2), "ylim": (-2.5, 6.5)},
    "y=ax^4+bx^2+c": {"expr": "1.0*x**4-1.3*x**2+0.2", "xlim": (-2.2, 2.2), "ylim": (-1.5, 5.5)},
    r"y=x^n,n\\geq5": {"expr": "x**5", "xlim": (-1.5, 1.5), "ylim": (-6, 6)},
    "y=\frac{ax+b}{cx+d}": {"expr": "(1.0*x+0.6)/(0.7*x-0.8)", "xlim": (-4, 4), "ylim": (-5, 5), "breaks": [0.8/0.7]},
    "y=\frac{x^2+bx+c}{x+a}": {"expr": "(x**2+0.4*x-1.0)/(x+0.9)", "xlim": (-4, 4), "ylim": (-6, 6), "breaks": [-0.9]},
    r"y=\\sin\\left(\\frac{1}{x}\\right)": {"expr": "sin(1/x)", "xlim": (-1.2, 1.2), "ylim": (-1.2, 1.2), "breaks": [0], "samples": 2400},
}


# Các thẻ đặc biệt/khó được khai báo bằng tham số của CÙNG renderer lấy mẫu.
# Không phải cơ chế vẽ thứ hai: tất cả vẫn đi qua sample_segments() và render_formula_svg().
NUM_OVERRIDES: Dict[int, Dict[str, Any]] = {
    79: {"expr": "cbrt(x)", "xlim": (-4, 4), "ylim": (-2, 2)},
    83: {"expr": "x**1.6", "xlim": (0, 4), "ylim": (0, 9)},
    84: {"expr": "(x-0.8)**1.6-0.3", "xlim": (0.8, 5), "ylim": (-0.5, 9)},
    85: {"expr": "abs(x)", "xlim": (-3, 3), "ylim": (-0.2, 3.5)},
    86: {"expr": "abs(x-1)", "xlim": (-3, 4), "ylim": (-0.2, 4)},
    87: {"expr": "sgn(x)", "xlim": (-3, 3), "ylim": (-1.3, 1.3), "breaks": [0]},
    88: {"expr": "H(x-0.5)", "xlim": (-3, 3), "ylim": (-0.3, 1.4), "breaks": [0.5]},
    89: {"expr": "floor(x)", "xlim": (-3, 3), "ylim": (-3.2, 3.2), "breaks": [-3, -2, -1, 0, 1, 2, 3]},
    90: {"expr": "ceil(x)", "xlim": (-3, 3), "ylim": (-3.2, 3.2), "breaks": [-2, -1, 0, 1, 2]},
    91: {"expr": "x-floor(x)", "xlim": (-3, 3), "ylim": (-0.05, 1.05), "breaks": [-3, -2, -1, 0, 1, 2, 3]},
    92: {"expr": "max(0,x)", "xlim": (-3, 3), "ylim": (-0.3, 3.2)},
    93: {"expr": "max(0.18*x,x)", "xlim": (-3, 3), "ylim": (-1, 3.2)},
    94: {"expr": "tri(x)", "xlim": (-2, 2), "ylim": (-0.2, 1.2)},
    95: {"expr": "sin(x)", "xlim": (-6.283185307, 6.283185307), "ylim": (-1.25, 1.25), "samples": 1400},
    96: {"expr": "cos(x)", "xlim": (-6.283185307, 6.283185307), "ylim": (-1.25, 1.25), "samples": 1400},
    97: {"expr": "tan(x)", "xlim": (-4.71238898038, 1.57079632679), "ylim": (-4.5, 4.5), "breaks": [-4.71238898038, -1.57079632679, 1.57079632679], "samples": 2200},
    98: {"expr": "1/tan(x)", "xlim": (-3.1, 3.1), "ylim": (-4.5, 4.5), "breaks": [-3.141592654, 0, 3.141592654], "samples": 1600},
    101: {"expr": "1.0*sin(1.6*x+0.4)", "xlim": (-4, 4), "ylim": (-1.3, 1.3), "samples": 1400},
    102: {"expr": "abs(sin(x))", "xlim": (-6.283185307, 6.283185307), "ylim": (-0.1, 1.2), "samples": 1400},
    103: {"expr": "sin(x)+cos(x)", "xlim": (-6.283185307, 6.283185307), "ylim": (-1.6, 1.6), "samples": 1400},
    104: {"expr": "1/cos(x)", "xlim": (-3.1, 3.1), "ylim": (-5, 5), "breaks": [-1.57079632679, 1.57079632679], "samples": 1600},
    105: {"expr": "1/sin(x)", "xlim": (-3.1, 3.1), "ylim": (-5, 5), "breaks": [-3.141592654, 0, 3.141592654], "samples": 1600},
    106: {"expr": "asin(x)", "xlim": (-1.0, 1.0), "ylim": (-1.7, 1.7), "samples": 1400},
    107: {"expr": "acos(x)", "xlim": (-1, 1), "ylim": (-0.2, 3.3)},
    108: {"expr": "atan(x)", "xlim": (-5, 5), "ylim": (-1.7, 1.7)},
    109: {"expr": "pi/2-atan(x)", "xlim": (-5, 5), "ylim": (-0.2, 3.3)},
    110: {"expr": "atan(1.5*x)+0.3", "xlim": (-5, 5), "ylim": (-1.5, 2.0)},
    111: {"expr": "exp(x)", "xlim": (-3.0, 2.0), "ylim": (-0.1, 8.0)},
    114: {"expr": "log(x)", "xlim": (0.05, 6), "ylim": (-3, 2.2), "breaks": [0]},
    115: {"expr": "log(x)/log(2)", "xlim": (0.05, 6), "ylim": (-4, 3), "breaks": [0]},
    120: {"expr": "x*exp(x)", "xlim": (-3, 2), "ylim": (-0.6, 12)},
    121: {"expr": "x*log(x)", "xlim": (0.05, 6), "ylim": (-0.5, 11), "breaks": [0]},
    122: {"expr": "sinh(x)", "xlim": (-2.4, 2.4), "ylim": (-5.5, 5.5)},
    123: {"expr": "cosh(x)", "xlim": (-2.4, 2.4), "ylim": (0, 6)},
    124: {"expr": "tanh(x)", "xlim": (-4, 4), "ylim": (-1.2, 1.2)},
    125: {"expr": "asinh(x)", "xlim": (-5, 5), "ylim": (-2.5, 2.5)},
    126: {"expr": "acosh(x)", "xlim": (1, 8), "ylim": (-0.1, 3)},
    127: {"expr": "atanh(x)", "xlim": (-0.95, 0.95), "ylim": (-2.5, 2.5)},
    128: {"expr": "exp(-0.35*x)*sin(2*x)", "xlim": (0, 8), "ylim": (-1.6, 1.6), "samples": 1600},
    129: {"expr": "x*sin(x)", "xlim": (-6.283185307, 6.283185307), "ylim": (-5.2, 2.2), "samples": 1800},
    130: {"expr": "sinc(x)", "xlim": (-10, 10), "ylim": (-0.35, 1.1), "samples": 1800},
    131: {"expr": "sin(1/x)", "xlim": (-0.6, 0.6), "ylim": (-1.1, 1.1), "breaks": [0], "samples": 2600},
    132: {"expr": "x+sin(x)", "xlim": (-5, 5), "ylim": (-6, 6), "samples": 1400},
    133: {"expr": "log(sin(x))", "xlim": (0.08, 3.061592654), "ylim": (-2.4, 0.12), "breaks": [0.0, 3.141592654], "samples": 2200},
    134: {"expr": "sqrt(1-x**2)", "xlim": (-1.15, 1.15), "ylim": (-0.1, 1.15), "samples": 1400},
    136: {"expr": "x/(1+x**2)", "xlim": (-4.0, 4.0), "ylim": (-0.7, 0.7), "samples": 1400},
    138: {"expr": "exp(-0.5*x**2)", "xlim": (-3.2, 3.2), "ylim": (-0.05, 1.05), "samples": 1400},
    139: {"expr": "exp(-abs(x))", "xlim": (-4, 4), "ylim": (-0.1, 1.1)},
    140: {"expr": "1/(1+x**2)", "xlim": (-4.0, 4.0), "ylim": (-0.05, 1.05), "samples": 1400},
    142: {"expr": "(1/x)*exp(-0.5*(log(x))**2)", "xlim": (0.03, 4.5), "ylim": (-0.02, 1.65), "samples": 1800},
    143: {"expr": "1/(1+exp(-x))", "xlim": (-6.0, 6.0), "ylim": (-0.05, 1.05), "samples": 1400},
    144: {"expr": "1/(1+exp(-1.6*(x-0.3)))", "xlim": (-5, 5), "ylim": (-0.1, 1.1)},
    145: {"expr": "exp(-exp(-x))", "xlim": (-4.5, 4.5), "ylim": (-0.05, 1.05), "samples": 1400},
    146: {"expr": "3*x/(1+x)", "xlim": (0, 6), "ylim": (-0.1, 3.2)},
    147: {"expr": "x**3/(1+x**3)", "xlim": (0, 5), "ylim": (-0.1, 1.1)},
    149: {"expr": "x/(1+x)", "xlim": (-5.0, 3.0), "ylim": (-3.0, 5.0), "breaks": [-1.0], "samples": 1600},
    150: {"expr": "elu(x)", "xlim": (-4, 4), "ylim": (-1.2, 4.2)},
    151: {"expr": "softplus(x)", "xlim": (-5, 5), "ylim": (-0.2, 5.2)},
    152: {"expr": "x/(1+exp(-x))", "xlim": (-5, 5), "ylim": (-0.5, 5.2)},
    153: {"expr": "gelu(x)", "xlim": (-5, 5), "ylim": (-0.5, 5.2)},
    154: {"expr": "mish(x)", "xlim": (-5, 5), "ylim": (-0.7, 5.2)},
    155: {"expr": "gamma(x)", "xlim": (0.15, 4.5), "ylim": (-2, 8), "samples": 1600},
    156: {"expr": "erf(x)", "xlim": (-3, 3), "ylim": (-1.2, 1.2)},
    157: {"expr": "j0(x)", "xlim": (0, 18), "ylim": (-0.5, 1.1), "samples": 1800},
}

SPECIAL_SVGS = {
    "dan_nhap": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 180" width="320" height="180">
  <rect width="320" height="180" fill="none"/>
  <g fill="#BFC7D2" stroke="none">
    <circle cx="84" cy="90" r="12"/>
    <circle cx="160" cy="90" r="12"/>
    <circle cx="236" cy="90" r="12"/>
  </g>
  <g stroke="#1F2937" stroke-width="3" stroke-linecap="round" fill="none">
    <path d="M 100 90 L 140 90"/>
    <path d="M 176 90 L 216 90"/>
  </g>
  <g fill="#1F2937">
    <path d="M 137 84 L 149 90 L 137 96 Z"/>
    <path d="M 213 84 L 225 90 L 213 96 Z"/>
  </g>
</svg>
""",
    "ham_so": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 180" width="320" height="180">
  <rect width="320" height="180" fill="none"/>
  <circle cx="65" cy="90" r="23" fill="#BFC7D2"/>
  <rect x="128" y="61" width="64" height="58" rx="13" fill="#BFC7D2"/>
  <circle cx="255" cy="90" r="23" fill="#BFC7D2"/>
  <g stroke="#1F2937" stroke-width="3" stroke-linecap="round" fill="none">
    <path d="M 90 90 L 124 90"/>
    <path d="M 196 90 L 230 90"/>
  </g>
  <g fill="#1F2937">
    <path d="M 117 84 L 129 90 L 117 96 Z"/>
    <path d="M 223 84 L 235 90 L 223 96 Z"/>
  </g>
  <g fill="#1F2937" font-family="sans-serif" font-size="24" text-anchor="middle">
    <text x="65" y="98">x</text>
    <text x="160" y="99">f</text>
    <text x="255" y="98">y</text>
  </g>
</svg>
""",
    "bien_thien": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 180" width="320" height="180">
  <rect width="320" height="180" fill="none"/>
  <g stroke="#BFC7D2" stroke-width="5" stroke-linecap="round">
    <path d="M 70 132 L 70 112"/>
    <path d="M 160 132 L 160 62"/>
    <path d="M 250 132 L 250 91"/>
  </g>
  <g stroke="#1F2937" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" fill="none">
    <path d="M 70 112 L 160 62 L 250 91"/>
    <path d="M 55 132 L 265 132"/>
  </g>
  <g fill="#1F2937">
    <circle cx="70" cy="112" r="7"/>
    <circle cx="160" cy="62" r="7"/>
    <circle cx="250" cy="91" r="7"/>
  </g>
</svg>
""",
    "do_thi": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 180" width="320" height="180">
  <rect width="320" height="180" fill="none"/>
  <g stroke="#1F2937" stroke-width="3" stroke-linecap="round" fill="none">
    <path d="M 45 138 L 278 138"/>
    <path d="M 78 153 L 78 28"/>
    <path d="M 270 132 L 282 138 L 270 144"/>
    <path d="M 72 36 L 78 24 L 84 36"/>
    <path d="M 102 125 C 126 99 145 64 170 57 C 198 49 218 75 252 112"/>
  </g>
  <g fill="#BFC7D2" stroke="#1F2937" stroke-width="2">
    <circle cx="115" cy="109" r="6"/>
    <circle cx="170" cy="57" r="6"/>
    <circle cx="232" cy="91" r="6"/>
  </g>
</svg>
""",
}


@dataclass
class PlotSpec:
    expr: str
    xlim: Tuple[float, float]
    ylim: Tuple[float, float]
    breaks: List[float]
    samples: int = 900
    hole_points: List[Tuple[float, float]] = None

    def __post_init__(self):
        if self.hole_points is None:
            self.hole_points = []


def parse_value(raw: Any) -> Any:
    return raw


def read_cards(data_path: Path):
    data = yaml.safe_load(data_path.read_text(encoding="utf-8")) or {}
    special = data.get("special") or []
    groups = data.get("groups") or []
    return special, groups


def normalize_formula(formula: str) -> str:
    return str(formula or "").replace("$", "").replace(" ", "").replace("\\,", "")


def latex_rhs(formula: str) -> str:
    s = normalize_formula(formula)
    if s.startswith("y="):
        s = s[2:]
    if "=" in s:
        s = s.split("=", 1)[0]
    return s


def strip_display_title(title: str) -> str:
    t = str(title or "").strip()
    return t.split(":", 1)[0].strip() if ":" in t else t


def display_title(item: dict, special: bool = False) -> str:
    if special:
        return strip_display_title(item.get("title", ""))
    return str(item.get("formula", ""))

def ensure_dir(path: Path):
    path.parent.mkdir(parents=True, exist_ok=True)


def find_matching_brace(s: str, start: int) -> int:
    depth = 0
    for i in range(start, len(s)):
        if s[i] == "{":
            depth += 1
        elif s[i] == "}":
            depth -= 1
            if depth == 0:
                return i
    raise ValueError("Unmatched brace")


def replace_frac(s: str) -> str:
    out = []
    i = 0
    while i < len(s):
        if s.startswith("\\frac", i):
            j = i + 5
            if j >= len(s) or s[j] != "{":
                out.append("\\frac")
                i = j
                continue
            a_end = find_matching_brace(s, j)
            num = s[j + 1:a_end]
            if a_end + 1 >= len(s) or s[a_end + 1] != "{":
                out.append(s[i:a_end + 1])
                i = a_end + 1
                continue
            b_start = a_end + 1
            b_end = find_matching_brace(s, b_start)
            den = s[b_start + 1:b_end]
            out.append(f"(({replace_frac(num)})/({replace_frac(den)}))")
            i = b_end + 1
        else:
            out.append(s[i])
            i += 1
    return "".join(out)


def replace_sqrt(s: str) -> str:
    while "\\sqrt{" in s:
        i = s.index("\\sqrt{")
        j = i + len("\\sqrt")
        end = find_matching_brace(s, j)
        inner = s[j + 1:end]
        s = s[:i] + f"sqrt({replace_sqrt(inner)})" + s[end + 1:]
    return s


def replace_abs(s: str) -> str:
    # chỉ xử lý các cặp |...| không lồng nhau
    while s.count("|") >= 2:
        a = s.find("|")
        b = s.find("|", a + 1)
        if b == -1:
            break
        inner = s[a + 1:b]
        s = s[:a] + f"abs({inner})" + s[b + 1:]
    return s


def insert_implicit_mul(s: str) -> str:
    """Insert multiplication signs without breaking function names.

    The goal is to handle LaTeX-style products such as 2x, 2(x+1),
    (x-1)(x+1), x(x+1), while avoiding corrupting names like exp, asin.
    """
    # number followed by x or opening parenthesis: 2x, 2(x+1), 1.0(x-0.8)
    s = re.sub(r"(?<=[0-9])(?=x|\()", "*", s)
    # x or closing parenthesis followed by opening parenthesis: x(x+1), )(
    s = re.sub(r"(?<=x|\))(?=\()", "*", s)
    # closing parenthesis followed by x or number: (x+1)x, (x+1)2
    s = re.sub(r"(?<=\))(?=x|[0-9])", "*", s)
    # x followed by known function names: xsin(x), xlog(x)
    s = re.sub(r"x(?=(sin|cos|tan|asin|acos|atan|sqrt|log|ln|abs|exp)\()", "x*", s)
    return s


def latex_to_expr_text(formula: str) -> str:
    s = latex_rhs(formula)
    key = normalize_formula(formula)
    if key in SPEC_OVERRIDES:
        return SPEC_OVERRIDES[key]["expr"]

    s = s.replace("\\left", "").replace("\\right", "")
    s = s.replace("\\cdot", "*")
    s = s.replace("\\times", "*")
    s = s.replace("{", "{").replace("}", "}")
    s = replace_frac(s)
    s = replace_sqrt(s)
    s = replace_abs(s)
    replacements = {
        "\\sin": "sin",
        "\\cos": "cos",
        "\\tan": "tan",
        "\\arcsin": "asin",
        "\\arccos": "acos",
        "\\arctan": "atan",
        "\\ln": "ln",
        "\\log": "log",
        "\\pi": "pi",
    }
    for k, v in replacements.items():
        s = s.replace(k, v)

    s = s.replace("^", "**")
    s = s.replace("{", "(").replace("}", ")")
    s = s.replace("[", "(").replace("]", ")")
    s = s.replace(",", ".")
    s = re.sub(r"\\geq.*$", "", s)
    s = re.sub(r"\\leq.*$", "", s)

    # log_a(x) -> log(x, a)
    s = re.sub(r"log_([0-9]+)\(([^()]*)\)", r"(log(\2, \1))", s)
    s = re.sub(r"log_([0-9]+)x", r"(log(x, \1))", s)

    s = re.sub(r"\s+", "", s)

    # tham số mặc định nếu còn sót. Làm trước khi thêm dấu nhân để xử lý a(x-h).
    for name, value in PARAM_DEFAULTS.items():
        s = re.sub(rf"(?<![A-Za-z0-9_]){name}(?![A-Za-z0-9_])", str(value), s)

    s = insert_implicit_mul(s)
    return s


def candidate_breaks_from_formula(formula: str) -> List[float]:
    key = normalize_formula(formula)
    if key in SPEC_OVERRIDES and "breaks" in SPEC_OVERRIDES[key]:
        return list(SPEC_OVERRIDES[key]["breaks"])

    rhs = latex_rhs(formula)
    denoms = re.findall(r"\\frac\{[^{}]*\}\{([^{}]*)\}", rhs)
    breaks: List[float] = []
    for den in denoms:
        d = den.replace(" ", "")
        # hỗ trợ x, x-a, x+a, cx+d
        if d == "x":
            breaks.append(0.0)
            continue
        m = re.fullmatch(r"x([+-]\d+(?:\.\d+)?)", d)
        if m:
            breaks.append(-float(m.group(1)))
            continue
        m = re.fullmatch(r"([+-]?\d+(?:\.\d+)?)x([+-]\d+(?:\.\d+)?)", d)
        if m:
            a = float(m.group(1))
            b = float(m.group(2))
            if a != 0:
                breaks.append(-b / a)
            continue
    # loại lặp gần nhau
    out = []
    for b in breaks:
        if not any(abs(b - c) < 1e-8 for c in out):
            out.append(b)
    return out



def plot_spec_from_base(base: Dict[str, Any], item: dict) -> PlotSpec:
    cfg = item.get("plot") or {}
    expr = str(item.get("plot_expr") or base.get("expr", "x"))
    xlim = tuple(cfg.get("xlim", base.get("xlim", (-3.0, 3.0))))
    ylim = tuple(cfg.get("ylim", base.get("ylim", (-3.0, 3.0))))
    samples = int(cfg.get("samples", base.get("samples", 900)))
    breaks = list(base.get("breaks", []))
    if item.get("breaks"):
        breaks.extend([float(v) for v in item.get("breaks")])
    if cfg.get("breaks"):
        breaks.extend([float(v) for v in cfg.get("breaks")])
    holes = [tuple(p) for p in base.get("holes", [])]
    unique_breaks = []
    for b in breaks:
        if not any(abs(float(b) - c) < 1e-9 for c in unique_breaks):
            unique_breaks.append(float(b))
    return PlotSpec(
        expr=expr,
        xlim=(float(xlim[0]), float(xlim[1])),
        ylim=(float(ylim[0]), float(ylim[1])),
        breaks=unique_breaks,
        samples=samples,
        hole_points=holes,
    )

def infer_plot_spec(item: dict) -> PlotSpec:
    formula = str(item.get("formula", ""))
    key = normalize_formula(formula)

    try:
        number = int(item.get("number", 0) or 0)
    except Exception:
        number = 0
    if number in NUM_OVERRIDES:
        return plot_spec_from_base(NUM_OVERRIDES[number], item)

    if item.get("plot_expr"):
        expr = str(item.get("plot_expr"))
    else:
        expr = latex_to_expr_text(formula)

    cfg = item.get("plot") or {}
    if key in SPEC_OVERRIDES:
        base = SPEC_OVERRIDES[key]
        expr = base.get("expr", expr)
        xlim = tuple(base.get("xlim", (-3.0, 3.0)))
        ylim = tuple(base.get("ylim", (-3.0, 3.0)))
        samples = int(base.get("samples", 900))
        breaks = list(base.get("breaks", []))
    else:
        xlim = tuple(cfg.get("xlim", (-3.0, 3.0)))
        ylim = tuple(cfg.get("ylim", (-3.0, 3.0)))
        samples = int(cfg.get("samples", 900))
        breaks = []

    # Heuristics by expression if not set explicitly.
    if not cfg.get("xlim") and key not in SPEC_OVERRIDES:
        rhs = latex_rhs(formula)
        if "sin" in expr or "cos" in expr:
            xlim, ylim = (-math.pi, math.pi), (-1.3, 1.3)
            samples = max(samples, 1200)
        elif "tan" in expr:
            xlim, ylim = (-1.35, 1.35), (-4.5, 4.5)
            samples = max(samples, 1400)
            breaks.extend([-math.pi / 2, math.pi / 2])
        elif "log" in expr or "ln" in expr:
            xlim, ylim = (0.05, 6.0), (-3.0, 3.0)
            breaks.append(0.0)
        elif "sqrt" in expr:
            xlim, ylim = (0.0, 6.0), (0.0, 3.0)
        elif "/" in expr:
            xlim, ylim = (-4.0, 4.0), (-5.0, 5.0)
            breaks.extend(candidate_breaks_from_formula(formula))
            samples = max(samples, 1200)
        elif "**5" in expr or "**4" in expr:
            xlim, ylim = (-2.0, 2.0), (-6.0, 6.0)
        elif "**3" in expr:
            xlim, ylim = (-2.2, 2.2), (-6.0, 6.0)
        elif "**2" in expr:
            xlim, ylim = (-3.0, 3.0), (-1.5, 6.0)
        elif "abs(" in expr:
            xlim, ylim = (-3.0, 3.0), (-0.2, 3.5)
        elif "exp(" in expr or "e**x" in expr:
            xlim, ylim = (-2.5, 2.5), (-0.2, 8.0)

    if cfg.get("xlim"):
        xlim = tuple(cfg["xlim"])
    if cfg.get("ylim"):
        ylim = tuple(cfg["ylim"])
    if cfg.get("samples"):
        samples = int(cfg["samples"])
    if item.get("breaks"):
        breaks.extend([float(v) for v in item.get("breaks")])
    if cfg.get("breaks"):
        breaks.extend([float(v) for v in cfg.get("breaks")])

    # trường hợp lỗ khuyết điển hình (removable discontinuity)
    holes = []
    if key == "y=\\frac{x^2-1}{x-1}=x+1":
        breaks.append(1.0)
        holes.append((1.0, 2.0))
        xlim, ylim = (-3, 3), (-2, 5)
    if key == "y=\\frac{x^2-1}{x^2-1}=1":
        breaks.extend([-1.0, 1.0])
        holes.extend([(-1.0, 1.0), (1.0, 1.0)])
        xlim, ylim = (-3, 3), (-0.5, 2.0)

    # unique breaks in-range-ish
    unique_breaks = []
    for b in breaks:
        if not any(abs(b - c) < 1e-9 for c in unique_breaks):
            unique_breaks.append(float(b))

    return PlotSpec(expr=expr, xlim=(float(xlim[0]), float(xlim[1])), ylim=(float(ylim[0]), float(ylim[1])), breaks=unique_breaks, samples=samples, hole_points=holes)


def eval_expr(expr: str, x: float) -> float:
    env = dict(SAFE_FUNCS)
    env["x"] = x
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", SyntaxWarning)
        return float(eval(expr, {"__builtins__": {}}, env))


def sample_segments(spec: PlotSpec) -> List[List[Tuple[float, float]]]:
    x0, x1 = spec.xlim
    y0, y1 = spec.ylim
    n = max(180, spec.samples)
    xs = [x0 + (x1 - x0) * i / (n - 1) for i in range(n)]
    segments: List[List[Tuple[float, float]]] = []
    current: List[Tuple[float, float]] = []
    y_range = abs(y1 - y0)
    split_slope = y_range * 0.9

    prev_xy = None
    for x in xs:
        if any(abs(x - b) < (x1 - x0) * 0.012 for b in spec.breaks):
            if len(current) >= 2:
                segments.append(current)
            current = []
            prev_xy = None
            continue
        try:
            y = eval_expr(spec.expr, x)
        except Exception:
            if len(current) >= 2:
                segments.append(current)
            current = []
            prev_xy = None
            continue
        if not math.isfinite(y) or abs(y) > max(abs(y0), abs(y1)) * 3 + 4:
            if len(current) >= 2:
                segments.append(current)
            current = []
            prev_xy = None
            continue

        if y < y0 or y > y1:
            if len(current) >= 2:
                segments.append(current)
            current = []
            prev_xy = None
            continue

        if prev_xy is not None and abs(y - prev_xy[1]) > split_slope:
            if len(current) >= 2:
                segments.append(current)
            current = []

        current.append((x, y))
        prev_xy = (x, y)

    if len(current) >= 2:
        segments.append(current)
    return segments


def map_point(x: float, y: float, spec: PlotSpec) -> Tuple[float, float]:
    x0, x1 = spec.xlim
    y0, y1 = spec.ylim
    px = PAD_X + (x - x0) / (x1 - x0) * (SVG_W - 2 * PAD_X)
    py = SVG_H - PAD_Y - (y - y0) / (y1 - y0) * (SVG_H - 2 * PAD_Y)
    return px, py


def polyline_path(points: List[Tuple[float, float]], spec: PlotSpec) -> str:
    mapped = [map_point(x, y, spec) for x, y in points]
    coords = [f"M {mapped[0][0]:.2f} {mapped[0][1]:.2f}"]
    coords += [f"L {x:.2f} {y:.2f}" for x, y in mapped[1:]]
    return " ".join(coords)


def render_formula_svg(item: dict) -> str:
    if item.get("plot") is False:
        return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {SVG_W} {SVG_H}" width="{SVG_W}" height="{SVG_H}">
  <rect width="{SVG_W}" height="{SVG_H}" fill="{BG}"/>
</svg>
'''

    spec = infer_plot_spec(item)
    segments = sample_segments(spec)
    paths = []
    for seg in segments:
        if len(seg) >= 2:
            paths.append(f'<path d="{polyline_path(seg, spec)}" fill="none" stroke="{STROKE}" stroke-width="{STROKE_WIDTH}" stroke-linecap="round" stroke-linejoin="round"/>')

    holes = []
    for hx, hy in spec.hole_points:
        px, py = map_point(hx, hy, spec)
        holes.append(f'<circle cx="{px:.2f}" cy="{py:.2f}" r="4.3" fill="{BG}" stroke="{STROKE}" stroke-width="1.8"/>')

    inner = "\n  ".join(paths + holes)
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {SVG_W} {SVG_H}" width="{SVG_W}" height="{SVG_H}">
  <rect width="{SVG_W}" height="{SVG_H}" fill="{BG}"/>
  {inner}
</svg>
'''


def make_svg(path: Path, item: dict, special: bool = False):
    ensure_dir(path)
    if special:
        illustration = str(
            item.get("illustration") or item.get("id") or "dan_nhap"
        )
        svg = SPECIAL_SVGS.get(
            illustration,
            SPECIAL_SVGS["dan_nhap"],
        )
    else:
        svg = render_formula_svg(item)
    path.write_bytes(svg.encode("utf-8"))


def published(item: dict) -> bool:
    return item.get("status") == "published" and bool(item.get("href"))


def card_markdown(item: dict, project_dir: Path, special: bool = False) -> str:
    if item.get("visible", True) is False:
        return ""
    image = item.get("image")
    if image:
        make_svg(project_dir / image, item, special=special)
    title = display_title(item, special=special)
    alt = html.escape(title)
    action_label = "Đọc bài" if published(item) else "Đang chờ"
    state = "is-published" if published(item) else "is-pending"

    if published(item):
        figure_open = f'<a class="zo-card-figure" href="{item.get("href")}">'
        figure_close = "</a>"
        action_html = f'<a class="zo-card-pill zo-card-pill--action" href="{item.get("href")}">{action_label}</a>'
    else:
        figure_open = '<div class="zo-card-figure">'
        figure_close = "</div>"
        action_html = '<span class="zo-card-pill zo-card-pill--action is-disabled">Đang chờ</span>'

    img_html = f'<img class="zo-card-image" src="{image}" alt="{alt}"/>' if image else ""

    return f'''::: {{.zo-card .{state}}}
{figure_open}{img_html}{figure_close}

::: {{.zo-card-body}}
::: {{.zo-card-title}}
{title}
:::

::: {{.zo-card-actions}}
{action_html}
:::
:::
:::
'''


def write_audits(project_dir: Path, special: List[dict], groups: List[dict]):
    audit_dir = Path("_audit")
    audit_dir.mkdir(exist_ok=True)
    slug = project_dir.name

    all_items = [x for x in special if x.get("visible", True) is not False]
    for group in groups:
        all_items.extend([x for x in (group.get("items") or []) if x.get("visible", True) is not False])

    published_items = [x for x in all_items if published(x)]
    pending_items = [x for x in all_items if not published(x)]

    summary_path = audit_dir / f"{slug}_card_grid_summary.txt"
    summary_text = "\n".join([
        "Tổng kết lưới thẻ",
        "",
        f"Dự án: {project_dir}",
        f"Tổng số thẻ đang hiển thị: {len(all_items)}",
        f"Đã có bài: {len(published_items)}",
        f"Đang chờ: {len(pending_items)}",
    ])
    summary_path.write_bytes(summary_text.encode("utf-8"))

    spec_path = audit_dir / f"{slug}_card_draw_kind_audit.txt"
    lines = ["Audit renderer SVG thống nhất", ""]
    for item in all_items:
        if item.get("number") is None:
            lines.append(f"SPECIAL | {display_title(item, special=True)}")
            continue

        if item.get("plot") is False:
            lines.append(
                f"#{int(item['number']):03d} | "
                f"{normalize_formula(item.get('formula', ''))} | plot=disabled"
            )
            continue

        spec = infer_plot_spec(item)
        lines.append(
            f"#{int(item['number']):03d} | "
            f"{normalize_formula(item.get('formula', ''))} | "
            f"expr={spec.expr} | xlim={spec.xlim} | ylim={spec.ylim} | "
            f"breaks={spec.breaks} | samples={spec.samples}"
        )
    spec_path.write_bytes("\n".join(lines).encode("utf-8"))

    print(f"Đã ghi audit: {summary_path}")
    print(f"Đã ghi audit: {spec_path}")


def main(argv: List[str]):
    if len(argv) != 2:
        print("Cách dùng: python scripts/zo_build_card_grid.py <thu_muc_du_an>")
        raise SystemExit(1)

    project_dir = Path(argv[1])
    data_path = project_dir / "_data" / "cards.yml"
    if not data_path.exists():
        print(f"Không tìm thấy: {data_path}")
        raise SystemExit(1)

    special, groups = read_cards(data_path)
    partial_path = project_dir / "_partials" / "card_grid.qmd"
    ensure_dir(partial_path)

    lines = [
        "<!-- Generated by scripts/zo_build_card_grid.py from _data/cards.yml. Do not edit directly. -->",
        "",
        "::: {.zo-card-grid}",
    ]

    for item in special:
        md = card_markdown(item, project_dir, special=True)
        if md:
            lines.append(md.rstrip())
            lines.append("")

    for group in groups:
        for item in group.get("items") or []:
            md = card_markdown(item, project_dir, special=False)
            if md:
                lines.append(md.rstrip())
                lines.append("")

    lines.append(":::")
    partial_path.write_bytes(("\n".join(lines).rstrip() + "\n").encode("utf-8"))
    print(f"Đã sinh partial: {partial_path}")
    write_audits(project_dir, special, groups)


if __name__ == "__main__":
    main(sys.argv)
