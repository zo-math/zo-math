-- Tự động chuyển đổi các khối Div có class "details" thành thẻ <details> trong HTML
function Div(el)
    if el.classes:includes("details") then
        local summary = el.content[1]
        local details_content = pandoc.List(el.content)
        details_content:remove(1) -- Bỏ tiêu đề khỏi nội dung

        return pandoc.Div(
            {
                pandoc.RawBlock("html", "<details><summary style='background: #f4cccc; padding: 10px; border-radius: 10px; font-weight: bold;'>"
                    .. pandoc.utils.stringify(summary) .. "</summary>\n"),
                pandoc.Div(details_content), -- Giữ nội dung dạng Markdown thay vì HTML thuần
                pandoc.RawBlock("html", "\n</details>")
            },
            pandoc.Attr("", {"details"})
        )
    end
end



