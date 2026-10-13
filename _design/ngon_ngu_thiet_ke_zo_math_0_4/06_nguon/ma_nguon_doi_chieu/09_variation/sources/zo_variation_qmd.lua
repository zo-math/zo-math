-- Shared ZO Math variation-table integration. Package filters configure this
-- module; they do not duplicate JSON loading, HTML, PDF or accessibility code.
local M = {}

local function esc(s)
  return s:gsub('&', '&amp;'):gsub('<', '&lt;'):gsub('>', '&gt;'):gsub('"', '&quot;')
end

local function tex(s)
  local value = pandoc.write(pandoc.Pandoc({pandoc.Plain({pandoc.Str(s)})}), 'latex'):gsub('%s+$', '')
  for glyph, command in pairs({['∞']='infty', ['↗']='nearrow', ['↘']='searrow', ['∥']='parallel'}) do
    value = value:gsub(glyph, function() return '\\ensuremath{\\'..command..'}' end)
  end
  return value
end

function M.new(options)
  assert(options and options.data_path and options.asset_dir, 'Variation integration requires data_path and asset_dir')
  local tables

  local function load_tables()
    if tables then return end
    local file = assert(io.open(options.data_path, 'r'))
    local data = pandoc.json.decode(file:read('*a'))
    file:close()
    tables = {}
    for _, item in ipairs(data) do
      assert(not tables[item.id], 'Duplicate BBT ID')
      tables[item.id] = item
    end
  end

  local function render(div)
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
    if FORMAT:match('html') then
      local output = {'<figure class="zo-variation-asset" data-bbt="'..esc(id)..'">',
        '<img class="zo-variation-image" src="'..options.asset_dir..'/'..id:lower()..'.svg" alt="'..esc(title)..' — '..esc(id)..'">',
        '<figcaption class="zo-variation-caption">'..esc(title)..'</figcaption>',
        '<div class="visually-hidden"><table class="variation" data-bbt="'..esc(id)..'"><caption>'..esc(title)..'</caption><thead>'}
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
      output[#output+1] = '</tbody></table></div></figure>'
      return pandoc.RawBlock('html', table.concat(output))
    end
    if FORMAT:match('latex') then
      local path = options.asset_dir..'/'..id:lower()..'.pdf'
      local output = {'\\begin{minipage}{\\linewidth}\\centering',
        '\\adjustbox{max width=.95\\linewidth,max totalheight=.22\\textheight}{\\includegraphics{'..path..'}}\\par\\smallskip',
        '{\\small\\color[HTML]{766F66}'..tex(title)..'}\\par',
        '\\end{minipage}'}
      return pandoc.RawBlock('latex', table.concat(output, '\n'))
    end
    error('ZO variation integration supports HTML/PDF only')
  end

  local function inject(doc)
    local includes = doc.meta['header-includes'] or pandoc.MetaList({})
    if pandoc.utils.type(includes) ~= 'List' then includes = pandoc.MetaList({includes}) end
    if FORMAT:match('html') then
      -- PANDOC_SCRIPT_FILE belongs to the package adapter, so use the canonical
      -- stylesheet path supplied by it instead of guessing a repository root.
      local file = assert(io.open(options.css_path, 'r'))
      local css = file:read('*a')
      file:close()
      includes:insert(pandoc.MetaBlocks({pandoc.RawBlock('html', '<style>\n'..css..'\n</style>')}))
    elseif FORMAT:match('latex') then
      includes:insert(pandoc.MetaBlocks({pandoc.RawBlock('latex', '\\usepackage{adjustbox}')}))
    else
      return doc
    end
    doc.meta['header-includes'] = includes
    return doc
  end

  return {render=render, inject=inject}
end

return M
