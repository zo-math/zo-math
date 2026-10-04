-- Candidate-only adapter. BBT values are literal data, never inferred.
local html = FORMAT:match('html') ~= nil
local latex = FORMAT:match('latex') ~= nil
local variant = 'full'
local download_specs = nil
local section_download_specs = nil
local section_specs_by_variant = {}
local table_specs = nil
local table_specs_by_id = {}
local linked_table_ids = {}
local COMMON_LEARNING_ID = 'cách-học-với-tài-liệu-này'
local COMMON_SOURCES_ID = 'nguon'
local DOWNLOADS_ID = 'tai-tai-lieu'
local script_dir = pandoc.path.directory(PANDOC_SCRIPT_FILE)
local variation_module_path = pandoc.path.join({script_dir, '../../../../../../assets/lua/zo_variation_qmd.lua'})
local variation_css_path = pandoc.path.join({script_dir, '../../../../../../assets/css/zo_variation.css'})
local variation_module = assert(loadfile(variation_module_path))()
local variation = variation_module.new({
  data_path=pandoc.path.join({script_dir, '../du_lieu/bang_bien_thien.json'}),
  asset_dir='hinh',
  css_path=variation_css_path
})

local function render_variation(div)
  local rendered = variation.render(div)
  if not latex then return rendered end
  local id = assert(div.attributes.bbt, 'R1-G01 BBT is missing its identifier')
  local path = 'hinh/'..id:lower()..'.pdf'
  local needle = '\\includegraphics{'..path..'}'
  local first, last = rendered.text:find(needle, 1, true)
  assert(first and not rendered.text:find(needle, last + 1, true),
    'R1-G01 expected exactly one PDF image for '..id)
  local replacement = '\\includegraphics[trim=8.01pt 5.67pt 5.67pt 5.67pt,clip]{'..path..'}'
  rendered.text = rendered.text:sub(1, first - 1)..replacement..rendered.text:sub(last + 1)
  return rendered
end

local function esc(s)
  return s:gsub('&', '&amp;'):gsub('<', '&lt;'):gsub('>', '&gt;'):gsub('"', '&quot;')
end

local function meta_text(value)
  return pandoc.utils.stringify(value)
end

local function meta_numbers(values)
  local result = pandoc.List()
  if not values then return result end
  for _, value in ipairs(values) do
    local number = tonumber(meta_text(value))
    assert(number, 'R1-G01 table contract contains a non-numeric value')
    result:insert(number)
  end
  return result
end

