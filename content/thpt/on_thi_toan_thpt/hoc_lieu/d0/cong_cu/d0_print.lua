-- Independent print composition from canonical AST, not an HTML page screenshot.
if not FORMAT:match('latex') then return {} end
local here = pandoc.path.directory(PANDOC_SCRIPT_FILE)
local f=assert(io.open(pandoc.path.join({here,'d0_print_profile.json'})))
local profile=pandoc.json.decode(f:read('*a'));f:close()
local print_adapter=assert(loadfile(pandoc.path.join({here,'d0_pdf.lua'})))()[1]
local source_path=pandoc.path.join({here,'d0.lua'})
local source_environment=setmetatable({PANDOC_SCRIPT_FILE=source_path},{__index=_G})
local source_adapter=assert(loadfile(source_path,'t',source_environment))()[1]
local shared=assert(loadfile(pandoc.path.join({here,'../../../../../../assets/lua/zo_course_print.lua'})))()
local function native_table(tbl)
  return shared.box_body({shared.table(tbl)})[1]
end
assert(profile.full,'D0 production print profile must include the complete QMD')
local selected={}
local function links(link)
  if link.target:match('^#') then
    local id=link.target:sub(2)
    if selected[id] then
      link.content:insert(pandoc.RawInline('latex',' (trang~\\pageref*{'..id..'})'))
    else
      link.target='https://zomath.vn/content/thpt/on_thi_toan_thpt/hoc_lieu/d0/index.html'..link.target
    end
    return link
  end
  return print_adapter.Link(link)
end
local function tex(blocks)
  local wrapped=pandoc.Div(blocks)
  local function picture(raw)
    local result=print_adapter.RawInline(raw)
    if result then result.text=result.text:gsub('width=%.52\\linewidth','scale=\\zoFigureScale');return result end
  end
  wrapped=wrapped:walk({Div=source_adapter.Div,Link=links,Table=native_table,RawInline=picture,RawBlock=print_adapter.RawBlock})
  return pandoc.write(pandoc.Pandoc(wrapped.content),'latex'):gsub('%s+$','')
