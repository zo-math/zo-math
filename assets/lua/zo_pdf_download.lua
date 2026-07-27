local function stringify(value)
  if value == nil then
    return nil
  end
  return pandoc.utils.stringify(value)
end

function Pandoc(doc)
  if not FORMAT:match("html") then
    return doc
  end

  local config = doc.meta["zo-pdf-download"]
  if config == nil then
    return doc
  end

  local href
  local label = "Tải bản PDF"

  if type(config) == "table" and config.href ~= nil then
    href = stringify(config.href)
    label = stringify(config.label) or label
  else
    href = stringify(config)
  end

  if href == nil or href == "" then
    return doc
  end

  local link = pandoc.Link(
    {
      pandoc.RawInline("html", '<i class="bi bi-file-earmark-pdf" aria-hidden="true"></i>'),
      pandoc.Space(),
      pandoc.Str(label),
    },
    href,
    "Tải bản PDF",
    pandoc.Attr("", {"zo-pdf-download__link"}, {{"download", ""}, {"aria-label", label}})
  )
  local block = pandoc.Div(
    {pandoc.Para({link})},
    pandoc.Attr("", {"zo-pdf-download"})
  )

  if doc.meta.resources == nil then
    doc.meta.resources = {pandoc.MetaString(href)}
  else
    table.insert(doc.meta.resources, pandoc.MetaString(href))
  end

  table.insert(doc.blocks, block)
  return doc
end
