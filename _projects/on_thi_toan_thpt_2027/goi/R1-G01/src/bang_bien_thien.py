"""Tạo bảng HTML từ dữ liệu tường minh. Không tự điền đạo hàm vào bảng chỉ có biến thiên.
Ô empty = không ghi dữ kiện; ô undefined ghi rõ Không tồn tại;
excluded_columns vẽ hai vạch qua các hàng đạo hàm và hàm số tại mốc bị loại.
"""
from html import escape

def render_table(rows, title='Bảng biến thiên', excluded_columns=()):
    out=['<div class="table-scroll"><table class="variation"><caption>'+escape(title)+'</caption><thead>']
    for i,row in enumerate(rows):
        out.append('<tr>')
        for j,value in enumerate(row):
            tag='th' if j==0 or i==0 else 'td'
            cls=' class="excluded"' if i>0 and j in excluded_columns else ''
            scope=' scope="row"' if j==0 else (' scope="col"' if i==0 else '')
            display='∥' if i>0 and j in excluded_columns else value
            out.append(f'<{tag}{scope}{cls}>{escape(display)}</{tag}>')
        out.append('</tr>')
        if i==0:out.append('</thead><tbody>')
    out.append('</tbody></table></div>')
    return ''.join(out)