end
local function raw(text) return pandoc.RawBlock('latex',text) end
local function layout(doc)
  local file=assert(io.open(pandoc.path.join({here,'../giao_dien/d0_tables.json'})))
  local specs=pandoc.json.decode(file:read('*a'));file:close()
  doc=doc:walk({Div=function(div)
    local spec=specs[div.identifier]
    if not spec then return div end
    div.content=pandoc.Pandoc(div.content):walk({Table=function(tbl)
      assert(#tbl.colspecs==#spec.widths,'D0 table/profile mismatch: '..div.identifier)
      tbl.attributes['zo-owner']=div.identifier;tbl.attributes['zo-widths']=table.concat(spec.widths,',')
      for i,w in ipairs(spec.widths) do tbl.colspecs[i]={pandoc.AlignLeft,w/100} end
      for _,i in ipairs(spec.center) do tbl.colspecs[i][1]=pandoc.AlignCenter end
      for _,i in ipairs(spec.right) do tbl.colspecs[i][1]=pandoc.AlignRight end
      return tbl
    end}).blocks
    return div
  end})
  local current_spec,current_id=nil,nil
  doc=doc:walk({Header=function(h)
    if h.level==2 then current_spec=specs[h.identifier];current_id=h.identifier end
  end,Table=function(tbl)
    if not current_spec or tbl.attributes['zo-owner'] then return tbl end
    assert(#tbl.colspecs==#current_spec.widths,'D0 section table/profile mismatch')
    tbl.attributes['zo-owner']=current_id;tbl.attributes['zo-widths']=table.concat(current_spec.widths,',')
    for i,w in ipairs(current_spec.widths) do tbl.colspecs[i]={pandoc.AlignLeft,w/100} end
    return tbl
  end})
  if profile.full then
    doc:walk({Div=function(div)
      if div.classes:includes('d0-primary-task') or div.classes:includes('d0-example-task')
        or div.classes:includes('zo-learning-solution') then selected[div.identifier]=true end
    end,Header=function(h) if h.identifier~='' then selected[h.identifier]=true end end})
  end
  local found={};doc:walk({Div=function(div) if selected[div.identifier] then found[div.identifier]=div end end})
  for id,_ in pairs(selected) do
    if id:match('^d0%-r%d') or id=='cau-minh-hoa' or id:match('^doi%-chieu') then
      assert(found[id],'Missing selected source block: '..id)
    end
  end
  local blocks=doc.blocks
  if #blocks==1 and blocks[1].t=='Div' then blocks=blocks[1].content end
  local function section(id)
    local container=blocks
    doc:walk({Div=function(div)
      for _,b in ipairs(div.content) do
        if b.t=='Header' and b.identifier==id then container=div.content end
      end
    end})
    local content={};local active=false;local level=nil
    for _,b in ipairs(container) do
      if b.t=='Header' and b.identifier==id then active=true;level=b.level
      elseif active and b.t=='Header' and b.level<=level then break
      elseif active then content[#content+1]=b end
    end
    assert(#content>0,'Missing source section: '..id);return content
  end
  local comparison_blocks=profile.full and section('doc-ket-qua') or nil
  local comparison_main,writing_guide={},{}
  if profile.full then
    local in_guide=false
    for _,b in ipairs(comparison_blocks) do
      if b.t=='Header' and pandoc.utils.stringify(b.content)=='Ghi điều em nhận ra' then in_guide=true end
      if in_guide then writing_guide[#writing_guide+1]=b else comparison_main[#comparison_main+1]=b end
    end
    assert(#writing_guide>1,'Missing reflection guidance from QMD')
  end
  local out={raw('\\zoPage{CÁCH DÙNG KHẢO SÁT}{Em muốn bắt đầu từ đâu?}\\hypertarget{bat-dau}{}\\label{bat-dau}'),raw(tex(section('bat-dau')))}
  if profile.full then
    out[#out+1]=raw('\\vspace{5mm}\\zoRole{GHI ĐIỀU EM NHẬN RA}'..tex({table.unpack(writing_guide,2)}))
  end
  local function task_heading(div)
    local heading
    for _,b in ipairs(div.content) do if b.t=='Header' then heading=b;break end end
    assert(heading,'Task heading missing: '..div.identifier)
    local full=pandoc.utils.stringify(heading.content)
    local tag,title=full:match('^(Bài %d%d) — (.+)$')
    assert(tag and title,'Task heading must use the current page-wide number: '..div.identifier)
    return tag,tex({pandoc.Para({pandoc.Str(title)})})
  end
  local function task(div)
    local tag,title=task_heading(div)
    local meta,prompt
    for _,b in ipairs(div.content) do if b.t=='Div' then
      if b.classes:includes('d0-task-meta') then meta=b.content end
      if b.classes:includes('d0-task-prompt') then prompt=b.content end
    end end
    assert(meta and prompt,'Task roles missing: '..div.identifier)
    local comparison=div.identifier=='cau-minh-hoa' and 'doi-chieu-minh-hoa' or 'doi-chieu-'..div.identifier:sub(4)
    return '\\begin{minipage}{\\linewidth}\\hypertarget{'..div.identifier..'}{}\\label{'..div.identifier..'}\\zoTaskHead{'..tag..'}{'..title..'}\n'..
      '{\\small\\color{zoMuted}\\setlength{\\parskip}{2pt}'..tex(meta)..'}\\par\\vspace{3mm}\n'..
      tex(prompt)..'\\par\\vspace{2mm}{\\small\\hyperlink{'..comparison..'}{Xem lời giải (trang~\\pageref*{'..comparison..'})}}\\zoDivider\\end{minipage}\\par'
  end
  if profile.full then
    local count_task,count_solution=0,0
    local function emit(block)
      if block.t=='Div' then
        if block.classes:includes('d0-private') then return end
        if block.classes:includes('d0-primary-task') or block.classes:includes('d0-example-task') then
          count_task=count_task+1;out[#out+1]=raw(task(block));return
        end
        if block.classes:includes('zo-learning-solution') then
          count_solution=count_solution+1
          local example=block.identifier=='doi-chieu-minh-hoa'
          local linked=example and 'cau-minh-hoa' or 'd0-'..block.identifier:sub(11)
          local source=assert(found[linked], 'Missing matching task: '..block.identifier)
          local tag,title=task_heading(source)
          local body={};local note,review,back
          for i=2,#block.content do
            local b=block.content[i];local s=pandoc.utils.stringify(b)
            if s:match('^Đối chiếu:') then note=tex({b})
            elseif s:match('^Nội dung cần ôn nếu còn vướng:') then review=tex({b})
            elseif s:match('^Xem đề bài') then back=tex({b})
            else body[#body+1]=b end
          end
          local backlink=back or ('\\hyperlink{'..linked..'}{Xem đề bài (trang~\\pageref*{'..linked..'})}')
          local content='\\begin{minipage}{\\linewidth}\\hypertarget{'..block.identifier..'}{}\\label{'..block.identifier..'}\\zoSolutionTitle{'..tag..'}{'..title..'}{'..backlink..'}'
          if example then content=content..'\\zoRole{ĐỐI CHIẾU BÀI MINH HỌA}'..tex(body)
          else
            assert(note and review and back,'Missing comparison roles: '..block.identifier)
            content=content..'\\zoRole{KẾT QUẢ VÀ LỜI GIẢI}'..tex(body)..'\\zoReview{'..note..'}{'..review..'}'
          end
          out[#out+1]=raw(content..'\\zoDivider\\end{minipage}\\par');return
        end
        if block.classes:includes('lesson-toc') then
          -- TOC links remain, but the duplicate generated label is kept as source text.
          out[#out+1]=raw(tex({block}));return
        end
        for _,child in ipairs(block.content) do emit(child) end
        return
      end
      if block.t=='Para' then
        local s=pandoc.utils.stringify(block)
        if s:match('^Xem lời giải') then return end
        if s:match('^Chọn câu khảo sát để làm') then return end
      end
      if block.t=='Header' then
        local id=block.identifier or ''
        local anchor=id~='' and ('\\hypertarget{'..id..'}{}\\label{'..id..'}') or ''
        local label=tex({pandoc.Para(block.content)})
        out[#out+1]=raw(anchor..'\\Needspace{5\\baselineskip}\\zoRole{'..label..'}')
      else
        local rendered=tex({block})
        if rendered:match('%S') then out[#out+1]=raw(rendered) end
      end
    end
    out[#out+1]=raw('\\zoPage{CHUẨN BỊ KHẢO SÁT}{Chuẩn bị và chọn câu khảo sát}\\hypertarget{khai-bao-pham-vi}{}\\label{khai-bao-pham-vi}')
    for _,b in ipairs(section('khai-bao-pham-vi')) do emit(b) end
    out[#out+1]=raw('\\zoPage{TỰ LÀM TRƯỚC KHI ĐỐI CHIẾU}{Làm khảo sát}\\hypertarget{khao-sat}{}\\label{khao-sat}')
    out[#out+1]=raw('{\\small\\hyperlink{khao-sat}{Chọn câu khảo sát để làm (trang~\\pageref*{khao-sat})}}\\par')
    for _,b in ipairs(section('khao-sat')) do emit(b) end
    out[#out+1]=raw('\\zoPage{ĐỐI CHIẾU SAU KHI TỰ LÀM}{Đối chiếu bài làm}\\hypertarget{doc-ket-qua}{}\\label{doc-ket-qua}')
    for _,b in ipairs(comparison_main) do emit(b) end
    out[#out+1]=raw('\\zoPage{CHỌN NỘI DUNG MUỐN HỌC TIẾP}{Chọn mạch ôn và bắt đầu}\\hypertarget{chon-mach}{}\\label{chon-mach}')
    for _,b in ipairs(section('chon-mach')) do emit(b) end
    assert(count_task==25 and count_solution==25,'Incomplete QMD inventory: '..count_task..' tasks, '..count_solution..' solutions')
    doc.blocks=pandoc.List(out)
    return doc
  end

end
return {{Pandoc=layout}}
