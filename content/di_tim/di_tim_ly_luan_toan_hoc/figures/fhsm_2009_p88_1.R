library(ggplot2)
library(dplyr)

# -----------------------
# Synthetic data (tạo có chủ đích)
# -----------------------
x_values <- c(
  rep(-4, 1),
  rep(-3, 3),
  rep(-2, 22),
  rep(-1, 6),
  rep( 1, 10),
  rep( 2, 22),
  rep( 3, 6),
  rep( 4, 2)
)

df <- tibble(x = x_values) |>
  group_by(x) |>
  mutate(y = row_number()) |>
  ungroup()

# -----------------------
# Plot
# -----------------------
p <- ggplot(df, aes(x = x, y = y)) +
  geom_point(size = 1.5, color = "black") +
  geom_hline(yintercept = 0, linewidth = 0.7) +
  scale_x_continuous(
    limits = c(-4.5, 4.5),
    breaks = seq(-4, 4, 1)
  ) +
  scale_y_continuous(
    expand = expansion(mult = c(0, 0.05))
  ) +
  theme_classic(base_size = 12) +
  theme(
    axis.title = element_blank(),
    axis.text.y = element_blank(),
    axis.ticks.y = element_blank(),
    axis.line.y = element_blank()
  )

# -----------------------
# Export
# -----------------------
ggsave("fhsm_2009_p88_1.pdf", plot = p, width = 8, height = 2.5, units = "in")
