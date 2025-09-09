import pandas as pd
import time
import psutil
import os
from memory_profiler import memory_usage

def filtering_task():
    total_lines = 21
    core_lines = 6  # read_csv, filter, to_csv, len(), round(), return

    # Setup metrics tracking
    process = psutil.Process(os.getpid())
    cpu_start = process.cpu_times().user
    wall_start = time.time()

    # Step 1: Load CSV
    df = pd.read_csv("../birth_gp_ratios.csv")

    # Step 2: Apply filters
    filtered = df[
        (df["ratio_type"] == "actual") &
        (df["gp_count"].notna()) &
        (df["actual_births"].notna()) &
        (df["sex"] == "persons")
    ]

    # Step 3: Save output
    filtered.to_csv("filtered_birth_gp_ratios.csv", index=False)

    # Final time stats
    wall_end = time.time()
    cpu_end = process.cpu_times().user

    runtime = round(wall_end - wall_start, 3)
    cpu_runtime = round(cpu_end - cpu_start, 3)

    print(f"Runtime (wall-clock): {runtime} seconds")
    print(f"CPU Runtime: {cpu_runtime} seconds")
    print(f"Filtered rows: {len(filtered)}")
    print(f"Total Lines of Code: {total_lines}")
    print(f"Core Lines of Code: {core_lines}")

    return runtime, cpu_runtime, total_lines, core_lines

if __name__ == "__main__":
    mem = memory_usage((filtering_task,), max_iterations=1)
    print(f"Memory Usage: {round(max(mem) - min(mem), 3)} MB")
