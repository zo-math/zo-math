# FHSM — canonical TeX workspace

This directory is the canonical editorial source for the Vietnamese FHSM edition.

## Canonical units

- `tieu_luan_dan_nhap_fhsm_ban_chuyen_ngu.tex`
- `dan_nhap.tex`
- `chuong_01.tex`–`chuong_11.tex`
- `thu_muc_chu_giai.tex`
- `khao_luan_he_thuat_ngu_ban_chuyen_ngu.tex`
- `references.bib`
- driver: `main.tex`

The former aggregate `luan_va_hieu.tex` has been retired. The modular TeX files listed above are the only editorial authority.

## Build

```bash
latexmk -C
latexmk -lualatex -interaction=nonstopmode -synctex=1 main.tex
```

QMD/Web is not an editorial authority for this edition.
