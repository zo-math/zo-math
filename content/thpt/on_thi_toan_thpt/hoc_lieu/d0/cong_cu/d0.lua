-- D0 migration adapter. Public HTML must not contain facilitator-only material.
local html = FORMAT:match('html') ~= nil
local script_dir = pandoc.path.directory(PANDOC_SCRIPT_FILE)
local components = assert(loadfile(pandoc.path.join({script_dir,
  '../../../../../../assets/lua/zo_learning_components.lua'})))().new({html=html})
local variation = assert(loadfile(pandoc.path.join({script_dir,
  '../../../../../../assets/lua/zo_variation_qmd.lua'})))().new({
  data_path=pandoc.path.join({script_dir, '../du_lieu/bang_bien_thien.json'}),
  asset_dir='hinh',
  css_path=pandoc.path.join({script_dir, '../../../../../../assets/css/zo_variation.css'})
})

function Div(div)
  if div.classes:includes('zo-variation') then return variation.render(div) end
  if html and div.classes:includes('d0-private') then
    return {}
  end
  if html and div.classes:includes('d0-task-prompt') then
    return div:walk({OrderedList=function(list)
      return pandoc.Div({list}, pandoc.Attr('', {'d0-response-options'}))
    end, Para=function(paragraph)
      local text = pandoc.utils.stringify(paragraph)
      if text:match('^[A-D]%. ') or text:match('^[a-d]%) ') then
        return pandoc.Div({paragraph}, pandoc.Attr('', {'d0-response-option'}))
      end
    end})
  end
  return nil
end

function Image(image)
  if html and image.src == 'hinh/hinh_hop.pdf' then
    image.src = 'hinh/hinh_hop.svg'
    -- HTML size follows the page text, not the historical percentage width.
    image.attributes['width'] = nil
    image.attributes['height'] = nil
  end
  return image
end

function Math(math)
  if html and math.mathtype == 'InlineMath' then
    return pandoc.Span({math}, pandoc.Attr('', {'d0-inline-math'}))
  end
end

function Table(tbl)
  if not html then return nil end
  tbl.classes:insert('r1-data-table')
  for _, row in ipairs(tbl.head.rows) do
    for _, cell in ipairs(row.cells) do cell.attributes['scope'] = 'col' end
  end
  for _, body in ipairs(tbl.bodies) do
    body.row_head_columns = 1
    for _, row in ipairs(body.body) do row.cells[1].attributes['scope'] = 'row' end
  end
  local columns = #tbl.colspecs
  local attributes = {
    ['role']='region', ['aria-label']='Bảng dữ liệu — cuộn ngang nếu cần',
    ['tabindex']='0', ['style']='--r1-table-min-width: '..(columns >= 4 and '32em' or '24em')
  }
  return pandoc.Div({tbl}, pandoc.Attr('', {'r1-table-scroll-x', 'd0-data-table'}, attributes))
end

return {{Div=Div, Image=Image, Table=Table, Math=Math}, components, {Pandoc=variation.inject}}
