"""Canonical editorial learning guidance for the 2027 course."""
from html import escape as esc

def guide_hub(guides, icon, btn):
    rows = ''.join(f'''<article class="guide-entry-row" id="{g['key']}">
      <h2>{esc(g['label'])}</h2><div><p class="guide-when">{esc(g['when'])}</p>
      <p>{esc(g['action'])}</p>{btn(g['file'],g['link_label'],'text')}</div></article>''' for g in guides)
    return f'''<main id="main-content" class="learning-hub">
      <header class="learning-heading"><h1>Cách học</h1>
      <p>Mỗi chuyên đề có bốn phần dưới đây. Em chọn phần phù hợp với việc mình cần làm; không bắt buộc học lần lượt từ đầu đến cuối.</p></header>
      <section class="learning-articles" aria-label="Bốn phần trong mỗi chuyên đề">{rows}</section>
      <section class="learning-tools learning-utilities" aria-labelledby="utilities-title"><h2 id="utilities-title">Ghi chép và dùng website</h2>
      <details id="ghi-chu-va-lich-on"><summary>Giữ bài làm và lịch ôn ở đâu?</summary><div>
      <p>Làm bài trên giấy hoặc công cụ ghi chú em đang dùng. Khi sửa, giữ phần ban đầu và viết phần sửa bên cạnh.</p>
      <p>Cuối buổi, ghi việc còn vướng, nơi sẽ học tiếp và ngày cần ôn. Mục <strong>Nhật kí</strong> trong mỗi chuyên đề có mẫu để sao chép; website chưa lưu bài giải hoặc gửi lời nhắc lịch ôn.</p></div></details>
      <details id="danh-dau-vi-tri"><summary>Làm sao mở lại chỗ đang học?</summary><div>
      <p>Dùng biểu tượng đánh dấu ở chuyên đề hoặc vị trí đọc. Lần sau, mở mục <strong>Đã lưu</strong> trên thanh đầu trang để quay lại.</p>
      <p>Dấu lưu được giữ trên trình duyệt đang dùng. Nó không thay cho bài giải và ghi chú, cũng không cho biết em đã hiểu bài.</p></div></details>
      <details id="doc-nguon"><summary>Khi cần hỏi hoặc đọc thêm thì làm gì?</summary><div>
      <p>Khi hỏi giáo viên, bạn học hoặc công cụ trí tuệ nhân tạo, gửi đề bài, phần đã tự làm và bước chưa hiểu. Nêu câu hỏi cụ thể, chẳng hạn: “Vì sao ở bước này được dùng công thức đó?”. Sau khi nhận gợi ý, thử tự viết lại lời giải.</p>
      <p>Muốn đọc thêm tài liệu dùng để biên soạn, mở mục <strong>Nguồn</strong> trong chuyên đề. Đối chiếu điều kiện và kí hiệu của tài liệu ấy với bài đang học.</p></div></details>
      </section>
      <div class="guide-catalog-entry"><p>Để bắt đầu một chuyên đề, mở <strong>Tổng quan</strong> để biết nội dung và kiến thức cần dùng, rồi chọn phần học.</p>{btn('chuyen-de.html','Chuyên đề','primary')}</div>
    </main>'''


def guide_article(g, guides, items, icon, btn):
    contents = ''.join(f'<a href="#{s["id"]}"><span aria-hidden="true">{i}</span>{esc(s["title"])}</a>' for i,s in enumerate(g['sections'],1))
    sections = ''.join(f'<section id="{s["id"]}" class="guidance-section"><h2><span class="guide-step-number" aria-hidden="true">{i}</span>{esc(s["title"])}</h2>{s["html"]}</section>' for i,s in enumerate(g['sections'],1))
    examples = ''.join(btn(href,label,'text') for label,href in g['trylinks'])
    return f'''<main id="main-content" class="guidance-main"><nav class="guidance-breadcrumb" aria-label="Đường dẫn"><a href="cach-hoc.html">Cách học</a>{icon('chevron')}<span>{esc(g['label'])}</span></nav>
      <header class="guidance-heading"><h1>{esc(g['title'])}</h1><p>{esc(g['summary'])}</p></header>
      <details class="guidance-mobile-toc"><summary>Các bước thực hiện</summary><nav aria-label="Mục lục trên điện thoại">{contents}<a href="#thu-trong-hoc-lieu">Ví dụ trong học liệu</a></nav></details><div class="guidance-layout"><aside class="guidance-toc"><strong>Các bước thực hiện</strong><nav aria-label="Mục lục hướng dẫn">{contents}<a href="#thu-trong-hoc-lieu">Ví dụ trong học liệu</a></nav></aside><article class="guidance-body">{sections}
      <section class="guidance-example" id="thu-trong-hoc-lieu"><h2>{esc(g['example']['title'])}</h2>{g['example']['html']}<div class="guidance-examples">{examples}</div></section>
      <div class="guide-catalog-entry"><p>Áp dụng với chuyên đề em đang học: trong danh mục, chọn <strong>{esc(g['label'])}</strong> trên thẻ của chuyên đề đó.</p>{btn('chuyen-de.html','Chuyên đề','primary')}</div>
      </article></div></main>'''
