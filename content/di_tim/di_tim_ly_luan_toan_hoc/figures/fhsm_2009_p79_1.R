# Run: Rscript fhsm_2009_p79_1_r.R
# Output (auto): fhsm_2009_p79_1_r.pdf  và  fhsm_2009_p79_1_r.svg

library(ggplot2)
library(dplyr)

# -----------------------
# Auto output names = script name
# -----------------------
args <- commandArgs(trailingOnly = FALSE)
file_arg <- grep("^--file=", args, value = TRUE)
if (length(file_arg) == 0) stop("Run via: Rscript <file>.R")

script_path <- sub("^--file=", "", file_arg)
script_dir  <- dirname(normalizePath(script_path, winslash = "/", mustWork = FALSE))
script_base <- tools::file_path_sans_ext(basename(script_path))

out_pdf <- file.path(script_dir, paste0(script_base, ".pdf"))
out_svg <- file.path(script_dir, paste0(script_base, ".svg"))

# -----------------------
# Data
# -----------------------
meaningful <- c(12, 15, 12, 12, 10, 3, 7, 11, 9, 14, 9, 10, 9, 5, 13)
nonsense   <- c(4, 6, 6, 5, 7, 5, 4, 7, 9, 10, 4, 8, 7, 3, 2)

df <- bind_rows(
  tibble(type = "Meaningful", x = meaningful),
  tibble(type = "Nonsense",   x = nonsense)
) |>
  mutate(type = factor(type, levels = c("Nonsense", "Meaningful")))

# -----------------------
# Parameters (chỉ chỉnh ở đây)
# -----------------------
x_min <- 1
x_max <- 16
x_breaks <- seq(2, 16, 2)

box_fill <- "grey75"

frame_w <- 0.55   # khung
box_w   <- 0.55   # hộp + whisker
tick_w  <- 0.45   # tick
med_w   <- 0.8    # median

out_w_in <- 8.8
out_h_in <- 3.6

base_family <- "sans"  # tránh lỗi font khi xuất SVG

# -----------------------
# Plot
# -----------------------
p <- ggplot(df, aes(x = x, y = type)) +
  geom_boxplot(
    width = 0.55,
    fill = box_fill,
    color = "black",
    linewidth = box_w,
    outlier.size = 2.2,
    outlier.stroke = 0.4,
    fatten = 1
  ) +
  scale_x_continuous(
    limits = c(x_min, x_max),
    breaks = x_breaks
  ) +
  labs(
    title = "Boxplot of Number Recalled",
    x = "Number Recalled",
    y = "Type of Word"
  ) +
  theme_classic(base_size = 12, base_family = base_family) +
  theme(
    plot.title = element_text(hjust = 0.5, face = "bold"),
    panel.border = element_rect(fill = NA, color = "black", linewidth = frame_w),
    axis.line = element_blank(),
    axis.ticks = element_line(color = "black", linewidth = tick_w),
    axis.ticks.length = grid::unit(3, "mm")
  )

# Vẽ lại median cho rõ (giống mẫu SGK)
med <- df |>
  group_by(type) |>
  summarise(m = median(x), .groups = "drop")

p <- p + geom_segment(
  data = med,
  aes(x = m, xend = m, y = type, yend = type),
  inherit.aes = FALSE,
  linewidth = med_w,
  color = "black"
)

# -----------------------
# Export PDF + SVG
# -----------------------
ggsave(out_pdf, plot = p, width = out_w_in, height = out_h_in, units = "in")

if (requireNamespace("svglite", quietly = TRUE)) {
  ggsave(out_svg, plot = p, width = out_w_in, height = out_h_in, units = "in",
         device = svglite::svglite)
} else {
  ggsave(out_svg, plot = p, width = out_w_in, height = out_h_in, units = "in",
         device = "svg")
}

cat("Wrote:\n", out_pdf, "\n", out_svg, "\n")
