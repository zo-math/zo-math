-- Shared native course print tables; literal mathematical data preserved.
local M={}
function M.variation(div,data_path)
    local file = assert(io.open(data_path))
    local data = pandoc.json.decode(file:read('*a')); file:close()
    for _, item in ipairs(data) do
      if item.id == div.attributes.bbt then
        local output = {'\\begin{minipage}{\\linewidth}\\centering\\small',
          '\\renewcommand{\\arraystretch}{1.6}\\arrayrulecolor{zoGrid}\\setlength{\\arrayrulewidth}{.5pt}',
          '\\begin{adjustbox}{max width=\\linewidth}\\begin{tabular}{|'..string.rep('c|',#item.rows[1])..'}\\hline'}
        local excluded = {}; for _, col in ipairs(item.excluded_columns or {}) do excluded[col+1]=true end
        for r,row in ipairs(item.rows) do
          local cells={}
          for c,cell in ipairs(row) do
            if r>1 and excluded[c] then cell='∥' end
            if cell:find('Không',1,true) then
              cells[#cells+1]='\\shortstack{Không\\\\xác định}'
            else
              local value=cell:gsub('−','-'):gsub('∞','\\infty'):gsub('′',"'")
                :gsub('↗','\\nearrow'):gsub('↘','\\searrow'):gsub('∥','\\parallel')
              cells[#cells+1]='$'..value..'$'
            end
          end
          output[#output+1]=table.concat(cells,' & ')..' \\\\ \\hline'
        end
        local caption=div.attributes.caption or item.title
        local title=pandoc.write(pandoc.Pandoc({pandoc.Plain({pandoc.Str(caption)})}),'latex'):gsub('%s+$','')
        output[#output+1]='\\end{tabular}\\end{adjustbox}\\par\\smallskip{\\small\\color{zoMuted}'..title..'}\\end{minipage}'
        return pandoc.RawBlock('latex',table.concat(output,'\n'))
      end
    end
    error('Missing current variation data: '..tostring(div.attributes.bbt))
end
function M.table(tbl)
    local widths={};local total=0
    for _,spec in ipairs(tbl.colspecs) do total=total+(tonumber(spec[2]) or 0) end
    for _,spec in ipairs(tbl.colspecs) do
      local fraction=total>0 and (tonumber(spec[2]) or 0)/total or 1/#tbl.colspecs
      local alignment=spec[1]==pandoc.AlignCenter and '\\centering' or '\\raggedright'
      widths[#widths+1]=string.format('>{%s\\arraybackslash}p{%.5f\\linewidth}',alignment,fraction*.96-.024)
    end
    local out={'\\begingroup\\small\\arrayrulecolor{zoGrid}\\setlength{\\arrayrulewidth}{.5pt}\\setlength{\\tabcolsep}{.012\\linewidth}\\renewcommand{\\arraystretch}{1.35}',
      '\\begin{longtable}{|'..table.concat(widths,'|')..'|}\\hline'}
    local function row(r,header)
      local cells={}
      for _,c in ipairs(r.cells) do
        cells[#cells+1]=(header and '\\bfseries ' or '')..pandoc.write(pandoc.Pandoc(c.contents),'latex'):gsub('%s+$','')
      end
      out[#out+1]=table.concat(cells,' & ')..' \\\\ \\hline'
    end
    for _,r in ipairs(tbl.head.rows) do row(r,true) end
    out[#out+1]='\\endfirsthead\\hline'
    for _,r in ipairs(tbl.head.rows) do row(r,true) end
    out[#out+1]='\\endhead'
    for _,body in ipairs(tbl.bodies) do
      for _,r in ipairs(body.head) do row(r,false) end
      for _,r in ipairs(body.body) do row(r,false) end
    end
    for _,r in ipairs(tbl.foot.rows) do row(r,false) end
    -- longtable's hline can insert a break even after a starred final row.
    -- cline keeps the closing rule with that row, preventing a lone line on
    -- the following page while preserving the full grid width.
    out[#out]=out[#out]:gsub(' \\\\ \\hline$', ' \\\\* \\cline{1-'..#tbl.colspecs..'}')
    out[#out+1]='\\end{longtable}\\endgroup'
    return pandoc.RawBlock('latex',table.concat(out,'\n'))
end

function M.references(doc)
  if not FORMAT:match('latex') or not doc.meta['zo-course-pdf-shell'] then return nil end
      doc = doc:walk({Div=function(div)
        if div.identifier ~= '' then
          div.content:insert(1,pandoc.RawBlock('latex','\\label{'..div.identifier..'}'))
        end
        if div.classes:includes('answer-link') then
          div.content:insert(1,pandoc.RawBlock('latex','\\nopagebreak[4]'))
        end
        return div
      end, Link=function(link)
        if link.target:sub(1,1)=='#' then
          link.content:insert(pandoc.RawInline('latex',' (trang~\\pageref*{'..link.target:sub(2)..'})'))
          return link
        end
      end})
  return doc
end
function M.box_body(blocks)
  -- longtable uses the page output routine, which is not valid inside a
  -- breakable tcolorbox's collected body. These short answer tables use
  -- tabular; the surrounding box can still split before/after the table.
  return pandoc.Pandoc(blocks):walk({RawBlock=function(block)
    if block.format~='latex' then return nil end
    if block.text:match('^\\Needspace{') then return {} end
    if block.text:find('\\begin{longtable}',1,true) then
      block.text=block.text:gsub('\\endfirsthead.-\\endhead','')
        :gsub('\\begin{longtable}','\\begin{tabular}')
        :gsub('\\end{longtable}','\\end{tabular}')
      return block
    end
  end}).blocks
end
return M
