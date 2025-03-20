library(shiny)

# Giao diện người dùng (UI)
ui <- fluidPage(
  titlePanel("Mẫu số liệu ghép nhóm: Các số đặc trưng đo xu thế trung tâm"),
  tags$head(
    tags$script(src = "https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.5/MathJax.js?config=TeX-AMS-MML_HTMLorMML"),
    tags$script(HTML("MathJax.Hub.Config({tex2jax: {inlineMath: [['$','$'], ['\\\\(','\\\\)']]}});")),
    tags$script(HTML("
      function playSound(type) {
        var soundEnabled = document.getElementById('sound_enabled').checked;
        if (soundEnabled) {
          var sound;
          if (type === 'success') {
            sound = document.getElementById('success_sound');
          } else if (type === 'error') {
            sound = document.getElementById('error_sound');
          }
          if (sound) {
            sound.play();
          }
        }
      }
    ")),
    tags$style(HTML("
      .button-group {
        display: flex;
        gap: 10px;
        margin-top: 10px;
      }
      #compute {
        background-color: #007bff;
        color: white;
        border: none;
        padding: 8px 16px;
        border-radius: 4px;
      }
      #clear_data {
        background-color: #6c757d;
        color: white;
        border: none;
        padding: 8px 16px;
        border-radius: 4px;
      }
      #export_csv {
        background-color: #17a2b8;
        color: white;
        border: none;
        padding: 8px 16px;
        border-radius: 4px;
      }
      #compute:hover {
        background-color: #0056b3;
      }
      #clear_data:hover {
        background-color: #5a6268;
      }
      #export_csv:hover {
        background-color: #138496;
      }
      #table1 table th, #table1 table td,
      #table2 table th, #table2 table td {
        text-align: center !important;
        white-space: normal !important;
        line-height: 1.2;
        padding: 8px;
      }
      /* Tùy chỉnh giao diện thông báo */
      .shiny-notification {
        font-size: 16px;
        line-height: 1.5;
        padding: 15px;
        max-width: 600px;
        white-space: pre-wrap;
      }
      .shiny-notification-error {
        background-color: #f8d7da;
        color: #721c24;
        border: 1px solid #f5c6cb;
      }
      .shiny-notification-warning {
        background-color: #fff3cd;
        color: #856404;
        border: 1px solid #ffeeba;
      }
      .shiny-notification-message {
        background-color: #d4edda;
        color: #155724;
        border: 1px solid #c3e6cb;
      }
    "))
  ),
  tags$audio(id = "success_sound", preload = "auto",
             tags$source(src = "success.flac", type = "audio/flac"),
             tags$source(src = "success.wav", type = "audio/wav")),
  tags$audio(id = "error_sound", preload = "auto",
             tags$source(src = "error.flac", type = "audio/flac"),
             tags$source(src = "error.wav", type = "audio/wav")),
  sidebarLayout(
    sidebarPanel(
      radioButtons("data_type", "Chọn cách nhập dữ liệu",
                   choices = list("Nhập số liệu" = "raw", "Nhập bảng tần số" = "grouped")),
      conditionalPanel(
        condition = "input.data_type == 'raw'",
        textAreaInput("raw_data", "Nhập số liệu", 
                      placeholder = "Ví dụ: 1.5, 2, 5, 100, 118.9"),
        textInput("left_bounds", "Danh sách đầu mút trái của nhóm", 
                  placeholder = "Ví dụ: 0, 10, 20, 30, 40"),
        textInput("right_bounds", "Danh sách đầu mút phải của nhóm", 
                  placeholder = "Ví dụ: 10, 20, 30, 40, 50"),
        helpText("Lưu ý: Nhập số theo chuẩn Quốc tế, sử dụng dấu chấm cho số thập phân (ví dụ: 1.5, 2.75). Các số liệu cách nhau bằng dấu phẩy")
      ),
      conditionalPanel(
        condition = "input.data_type == 'grouped'",
        textInput("freq_grouped", "Danh sách tần số", 
                  placeholder = "Ví dụ: 5, 8, 12, 9, 6"),
        textInput("left_bounds_grouped", "Danh sách đầu mút trái của nhóm", 
                  placeholder = "Ví dụ: 0, 10, 20, 30, 40"),
        textInput("right_bounds_grouped", "Danh sách đầu mút phải của nhóm", 
                  placeholder = "Ví dụ: 10, 20, 30, 40, 50"),
        helpText("Lưu ý: Nhập số theo chuẩn Quốc tế, sử dụng dấu chấm cho số thập phân.")
      ),
      numericInput("decimal_places", "Số chữ số thập phân", value = 2, min = 0, max = 10),
      checkboxInput("sound_enabled", "Bật âm thanh thông báo", value = TRUE),
      div(class = "button-group",
          actionButton("compute", "Tính toán"),
          actionButton("clear_data", "Xóa dữ liệu"),
          conditionalPanel(
            condition = "output.table1 && output.table2",
            downloadButton("export_csv", "Xuất CSV")
          )
      )
    ),
    mainPanel(
      h3("Bảng 1: Tần số"),
      tableOutput("table1"),
      h3("Bảng 2: Các chỉ số thống kê"),
      uiOutput("table2")
    )
  )
)

