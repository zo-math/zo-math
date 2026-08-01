local stringify = pandoc.utils.stringify

local function trim(value)
  return value:gsub("^%s+", ""):gsub("%s+$", "")
end

local function escape_latex(value)
  local replacements = {
    ["\\"] = "\\textbackslash{}",
    ["{"] = "\\{",
    ["}"] = "\\}",
    ["#"] = "\\#",
    ["$"] = "\\$",
    ["%"] = "\\%",
    ["&"] = "\\&",
    ["_"] = "\\_",
    ["^"] = "\\textasciicircum{}",
    ["~"] = "\\textasciitilde{}",
  }
  return (value:gsub("[\\{}#$%%&_~^]", replacements))
end

local function latex_from_meta(value)
  if value == nil then
    return ""
  end

  local value_type = pandoc.utils.type(value)

  if value_type == "Inlines" then
    local document = pandoc.Pandoc({ pandoc.Plain(value) })
    return trim(pandoc.write(document, "latex"))
  end

  if value_type == "Blocks" then
    return trim(pandoc.write(pandoc.Pandoc(value), "latex"))
  end

  return escape_latex(stringify(value))
end

local function comma_list(value)
  if value == nil then
    return ""
  end

  if pandoc.utils.type(value) == "List" then
    local items = {}
    for _, item in ipairs(value) do
      items[#items + 1] = stringify(item)
    end
    return table.concat(items, ", ")
  end

  return stringify(value)
end

local function raw_url(value, fallback)
  local result = value and stringify(value) or fallback
  if result:find("[{}]") then
    error("URL nhận diện PDF không được chứa dấu ngoặc nhọn.")
  end
  return result
end

local function append_header_include(meta, latex)
  if quarto ~= nil and quarto.doc ~= nil and quarto.doc.include_text ~= nil then
    quarto.doc.include_text("in-header", latex)
    return
  end

  local includes = meta["header-includes"]
  if includes == nil then
    includes = pandoc.MetaList({})
  elseif pandoc.utils.type(includes) ~= "List" then
    includes = pandoc.MetaList({ includes })
  end

  includes[#includes + 1] =
    pandoc.MetaBlocks({ pandoc.RawBlock("latex", latex) })
  meta["header-includes"] = includes
end

function Meta(meta)
  local branding = meta["zo-pdf-branding"] or {}
  local title = latex_from_meta(meta.title)
  local meta_title = latex_from_meta(meta["title-meta"] or meta.title)
  local subtitle = latex_from_meta(meta.subtitle)
  local short_title = latex_from_meta(branding["short-title"] or meta.title)
  local collection = latex_from_meta(
    branding.collection or "Tài liệu học toán của ZO Math"
  )
  local date = latex_from_meta(meta.date)
  local subject = latex_from_meta(
    meta.summary or meta.description or "Tài liệu học toán của ZO Math"
  )
  local keywords = escape_latex(comma_list(meta.keywords))
  local canonical_url = raw_url(
    branding["canonical-url"],
    "https://zo-math.github.io/zo-math/"
  )
  local display_url = raw_url(
    branding["display-url"],
    "zo-math.github.io/zo-math"
  )

  local definitions = table.concat({
    "\\providecommand{\\zoPdfTitle}{}",
    "\\providecommand{\\zoPdfMetaTitle}{}",
    "\\providecommand{\\zoPdfSubtitle}{}",
    "\\providecommand{\\zoPdfShortTitle}{}",
    "\\providecommand{\\zoPdfCollection}{}",
    "\\providecommand{\\zoPdfDate}{}",
    "\\providecommand{\\zoPdfSubject}{}",
    "\\providecommand{\\zoPdfKeywords}{}",
    "\\renewcommand{\\zoPdfTitle}{" .. title .. "}",
    "\\renewcommand{\\zoPdfMetaTitle}{" .. meta_title .. "}",
    "\\renewcommand{\\zoPdfSubtitle}{" .. subtitle .. "}",
    "\\renewcommand{\\zoPdfShortTitle}{" .. short_title .. "}",
    "\\renewcommand{\\zoPdfCollection}{" .. collection .. "}",
    "\\renewcommand{\\zoPdfDate}{" .. date .. "}",
    "\\renewcommand{\\zoPdfSubject}{" .. subject .. "}",
    "\\renewcommand{\\zoPdfKeywords}{" .. keywords .. "}",
    "\\edef\\zoPdfCanonicalUrl{\\detokenize{" .. canonical_url .. "}}",
    "\\edef\\zoPdfDisplayUrl{\\detokenize{" .. display_url .. "}}",
  }, "\n")

  append_header_include(meta, definitions)
  return meta
end
