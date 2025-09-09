import pandas as pd
from memory_profiler import memory_usage
import time
import inspect
import os
import psutil

def type_conversion_task():
    wall_start = time.time()
    cpu_start = time.process_time()

    df = pd.read_csv("../birth_gp_ratios.csv")
    df["gp_count"] = pd.to_numeric(df["gp_count"], errors="coerce")
    df["actual_births"] = pd.to_numeric(df["actual_births"], errors="coerce")

    df.to_csv("converted_types.csv", index=False)

    wall_end = time.time()
    cpu_end = time.process_time()

    wall_runtime = round(wall_end - wall_start, 3)
    cpu_runtime = round(cpu_end - cpu_start, 3)
    
    print(f"Runtime (Wall): {wall_runtime} seconds")
    print(f"CPU Runtime: {cpu_runtime} seconds")

    source_lines = inspect.getsource(type_conversion_task).split('\n')
    total_lines = len(source_lines)
    core_lines = len([line for line in source_lines if line.strip() and not line.strip().startswith("#")])
    
    print(f"Total Lines of Code: {total_lines}")
    print(f"Core Lines of Code: {core_lines - 3}")  # Adjust for function header and return

    return wall_runtime, cpu_runtime

if __name__ == "__main__":
    mem_usage = memory_usage((type_conversion_task,), max_iterations=1)
    print(f"Memory usage: {round(max(mem_usage) - min(mem_usage), 3)} MB")
