local M = {}

local function esc(value)
  return tostring(value):gsub('&', '&amp;'):gsub('"', '&quot;'):gsub('<', '&lt;'):gsub('>', '&gt;')
end

local function has_any(classes, names)
  for _, name in ipairs(names) do
    if classes:includes(name) then return true end
  end
  return false
end

local function add_class(classes, name)
  if not classes:includes(name) then classes:insert(name) end
end

function M.new(options)
  options = options or {}
  local html = options.html == true
  local legacy = options.legacy or {}
  local legacy_task = legacy.task
  local legacy_pause = legacy.pause

  local summary_classes = {'zo-learning-summary'}
  if legacy.summary then summary_classes[#summary_classes + 1] = legacy.summary end

  local disclosure_classes = {
    'zo-learning-guidance',
    'zo-learning-hint',
    'zo-learning-solution'
  }
  if legacy.details then disclosure_classes[#disclosure_classes + 1] = legacy.details end

  local function classify(div)
    if legacy.guidance and div.classes:includes(legacy.guidance) then
      if div.classes:includes('zo-learning-hint') then return 'zo-learning-hint' end
      return 'zo-learning-guidance'
    end
    if legacy.solution and div.classes:includes(legacy.solution) then
      return 'zo-learning-solution'
    end
    if div.classes:includes('zo-learning-hint') then return 'zo-learning-hint' end
    if div.classes:includes('zo-learning-solution') then return 'zo-learning-solution' end
    if div.classes:includes('zo-learning-guidance') then return 'zo-learning-guidance' end
    return nil
  end

  local function Div(div)
    if div.classes:includes('zo-learning-task') or
        (legacy_task and div.classes:includes(legacy_task)) then
      add_class(div.classes, 'zo-learning-task')
      if div.classes:includes('zo-learning-task--pause') or
          (legacy_pause and div.classes:includes(legacy_pause)) then
        add_class(div.classes, 'zo-learning-task--pause')
      else
        add_class(div.classes, 'zo-learning-task--item')
      end
      return div
    end

    if has_any(div.classes, summary_classes) then
      if not html then return nil end
      local inlines = div.content[1] and div.content[1].content or {}
      return {
        pandoc.RawBlock('html', '<summary class="zo-block-title zo-learning-summary">'),
        pandoc.Plain(inlines),
        pandoc.RawBlock('html', '</summary><div class="zo-block-body">')
      }
    end

    if not has_any(div.classes, disclosure_classes) then return nil end
    local role = classify(div)
    if not role then return nil end
    add_class(div.classes, role)
    add_class(div.classes, 'zo-learning-disclosure')
    if not html then return div end

    add_class(div.classes, 'zo-block')
    add_class(div.classes, 'zo-block-gray')
    local id = div.identifier ~= '' and ' id="'..esc(div.identifier)..'"' or ''
    local classes = esc(table.concat(div.classes, ' '))
    local result = {pandoc.RawBlock('html', '<details'..id..' class="'..classes..'">')}
    for _, block in ipairs(div.content) do result[#result + 1] = block end
    result[#result + 1] = pandoc.RawBlock('html', '</div></details>')
    return result
  end

  return {Div=Div}
end

return M
