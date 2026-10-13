from pathlib import Path
import json,base64,mimetypes,html,re
R=Path(__file__).resolve().parents[1]
def uri(p):
 p=R/p;return 'data:'+(mimetypes.guess_type(p.name)[0] or 'application/octet-stream')+';base64,'+base64.b64encode(p.read_bytes()).decode()
def theme_controls():
 p=json.loads((R/'design/color_system.json').read_text());names={'red':'Đỏ ZO','yellow':'Vàng ZO','gray':'Xám ZO'}
 choices=''.join(f'<label class="theme-choice"><input type="radio" name="pageBackground" value="{k}" {"checked" if k==p["default_background"] else ""}><span class="theme-chip" style="background:{p["palette"][k]}"></span><span>{names[k.split("-")[0]]} {k.split("-")[1]}</span> <span class="theme-check" aria-hidden="true">✓</span></label>' for k in p['backgrounds'])
 return '<details class="theme-settings"><summary>Nền trang <span id="themeName" class="muted">Xám ZO 3</span></summary><div class="theme-choices">'+choices+'</div><div class="theme-tools"><label><input type="checkbox" id="grayMode"> Sắc xám</label><label>Cỡ chữ <select id="textSize"><option value="1">100%</option><option value="1.25">125%</option><option value="1.5">150%</option><option value="2">200%</option></select></label><label><input type="checkbox" id="reduceMotion"> Giảm chuyển động</label></div><p class="theme-status" role="status" id="themeStatus">Nền bao quanh thay đổi; các vùng đọc giữ nền trắng.</p></details>'
def support(compact=False,id='support04'):
 if compact:return f'<aside class="support-panel support-inline support-compact" data-added-note="true"><div><span class="role-tag">Cùng phát triển ZO Math</span><strong>Giữ những học liệu này tiếp tục được biên soạn.</strong><p class="support-explainer">ZO Math hiện chưa có tài trợ và cần kinh phí phát triển.</p></div><a class="button" href="#r1-support-title">Ủng hộ ZO Math</a></aside>'
 qr=R/'assets/qr_bao_tro_zo_math_vietcombank.jpg'
 return f'''<section class="support-panel" id="{id}" data-added-note="true"><span class="role-tag">Cùng phát triển ZO Math</span><h2>Ủng hộ ZO Math</h2><p class="support-copy">ZO Math hiện chưa có tài trợ và cần kinh phí để tiếp tục biên soạn, xây dựng và duy trì học liệu. Nếu những nội dung này hữu ích với bạn, bạn có thể góp một phần để ZO Math tiếp tục phát triển.</p><div class="r1-support-details"><img class="r1-support-qr" src="{uri('assets/'+qr.name)}" alt="Mã QR Vietcombank từ nguồn ZO Math"><dl><div><dt>Ngân hàng</dt><dd>Vietcombank</dd></div><div><dt>Số tài khoản</dt><dd><span id="supportAccount{id}">0601000137768</span> <button class="button secondary" data-copy-account="0601000137768" type="button">Sao chép</button></dd></div><div><dt>Chủ tài khoản</dt><dd>Nguyễn Tấn Nhựt</dd></div><div><dt>Nội dung chuyển khoản</dt><dd>BAO TRO ZO MATH</dd></div></dl></div><p class="support-copy-status" role="status"></p><p><a href="https://zomath.vn/content/support/donate.html">Thông tin bảo trợ ZO Math</a></p><p class="support-explainer">Sự ủng hộ hoàn toàn tự nguyện. Bạn vẫn có thể tiếp tục sử dụng học liệu.</p></section>'''
def upgrade(page,kind):
 # Each generated document is controlled here; remove the superseded toolbar only.
 page=re.sub(r'<div class="toolbar(?: screen-only)?">.*?</div>','',page,flags=re.S)
 page=page.replace('<div class="wrap">','<div class="wrap">'+theme_controls()) if kind=='gallery' else page.replace('<div class="reader-shell">','<div class="reader-shell">'+theme_controls())
 if kind=='r1':page=page.replace('<div class="top-meta">','<a class="support-top" href="#r1-support-title">Ủng hộ ZO Math</a><div class="top-meta">')
 # Shared preference code comes after the source controller and old common behavior.
 page=page.replace('</body>','<script>'+(R/'source/experience04.js').read_text()+'</script></body>')
 return page
