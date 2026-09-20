-- Candidate-only adapter. BBT values are literal data, never inferred.
local html = FORMAT:match('html') ~= nil
local latex = FORMAT:match('latex') ~= nil
local tables

local function esc(s)
  return s:gsub('&', '&amp;'):gsub('<', '&lt;'):gsub('>', '&gt;'):gsub('"', '&quot;')
end

local function tex(s)
  local value = pandoc.write(pandoc.Pandoc({pandoc.Plain({pandoc.Str(s)})}), 'latex'):gsub('%s+$', '')
  -- Literal glyph translation only: use the project's math font, not text glyphs.
  for glyph, command in pairs({['∞']='infty', ['↗']='nearrow', ['↘']='searrow', ['∥']='parallel'}) do
    value = value:gsub(glyph, function() return '\\ensuremath{\\'..command..'}' end)
  end
  return value
end

local function load_tables()
  if tables then return end
  local path = pandoc.path.join({pandoc.path.directory(PANDOC_SCRIPT_FILE), '../du_lieu/bang_bien_thien.json'})
  local file = assert(io.open(path, 'r'))
  local data = pandoc.json.decode(file:read('*a'))
  file:close()
  tables = {}
  for _, item in ipairs(data) do
    assert(not tables[item.id], 'Duplicate BBT ID')
    tables[item.id] = item
  end
end

local function variation(div)
  load_tables()
  local id = div.attributes.bbt
  local data = assert(tables[id], 'Missing BBT: '..tostring(id))
  local title = div.attributes.caption or data.title or 'Bảng biến thiên'
  local excluded = {}
  for _, column in ipairs(data.excluded_columns or {}) do excluded[column + 1] = true end
  local rows = {}
  for i, row in ipairs(data.rows) do
    rows[i] = {}
    for j, value in ipairs(row) do rows[i][j] = i > 1 and excluded[j] and '∥' or value end
  end
  if html then
    local output = {'<table class="variation" data-bbt="'..esc(id)..'"><caption>'..esc(title)..'</caption><thead>'}
    for i, row in ipairs(rows) do
      output[#output+1] = '<tr>'
      for j, value in ipairs(row) do
        local tag = (i == 1 or j == 1) and 'th' or 'td'
        local scope = j == 1 and ' scope="row"' or (i == 1 and ' scope="col"' or '')
        local class = i > 1 and excluded[j] and ' class="excluded"' or ''
        output[#output+1] = '<'..tag..scope..class..'>'..esc(value)..'</'..tag..'>'
      end
      output[#output+1] = '</tr>'
      if i == 1 then output[#output+1] = '</thead><tbody>' end
    end
    output[#output+1] = '</tbody></table>'
    return pandoc.RawBlock('html', table.concat(output))
  elseif latex then
    local count = #rows[1]
    local output = {'\\begin{center}\\small', tex(title)..'\\par\\medskip',
      '\\begin{tabular}{|'..string.rep('c|', count)..'}\\hline'}
    for _, row in ipairs(rows) do
      local cells = {}
      for _, value in ipairs(row) do cells[#cells+1] = tex(value) end
      output[#output+1] = table.concat(cells, ' & ')..' \\\\ \\hline'
    end
    output[#output+1] = '\\end{tabular}\\end{center}'
    return pandoc.RawBlock('latex', table.concat(output, '\n'))
  end
  error('R1-G01 supports HTML/PDF only')
end

function Div(div)
  if div.classes:includes('r1-bbt') then return variation(div) end
  if div.classes:includes('r1-summary') then
    if html then
      local inlines = div.content[1].content
      return {pandoc.RawBlock('html', '<summary>'), pandoc.Plain(inlines), pandoc.RawBlock('html', '</summary>')}
    end
    return div
  end
  if div.classes:includes('r1-details') then
    if html then
      if div.classes:includes('r1-solution') then div.classes:insert('solution') end
      local attrs = div.identifier ~= '' and ' id="'..esc(div.identifier)..'"' or ''
      local result = {pandoc.RawBlock('html', '<details'..attrs..' class="'..esc(table.concat(div.classes, ' '))..'">')}
      for _, block in ipairs(div.content) do result[#result+1] = block end
      result[#result+1] = pandoc.RawBlock('html', '</details>')
      return result
    end
    -- PDF always includes all solution/extension content; no student edition here.
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
  if latex and image.src:match('hinh/do_thi_%d+%.svg$') then
    image.src = image.src:gsub('%.svg$', '.png')
    image.attributes.width = '95%'
  end
  return image
end

-- The explicit outer figure owns the caption; suppress Pandoc's implicit one.
function Figure(figure)
  return figure.content
end

function Pandoc(doc)
  local maths, images = 0, 0
  doc:walk({
    Math = function() maths = maths + 1 end,
    Image = function() images = images + 1 end
  })
  assert(maths == 985, 'R1-G01 migration invariant: expected 985 math nodes')
  assert(images == 10, 'R1-G01 migration invariant: expected 10 graph images')
  io.stderr:write('R1-G01 render invariants: math=985; images=10\n')
  return doc
end
