-- Candidate-only adapter. BBT values are literal data, never inferred.
local html = FORMAT:match('html') ~= nil
local latex = FORMAT:match('latex') ~= nil
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
  if div.classes:includes('r1-bbt') then return variation.render(div) end
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
  local graph_number = image.src:match('^hinh/do_thi_(%d%d)%.svg$')
  graph_number = tonumber(graph_number)
  if latex and graph_number and graph_number >= 1 and graph_number <= 10 then
    image.src = image.src:gsub('%.svg$', '.pdf')
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
  doc = variation.inject(doc)
  return doc
end
