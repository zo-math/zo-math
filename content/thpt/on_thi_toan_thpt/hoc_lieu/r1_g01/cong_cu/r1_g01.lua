-- Candidate-only adapter. BBT values are literal data, never inferred.
local html = FORMAT:match('html') ~= nil
local latex = FORMAT:match('latex') ~= nil
local variant = 'full'
local script_dir = pandoc.path.directory(PANDOC_SCRIPT_FILE)
local variation_module_path = pandoc.path.join({script_dir, '../../../../../../assets/lua/zo_variation_qmd.lua'})
local variation_css_path = pandoc.path.join({script_dir, '../../../../../../assets/css/zo_variation.css'})
local variation_module = assert(loadfile(variation_module_path))()
local variation = variation_module.new({
  data_path=pandoc.path.join({script_dir, '../du_lieu/bang_bien_thien.json'}),
  asset_dir='hinh',
  css_path=variation_css_path
})

local function esc(s)
  return s:gsub('&', '&amp;'):gsub('<', '&lt;'):gsub('>', '&gt;'):gsub('"', '&quot;')
end

function Div(div)
  if html and div.classes:includes('r1-g01') then
    -- Expose headings to Pandoc's native TOC while retaining the HTML scope.
    local blocks = pandoc.List({pandoc.RawBlock('html', '<div class="r1-g01">')})
    blocks:extend(div.content)
    blocks:insert(pandoc.RawBlock('html', '</div>'))
    return blocks
  end
  if div.classes:includes('r1-downloads') then
    if not html then return {} end
    local links = {}
    for _, item in ipairs({
      {'index_hoc_sinh.pdf', 'R1-G01_hoc_va_bai_tap_v1.2.pdf', 'PDF học và bài tập — không lời giải'},
      {'index.pdf', 'R1-G01_hoc_lieu_day_du_v1.2.pdf', 'PDF đầy đủ — có lời giải'}
    }) do
      links[#links+1] = pandoc.Link({pandoc.RawInline('html', '<i class="bi bi-file-earmark-pdf" aria-hidden="true"></i>'),
        pandoc.Space(), pandoc.Str(item[3])}, item[1], '',
        pandoc.Attr('', {'zo-pdf-download__link'}, {download=item[2]}))
      links[#links+1] = pandoc.Space()
    end
    return pandoc.Div({pandoc.Plain(links)}, div.attr)
  end
  if div.classes:includes('r1-guidance') and latex then
    local text = 'Tải bản học và bài tập để tự làm; dùng bản đầy đủ khi cần đối chiếu lời giải.'
    if variant == 'student' then
      text = text..' Bản này không kèm lời giải. Khi cần đối chiếu, dùng bản PDF đầy đủ.'
    end
    return pandoc.Para({pandoc.Str(text)})
  end
  if div.classes:includes('r1-bbt') then return variation.render(div) end
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
      div.classes:insert(div.classes:includes('r1-solution') and 'zo-block-gray' or 'zo-block-yellow')
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
      local color = div.classes:includes('r1-solution') and 'zo-block-gray' or 'zo-block-yellow'
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
  if div.classes:includes('r1-figure') and html then
    local result = {pandoc.RawBlock('html', '<figure>')}
    for _, block in ipairs(div.content) do result[#result+1] = block end
    result[#result+1] = pandoc.RawBlock('html', '</figure>')
    return result
  end
end

function Image(image)
  local graph_number = image.src:match('^hinh/do_thi_(%d%d)%.svg$')
  graph_number = tonumber(graph_number)
  if latex and graph_number and graph_number >= 1 and graph_number <= 10 then
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

function Blocks(blocks)
  if not latex then return nil end
  local result = pandoc.List()
  for i, block in ipairs(blocks) do
    local following = blocks[i + 1]
    local previous = blocks[i - 1]
    if block.t == 'Header' and block.identifier == 'nhat-ky' then
      -- The short learning-log table fits on one page. Start its semantic
      -- group only where the heading, lead-in and complete table can stay
      -- together, avoiding a repeated longtable header on the next page.
      result:insert(pandoc.RawBlock('latex', '\\Needspace{18\\baselineskip}'))
    end
    if block.t == 'Header' and following and following.t == 'Div'
      and following.classes:includes('answer-link') then
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
  if latex then
    local includes = doc.meta['header-includes'] or pandoc.MetaList({})
    if pandoc.utils.type(includes) ~= 'List' then includes = pandoc.MetaList({includes}) end
    includes:insert(pandoc.MetaBlocks({pandoc.RawBlock('latex', '\\usepackage{needspace}')}))
    doc.meta['header-includes'] = includes
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
  for key, value in pairs(expected) do
    assert(found[key] == value, 'R1-G01 '..label..': '..key..' expected '..value..', got '..found[key])
  end
  io.stderr:write('R1-G01 '..label..' inventory: '..pandoc.json.encode(found)..'\n')
end

local function prepare(doc)
  assert_inventory(doc, {math=989, images=10, tables=17, bbt=13, details=16, answers=42}, 'source')
  if latex then
    variant = pandoc.utils.stringify(doc.meta['zo-pdf-variant'] or 'full')
    assert(variant == 'full' or variant == 'student', 'Unknown R1-G01 PDF variant')
    if variant == 'student' then
      local removed = false
      doc = doc:walk({Div=function(d)
        if d.classes:includes('answer-link') then return {} end
        if not d.classes:includes('r1-g01') then return nil end
        local blocks, excluding = pandoc.List(), false
        for _, block in ipairs(d.content) do
          if block.t == 'Header' and block.level == 2 then
            excluding = block.identifier == 'loi-giai'
            if excluding then assert(not removed, 'Duplicate solution section'); removed = true end
          end
          if not excluding then blocks:insert(block) end
        end
        d.content = blocks
        return d
      end})
      assert(removed, 'Student projection did not find #loi-giai')
      -- Approved R1-G01 editorial projection; #loi-giai removes 399 math / 4 ordinary tables.
      assert_inventory(doc, {math=590, images=8, tables=13, bbt=11, details=1, answers=0}, 'student')
    else
      assert_inventory(doc, {math=989, images=10, tables=17, bbt=13, details=16, answers=42}, 'full')
    end
  end
  return doc
end

return {{Pandoc=prepare}, {Div=Div, Image=Image, Figure=Figure, Blocks=Blocks}, {Pandoc=finish}}
