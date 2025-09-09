# --------------------- SETUP (Not Benchmarked) ---------------------
setwd("C:/Users/HP/Downloads/metrics_r/taxonomy_1")

# Load required package
if (!requireNamespace("pryr", quietly = TRUE)) {
  install.packages("pryr")
}
library(pryr)

# Load data
df_main <- read.csv("../birth_gp_ratios.csv")

# Track total lines of code in script
script_path <- "joining.R"
if (file.exists(script_path)) {
  total_lines_of_code <- length(readLines(script_path))
} else {
  total_lines_of_code <- NA
  warning("⚠️ Script file not found. LOC count failed.")
}

# --------------------- BENCHMARK STARTS HERE ---------------------
start_time <- Sys.time()
cpu_start <- proc.time()
mem_before <- mem_used()

# --- Core Task: Create dummy lookup and perform join ---
gss_codes <- unique(na.omit(df_main$gss_code))[1:10]
dummy_lookup <- data.frame(
  gss_code = gss_codes,
  region = paste0("Region_", seq_along(gss_codes))
)

merged <- merge(df_main, dummy_lookup, by = "gss_code", all.x = TRUE)
write.csv(merged, "joined_data.csv", row.names = FALSE)

# --------------------- BENCHMARK ENDS HERE ---------------------
mem_after <- mem_used()
cpu_end <- proc.time()
end_time <- Sys.time()

# Compute benchmark metrics
runtime <- round(as.numeric(difftime(end_time, start_time, units = "secs")), 3)
cpu_time <- round((cpu_end - cpu_start)[["user.self"]], 3)
mem_used_mb <- round((mem_after - mem_before) / 1024^2, 3)

# Estimate lines used for core task: 3 lines
core_task_lines <- 3

# Output results
cat("✅ Performed left join with dummy region lookup on gss_code\n")
cat("Runtime (seconds):", runtime, "\n")
cat("CPU Time (seconds):", cpu_time, "\n")
cat("Memory usage (MB):", mem_used_mb, "\n")
cat("Total Lines of Code (script_path):", total_lines_of_code, "\n")
cat("Lines of Core Task Only:", core_task_lines, "\n")
