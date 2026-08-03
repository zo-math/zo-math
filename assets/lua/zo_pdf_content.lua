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


local function has_class(classes, name)
  return classes ~= nil and classes:includes(name)
end


local function block_environment(classes)
  if has_class(classes, "zo-block-red") then
    return "zoBlockRed"
  end
  if has_class(classes, "zo-block-yellow") then
    return "zoBlockYellow"
  end
  if has_class(classes, "zo-block-gray") then
    return "zoBlockGray"
  end
  return "zoBlockGray"
end


local function html_environment(text)
  if text:match("zo%-block%-red") then
    return "zoBlockRed"
  end
  if text:match("zo%-block%-yellow") then
    return "zoBlockYellow"
  end
  return "zoBlockGray"
end


local function latex_from_blocks(blocks)
  if blocks == nil or #blocks == 0 then
    return ""
  end

  local latex = pandoc.write(pandoc.Pandoc(blocks), "latex")
  latex = latex:gsub("^%s+", ""):gsub("%s+$", "")
  return latex
end


local function append_all(target, source)
  for _, item in ipairs(source) do
    table.insert(target, item)
  end
end


local function box_begin(environment, title)
  return pandoc.RawBlock(
    "latex",
    "\\begin{" .. environment .. "}{" .. title .. "}"
  )
end


local function box_end(environment)
  return pandoc.RawBlock("latex", "\\end{" .. environment .. "}")
end


local transform_blocks


local function transform_div(div)
  if has_class(div.classes, "zo-block") then
    local title_blocks = {}
    local body_blocks = {}

    for _, child in ipairs(div.content) do
      if child.t == "Div" and has_class(child.classes, "zo-block-title") then
        append_all(title_blocks, child.content)
      elseif child.t == "Div" and has_class(child.classes, "zo-block-body") then
        append_all(body_blocks, child.content)
      else
        table.insert(body_blocks, child)
      end
    end

    local environment = block_environment(div.classes)
    local result = {box_begin(environment, latex_from_blocks(title_blocks))}
    append_all(result, transform_blocks(body_blocks))
    table.insert(result, box_end(environment))
    return result
  end

  if has_class(div.classes, "zo-block-title") then
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

  div.content = transform_blocks(div.content)
  return {div}
end


transform_blocks = function(blocks)
  local output = {}
  local details = nil
  local summary_pending = false

  for _, block in ipairs(blocks) do
    if block.t == "Div" then
      append_all(output, transform_div(block))

    elseif block.t == "RawBlock" and block.format == "html" then
      local text = block.text

      if details == nil
        and text:match("^%s*<details[%s>]")
        and text:match("zo%-block")
      then
        details = {
          environment = html_environment(text),
          started = false,
        }
        summary_pending = false

      elseif details ~= nil and text:match("^%s*<summary[%s>]") then
        summary_pending = true

      elseif details ~= nil and text:match("^%s*</summary%s*>") then
        -- Bỏ thẻ HTML; tiêu đề đã được đưa vào môi trường LaTeX.

      elseif details ~= nil
        and text:match("^%s*<div[%s>]")
        and text:match("zo%-block%-body")
      then
        -- Bỏ thẻ bao thân HTML.

      elseif details ~= nil and text:match("^%s*</div%s*>") then
        -- Bỏ thẻ bao thân HTML.

      elseif details ~= nil and text:match("^%s*</details%s*>") then
        if not details.started then
          table.insert(output, box_begin(details.environment, ""))
        end
        table.insert(output, box_end(details.environment))
        details = nil
        summary_pending = false

      elseif details == nil then
        table.insert(output, block)
      end

    elseif details ~= nil and summary_pending
      and (block.t == "Plain" or block.t == "Para")
    then
      table.insert(
        output,
        box_begin(details.environment, latex_from_blocks({block}))
      )
      details.started = true
      summary_pending = false

    else
      if details ~= nil and not details.started then
        table.insert(output, box_begin(details.environment, ""))
        details.started = true
      end
      table.insert(output, block)
    end
  end

  if details ~= nil then
    if not details.started then
      table.insert(output, box_begin(details.environment, ""))
    end
    table.insert(output, box_end(details.environment))
  end

  return output
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

  doc.blocks = transform_blocks(doc.blocks)
  return doc
end
