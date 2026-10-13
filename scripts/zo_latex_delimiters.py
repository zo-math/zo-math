"""Shared LaTeX delimiter rule; detect, never silently rewrite source."""
from __future__ import annotations
import re

# TeX grouping braces are not printed delimiters. Mixed interval endpoints
# (e.g. [a;b)) are intentional, so pair by nesting rather than glyph shape.
TOKEN = re.compile(r'\\(?:left|right)\s*(?:\\[A-Za-z]+|\\[{}|]|[()[\]|.])|\\(?:lvert|rvert|lVert|rVert|langle|rangle|lbrace|rbrace)\b|\\[{}|]|[()[\]|]')
OPEN = {'(', '[', r'\{', r'\lbrace', r'\langle', r'\lvert', r'\lVert'}
CLOSE = {')', ']', r'\}', r'\rbrace', r'\rangle', r'\rvert', r'\rVert'}
SYMMETRIC = {'|', r'\|'}
TALL = re.compile(r'\\(?:[dt]?frac|sqrt|binom|[dt]binom|overset|underset|stackrel|sum|prod|int|iint|iiint|oint)\b|\\begin\{(?:[pbBvV]?matrix|aligned|cases)\}')


def delimiter_errors(formula: str) -> list[dict]:
    stack = []; errors = []
    # Optional root indices use syntactic brackets, not printed delimiters.
    indices = [(m.start(1),m.end(1)) for m in re.finditer(r'\\sqrt\s*(\[[^]]*\])',formula)]
    for token in TOKEN.finditer(formula):
        if any(a<=token.start()<b for a,b in indices):continue
        raw = token[0]; scaled = raw.startswith((r'\left', r'\right'))
        opening = raw.startswith(r'\left') or raw in OPEN
        closing = raw.startswith(r'\right') or raw in CLOSE
        if raw in SYMMETRIC:
            closing = bool(stack and re.sub(r'^\\left\s*','',stack[-1][2]) == raw)
            opening = not closing
        if opening:
            stack.append((token.start(), token.end(), raw, scaled))
        elif closing and stack:
            start, end, left, left_scaled = stack.pop()
            body = formula[end:token.start()]
            if TALL.search(body) and not (left_scaled and scaled):
                errors.append({'rule':'tall-content-requires-left-right',
                               'start':start,'end':token.end(),
                               'left_end':end,'right_start':token.start(),
                               'left':left,'right':raw,'expression':formula[start:token.end()]})
    return errors


def self_test() -> dict:
    bad = [r'[0;\frac{\pi}{2}]', r'(\frac{1}{2};1]',
           r'f(\frac{\pi}{2})', r'\{\frac{1}{x}\}',
           r'|\frac{1}{x}|', r'\lVert\frac{1}{x}\rVert',
           r'(\sqrt{x})', r'[\left(\frac{1}{x}\right)]',
           r'\left[0;\frac{1}{2}]', r'\left|\frac{1}{x}|']
    good = [r'\left[0;\frac{\pi}{2}\right]', r'\left(\frac{1}{2};1\right]',
            r'f\left(\frac{\pi}{2}\right)', r'\left\{\frac{1}{x}\right\}',
            r'\left|\frac{1}{x}\right|', r'\left\lVert\frac{1}{x}\right\rVert',
            r'\frac{1}{x}', r'[0;1]', r'(x-1)^2',
            r'\sqrt[3]{x}', r'\sqrt[\frac{1}{2}]{x}', r'\left.\frac{1}{x}\right|_1^2',
            r'\left[\left(\frac{1}{x}\right)\right]']
    return {**{f'reject {x}':bool(delimiter_errors(x)) for x in bad},
            **{f'accept {x}':not delimiter_errors(x) for x in good}}
