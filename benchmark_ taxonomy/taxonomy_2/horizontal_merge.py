import pandas as pd
import time
import os
import psutil
from memory_profiler import memory_usage

def python_merge_task():
    total_lines = 27
    core_lines = 6 

    process = psutil.Process(os.getpid())
    cpu_start = process.cpu_times().user
    wall_start = time.time()

    # Read main file
    main = pd.read_csv("../birth_gp_ratios.csv")

    # Create dummy lookup
    dummy_lookup = pd.DataFrame({
        "gss_code": main["gss_code"].dropna().unique()[:10],
        "region_group": [f"Group_{i+1}" for i in range(10)]
    })

    # Merge operation
    merged = pd.merge(main, dummy_lookup, on="gss_code", how="left")
    merged.to_csv("python_merged_with_lookup.csv", index=False)

    wall_end = time.time()
    cpu_end = process.cpu_times().user

    runtime = round(wall_end - wall_start, 3)
    cpu_runtime = round(cpu_end - cpu_start, 3)
    row_count = len(merged)

    return runtime, cpu_runtime, row_count, total_lines, core_lines

if __name__ == "__main__":
    mem_usage = memory_usage((python_merge_task,), max_iterations=1)
    runtime, cpu_runtime, row_count, total_lines, core_lines = python_merge_task()

    print(f"Runtime (wall-clock): {runtime} seconds")
    print(f"CPU Runtime: {cpu_runtime} seconds")
    print(f"Rows after merge: {row_count}")
    print(f"Memory Usage: {round(max(mem_usage) - min(mem_usage), 3)} MB")
    print(f"Total Lines of Code: {total_lines}")
    print(f"Core Lines of Code: {core_lines}")
