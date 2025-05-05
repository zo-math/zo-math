-- Đổi mặc định tiếng Anh sang tiếng Việt, nếu có bản dịch trong Quarto
function Meta(m)
    if m["lang"] == "en" then
      m["lang"] = "vi"
    end
    return m
  end
  
