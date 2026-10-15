-- Print-only presentation. Text, math, IDs and question/answer order are retained.
if not FORMAT:match('latex') then return {} end

local function latex(blocks)
  return pandoc.write(pandoc.Pandoc(blocks), 'latex'):gsub('%s+$', '')
end

function Header(h)
  -- Original levels: 2=page area, 3=group, 4=task title.
  if (h.level == 2 and h.identifier ~= 'khao-sat') or h.identifier:match('^mach%-r%d$') then
    return {pandoc.RawBlock('latex', '\\clearpage'), h}
  end
  return {pandoc.RawBlock('latex', '\\Needspace{5\\baselineskip}'), h}
end

function Div(div)
  if div.classes:includes('d0-private') then return {} end
  if div.classes:includes('zo-learning-solution') then
    if div.identifier == 'doi-chieu-r8-03' then
      div.content:insert(1, pandoc.RawBlock('latex', '\\clearpage'))
    end
    if div.identifier:match('^doi%-chieu%-r[2-8]%-01$') then
      div.content:insert(1, pandoc.RawBlock('latex', '\\clearpage'))
    end
    div.content:insert(1, pandoc.RawBlock('latex', '\\hypertarget{'..div.identifier..'}{}\\label{'..div.identifier..'}'))
    return div
  end
  if div.classes:includes('zo-learning-summary') then
    return pandoc.RawBlock('latex', '\\Needspace{8\\baselineskip}\\dZeroSolution{'..latex(div.content)..'}')
  end
  if div.classes:includes('d0-task-meta') then
    local blocks = pandoc.List({pandoc.RawBlock('latex', '{\\small\\color{zoMuted}')})
    blocks:extend(div.content)
    blocks:insert(pandoc.RawBlock('latex', '}'))
    return blocks
  end
  if div.classes:includes('d0-primary-task') or div.classes:includes('d0-example-task') then
    local content = div.content
    if content[1] and content[1].t == 'Para' and content[2] and content[2].t == 'Header' then
      -- Keep the same wording; use the existing Bài number as the visible anchor.
      content[1] = pandoc.RawBlock('latex', '\\Needspace{12\\baselineskip}\\dZeroTag{'..latex({content[1]})..'}')
    end
    div.content:insert(1, pandoc.RawBlock('latex', '\\hypertarget{'..div.identifier..'}{}\\label{'..div.identifier..'}'))
    return div
  end
end

local function html_image(raw)
  if raw.format == 'html' and raw.text:find('hinh/hinh_hop.svg', 1, true) then
    return pandoc.RawBlock('latex', '\\begin{center}\\includegraphics[width=.52\\linewidth]{hinh/hinh_hop.pdf}\\end{center}')
  end
end

function RawInline(raw)
  local block = html_image(raw)
  if block then return pandoc.RawInline('latex', block.text) end
end

function Link(link)
  if link.target:match('^#doi%-chieu') or link.target:match('^#d0%-r') or link.target == '#cau-minh-hoa' then
    local id = link.target:sub(2)
    link.content:insert(pandoc.RawInline('latex', ' (trang~\\pageref*{'..id..'})'))
  end
  if link.target:match('%.qmd') then
    local joined = 'content/thpt/on_thi_toan_thpt/hoc_lieu/d0/'..link.target
    local parts = {}
    for part in joined:gmatch('[^/]+') do
      if part == '..' then
        assert(#parts > 0, 'Link escapes repository')
        table.remove(parts)
      elseif part ~= '.' then parts[#parts+1] = part end
    end
    local absolute = table.concat(parts, '/')
    link.target = 'https://zomath.vn/'..absolute:gsub('%.qmd', '.html')
  end
  return link
end

function Table(tbl)
  -- Native full-grid print table, never an HTML screenshot.
  local count = #tbl.colspecs
  local widths = {}
  local specified = 0
  for _, spec in ipairs(tbl.colspecs) do specified = specified + (tonumber(spec[2] or spec.width) or 0) end
  for index, spec in ipairs(tbl.colspecs) do
    local fraction = specified > 0 and (tonumber(spec[2] or spec.width) or 0) / specified or 1 / count
    if count == 2 then fraction = index == 1 and .36 or .64 end
    local numeric = count > 2
    widths[#widths+1] = string.format('>{'..(numeric and '\\centering' or '\\raggedright')..'\\arraybackslash}p{%.5f\\linewidth}',
      fraction * 0.95 - 0.012 * 2)
  end
  local output = {'{\\small\\arrayrulecolor{zoGrid}\\setlength{\\arrayrulewidth}{.5pt}\\setlength{\\tabcolsep}{0.012\\linewidth}',
    '\\renewcommand{\\arraystretch}{1.5}',
    '\\begin{longtable}{|'..table.concat(widths, '|')..'|}\\hline'}
  local function row(r, header)
    local cells = {}
    for _, c in ipairs(r.cells) do
      cells[#cells+1] = (header and '\\bfseries ' or '')..latex(c.contents)
    end
    output[#output+1] = table.concat(cells, ' & ')..' \\\\ \\hline'
  end
  for _, r in ipairs(tbl.head.rows) do row(r, true) end
  output[#output+1] = '\\endfirsthead'
  output[#output+1] = '\\hline'
  for _, r in ipairs(tbl.head.rows) do row(r, true) end
  output[#output+1] = '\\endhead'
  for _, body in ipairs(tbl.bodies) do
    for _, r in ipairs(body.head) do row(r, false) end
    for _, r in ipairs(body.body) do row(r, false) end
  end
  for _, r in ipairs(tbl.foot.rows) do row(r, false) end
  output[#output+1] = '\\end{longtable}}'
  return pandoc.RawBlock('latex', table.concat(output, '\n'))
end

return {{Header=Header, Div=Div, Link=Link, Table=Table, RawBlock=html_image, RawInline=RawInline}}
