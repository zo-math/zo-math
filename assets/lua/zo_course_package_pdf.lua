-- Source-owned PDF projection for native QMD packages using the shared course shell.
local print = assert(loadfile(pandoc.path.join({pandoc.path.directory(PANDOC_SCRIPT_FILE), 'zo_course_print.lua'})))()
local latex = FORMAT:match('latex') ~= nil
local canonical, variant
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
      if s:match('^%s*<details[%s>]') then
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
    elseif b.t=='Div' then b.content=normalize(b.content);current:insert(b)
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
local function prepare(doc)
  if not latex or #doc.blocks==0 then return nil end
  assert(doc.meta['zo-course-pdf-shell'],'Build through zo_pdf.py with shared shell')
  variant=str(doc.meta['zo-pdf-variant']);canonical=str(doc.meta['zo-pdf-branding']['canonical-url'])
  local root=nil
  for _,b in ipairs(doc.blocks) do if b.t=='Div' and b.classes:includes('zo-on-thi-package') then root=b end end
  assert(root,'Missing canonical package root')
  local before={};doc:walk({Math=function(m) before[#before+1]=m.text end})
  doc.blocks=normalize(root.content)
  local after={};doc:walk({Math=function(m) after[#after+1]=m.text end})
  assert(table.concat(before,'\0')==table.concat(after,'\0'),'PDF normalization changed mathematics')
  doc=doc:walk({RawInline=function(r)
    if r.format=='html' then
      local id=r.text:match('<a%s+id="([^"]+)"')
      if id then return pandoc.Span({},pandoc.Attr(id)) end
    end
  end})
  local original=ids(doc);local specs={}
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
      link.target=canonical..'#'..id
      link.content:insert(pandoc.Str(' (mở trên trang học liệu)'))
      return link
    end
  end})
  -- Store real anchors before the common block transform consumes Divs.
  doc=print.references(doc)
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
    i.attributes.width=nil
  end
  return i
end
local function header_filter(h)
  if latex and h.identifier~='' then h.content:insert(1,pandoc.RawInline('latex','\\label{'..h.identifier..'}')) end
  return h
end
local function blocks_filter(blocks)
  if not latex then return nil end
  local out=pandoc.Blocks{}
  for _,b in ipairs(blocks) do
    if b.t=='Header' then out:insert(pandoc.RawBlock('latex','\\Needspace{10\\baselineskip}')) end
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
  assert(loadfile(pandoc.path.join({pandoc.path.directory(PANDOC_SCRIPT_FILE),'zo_pdf_content.lua'}),'t',env))()
  return env.Pandoc(doc)
end
return {{Pandoc=prepare},{Table=table_filter,Image=image_filter,Header=header_filter,Blocks=blocks_filter},{Pandoc=finish}}
