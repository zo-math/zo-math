local canonical_url = nil


local function stringify(value)
  if value == nil then
    return nil
  end

  local text = pandoc.utils.stringify(value)
  if text == "" then
    return nil
  end

  return text
end


local function normalize_url(url)
  local scheme, authority, path =
    url:match("^([%a][%w+.-]*://)([^/]+)(/.*)$")

  if scheme == nil then
    return url
  end

  local normalized = {}
  for segment in path:gmatch("[^/]+") do
    if segment == ".." then
      if #normalized > 0 then
        table.remove(normalized)
      end
    elseif segment ~= "." and segment ~= "" then
      table.insert(normalized, segment)
    end
  end

  return scheme .. authority .. "/" .. table.concat(normalized, "/")
end


local function rewrite_link(link)
  if canonical_url == nil then
    return nil
  end

  local target = link.target

  if target:match("^#")
    or target:match("^//")
    or target:match("^[%a][%w+.-]*:")
  then
    return nil
  end

  local path, suffix = target:match("^([^?#]+)(.*)$")
  if path == nil or not path:lower():match("%.qmd$") then
    return nil
  end

  local html_path = path:gsub("%.[Qq][Mm][Dd]$", ".html")
  local base = canonical_url:match("^(.*)/[^/]*$")
  if base == nil then
    return nil
  end

  link.target = normalize_url(base .. "/" .. html_path) .. suffix
  return link
end


function Div(div)
  if div.classes:includes("zo-block-title") then
    local blocks = {}
    for _, block in ipairs(div.content) do
      if block.t == "Para" or block.t == "Plain" then
        table.insert(blocks, pandoc.Para({pandoc.Strong(block.content)}))
      else
        table.insert(blocks, block)
      end
    end
    return blocks
  end

  return nil
end


function Pandoc(doc)
  canonical_url = nil

  local branding = doc.meta["zo-pdf-branding"]
  if branding ~= nil then
    canonical_url = stringify(branding["canonical-url"])
  end

  if canonical_url ~= nil then
    doc = doc:walk({Link = rewrite_link})
  end

  local blocks = {}
  local summary_pending = false

  for _, block in ipairs(doc.blocks) do
    if block.t == "RawBlock" and block.format == "html" then
      if block.text:match("^%s*<summary[%s>]") then
        summary_pending = true
      end

      local tag = block.text:match("^%s*</?([%w-]+)")
      if tag ~= nil and (tag:lower() == "details" or tag:lower() == "summary") then
        goto continue
      end
    end

    if summary_pending and block.t == "Plain" then
      table.insert(blocks, pandoc.Para({pandoc.Strong(block.content)}))
      summary_pending = false
    else
      table.insert(blocks, block)
    end

    ::continue::
  end

  doc.blocks = blocks
  return doc
end
