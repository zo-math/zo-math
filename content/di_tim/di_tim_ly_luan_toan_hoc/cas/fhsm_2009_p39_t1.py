from __future__ import annotations

import sympy as sp
from pathlib import Path


def factor_ordered_as_x_minus_a(expr: sp.Expr, x: sp.Symbol) -> sp.Expr:
    """
    Factor expr and order linear factors (x-a) by increasing a, so we get:
    (x-1)(x-2)(x-3) instead of (x-3)(x-2)(x-1).
    Falls back to sympy.factor if something unexpected happens.
    """
    try:
        const, factors = sp.factor_list(expr)  # (const, [(factor, exp), ...])

        def key_factor(fe):
            fac, exp = fe
            sols = sp.solve(sp.Eq(fac, 0), x)
            if sols:
                return float(sp.N(sols[0]))
            return 0.0

        factors_sorted = sorted(factors, key=key_factor)
        rebuilt = sp.Mul(const, *[fac ** exp for fac, exp in factors_sorted])
        return rebuilt
    except Exception:
        return sp.factor(expr)


def main() -> None:
    # ---- Parameters you can change ----
    k_value = 8  # set to 3 if you want the "triple that" line from the book
    out_tex = Path(__file__).resolve().parent / "fhsm_2009_p39_t1.tex"
    # ----------------------------------

    x = sp.Symbol("x")

    # Define functions
    f = 4 * x - 1
    g = x**3 - 6 * x**2 + 15 * x - 7
    h = sp.expand(g - f)
    k = sp.nsimplify(k_value)
    j = sp.expand(f + k * h)

    h_fact = factor_ordered_as_x_minus_a(h, x)

    # Values at x = 1,2,3 (for the "same sequence" point)
    j1 = sp.simplify(j.subs(x, 1))
    j2 = sp.simplify(j.subs(x, 2))
    j3 = sp.simplify(j.subs(x, 3))

    # Helpers to render latex nicely
    def L(expr: sp.Expr) -> str:
        return sp.latex(expr)

    # Build LaTeX file (standalone, border=6pt)
    tex = rf"""\documentclass[border=6pt]{{standalone}}
\usepackage{{amsmath}}
\usepackage{{array}}

\begin{{document}}

\fbox{{%
\begin{{minipage}}{{13.2cm}}
\renewcommand{{\arraystretch}}{{1.25}}
\begin{{tabular}}{{@{{}}l@{{}}}}
\textbf{{CAS output (Example 9)}}\\[2pt]
$f(x) = {L(f)}$\\
$g(x) = {L(g)}$\\
$h(x)=g(x)-f(x) = {L(h)}$\\
$\operatorname{{factor}}(h(x)) = {L(h_fact)}$\\
$k = {L(k)}$\\
$j(x)=f(x)+k\cdot h(x) = {L(j)}$\\
$j(1)={L(j1)},\quad j(2)={L(j2)},\quad j(3)={L(j3)}$\\
\end{{tabular}}
\end{{minipage}}%
}}

\end{{document}}
"""

    out_tex.write_text(tex, encoding="utf-8")
    print(f"[OK] Wrote: {out_tex}")


if __name__ == "__main__":
    main()
