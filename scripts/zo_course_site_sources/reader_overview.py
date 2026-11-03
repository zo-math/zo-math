"""Authored orientations; learning goals and the learning DOM stay intact."""
from copy import deepcopy
from html import escape
from .overview_content import OVERVIEWS


def overview_aliases(key):
    """Only equivalent orientation anchors are migrated; other text stays readable."""
    if key == 'd0':
        return {}
    aliases = {'bat-dau':'tong-quan', 'overview-lessons':'bai-hoc',
               'overview-practice':'phieu-luyen'}
    source_ids = {
        'r1_g01': (['học-xong-em-cần-làm-được-gì','r1-table-t02'], [],
                   ['cách-học-với-tài-liệu-này','chọn-nơi-bắt-đầu','bản-đồ-học']),
        'r1_g02': (['học-xong-em-cần-làm-được-gì','r1-g02-table-t09'], [],
                   ['cách-học-với-tài-liệu-này','chọn-nơi-bắt-đầu','bản-đồ-học']),
        'r1_g03': (['mục-tiêu','g03-table-02'], ['tiên-quyết'],
                   ['cách-học','chọn-nơi-bắt-đầu','bản-đồ-học']),
        'r1_g04': (['mục-tiêu','g04-table-02'], ['tiên-quyết'],
                   ['cách-học-và-chọn-nơi-bắt-đầu']),
        'r1_g05': (['muc-tieu','g05-table-01'], ['diem-vao'], []),
        'r2_g01': (['muc-tieu','r2g01-table-01'], [], ['chọn-nơi-bắt-đầu']),
        'r2_g02': (['muc-tieu','r2g02-table-01'], [], []),
    }
    for ids, target in zip(source_ids[key], ['overview-goals','overview-prerequisites','overview-start']):
        aliases.update(dict.fromkeys(ids, target))
    return aliases


def _inline(node):
    """Reuse source wording/notation without duplicating IDs in the page."""
    copy = deepcopy(node)
    for element in [copy] + list(copy.select('[id]')):
        element.attrs.pop('id', None)
    for decoration in copy.select('.anchorjs-link, .header-anchor'):
        decoration.decompose()
    return copy.decode_contents()


def _anchor(heading, boundary):
    node = heading if heading.get('id') else heading.find_parent(id=True)
    if node is None or node is boundary:
        raise ValueError('A content heading needs its own source anchor: '
                         + heading.get_text(' ', strip=True))
    return node['id']


def _link(target, label, icon):
    return ('<a href="#' + escape(target, quote=True) + '"><span>'
            + escape(label) + '</span>' + icon('arrow') + '</a>')


def _d0(content, icon, btn):
    start = content.select_one('#bat-dau .reading-region')
    paragraphs = start.find_all('p', recursive=False)
    intro = ''.join('<p>' + _inline(p) + '</p>' for p in paragraphs[:3])
    steps = [
        ('khai-bao-pham-vi', 'Chuẩn bị và chọn câu khảo sát',
         'Đọc dòng “Kiến thức cần dùng” để chọn câu thuộc phần đã học. '
         'Không cần làm hết 24 bài.'),
        ('khao-sat', 'Tự làm những câu đã chọn',
         'Giữ bài tự làm trên giấy. Có thể bỏ qua câu dùng kiến thức chưa từng học; '
         'nếu ghi lại, phân biệt với phần đã học nhưng còn vướng.'),
        ('doc-ket-qua', 'Đối chiếu bài làm',
         'Mở hướng dẫn của những câu đã thử. So sánh cách làm, '
         'ghi chỗ chưa hiểu và nội dung nên ôn.'),
        ('chon-mach', 'Chọn nội dung để bắt đầu ôn',
         'Dựa vào bài vừa làm để chọn một hoặc hai nội dung muốn học. '
         'Em có thể dừng khảo sát và chuyển sang học bất cứ lúc nào.'),
    ]
    rows = []
    for target, title, description in steps:
        if content.find(id=target) is None:
            raise ValueError('Missing diagnostic section: ' + target)
        rows.append('<li>' + _link(target, title, icon)
                    + '<p>' + description + '</p></li>')
    return ('<div class="topic-overview-intro">' + intro + '</div>'
            '<div class="topic-overview-actions">'
            + btn('#khai-bao-pham-vi', 'Chọn câu khảo sát')
            + btn('chuyen-de.html', 'Chọn chuyên đề', 'secondary', 'book')
            + '</div><section class="topic-overview-section" id="overview-diagnostic"><h2>Cách làm khảo sát</h2>'
            '<ol class="topic-outline diagnostic-outline">' + ''.join(rows)
            + '</ol></section>')


