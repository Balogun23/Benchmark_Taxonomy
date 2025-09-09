# Set working directory
setwd("C:/Users/HP/Desktop/metrics_r")

# Start time
start_time <- Sys.time()

# Load data
df <- read.csv("birth_gp_ratios.csv")

# Filter rows where actual_births > 1000
filtered_df <- subset(df, actual_births > 1000)

# End time
end_time <- Sys.time()

# Calculate runtime
runtime <- round(difftime(end_time, start_time, units = "secs"), 3)

# Estimate memory usage of filtered data (in MB)
mem_usage_mb <- round(as.numeric(object.size(filtered_df)) / 1024^2, 3)

# Output
cat("Runtime (seconds):", runtime, "\n")
cat("Memory usage (MB):", mem_usage_mb, "\n")
cat("Lines of code:", 5, "\n")
