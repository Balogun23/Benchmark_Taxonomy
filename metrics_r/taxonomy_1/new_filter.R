setwd("C:/Users/HP/Downloads/metrics_r/taxonomy_1")

if (!requireNamespace("pryr", quietly = TRUE)) {
  install.packages("pryr")
}
library(pryr)

df <- read.csv("../birth_gp_ratios.csv")

script_path <- "new_filter.R"
if (file.exists(script_path)) {
  total_lines_of_code <- length(readLines(script_path))
} else {
  total_lines_of_code <- NA
  warning("⚠️ Script file not found. LOC count failed.")
}

start_time <- Sys.time()
cpu_start <- proc.time()
mem_before <- mem_used()

filtered_df <- subset(df, actual_births > 1000)

mem_after <- mem_used()
cpu_end <- proc.time()
end_time <- Sys.time()


runtime <- round(as.numeric(difftime(end_time, start_time, units = "secs")), 3)
cpu_time <- round((cpu_end - cpu_start)[["user.self"]], 3)
mem_used_mb <- round((mem_after - mem_before) / 1024^2, 3)


core_task_lines <- 1


cat("✅ Filtered Rows (actual_births > 1000):", nrow(filtered_df), "\n")
cat("Runtime (seconds):", runtime, "\n")
cat("CPU Time (seconds):", cpu_time, "\n")
cat("Memory usage (MB):", mem_used_mb, "\n")
cat("Total Lines of Code (script):", total_lines_of_code, "\n")
cat("Lines of Core Task Only:", core_task_lines, "\n")
