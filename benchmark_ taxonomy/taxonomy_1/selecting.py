import pandas as pd
import time
import psutil
import os
from memory_profiler import memory_usage

def select_columns_task():
    total_lines = 17
    core_lines = 4  # read_csv, select columns, to_csv, len()

    process = psutil.Process(os.getpid())
    cpu_start = process.cpu_times().user
    wall_start = time.time()

    df = pd.read_csv("../birth_gp_ratios.csv")
    selected = df[["gss_name", "gp_count", "actual_births", "date"]]
    selected.to_csv("selected_columns.csv", index=False)

    wall_end = time.time()
    cpu_end = process.cpu_times().user

    runtime = round(wall_end - wall_start, 3)
    cpu_runtime = round(cpu_end - cpu_start, 3)

    return runtime, cpu_runtime, len(selected), total_lines, core_lines

if __name__ == "__main__":
    mem_values, result = memory_usage((select_columns_task,), max_iterations=1, retval=True)
    runtime, cpu_runtime, row_count, total_lines, core_lines = result
    mem_used = round(max(mem_values) - min(mem_values), 3)

    print(f"Runtime: {runtime} seconds")
    print(f"CPU Runtime: {cpu_runtime} seconds")
    print(f"Selected rows: {row_count}")
    print(f"Memory usage: {mem_used} MB")
    print(f"Total Lines of Code: {total_lines}")
    print(f"Core Lines of Code: {core_lines}")