local function replace_plain(text, needle, replacement)
  local result, start = {}, 1
  while true do
    local first, last = text:find(needle, start, true)
    if not first then
      result[#result + 1] = text:sub(start)
      return table.concat(result)
    end
    result[#result + 1] = text:sub(start, first - 1)
    result[#result + 1] = replacement
    start = last + 1
  end
end

local function render_grid_table(tbl)
  local output = pandoc.write(pandoc.Pandoc({tbl}), 'latex')
  output = output:gsub('\r', '')
  output = replace_plain(output, '@{}', '|')
  output = output:gsub('(%}%s*)\n(%s*>%{)', '%1|\n%2')
  output = replace_plain(output, '\\toprule\\noalign{}', '\\hline')
  output = replace_plain(output, '\\midrule\\noalign{}', '')
  output = replace_plain(output, '\\bottomrule\\noalign{}', '')
  output = replace_plain(output, '\\\\\n', '\\\\ \\hline\n')
  return pandoc.RawBlock('latex', table.concat({
    '\\begingroup',
    '\\arrayrulecolor[HTML]{D8D2CA}',
    '\\renewcommand{\\arraystretch}{1.18}',
    '\\setlength{\\tabcolsep}{4pt}',
    output,
    '\\endgroup'
  }, '\n'))
end

local function table_in(div)
  for _, block in ipairs(div.content) do
    if block.t == 'Table' then return block end
  end
  return nil
end

local function configure_table(block, tbl, spec, seen_ids)
  local id, label = meta_text(spec.id), meta_text(spec.label)
  local family, mode = meta_text(spec.family), meta_text(spec.mode)
  local widths, centers = meta_numbers(spec.widths), meta_numbers(spec.center)
  local row_header = meta_text(spec.row_header) == 'true'
  assert(id:match('^r1%-table%-t%d%d$') and not seen_ids[id], 'Invalid or duplicate R1-G01 table id: '..id)
  assert(family == 'R' or family == 'J', 'Invalid R1-G01 table family: '..family)
  assert(mode == 'fit' or mode == 'scroll', 'Invalid R1-G01 table mode: '..mode)
  assert(#widths == #tbl.colspecs, 'R1-G01 table '..id..' width count does not match its columns')
  local total = 0
  for _, width in ipairs(widths) do total = total + width end
  assert(total == 100, 'R1-G01 table '..id..' column widths must total 100')
  local min_width = spec.min_width and meta_text(spec.min_width) or ''
  assert((mode == 'fit' and min_width == '') or (mode == 'scroll' and min_width:match('^%d+em$')),
    'R1-G01 table '..id..' has an invalid min-width contract')
  seen_ids[id] = true

  block.identifier = id
  block.classes:insert('r1-table')
  block.classes:insert('r1-table-family-'..family:lower())
  block.classes:insert(mode == 'fit' and 'r1-table-fit' or 'r1-table-scroll-x')
  block.attributes['data-r1-table'] = id:sub(-3):upper()
  block.attributes['data-family'] = family
  block.attributes['data-responsive'] = mode
  block.attributes['data-col-widths'] = table.concat(widths, ',')
  block.attributes['data-row-header'] = tostring(row_header)
  if min_width ~= '' then
    block.attributes['data-min-width'] = min_width
    block.attributes['style'] = '--r1-table-min-width: '..min_width
  end
  if html and mode == 'scroll' then
    block.attributes['role'] = 'region'
    block.attributes['aria-label'] = label
    block.attributes['aria-describedby'] = id..'-hint'
    block.attributes['tabindex'] = '0'
  end

  tbl.classes:insert('r1-data-table')
  tbl.attributes['aria-label'] = label
  local centered = {}
  for _, column in ipairs(centers) do
    assert(column >= 1 and column <= #widths and column % 1 == 0,
      'R1-G01 table '..id..' has an invalid centered column')
    centered[column] = true
  end
  for column, width in ipairs(widths) do
    local alignment = centered[column] and pandoc.AlignCenter or tbl.colspecs[column][1]
    tbl.colspecs[column] = {alignment, width / 100}
  end
  for _, row in ipairs(tbl.head.rows) do
    for _, cell in ipairs(row.cells) do cell.attributes['scope'] = 'col' end
  end
  for _, body in ipairs(tbl.bodies) do
    body.row_head_columns = row_header and 1 or 0
    if row_header then
      for _, row in ipairs(body.body) do row.cells[1].attributes['scope'] = 'row' end
    end
  end
end

local function table_contains_link(tbl)
  return pandoc.write(pandoc.Pandoc({tbl}), 'json'):find('"t":"Link"', 1, true) ~= nil
end

local function render_linked_html_table(div)
  -- Quarto reconstructs link-bearing pipe tables after this filter and can drop
  -- Table attributes while retaining the wrapper. Keep the ordinary writer for
  -- the table content, and make its contracted minimum width explicit through
  -- the preserved wrapper so horizontal scrolling remains available.
  div.attributes['data-r1-linked-table'] = 'true'
  local style = pandoc.RawBlock('html', [[
<style>
.r1-table[data-r1-linked-table="true"] > table {
  min-width: var(--r1-table-min-width);
}
</style>]])
  local hint = pandoc.Div(
    {pandoc.Plain({pandoc.Str('Bảng có thể cuộn ngang. Kéo sang bên hoặc dùng phím mũi tên khi bảng đang được chọn.')})},
    pandoc.Attr(div.identifier..'-hint', {'r1-table-scroll-hint'}, {hidden='hidden'}))
  return {style, hint, div}
end

local function collect_linked_table_ids(doc, contract)
  local index = 0
  local function collect(blocks)
    for _, block in ipairs(blocks) do
      if block.t == 'Div' then
        local tbl = table_in(block)
        if tbl then
          index = index + 1
          local spec = assert(contract[index], 'R1-G01 ordinary table is missing a contract entry')
          if table_contains_link(tbl) then linked_table_ids[meta_text(spec.id)] = true end
        else
          collect(block.content)
        end
      elseif block.t == 'BlockQuote' then
        collect(block.content)
      end
    end
  end
  collect(doc.blocks)
  assert(index == #contract, 'R1-G01 ordinary table inventory changed while collecting linked tables')
end

local function apply_table_contract(doc)
  local contract = doc.meta['r1-tables']
  assert(contract and #contract == 18, 'R1-G01 table contract must contain 18 entries')
  local index, seen_ids = 0, {}
  local function configure(blocks)
    for _, block in ipairs(blocks) do
      if block.t == 'Div' then
        local tbl = table_in(block)
        if tbl then
          index = index + 1
          local spec = assert(contract[index], 'R1-G01 ordinary table is missing a contract entry')
          configure_table(block, tbl, spec, seen_ids)
        else
          configure(block.content)
        end
      elseif block.t == 'BlockQuote' then
        configure(block.content)
      end
    end
  end
  configure(doc.blocks)
  assert(index == 18, 'R1-G01 ordinary table inventory expected 18, got '..index)
  return doc
end

function Div(div)
  local configured_table = false
  if html and not div.classes:includes('r1-table') then
    local tbl = table_in(div)
    local spec = tbl and table_specs_by_id[div.identifier] or nil
    if spec then
      configure_table(div, tbl, spec, {})
      configured_table = true
    end
  end
  if html and div.classes:includes('r1-g01') then
    -- Expose headings to Pandoc's native TOC while retaining the HTML scope.
    local title = esc(div.attributes['r1-title'] or 'Đơn điệu và cực trị')
    local code = esc(div.attributes['r1-code'] or 'R1-G01')
    local blocks = pandoc.List({pandoc.RawBlock('html',
      '<div class="zo-on-thi-package r1-g01" data-r1-code="'..code..'" data-r1-title="'..title..'">')})
    blocks:extend(div.content)
    blocks:insert(pandoc.RawBlock('html', '</div>'))
    return blocks
  end
  if div.classes:includes('r1-downloads') then
    if not html then return {} end
    assert(download_specs and #download_specs == 2, 'R1-G01 download contract is unavailable')
    local cards = {}
    for _, item in ipairs(download_specs) do
      cards[#cards+1] = table.concat({
        '<article class="r1-download-card">',
        '<div class="r1-download-card__type" aria-hidden="true">PDF</div>',
        '<h3>', esc(item.title), '</h3>',
        '<p>', esc(item.description), '</p>',
        '<p class="r1-download-card__meta">', esc(item.pages), ' trang · PDF</p>',
        '<a class="zo-pdf-download__link" href="', esc(item.href), '" download="', esc(item.download), '">',
        '<i class="bi bi-download" aria-hidden="true"></i> Tải ', esc(item.title), '</a>',
        '</article>'
      })
    end
    return pandoc.RawBlock('html', '<div class="r1-downloads" aria-label="Các bản PDF">'..table.concat(cards)..'</div>')
  end
  if div.classes:includes('r1-section-downloads') then
    if not html then return {} end
    assert(section_download_specs and #section_download_specs == 6,
      'R1-G01 section download contract is unavailable')
    local items = {}
    for _, item in ipairs(section_download_specs) do
      items[#items+1] = table.concat({
        '<li class="r1-section-download-item">',
        '<span class="r1-section-download-copy">',
        '<span class="r1-section-download-title">', esc(item.title), '</span>',
        '<span class="r1-section-download-description">', esc(item.description), '</span>',
        '</span>',
        '<a class="zo-pdf-download__link r1-section-download-link" href="', esc(item.href),
        '" download="', esc(item.download), '">',
        '<i class="bi bi-download" aria-hidden="true"></i> Tải PDF</a>',
        '</li>'
      })
    end
    return pandoc.RawBlock('html',
      '<h3 class="r1-section-download-heading">Tải theo phần</h3>'..
      '<ul class="r1-section-download-list" aria-label="Các bản PDF theo phần">'..
      table.concat(items)..'</ul>')
  end
  if div.classes:includes('r1-download-support') then
    if not html then return {} end
    return pandoc.RawBlock('html', [[
<div class="r1-download-support" aria-labelledby="r1-support-title">
  <img class="r1-brand-mark" src="hinh/dau_nhan_zo.svg" alt="" width="198" height="8">
  <h3 id="r1-support-title">Ủng hộ ZO Math</h3>
  <p>Nếu học liệu hữu ích với bạn, bạn có thể ủng hộ ZO Math tiếp tục biên soạn và chia sẻ.</p>
  <div class="r1-support-details">
    <img class="r1-support-qr" src="/assets/images/qr_bao_tro_zo_math_vietcombank.jpg" alt="Mã QR Vietcombank để ủng hộ ZO Math" width="240" height="240">
    <dl>
      <div><dt>Ngân hàng</dt><dd>Vietcombank</dd></div>
      <div><dt>Số tài khoản</dt><dd>0601000137768</dd></div>
      <div><dt>Chủ tài khoản</dt><dd>Nguyễn Tấn Nhựt</dd></div>
      <div><dt>Nội dung chuyển khoản</dt><dd>BAO TRO ZO MATH</dd></div>
    </dl>
  </div>
  <p class="r1-support-link"><a href="/content/support/donate.html">Xem thông tin bảo trợ ZO Math</a></p>
</div>]])
  end
  if html and configured_table and linked_table_ids[div.identifier] then
    return render_linked_html_table(div)
  end
  if html and div.classes:includes('r1-table-scroll-x') then
    local hint = pandoc.Div(
      {pandoc.Plain({pandoc.Str('Bảng có thể cuộn ngang. Kéo sang bên hoặc dùng phím mũi tên khi bảng đang được chọn.')})},
      pandoc.Attr(div.identifier..'-hint', {'r1-table-scroll-hint'}, {hidden='hidden'}))
    return {hint, div}
  end
  if div.classes:includes('r1-bbt') then return render_variation(div) end
  if div.classes:includes('r1-summary') then
    if html then
      local inlines = div.content[1].content
      return {pandoc.RawBlock('html', '<summary class="zo-block-title">'), pandoc.Plain(inlines), pandoc.RawBlock('html', '</summary><div class="zo-block-body">')}
    end
    if latex then
      -- A flattened details label must stay with the start of its solution.
      return {pandoc.RawBlock('latex', '\\Needspace{3\\baselineskip}'), div}
    end
    return div
  end
  if div.classes:includes('r1-details') then
    if html then
      if div.classes:includes('r1-solution') then div.classes:insert('solution') end
      div.classes:insert('zo-block')
      div.classes:insert('zo-block-gray')
      local attrs = div.identifier ~= '' and ' id="'..esc(div.identifier)..'"' or ''
      local result = {pandoc.RawBlock('html', '<details'..attrs..' class="'..esc(table.concat(div.classes, ' '))..'">')}
      for _, block in ipairs(div.content) do result[#result+1] = block end
      result[#result+1] = pandoc.RawBlock('html', '</div></details>')
      return result
    end
    if latex then
      local title, body, before = nil, pandoc.List(), pandoc.List()
      for _, block in ipairs(div.content) do
        if block.t == 'Div' and block.classes:includes('r1-summary') then
          title = pandoc.Div(block.content, pandoc.Attr('', {'zo-block-title'}))
        elseif not title and block.t == 'RawBlock' and block.format == 'latex'
          and block.text == '\\Needspace{3\\baselineskip}' then
          -- Preserve the Phase 4 guard, but apply it outside the breakable box:
          -- its page-goal calculation is invalid inside a tcolorbox body.
          before:insert(block)
        else body:insert(block) end
      end
      assert(title, 'Details without summary')
      local color = div.classes:includes('zo-learning-guidance')
        and 'zo-block-white' or 'zo-block-gray'
      local box = pandoc.Div({title, pandoc.Div(body, pandoc.Attr('', {'zo-block-body'}))},
        pandoc.Attr('', {'zo-block', color}))
      -- Keep the original target; the common PDF block adapter owns the box.
      before:insert(box)
      return pandoc.Div(before, div.attr)
    end
    return div
  end
  if div.classes:includes('r1-figcaption') and html then
    local result = {pandoc.RawBlock('html', '<figcaption aria-hidden="true">')}
    for _, block in ipairs(div.content) do result[#result+1] = block end
    result[#result+1] = pandoc.RawBlock('html', '</figcaption>')
    return result
  end
  if div.classes:includes('r1-figcaption') and latex then
    local result = {pandoc.RawBlock('latex', '\\par\\smallskip{\\small\\color[HTML]{766F66}')}
    for _, block in ipairs(div.content) do result[#result+1] = block end
    result[#result+1] = pandoc.RawBlock('latex', '\\par}')
    return result
  end
  if div.classes:includes('r1-figure') and html then
    local result = {pandoc.RawBlock('html', '<figure>')}
    for _, block in ipairs(div.content) do result[#result+1] = block end
    result[#result+1] = pandoc.RawBlock('html', '</figure>')
    return result
  end
  if div.classes:includes('r1-figure') and latex then
    local result = {pandoc.RawBlock('latex', '\\begin{center}')}
    for _, block in ipairs(div.content) do result[#result+1] = block end
    result[#result+1] = pandoc.RawBlock('latex', '\\end{center}')
    return result
  end
  if configured_table then return div end
end

function Image(image)
  local graph_number = image.src:match('^hinh/do_thi_(%d%d)%.svg$')
  graph_number = tonumber(graph_number)
  if latex and graph_number and graph_number >= 1 and graph_number <= 13 then
    image.src = image.src:gsub('%.svg$', '.pdf')
    -- Preserve the asset's canonical physical size. Pandoc's \maxwidth policy
    -- still shrinks an oversized asset, but must never enlarge a narrow one.
    image.attributes.width = nil
  end
  return image
end

-- The explicit outer figure owns the caption; suppress Pandoc's implicit one.
function Figure(figure)
  return figure.content
end

function Table(tbl)
  if latex then return render_grid_table(tbl) end
end

function Header(header)
  if latex and header.level == 2 then
    header.content:insert(1, pandoc.RawInline('latex', '\\color{zomathred}'))
  end
  return header
end

function Blocks(blocks)
  if not latex then return nil end
  local result = pandoc.List()
  for i, block in ipairs(blocks) do
    local following = blocks[i + 1]
    local previous = blocks[i - 1]
    local label = (block.t == 'Para' or block.t == 'Plain') and pandoc.utils.stringify(block) or ''
    if block.t == 'Header' and following and following.t == 'Div'
      and following.classes:includes('r1-guidance') then
      -- Keep a section heading with the flattened guidance label and useful
      -- opening content. The box remains breakable; only the opening group is
      -- protected. The short four-step repair cycle can stay whole.
      local lines = following.identifier == 'cach-thuc-hien-sua-loi' and 16 or 10
      result:insert(pandoc.RawBlock('latex', '\\Needspace{'..lines..'\\baselineskip}'))
    end
    if (block.t == 'Para' or block.t == 'Plain') and following and following.t == 'Div'
      and following.classes:includes('answer-link')
      and not pandoc.utils.stringify(following):match('^Xem đề bài') then
      -- A return link closes the preceding explanation. Start that final
      -- paragraph only where a useful part of it and the link can stay together.
      result:insert(pandoc.RawBlock('latex', '\\Needspace{8\\baselineskip}'))
    end
    if (label == 'Bảng I' or label == 'Bảng II') and following and following.t == 'Div'
      and following.classes:includes('table-scroll') then
      -- Keep the exercise label with the BBT caption and table that it names.
      result:insert(pandoc.RawBlock('latex', '\\Needspace{12\\baselineskip}'))
    end
    if block.t == 'Header' and block.identifier == 'nhat-ky' then
      -- The short learning-log table fits on one page. Start its semantic
      -- group only where the heading, lead-in and complete table can stay
      -- together, avoiding a repeated longtable header on the next page.
      result:insert(pandoc.RawBlock('latex', '\\Needspace{18\\baselineskip}'))
    end
    if block.t == 'Header' and following and following.t == 'Div'
      and following.classes:includes('answer-link')
      and not pandoc.utils.stringify(following):match('^Xem đề bài') then
      -- A link is not the beginning of the task: keep some actual question text
      -- with its heading as well, without grouping the entire exercise.
      result:insert(pandoc.RawBlock('latex', '\\Needspace{10\\baselineskip}'))
    end
    if block.t == 'Header' and following and following.t == 'Div'
      and following.classes:includes('table-scroll') then
      -- Longtable may otherwise leave its section heading on the previous page.
      result:insert(pandoc.RawBlock('latex', '\\Needspace{6\\baselineskip}'))
      -- H4 now maps to a paragraph heading; allow for a multi-line first row
      -- as well as the heading/header (the Phase 4 six-line guard stays above).
      if block.level == 4 then
        result:insert(pandoc.RawBlock('latex', '\\Needspace{10\\baselineskip}'))
      end
    end
    if block.t == 'Header' and following and following.t == 'Div'
      and following.classes:includes('r1-example') then
      -- Keep a numbered knowledge subsection with the beginning of its example.
      result:insert(pandoc.RawBlock('latex', '\\Needspace{8\\baselineskip}'))
    end
    if block.t == 'Div' and block.classes:includes('r1-task') then
      -- A functional label is not a heading, so give its short task group an
      -- explicit guard against a label stranded at the foot of a page.
      result:insert(pandoc.RawBlock('latex', '\\Needspace{6\\baselineskip}'))
    end
    if block.t == 'Div' and block.classes:includes('table-scroll')
      and previous and previous.t == 'Div' and previous.classes:includes('r1-summary') then
      -- Keep a compact label/table group without duplicated paragraph/table gaps.
      result:insert(pandoc.RawBlock('latex', '\\begingroup\\setlength{\\LTpre}{\\smallskipamount}\\setlength{\\LTpost}{\\smallskipamount}'))
      result:insert(block)
      result:insert(pandoc.RawBlock('latex', '\\endgroup'))
    else
      result:insert(block)
    end
  end
  return result
end

local function finish(doc)
  doc = variation.inject(doc)
  if html then
    -- Quarto 1.8 probes returned Pandoc callbacks with a metadata document.
    -- Mutate that metadata in place but do not replace the real block stream.
    return nil
  end
  if latex then
    local includes = doc.meta['header-includes'] or pandoc.MetaList({})
    if pandoc.utils.type(includes) ~= 'List' then includes = pandoc.MetaList({includes}) end
    includes:insert(pandoc.MetaBlocks({pandoc.RawBlock('latex', '\\usepackage{needspace}')}))
    includes:insert(pandoc.MetaBlocks({pandoc.RawBlock('latex',
      '\\AtBeginDocument{\\hypersetup{urlcolor=zomathgray}}')}))
    -- Keep the shared one-line ZO Math + official short-title running header.
    -- Variant labels belong to the cover/download cards, not repeated headers.
    includes:insert(pandoc.MetaBlocks({pandoc.RawBlock('latex', [[
\AtBeginDocument{%
  \renewcommand{\maketitle}{%
    \thispagestyle{plain}%
    \begin{center}
      \vspace*{-1.5em}%
      \includegraphics[width=27mm]{zo_math_logo_black_on_transprentt_1024.pdf}\par
      \vspace{0.8em}%
      {\small\color{zomathgray}\zoPdfCollection\par}%
      \vspace{0.75em}%
      \includegraphics[width=46mm]{hinh/dau_nhan_zo.png}\par
      \vspace{1.3em}%
      {\LARGE\bfseries\color{zomathred}\zoPdfTitle\par}%
      \vspace{0.55em}%
      {\large\color{zomathgray}\zoPdfSubtitle\par}%
      \vspace{0.8em}%
      {\small\color{zomathgray}Phiên bản ứng viên v1.3\enspace·\enspace
        \href{\zoPdfCanonicalUrl}{\zoPdfDisplayUrl}\par}%
    \end{center}%
    \vspace{0.8em}%
  }%
}]])}))
    doc.meta['header-includes'] = includes
    doc.blocks:insert(pandoc.RawBlock('latex', [[
\par\medskip
\begin{center}
  \includegraphics[width=38mm]{hinh/dau_nhan_zo.png}\par
  \vspace{0.7em}
  {\small\bfseries Kết thúc học liệu “\zoPdfTitle”.\par}
  \vspace{0.35em}
  {\small\color{zomathgray}
    \href{\zoPdfCanonicalUrl}{Trở lại gói học liệu trực tuyến}\par}
  \vspace{0.6em}
  \href{\zoPdfCanonicalUrl}{\qrcode[height=15mm]{\zoPdfCanonicalUrl}}\par
\end{center}
]]))
  end
  if latex then
    -- Reuse, do not fork, the shared ZO Math PDF block conversion. Its earlier
    -- project pass cannot see the package-specific details until this adapter.
    local env = setmetatable({}, {__index=_G})
    local common = pandoc.path.join({script_dir, '../../../../../../assets/lua/zo_pdf_content.lua'})
    assert(loadfile(common, 't', env))()
    doc = env.Pandoc(doc)
  end
  return doc
end

local function inventory(doc)
  local found = {math=0, images=0, tables=0, bbt=0, details=0, answers=0}
  doc:walk({Math=function() found.math=found.math+1 end,
    Image=function() found.images=found.images+1 end,
    Table=function() found.tables=found.tables+1 end,
    Div=function(d)
      if d.classes:includes('r1-bbt') then found.bbt=found.bbt+1 end
      if d.classes:includes('r1-details') then found.details=found.details+1 end
      if d.classes:includes('answer-link') then found.answers=found.answers+1 end
    end})
  return found
end

local function assert_inventory(doc, expected, label)
  local found = inventory(doc)
  io.stderr:write('R1-G01 '..label..' inventory: '..pandoc.json.encode(found)..'\n')
  for key, value in pairs(expected) do
    assert(found[key] == value, 'R1-G01 '..label..': '..key..' expected '..value..', got '..found[key])
  end
end

local function blocks_slice(blocks, first, last)
  local result = pandoc.List()
  for index = first, last do result:insert(blocks[index]) end
  return result
end

local function blocks_extend(target, source)
  for _, block in ipairs(source) do target:insert(block) end
end

local function identifiers_in_blocks(blocks)
  local identifiers = {}
  local function remember(element)
    if element.identifier and element.identifier ~= '' then
      assert(not identifiers[element.identifier],
        'Duplicate R1-G01 identifier in PDF projection: '..element.identifier)
      identifiers[element.identifier] = true
    end
  end
  pandoc.Pandoc(blocks):walk({
    Header=remember, Div=remember, Span=remember, CodeBlock=remember, Table=remember
  })
  return identifiers
end

local function h2_positions(blocks)
  local positions = {}
  for index, block in ipairs(blocks) do
    if block.t == 'Header' and block.level == 2 then
      assert(block.identifier ~= '', 'R1-G01 H2 is missing an identifier')
      assert(not positions[block.identifier], 'Duplicate R1-G01 H2: '..block.identifier)
      positions[block.identifier] = index
    end
  end
  return positions
end

local function projection_boundary_chain(specs)
  assert(specs and #specs > 0, 'R1-G01 section projection manifest is empty')
  local boundaries = pandoc.List({COMMON_LEARNING_ID})
  local expected_start = nil
  for _, spec in ipairs(specs) do
    assert(spec.start ~= '' and spec.end_before ~= '',
      'R1-G01 section projection boundary is incomplete')
    if expected_start then
      assert(spec.start == expected_start,
        'R1-G01 section projection boundaries are not contiguous at #'..spec.start)
    end
    boundaries:insert(spec.start)
    expected_start = spec.end_before
  end
  assert(expected_start == COMMON_SOURCES_ID,
    'R1-G01 final section projection boundary must precede #'..COMMON_SOURCES_ID)
  boundaries:insert(COMMON_SOURCES_ID)
  boundaries:insert(DOWNLOADS_ID)
  return boundaries
end

local function verify_projection_boundary_fixture()
  local fixture = {
    {start='fixture-first', end_before='fixture-second'},
    {start='fixture-second', end_before=COMMON_SOURCES_ID},
  }
  local before = projection_boundary_chain(fixture)
  fixture[1].start = 'fixture-renamed'
  local after = projection_boundary_chain(fixture)
  assert(before[2] == 'fixture-first' and after[2] == 'fixture-renamed'
      and before[3] == 'fixture-second' and after[3] == 'fixture-second',
    'R1-G01 fixture manifest boundary change was not reflected in the derived chain')
end

local function append_external_label(link)
  link.content:insert(pandoc.Space())
  link.content:insert(pandoc.Str('(mở'))
  link.content:insert(pandoc.Space())
  link.content:insert(pandoc.Str('trên'))
  link.content:insert(pandoc.Space())
  link.content:insert(pandoc.Str('trang'))
  link.content:insert(pandoc.Space())
  link.content:insert(pandoc.Str('học'))
  link.content:insert(pandoc.Space())
  link.content:insert(pandoc.Str('liệu)'))
end

local function rewrite_projection_links(doc, original_blocks, positions, canonical_url, boundary_chain)
  local owner_by_id = {}
  for _, spec in ipairs(section_download_specs) do
    local first, last = positions[spec.start], positions[spec.end_before] - 1
    for identifier in pairs(identifiers_in_blocks(blocks_slice(original_blocks, first, last))) do
      assert(not owner_by_id[identifier], 'R1-G01 identifier has multiple owner views: '..identifier)
      owner_by_id[identifier] = spec.view
    end
  end
  local common_ranges = {
    {positions[COMMON_LEARNING_ID], positions[boundary_chain[2]] - 1, 'cach-hoc'},
    {positions[COMMON_SOURCES_ID], positions[DOWNLOADS_ID] - 1, 'cach-hoc'},
  }
  for _, range in ipairs(common_ranges) do
    for identifier in pairs(identifiers_in_blocks(blocks_slice(original_blocks, range[1], range[2]))) do
      owner_by_id[identifier] = range[3]
    end
  end

  local included = identifiers_in_blocks(doc.blocks)
  local rewritten = 0
  doc = doc:walk({Link=function(link)
    if link.target:sub(1, 1) ~= '#' then return nil end
    local target = link.target:sub(2)
    if included[target] then return nil end
    local owner = assert(owner_by_id[target], 'R1-G01 cannot resolve omitted link target: #'..target)
    link.target = canonical_url..'?r1-view='..owner..'#'..target
    append_external_label(link)
    rewritten = rewritten + 1
    return link
  end})
  local final_ids = identifiers_in_blocks(doc.blocks)
  doc:walk({Link=function(link)
    if link.target:sub(1, 1) == '#' then
      assert(final_ids[link.target:sub(2)], 'R1-G01 dangling PDF hash link: '..link.target)
    end
  end})
  return doc, rewritten
end

local function project_part(doc, spec, canonical_url)
  local root = nil
  for _, block in ipairs(doc.blocks) do
    if block.t == 'Div' and block.classes:includes('r1-g01') then
      assert(not root, 'Duplicate R1-G01 root div')
      root = block
    end
  end
  assert(root, 'R1-G01 PDF projection root is missing')
  local original_blocks = root.content
  local positions = h2_positions(original_blocks)
  local required = projection_boundary_chain(section_download_specs)
  local previous = 0
  for _, identifier in ipairs(required) do
    local current = assert(positions[identifier], 'R1-G01 projection boundary is missing: #'..identifier)
    assert(current > previous, 'R1-G01 projection boundaries are out of order at #'..identifier)
    previous = current
  end
  local first = assert(positions[spec.start], 'R1-G01 part start is missing: #'..spec.start)
  local after = assert(positions[spec.end_before], 'R1-G01 part end is missing: #'..spec.end_before)
  assert(first < after, 'R1-G01 part boundaries are out of order: '..spec.variant)

  local preface = blocks_slice(original_blocks, 1, positions[COMMON_LEARNING_ID] - 1)
  local learning = blocks_slice(original_blocks, positions[COMMON_LEARNING_ID], positions[required[2]] - 1)
  local selected = blocks_slice(original_blocks, first, after - 1)
  local sources = blocks_slice(original_blocks, positions[COMMON_SOURCES_ID], positions[DOWNLOADS_ID] - 1)
  local shared = pandoc.List()
  blocks_extend(shared, preface)
  blocks_extend(shared, learning)
  blocks_extend(shared, sources)
  local projected = pandoc.List()
  blocks_extend(projected, preface)
  blocks_extend(projected, learning)
  blocks_extend(projected, selected)
  blocks_extend(projected, sources)
  root.content = projected

  local selected_inventory = inventory(pandoc.Pandoc(selected))
  local shared_inventory = inventory(pandoc.Pandoc(shared))
  local combined_inventory = inventory(doc)
  io.stderr:write('R1-G01 part inventory: '..pandoc.json.encode({
    variant=spec.variant, selected=selected_inventory,
    shared=shared_inventory, combined=combined_inventory
  })..'\n')
  local rewritten
  doc, rewritten = rewrite_projection_links(doc, original_blocks, positions, canonical_url, required)
  io.stderr:write('R1-G01 '..spec.variant..' externalized links: '..rewritten..'\n')
  return doc
end

local function build_lesson_toc(doc)
  local headings = pandoc.List()
  doc:walk({Header=function(heading)
    if tonumber(heading.level) == 3 and #headings < 9 then
      headings:insert(heading)
    end
  end})
  assert(#headings == 9, 'R1-G01 lesson TOC expected 9 H3 headings, got '..#headings)
  assert(headings[1].identifier == 'bắt-đầu-từ-đâu' and headings[9].identifier == 'khép-lại-bài-học',
    'R1-G01 lesson TOC boundaries changed unexpectedly')
  local lines = pandoc.List()
  for _, heading in ipairs(headings) do
    lines:insert(pandoc.List({pandoc.Link(heading.content, '#'..heading.identifier)}))
  end
  local replaced = 0
  doc = doc:walk({Div=function(div)
    if div.classes:includes('lesson-toc') then
      div.content = pandoc.List({pandoc.LineBlock(lines)})
      replaced = replaced + 1
      return div
    end
  end})
  assert(replaced == 1, 'R1-G01 lesson TOC placeholder expected once, got '..replaced)
  return doc
end

local function prepare(doc)
  local download_meta = doc.meta['r1-download-files']
  assert(download_meta and #download_meta == 2, 'R1-G01 download contract must contain 2 entries')
  download_specs = {}
  for _, item in ipairs(download_meta) do
    local spec = {
      href=meta_text(item.href), download=meta_text(item.download),
      title=meta_text(item.title), description=meta_text(item.description),
      pages=meta_text(item.pages)
    }
    assert(spec.href:match('%.pdf$') and spec.download:match('%.pdf$'), 'Invalid R1-G01 PDF download')
    assert(tonumber(spec.pages) and tonumber(spec.pages) > 0, 'Invalid R1-G01 PDF page count')
    download_specs[#download_specs+1] = spec
  end
  local section_download_meta = doc.meta['r1-section-download-files']
  assert(section_download_meta and #section_download_meta == 6,
    'R1-G01 section download contract must contain 6 entries')
  section_download_specs = {}
  section_specs_by_variant = {}
  local seen_outputs, seen_downloads = {}, {}
  for _, item in ipairs(section_download_meta) do
    local spec = {
      variant=meta_text(item.variant), href=meta_text(item.href),
      download=meta_text(item.download), title=meta_text(item.title),
      description=meta_text(item.description), start=meta_text(item.start),
      end_before=meta_text(item['end-before']), view=meta_text(item.view)
    }
    assert(spec.variant:match('^[a-z][a-z0-9_]*$'), 'Invalid R1-G01 section PDF variant')
    assert(spec.href:match('^[a-z0-9_]+%.pdf$') and spec.download:match('^[A-Za-z0-9_.-]+%.pdf$'),
      'Invalid R1-G01 section PDF filename')
    assert(spec.start ~= '' and spec.end_before ~= '' and spec.view ~= '',
      'Incomplete R1-G01 section projection contract')
    assert(not section_specs_by_variant[spec.variant], 'Duplicate R1-G01 section variant: '..spec.variant)
    assert(not seen_outputs[spec.href:lower()], 'Duplicate R1-G01 section output: '..spec.href)
    assert(not seen_downloads[spec.download:lower()], 'Duplicate R1-G01 section download name: '..spec.download)
    section_specs_by_variant[spec.variant] = spec
    seen_outputs[spec.href:lower()] = true
    seen_downloads[spec.download:lower()] = true
    section_download_specs[#section_download_specs+1] = spec
  end
  verify_projection_boundary_fixture()
  table_specs = doc.meta['r1-tables']
  assert(table_specs and #table_specs == 18, 'R1-G01 table contract must contain 18 entries')
  table_specs_by_id = {}
  for _, spec in ipairs(table_specs) do
    local id = meta_text(spec.id)
    assert(not table_specs_by_id[id], 'Duplicate R1-G01 table contract id: '..id)
    table_specs_by_id[id] = spec
  end
  if html then collect_linked_table_ids(doc, table_specs) end
  if html then return nil end
  if latex then doc = build_lesson_toc(doc) end
  doc = apply_table_contract(doc)
  assert_inventory(doc, {math=1468, images=13, tables=18, bbt=13, details=52, answers=100}, 'source')
  if latex then
    variant = pandoc.utils.stringify(doc.meta['zo-pdf-variant'] or 'full')
    local part_spec = section_specs_by_variant[variant]
    assert(variant == 'full' or variant == 'student' or part_spec,
      'Unknown R1-G01 PDF variant')
    if part_spec then
      local output = pandoc.utils.stringify(doc.meta['zo-pdf-output'] or '')
      assert(output == part_spec.href,
        'R1-G01 manifest/registry output mismatch for '..variant)
      local branding = assert(doc.meta['zo-pdf-branding'], 'R1-G01 PDF branding is missing')
      local canonical_url = meta_text(branding['canonical-url'])
      assert(canonical_url:match('^https://[^#?]+$'), 'R1-G01 canonical URL must come from PDF branding metadata')
      doc = project_part(doc, part_spec, canonical_url)
      return doc
    end
    local removed_download = false
    doc = doc:walk({Div=function(d)
      if not d.classes:includes('r1-g01') then return nil end
      local blocks, excluding = pandoc.List(), false
      for _, block in ipairs(d.content) do
        if block.t == 'Header' and block.level == 2 and block.identifier == 'tai-tai-lieu' then
          excluding = true
          removed_download = true
        end
        if not excluding then blocks:insert(block) end
      end
      d.content = blocks
      return d
    end})
    assert(removed_download, 'PDF projection did not find #tai-tai-lieu')
    if variant == 'student' then
      local solution_start = assert(section_specs_by_variant['loi_giai'],
        'R1-G01 solution projection is missing from the manifest').start
      local removed = false
      doc = doc:walk({Div=function(d)
        if d.classes:includes('answer-link') then return {} end
        if not d.classes:includes('r1-g01') then return nil end
        local blocks, excluding = pandoc.List(), false
        for _, block in ipairs(d.content) do
          if block.t == 'Header' and block.level == 2 then
            excluding = block.identifier == solution_start
            if excluding then assert(not removed, 'Duplicate solution section'); removed = true end
          end
          if not excluding then blocks:insert(block) end
        end
        d.content = blocks
        return d
      end})
      assert(removed, 'Student projection did not find #'..solution_start)
      -- Approved R1-G01 editorial projection; the solution section removes 669 math,
      -- 2 images, 4 ordinary tables, 2 BBT blocks, 37 details blocks and 100 answer links.
      assert_inventory(doc, {math=799, images=11, tables=14, bbt=11, details=15, answers=0}, 'student')
    else
      assert_inventory(doc, {math=1468, images=13, tables=18, bbt=13, details=52, answers=100}, 'full')
    end
    local identifiers = identifiers_in_blocks(doc.blocks)
    doc:walk({Link=function(link)
      if link.target:sub(1, 1) == '#' then
        assert(identifiers[link.target:sub(2)], 'R1-G01 dangling PDF hash link: '..link.target)
      end
    end})
  end
  return doc
end

return {{Pandoc=prepare}, {Div=Div, Image=Image, Figure=Figure, Table=Table, Header=Header, Blocks=Blocks}, {Pandoc=finish}}