# Server logic
server <- function(input, output, session) {
  validate_numeric_input <- function(input_str, field_name) {
    values <- unlist(strsplit(trimws(input_str), ","))
    for (val in values) {
      val <- trimws(val)
      if (val == "" || is.na(suppressWarnings(as.numeric(val)))) {
        showNotification(
          paste0("Lỗi: Ô '", field_name, "' chứa giá trị không phải số: '", val, "'. Vui lòng nhập lại!"),
          type = "error",
          action = tags$script(HTML("playSound('error');")),
          closeButton = TRUE,
          duration = NULL  # Không tự đóng
        )
        return(FALSE)
      }
    }
    return(TRUE)
  }

  validate_intervals <- function(left_bounds, right_bounds, context = "Nhập số liệu") {
    # Kiểm tra đầu mút trái nhỏ hơn đầu mút phải
    for (i in seq_along(left_bounds)) {
      if (left_bounds[i] >= right_bounds[i]) {
        showNotification(
          paste0("Lỗi (", context, "): Khoảng [", left_bounds[i], ", ", right_bounds[i], 
                 ") không hợp lệ: Đầu mút trái phải nhỏ hơn đầu mút phải!"),
          type = "error",
          action = tags$script(HTML("playSound('error');")),
          closeButton = TRUE,
          duration = NULL  # Không tự đóng
        )
        return(FALSE)
      }
    }
    # Kiểm tra các khoảng tăng dần và liên tiếp
    for (i in 1:(length(left_bounds) - 1)) {
      if (left_bounds[i] >= left_bounds[i + 1]) {
        showNotification(
          paste0("Lỗi (", context, "): Các khoảng không được sắp xếp tăng dần: ", 
                 left_bounds[i], " >= ", left_bounds[i + 1], "!"),
          type = "error",
          action = tags$script(HTML("playSound('error');")),
          closeButton = TRUE,
          duration = NULL
        )
        return(FALSE)
      }
      if (right_bounds[i] >= right_bounds[i + 1]) {
        showNotification(
          paste0("Lỗi (", context, "): Các khoảng không được sắp xếp tăng dần: ", 
                 right_bounds[i], " >= ", right_bounds[i + 1], "!"),
          type = "error",
          action = tags$script(HTML("playSound('error');")),
          closeButton = TRUE,
          duration = NULL
        )
        return(FALSE)
      }
      if (right_bounds[i] != left_bounds[i + 1]) {
        showNotification(
          paste0("Lỗi (", context, "): Các khoảng không liên tiếp: Có khoảng trống từ ", 
                 right_bounds[i], " đến ", left_bounds[i + 1], "!"),
          type = "error",
          action = tags$script(HTML("playSound('error');")),
          closeButton = TRUE,
          duration = NULL
        )
        return(FALSE)
      }
    }
    # Kiểm tra độ dài các khoảng có bằng nhau không
    if (length(left_bounds) > 1) {
      interval_lengths <- right_bounds - left_bounds
      if (!all(interval_lengths == interval_lengths[1])) {
        showNotification(
          paste0("Lỗi (", context, "): Các khoảng có độ dài không bằng nhau (",
                 paste(interval_lengths, collapse = ", "), "). ",
                 "Điều này không được phép vì: (1) Các công thức thống kê (trung vị, tứ phân vị, mốt) giả định phân bố đều trong mỗi khoảng, ",
                 "và độ dài không bằng nhau sẽ làm sai lệch kết quả; (2) Gây khó khăn trong việc lập luận và diễn giải dữ liệu; ",
                 "(3) Không tuân theo thực tiễn thống kê, vốn yêu cầu các khoảng có độ dài bằng nhau để đảm bảo tính nhất quán. ",
                 "Vui lòng điều chỉnh các khoảng để có độ dài bằng nhau!"),
          type = "error",
          action = tags$script(HTML("playSound('error');")),
          closeButton = TRUE,
          duration = NULL
        )
        return(FALSE)
      }
    }
    return(TRUE)
  }

  validate_frequencies <- function(freq_values) {
    if (any(freq_values < 0)) {
      showNotification(
        paste0("Lỗi: Tần số không được âm: ", paste(freq_values[freq_values < 0], collapse = ", "), "!"),
        type = "error",
        action = tags$script(HTML("playSound('error');")),
        closeButton = TRUE,
        duration = NULL
      )
      return(FALSE)
    }
    return(TRUE)
  }

  find_quantile <- function(p, n, group_data, decimal_places) {
    pos <- p * n
    idx <- which(group_data$cum_freq >= pos)[1]
    if (is.na(idx) || idx > nrow(group_data)) return(NA)
    L <- group_data$left[idx]
    F <- if (idx == 1) 0 else group_data$cum_freq[idx - 1]
    f <- group_data$count[idx]
    h <- group_data$right[idx] - group_data$left[idx]
    if (f == 0) return(NA)
    return(round(L + ((pos - F) / f) * h, decimal_places))
  }

  group_data_reactive <- eventReactive(input$compute, {
    decimal_places <- input$decimal_places

    if (input$data_type == "raw") {
      if (!validate_numeric_input(input$raw_data, "Nhập số liệu")) return(NULL)
      if (!validate_numeric_input(input$left_bounds, "Danh sách đầu mút trái")) return(NULL)
      if (!validate_numeric_input(input$right_bounds, "Danh sách đầu mút phải")) return(NULL)

      raw_numbers <- as.numeric(unlist(strsplit(trimws(input$raw_data), ",")))
      left_bounds <- as.numeric(unlist(strsplit(trimws(input$left_bounds), ",")))
      right_bounds <- as.numeric(unlist(strsplit(trimws(input$right_bounds), ",")))

      if (length(raw_numbers) == 0) {
        showNotification(
          "Vui lòng nhập dữ liệu số hợp lệ (cách nhau bằng dấu phẩy)!",
          type = "error",
          action = tags$script(HTML("playSound('error');")),
          closeButton = TRUE,
          duration = NULL
        )
        return(NULL)
      }
      if (length(left_bounds) == 0 || length(right_bounds) == 0 || length(left_bounds) != length(right_bounds)) {
        showNotification(
          "Số lượng đầu mút trái và phải phải bằng nhau và không được để trống!",
          type = "error",
          action = tags$script(HTML("playSound('error');")),
          closeButton = TRUE,
          duration = NULL
        )
        return(NULL)
      }

      if (!validate_intervals(left_bounds, right_bounds, "Nhập số liệu")) return(NULL)

      if (any(raw_numbers < min(left_bounds) | raw_numbers >= max(right_bounds))) {
        showNotification(
          "Một số giá trị nằm ngoài khoảng nhóm đã định!",
          type = "warning",
          action = tags$script(HTML("playSound('error');")),
          closeButton = TRUE,
          duration = 7  # Tự đóng sau 7 giây
        )
      }

      breaks <- unique(sort(c(left_bounds, right_bounds)))
      intervals <- cut(raw_numbers, breaks = breaks, right = FALSE, include.lowest = TRUE)
      levels_intervals <- levels(intervals)
      freq_table <- table(factor(intervals, levels = levels_intervals))
      group_data <- data.frame(
        left = left_bounds,
        right = right_bounds,
        count = as.integer(freq_table)
      )
    } else {
      if (!validate_numeric_input(input$freq_grouped, "Danh sách tần số")) return(NULL)
      if (!validate_numeric_input(input$left_bounds_grouped, "Danh sách đầu mút trái")) return(NULL)
      if (!validate_numeric_input(input$right_bounds_grouped, "Danh sách đầu mút phải")) return(NULL)

      left_bounds <- as.numeric(unlist(strsplit(trimws(input$left_bounds_grouped), ",")))
      right_bounds <- as.numeric(unlist(strsplit(trimws(input$right_bounds_grouped), ",")))
      freq_values <- as.integer(unlist(strsplit(trimws(input$freq_grouped), ",")))

      if (length(left_bounds) == 0 || length(right_bounds) == 0 || length(freq_values) == 0 ||
          length(left_bounds) != length(right_bounds) || length(left_bounds) != length(freq_values)) {
        showNotification(
          "Dữ liệu nhóm không hợp lệ: Kiểm tra số lượng đầu mút và tần số!",
          type = "error",
          action = tags$script(HTML("playSound('error');")),
          closeButton = TRUE,
          duration = NULL
        )
        return(NULL)
      }

      if (!validate_intervals(left_bounds, right_bounds, "Nhập bảng tần số")) return(NULL)
      if (!validate_frequencies(freq_values)) return(NULL)

      total_freq <- sum(freq_values)
      if (total_freq > 1000) {
        showNotification(
          "Tổng tần số quá lớn, có thể không hợp lý với khoảng nhóm!",
          type = "warning",
          action = tags$script(HTML("playSound('error');")),
          closeButton = TRUE,
          duration = 7
        )
      }

      group_data <- data.frame(left = left_bounds, right = right_bounds, count = freq_values)
    }

    if (nrow(group_data) > 0) {
      group_data$mids <- round((group_data$left + group_data$right) / 2, decimal_places)
      group_data$cum_freq <- cumsum(group_data$count)
      group_data$group <- paste0("[", group_data$left, ", ", group_data$right, ")")
    }
    return(group_data)
  })

  stats_data_reactive <- reactiveVal(NULL)

  observeEvent(input$compute, {
    group_data <- group_data_reactive()
    if (is.null(group_data)) return()

    decimal_places <- input$decimal_places
    n <- sum(group_data$count)

    if (n == 0) {
      mean_x <- q1 <- q2 <- q3 <- mode_x <- NA
    } else {
      mean_x <- round(sum(group_data$mids * group_data$count) / n, decimal_places)
      q1 <- find_quantile(0.25, n, group_data, decimal_places)
      q2 <- find_quantile(0.50, n, group_data, decimal_places)
      q3 <- find_quantile(0.75, n, group_data, decimal_places)

      mode_idx <- which.max(group_data$count)
      if (length(mode_idx) == 0 || mode_idx < 1 || mode_idx > nrow(group_data)) {
        mode_x <- NA
      } else {
        L <- group_data$left[mode_idx]
        f_mot <- group_data$count[mode_idx]
        f_truoc <- ifelse(mode_idx > 1, group_data$count[mode_idx - 1], 0)
        f_sau <- ifelse(mode_idx < nrow(group_data), group_data$count[mode_idx + 1], 0)
        h <- group_data$right[mode_idx] - group_data$left[mode_idx]
        denominator <- 2 * f_mot - f_truoc - f_sau
        mode_x <- if (denominator == 0) NA else round(L + ((f_mot - f_truoc) / denominator) * h, decimal_places)
      }
    }

    output$table1 <- renderTable({
      group_data$mids <- formatC(group_data$mids, format = "f", digits = decimal_places)
      colnames(group_data) <- c("Left", "Right", "Tần số", "Giá trị đại diện", "Tần số tích lũy", "Nhóm")
      group_data[, c("Nhóm", "Giá trị đại diện", "Tần số", "Tần số tích lũy")]
    })

    output$table2 <- renderUI({
      table_content <- renderTable({
        df <- data.frame(
          "Trung bình" = formatC(mean_x, format = "f", digits = decimal_places),
          "Trung vị" = formatC(q2, format = "f", digits = decimal_places),
          "Tứ phân vị thứ nhất" = formatC(q1, format = "f", digits = decimal_places),
          "Tứ phân vị thứ hai" = formatC(q2, format = "f", digits = decimal_places),
          "Tứ phân vị thứ ba" = formatC(q3, format = "f", digits = decimal_places),
          "Mốt" = formatC(mode_x, format = "f", digits = decimal_places),
          check.names = FALSE
        )
        stats_data_reactive(df)
        df
      }, sanitize.text.function = function(x) x)

      tagList(
        withMathJax(),
        table_content,
        tags$script(HTML("MathJax.Hub.Queue(['Typeset', MathJax.Hub]);"))
      )
    })

    showNotification(
      "Tính toán thành công!",
      type = "message",
      action = tags$script(HTML("playSound('success');")),
      closeButton = TRUE,
      duration = 5  # Tự đóng sau 5 giây
    )
  })

  output$export_csv <- downloadHandler(
    filename = function() {
      paste("thong-ke-", Sys.Date(), ".csv", sep = "")
    },
    content = function(file) {
      group_data <- group_data_reactive()
      if (is.null(group_data) || is.null(stats_data_reactive())) {
        showNotification(
          "Không có dữ liệu để xuất!",
          type = "error",
          action = tags$script(HTML("playSound('error');")),
          closeButton = TRUE,
          duration = NULL
        )
        return(NULL)
      }
      decimal_places <- input$decimal_places
      table1_data <- group_data[, c("group", "mids", "count", "cum_freq")]
      table1_data$mids <- formatC(table1_data$mids, format = "f", digits = decimal_places)
      table1_data$cum_freq <- formatC(table1_data$cum_freq, format = "f", digits = 0)
      table1_data$count <- formatC(table1_data$count, format = "f", digits = 0)
      colnames(table1_data) <- c("Nhóm", "Giá trị đại diện", "Tần số", "Tần số tích lũy")

      table2_data <- stats_data_reactive()
      if (is.null(table2_data)) return(NULL)

      export_time <- format(Sys.time(), "%Y-%m-%d %H:%M:%S")
      write.csv(data.frame("Dữ liệu được xuất vào" = export_time), file, row.names = FALSE, append = FALSE)
      write.table(data.frame(" " = ""), file, row.names = FALSE, col.names = FALSE, append = TRUE)
      write.csv(data.frame("Bảng 1: Tần số" = ""), file, row.names = FALSE, append = TRUE)
      write.csv(table1_data, file, row.names = FALSE, append = TRUE)
      write.table(data.frame(" " = ""), file, row.names = FALSE, col.names = FALSE, append = TRUE)
      write.csv(data.frame("Bảng 2: Các chỉ số thống kê" = ""), file, row.names = FALSE, append = TRUE)
      write.csv(table2_data, file, row.names = FALSE, append = TRUE)

      showNotification(
        "Xuất CSV thành công!",
        type = "message",
        action = tags$script(HTML("playSound('success');")),
        closeButton = TRUE,
        duration = 5
      )
    }
  )

  observeEvent(input$clear_data, {
    showModal(modalDialog(
      title = "Xác nhận xóa dữ liệu",
      "Bạn có chắc chắn muốn xóa tất cả dữ liệu đã nhập và kết quả tính toán không?",
      footer = tagList(
        modalButton("Hủy"),
        actionButton("confirm_clear", "Xóa", class = "btn-danger")
      )
    ))
  })

  observeEvent(input$confirm_clear, {
    updateTextAreaInput(session, "raw_data", value = "")
    updateTextInput(session, "left_bounds", value = "")
    updateTextInput(session, "right_bounds", value = "")
    updateTextInput(session, "freq_grouped", value = "")
    updateTextInput(session, "left_bounds_grouped", value = "")
    updateTextInput(session, "right_bounds_grouped", value = "")
    updateNumericInput(session, "decimal_places", value = 2)

    output$table1 <- renderTable(NULL)
    output$table2 <- renderUI(NULL)
    stats_data_reactive(NULL)

    removeModal()

    showNotification(
      "Dữ liệu đã được xóa thành công!",
      type = "message",
      action = tags$script(HTML("playSound('success');")),
      closeButton = TRUE,
      duration = 5
    )
  })
}

# Chạy ứng dụng
shinyApp(ui, server)