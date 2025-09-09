import pandas as pd
import time
import psutil
import os
from memory_profiler import memory_usage

def partial_read_task():
    total_lines = 16
    core_lines = 3  # read_csv, to_csv, len()

    process = psutil.Process(os.getpid())
    cpu_start = process.cpu_times().user
    wall_start = time.time()

    df = pd.read_csv("../birth_gp_ratios.csv", nrows=5000)
    df.to_csv("partial_rows.csv", index=False)

    wall_end = time.time()
    cpu_end = process.cpu_times().user

    runtime = round(wall_end - wall_start, 3)
    cpu_runtime = round(cpu_end - cpu_start, 3)

    return runtime, cpu_runtime, len(df), total_lines, core_lines

if __name__ == "__main__":
    mem_profile, result = memory_usage((partial_read_task,), max_iterations=1, retval=True)
    runtime, cpu_runtime, rows_read, total_lines, core_lines = result
    mem_used = round(max(mem_profile) - min(mem_profile), 3)

    print(f"Runtime (wall-clock): {runtime} seconds")
    print(f"CPU Runtime: {cpu_runtime} seconds")
    print(f"Rows read: {rows_read}")
    print(f"Memory Usage: {mem_used} MB")
    print(f"Total Lines of Code: {total_lines}")
    print(f"Core Lines of Code: {core_lines}")