def overview_content(p, content, icon, btn):
    """One orientation per topic, with four purposeful entries at its end."""
    if p['id'] == 'd0':
        return _d0(content, icon, btn)

    start = content.select_one('#bat-dau .reading-region')
    if start is None:
        raise ValueError('Missing source introduction: ' + p['id'])
    copy = OVERVIEWS.get(p['id'])
    if p['id']=='r2_g02':
        paragraphs_in_start=start.find_all('p',recursive=False)
        prerequisite=next(n for n in paragraphs_in_start if n.get_text(' ',strip=True).startswith('Kiến thức cần có.'))
        copy={'intro':[], 'prerequisites':[], 'choices':{
            'bai-hoc':'Cần học hoặc học lại thì vào Bài học.',
            'phieu-luyen':'Đã hiểu và muốn tự vận dụng thì vào Luyện tập.',
            'tu-kiem-tra':'Nếu đã chuẩn bị kĩ hoặc đủ tự tin, em có thể bắt đầu Kiểm tra.',
            'on-lai':'Ôn lại dành cho việc tự huy động kiến thức sau khoảng trễ.'}}
    if copy is None:raise ValueError('Missing source-owned orientation: '+p['id'])
    def paragraphs(values):
        return ''.join('<p>' + escape(value) + '</p>' for value in values)
    intro = ('<section class="overview-introduction" id="overview-introduction" aria-label="Giới thiệu chuyên đề">'
             + (''.join('<p>'+_inline(n)+'</p>' for n in paragraphs_in_start[:2]) if p['id']=='r2_g02' else paragraphs(copy['intro'])) + '</section>')

    goal_id = next(key for key,value in overview_aliases(p['id']).items()
                   if value == 'overview-goals' and 'table-' in key)
    goal_node = content.find(id=goal_id)
    goal_table = goal_node if goal_node and goal_node.name == 'table' else goal_node.find('table') if goal_node else None
    if goal_table is None:
        raise ValueError('Missing source learning goals: ' + p['id'])
    goals = []
    for row in goal_table.select('tbody tr'):
        cells = row.find_all(['td', 'th'], recursive=False)
        if len(cells) != 2:
            raise ValueError('Unexpected learning-goal row: ' + p['id'])
        goals.append('<div><dt>' + _inline(cells[0]) + '</dt><dd>'
                     + _inline(cells[1]) + '</dd></div>')
    if not goals:
        raise ValueError('Empty source learning goals: ' + p['id'])

    choices = []
    for target, title, symbol in [('bai-hoc','Bài học','book'),
                                  ('phieu-luyen','Luyện tập','pen'),
                                  ('tu-kiem-tra','Kiểm tra','check'),
                                  ('on-lai','Ôn lại','repeat')]:
        if content.find(id=target) is None:
            raise ValueError('Missing activity: ' + p['id'] + '/' + target)
        choices.append('<div class="overview-choice"><a href="#' + target + '">'
                       + icon(symbol) + '<span>' + title + '</span>' + icon('arrow')
                       + '</a><p>' + escape(copy['choices'][target]) + '</p></div>')
    return (intro
            + '<section class="topic-overview-section" id="overview-goals"><h2>Học xong, em cần làm được gì?</h2>'
            + '<dl class="overview-goals">' + ''.join(goals) + '</dl></section>'
            + '<section class="topic-overview-section" id="overview-prerequisites"><h2>Kiến thức cần dùng</h2>'
            + ('<p>'+_inline(prerequisite)+'</p>' if p['id']=='r2_g02' else paragraphs(copy['prerequisites'])) + '</section>'
            + '<section class="topic-overview-section" id="overview-start"><h2>Chọn phần học</h2>'
            + '<p>Em có thể chọn phần phù hợp với việc mình cần làm, không phải hoàn thành lần lượt cả bốn phần.</p>'
            + '<nav class="overview-choices" aria-label="Chọn phần học">'
            + ''.join(choices) + '</nav></section>')
