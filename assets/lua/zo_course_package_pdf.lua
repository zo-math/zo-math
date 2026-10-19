local print_dir=pandoc.path.directory(debug.getinfo(1,"S").source:gsub("^@", ""))
-- Source-owned PDF projection for native QMD packages using the shared course shell.
local print = assert(loadfile(pandoc.path.join({print_dir, 'zo_course_print.lua'})))()
local latex = FORMAT:match('latex') ~= nil
local canonical, variant
local layout=nil
local section_views={ ["bat-dau"]="bat-dau",["bai-hoc"]="bai-hoc",["phieu-luyen"]="luyen-tap",["tu-kiem-tra"]="kiem-tra",["on-lai"]="on-lai",["on-nen"]="on-nen",["sua-loi"]="sua-loi",["nhat-ky"]="nhat-ki",["loi-giai"]="loi-giai" }
local function str(v) return pandoc.utils.stringify(v or '') end
local function raw_title(s)
  local title=s:match('<summary[^>]*>(.-)</summary>')
  return title and pandoc.read(title,'html').blocks or nil
end
local function normalize(blocks)
  local out=pandoc.Blocks{}; local stack={}; local current=out
  for _,b in ipairs(blocks) do
    if b.t=='RawBlock' and b.format=='html' then
      local s=b.text
      if s:match('^%s*<figure[%s>]') then
        local frame={parent=current,body=pandoc.Blocks{},title=pandoc.Blocks{},kind='figure'}
        stack[#stack+1]=frame;current=frame.body
      elseif s:match('^%s*<figcaption[%s>]') then
        assert(#stack>0 and stack[#stack].kind=='figure','Caption without figure');stack[#stack].pending=true
      elseif s:match('^%s*</figcaption>') then
        stack[#stack].pending=false
      elseif s:match('^%s*</figure>') then
        local frame=assert(table.remove(stack),'Figure without opening');assert(frame.kind=='figure')
        local content=pandoc.Blocks{}
        for _,child in ipairs(current) do
          if child.t=='Figure' then content:extend(child.content) else content:insert(child) end
        end
        local fig=pandoc.Figure(content,pandoc.Caption(frame.title))
        fig.attributes['zo-explicit-caption']='true'
        current=frame.parent;current:insert(fig)
      elseif s:match('^%s*<details[%s>]') then
        local id=s:match('id="([^"]+)"') or ''
        local guidance=s:find('zo%-learning%-guidance') or s:find('r1%-foundation%-unit')
        local frame={parent=current,body=pandoc.Blocks{},title=pandoc.Blocks{},id=id,guidance=guidance}
        stack[#stack+1]=frame;current=frame.body
        local title=raw_title(s);if title then frame.title=title end
      elseif s:match('^%s*</details>') then
        local frame=assert(table.remove(stack),'Unbalanced PDF details')
        local body=print.box_body(current)
        local box=pandoc.Div({pandoc.Div(frame.title,pandoc.Attr('',{'zo-block-title'})),pandoc.Div(body,pandoc.Attr('',{'zo-block-body'}))},pandoc.Attr(frame.id,{'zo-block',frame.guidance and 'zo-block-white' or 'zo-block-gray'}))
        current=frame.parent;current:insert(box)
      elseif s:match('^%s*<summary') then
        assert(#stack>0,'Summary without details');local title=raw_title(s);if title then stack[#stack].title=title else stack[#stack].pending=true end
      elseif s:match('^%s*</summary') then
        if #stack>0 then stack[#stack].pending=false end
      elseif s:match('^%s*<a id=') then
        current:insert(pandoc.Div({},pandoc.Attr(assert(s:match('id="([^"]+)"')))))
      elseif s:match('^%s*<figure') or s:match('^%s*</figure') or s:match('^%s*</?figcaption') or s:find('lesson%-toc') then
        -- Presentation-only HTML wrappers have no learner content.
      else current:insert(b) end
    elseif #stack>0 and stack[#stack].pending then
      stack[#stack].title:insert(b)
    elseif b.t=='Div' then
      b.content=normalize(b.content)
      if b.classes:includes('r1-figure') then
        local figure,caption=nil,nil
        for _,child in ipairs(b.content) do
          if child.t=='Figure' then figure=child end
          if child.t=='Div' and child.classes:includes('r1-figcaption') then caption=child end
        end
        if figure and caption then
          figure.caption.long=caption.content
          figure.attributes['zo-explicit-caption']='true'
          local kept=pandoc.Blocks{}
          for _,child in ipairs(b.content) do
            if not (child.t=='Div' and child.classes:includes('r1-figcaption')) then kept:insert(child) end
          end
          b.content=kept
        end
      end
      current:insert(b)
    else current:insert(b) end
  end
  assert(#stack==0,'Unclosed PDF details')
  return out
end
local function ids(doc)
  local result={}
  local function keep(n) if n.identifier and n.identifier~='' then result[n.identifier]=true end end
  doc:walk({Header=keep,Div=keep,Span=keep,Table=keep,Image=keep})
  return result
end
local function visible_math(doc)
  -- An image alt string can be duplicated in Pandoc's implicit Figure caption.
  -- When the source provides a separate caption, only that caption is visible.
  local copy=doc:walk({Div=function(div)
    if div.classes:includes('r1-figure') then
      local explicit=false
      for _,child in ipairs(div.content) do
        if child.t=='Div' and child.classes:includes('r1-figcaption') then explicit=true end
      end
      if explicit then
        div.content=pandoc.Pandoc(div.content):walk({Figure=function(fig)
          if fig.attributes['zo-explicit-caption']~='true' then fig.caption.long=pandoc.Blocks{} end
          return fig
        end}).blocks
      end
    end
    return div
  end,Image=function(image) image.caption=pandoc.Inlines{};return image end})
  local values={};copy:walk({Math=function(m) values[#values+1]=m.text end})
  return table.concat(values,'\0')
end
local function prepare(doc)
  if not latex or #doc.blocks==0 then return nil end
  assert(doc.meta['zo-course-pdf-shell'],'Build through zo_pdf.py with shared shell')
  variant=str(doc.meta['zo-pdf-variant']);canonical=str(doc.meta['zo-pdf-branding']['canonical-url'])
  if doc.meta['zo-course-print-v2'] then
    local file=assert(io.open(pandoc.path.join({print_dir,'../tex/zo-course-print-runtime.json'}),'r'))
    layout=pandoc.json.decode(file:read('*a'));file:close()
  end
  local root=nil
  for _,b in ipairs(doc.blocks) do if b.t=='Div' and b.classes:includes('zo-on-thi-package') then root=b end end
  assert(root,'Missing canonical package root')
  local before=visible_math(doc)
  doc.blocks=normalize(root.content)
  local after=visible_math(doc)
  assert(before==after,'PDF normalization changed visible mathematics')
  doc=doc:walk({RawInline=function(r)
    if r.format=='html' then
      local id=r.text:match('<a%s+id="([^"]+)"')
      if id then return pandoc.Span({},pandoc.Attr(id)) end
    end
  end})
  if layout then
    doc=doc:walk({Para=function(p)
      if #p.content==1 and p.content[1].t=='Image' and p.content[1].src:match('figures_0_4/.+%.svg$') then
        return pandoc.Figure({pandoc.Plain(p.content)},pandoc.Caption({}))
      end
    end})
  end
  local original=ids(doc);local specs={}
  local owners={};local current_view='bat-dau'
  doc:walk({Header=function(h)
    if h.level==2 then current_view=section_views[h.identifier] or current_view end
    if h.identifier~='' then owners[h.identifier]=current_view end
  end})
  for _,v in ipairs(doc.meta['r1-section-download-files'] or {}) do specs[str(v.variant)]=v end
  local part=specs[variant]
  assert(variant=='full' or variant=='student' or part,'Unknown PDF variant')
  local section='';local projected=pandoc.Blocks{}
  for _,b in ipairs(doc.blocks) do
    if b.t=='Header' and b.level==2 then section=b.identifier end
    local keep=not part or section=='bat-dau' or section=='nguon' or section==str(part.start)
    if variant=='student' and section=='loi-giai' then keep=false end
    if section=='tai-tai-lieu' then keep=false end
    if keep then projected:insert(b) end
  end
  doc.blocks=projected
  local retained=ids(doc)
  doc=doc:walk({Link=function(link)
    local id=link.target:match('^#(.+)$')
    if id and not retained[id] then
      assert(original[id],'Broken source PDF target: '..id)
      link.target=canonical..(layout and ('?r1-view='..(owners[id] or 'bai-hoc')) or '')..'#'..id
      link.content:insert(pandoc.Str(' (mở trên trang học liệu)'))
      return link
    end
  end})
  if layout then
    -- Apply shared table roles before traversal consumes Divs or captions.
    doc=doc:walk({Div=function(div)
      if div.classes:includes('zo-native-bbt') or div.classes:includes('r1-bbt') then
        div.attributes.bbt=div.attributes['data-bbt'] or div.attributes.bbt
        if div.identifier=='' then div.identifier=div.attributes.bbt end
        local b=print.variation(div,'du_lieu/bang_bien_thien.json',true)
        b.text='% zo-variation '..div.identifier..'\n'..'\\hypertarget{'..div.identifier..'}{}\\label{'..div.identifier..'}\n'..b.text
        return b
      end
      local spec=layout.tables[div.identifier]
      if spec then
        div.content=pandoc.Pandoc(div.content):walk({Table=function(t)
          assert(#t.colspecs==#spec.widths,'PDF table column mismatch: '..div.identifier)
          t.attributes['zo-owner']=div.identifier
          t.attributes['zo-widths']=table.concat(spec.widths,',')
          local total=0;for _,w in ipairs(spec.widths) do total=total+w end
          for i,w in ipairs(spec.widths) do t.colspecs[i]={pandoc.AlignLeft,w/total} end
          for _,i in ipairs(spec.center_columns or {}) do t.colspecs[i+1][1]=pandoc.AlignCenter end
          for _,i in ipairs(spec.right_columns) do t.colspecs[i][1]=pandoc.AlignRight end
          return t
        end}).blocks
      end
      return div
    end})
    -- Source H2 owns a main area; print it as a top-level section. Keep
    -- task headings on their own line instead of Pandoc's run-in fallback.
    doc=doc:walk({Header=function(h) h.level=math.max(1,h.level-1);return h end})
  end
  if layout then
    local function pdfid(id) return (id:gsub('[^A-Za-z0-9%-%_%.:]',function(c) return string.format('_%02X',string.byte(c)) end)) end
    local function anchor(n) if n.identifier and n.identifier~='' then n.identifier=pdfid(n.identifier) end;return n end
    doc=doc:walk({Header=anchor,Div=anchor,Span=anchor,Table=anchor,Image=anchor,Link=function(link)
      if link.target:sub(1,1)=='#' then link.target='#'..pdfid(link.target:sub(2)) end;return link
    end})
  end
  -- Store real anchors before the common block transform consumes Divs.
  doc=print.references(doc,layout~=nil)
  if layout then
    doc=doc:walk({Str=function(s)
      local symbols={['∞']='\\infty',['→']='\\rightarrow',['←']='\\leftarrow',['↔']='\\leftrightarrow'}
      local result=pandoc.Inlines{};local buffer='';local changed=false
      for _,code in utf8.codes(s.text) do
        local c=utf8.char(code)
        if symbols[c] then
          if buffer~='' then result:insert(pandoc.Str(buffer));buffer='' end
          result:insert(pandoc.Math('InlineMath',symbols[c]));changed=true
        else buffer=buffer..c end
      end
      if buffer~='' then result:insert(pandoc.Str(buffer)) end
      return changed and result or s
    end})
  end
  return doc
end
local function table_filter(t)
  if not latex then return nil end
  return print.table(t)
end
local function image_filter(i)
  if not latex then return nil end
  if i.src:match('figures_0_4/.+%.svg$') then
    i.src=i.src:gsub('%.svg$','.pdf');assert(io.open(i.src,'rb'),'Missing paired PDF graph')
    if layout then
      local spec=assert(layout.graphs[i.src:gsub('%.pdf$','.svg')],'Unbound PDF graph: '..i.src)
      i.attributes.width=string.format('%.5fpt',spec.width_pt)
      i.attributes.height=nil
    else i.attributes.width=nil end
  end
  return i
end
local function figure_filter(fig)
  if not latex or not layout then return nil end
  local wide=false
  fig:walk({Image=function(i)
    local spec=layout.graphs[i.src:gsub('%.pdf$','.svg')]
    if spec and spec.rotate then wide=true end
  end})
  local explicit=fig.attributes['zo-explicit-caption']=='true'
  if not explicit then fig.caption.long=pandoc.Blocks{} end
  do
    local tex=pandoc.write(pandoc.Pandoc({fig}),'latex')
    -- Do not let print floats move a graph across the following explanation.
    local changed
    tex,changed=tex:gsub('\\begin{figure}%b[]',function() return '\\begin{figure}[H]' end)
    if changed==0 then tex=tex:gsub('\\begin{figure}',function() return '\\begin{figure}[H]' end) end
    if wide then tex=tex:gsub('(\\includegraphics%[[^%]]*%]%{[^}]+%})',function(image) return '\\rotatebox{90}{'..image..'}' end) end
    if explicit then
      tex=tex:gsub('\\caption',function() return '\\captionsetup{labelformat=empty}\\caption' end)
      tex='% zo-explicit-figure-caption\n'..tex
    end
    return pandoc.RawBlock('latex',tex)
  end
end
local function header_filter(h)
  if latex and not layout and h.identifier~='' then h.content:insert(1,pandoc.RawInline('latex','\\label{'..h.identifier..'}')) end
  return h
end
local function blocks_filter(blocks)
  if not latex then return nil end
  local out=pandoc.Blocks{}
  for index,b in ipairs(blocks) do
    if b.t=='Header' then
      if layout and b.level==1 then out:insert(pandoc.RawBlock('latex','\\clearpage')) end
      local function reserve(i)
        local h=blocks[i];local lines=8
        if layout and h.attributes['data-zo-task'] then
          local chars=0
          for j=i+1,#blocks do
            if blocks[j].t=='Header' then break end
            chars=chars+(utf8.len(pandoc.utils.stringify(blocks[j])) or 0)
          end
          lines=math.max(8,math.min(20,math.ceil(chars/70)+5))
        end
        if layout and blocks[i+1] and blocks[i+1].t=='Header' then
          lines=math.max(lines,reserve(i+1)+4)
        end
        return math.min(26,lines)
      end
      local lines=layout and reserve(index) or 6
      out:insert(pandoc.RawBlock('latex','\\Needspace{'..lines..'\\baselineskip}'))
      if layout and b.identifier~='' then out:insert(pandoc.RawBlock('latex','\\gdef\\zoNextAnchor{'..b.identifier..'}')) end
    end
    if layout and (b.t=='Para' or b.t=='Plain') and str(b):match('^Bảng%s+[IVX]+$') then
      out:insert(pandoc.RawBlock('latex','\\Needspace{10\\baselineskip}'))
    end
    out:insert(b)
    if (b.t=='Para' or b.t=='Plain') and pandoc.utils.stringify(b):match('^Nhiệm vụ%s+%d+') then
      out:insert(pandoc.RawBlock('latex','\\nopagebreak[4]'))
    end
  end
  return out
end
local function finish(doc)
  if not latex then return nil end
  local env=setmetatable({},{__index=_G})
  assert(loadfile(pandoc.path.join({print_dir,'zo_pdf_content.lua'}),'t',env))()
  return env.Pandoc(doc)
end
return {{Pandoc=prepare},{Table=table_filter,Image=image_filter,Figure=figure_filter,Header=header_filter,Blocks=blocks_filter},{Pandoc=finish}}
