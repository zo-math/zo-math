library(ggplot2)
library(dplyr)
library(tidyr)

# Lấy đường dẫn file .R đang chạy
args <- commandArgs(trailingOnly = FALSE)
file_arg <- grep("^--file=", args, value = TRUE)

script_path <- if (length(file_arg) > 0) {
  sub("^--file=", "", file_arg)
} else {
  stop("Script must be run via Rscript")
}

# Tạo tên PDF giống tên file .R
out_pdf <- sub("\\.R$", ".pdf", basename(script_path))

# -----------------------
# Data
# -----------------------
meaningful <- c(12, 15, 12, 12, 10, 3, 7, 11, 9, 14, 9, 10, 9, 5, 13)
nonsense   <- c(4, 6, 6, 5, 7, 5, 4, 7, 9, 10, 4, 8, 7, 3, 2)

# -----------------------
# Parameters (chỉ chỉnh ở đây)
# -----------------------
x_min <- 1
x_max <- 16
x_breaks <- seq(2, 16, 2)

base_nonsense   <- 1.0
base_meaningful <- 2.0

# (1) Khoảng cách chồng: nhỏ để giống mẫu nhưng đủ để không dính
# Nếu vẫn dính: tăng nhẹ lên 0.07; nếu quá thưa: giảm xuống 0.05
stack_step <- 0.15

# (1) Kích thước chấm: giảm nhẹ để có khe trắng giữa các chấm chồng
# Nếu muốn nhỏ hơn nữa: 1.8; nếu muốn to hơn: 2.2
pt_size <- 1.25

# (2) Độ dày nét: tách riêng
frame_w     <- 0.55  # khung + tick
base_line_w <- 0.25  # 2 đường ngang xuyên qua điểm (mảnh hơn)

# -----------------------
# Build stacked coordinates automatically
# -----------------------
df <- bind_rows(
  tibble(type = "Meaningful", x = meaningful, base = base_meaningful),
  tibble(type = "Nonsense",   x = nonsense,   base = base_nonsense)
) |>
  arrange(type, x) |>
  group_by(type, x) |>
  mutate(k = row_number()) |>
  ungroup() |>
  mutate(y = base + (k - 1) * stack_step)

# -----------------------
# Plot
# -----------------------
p <- ggplot(df, aes(x = x, y = y)) +
  # two baselines like the sample (mảnh hơn)
  geom_hline(yintercept = base_nonsense,   linewidth = base_line_w, color = "black") +
  geom_hline(yintercept = base_meaningful, linewidth = base_line_w, color = "black") +
  # points
  geom_point(size = pt_size, color = "black") +
  # y labels at the baselines
  scale_y_continuous(
    breaks = c(base_nonsense, base_meaningful),
    labels = c("Nonsense", "Meaningful"),
    limits = c(0.7, 2.55)
  ) +
  scale_x_continuous(
    limits = c(x_min, x_max),
    breaks = x_breaks
  ) +
  labs(
    title = "Dotplot of Number Recalled",
    x = "Number Recalled",
    y = "Type of Word"
  ) +
  theme_classic(base_size = 12) +
  theme(
    plot.title = element_text(hjust = 0.5, face = "bold"),
    panel.border = element_rect(fill = NA, color = "black", linewidth = frame_w),
    axis.line = element_blank(),
    axis.ticks = element_line(color = "black", linewidth = frame_w),
    axis.ticks.length = grid::unit(3, "mm")
  )

# -----------------------
# Export PDF
# -----------------------

#ggsave("fhsm_2009_p75_1_r.pdf", plot = p, width = 8.8, height = 2.1, units = "in")

ggsave(out_pdf, plot = p, width = 8.8, height = 2.1, units = "in")
ggsave("fhsm_2009_p75_1_a.svg", plot = p,
       width = 8.8, height = 2.1, units = "in", device = "svg")
