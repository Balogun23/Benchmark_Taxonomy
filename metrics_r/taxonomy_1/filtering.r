 
start_time <- Sys.time()

df <- read.csv("birth_gp_ratios.csv")

filtered_df <- subset(df, actual_births > 1000)

end_time <- Sys.time()

runtime <- round(difftime(end_time, start_time, units = "secs"), 3)

mem_usage_mb <- round(as.numeric(object.size(filtered_df)) / 1024^2, 3)


cat("Runtime (seconds):", runtime, "\n")
cat("Memory usage (MB):", mem_usage_mb, "\n")
cat("Lines of code:", 5, "\n")
