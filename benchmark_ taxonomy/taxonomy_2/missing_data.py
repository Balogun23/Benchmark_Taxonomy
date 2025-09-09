import pandas as pd
import time
import inspect
from memory_profiler import memory_usage

def handle_missing_data():
    start_wall = time.time()
    start_cpu = time.process_time()

    df = pd.read_csv("../birth_gp_ratios.csv")
    df_cleaned = df.dropna(subset=["gp_count", "actual_births"])
    df_cleaned.to_csv("cleaned_missing.csv", index=False)

    end_wall = time.time()
    end_cpu = time.process_time()

    runtime = round(end_wall - start_wall, 3)
    cpu_time = round(end_cpu - start_cpu, 3)

    print(f"Remaining rows: {len(df_cleaned)}")
    print(f"Wall clock time: {runtime} seconds")
    print(f"CPU time: {cpu_time} seconds")

    source_lines = inspect.getsource(handle_missing_data).split('\n')
    total_lines = len(source_lines)
    core_lines = len([
        line for line in source_lines
        if line.strip() and not line.strip().startswith("#") and not line.strip().startswith("import")
    ]) - 3  
    print(f"Total lines of code: {total_lines}")
    print(f"Core logic lines of code: {core_lines}")

    return runtime, cpu_time, total_lines, core_lines

if __name__ == "__main__":
    mem_usage = memory_usage((handle_missing_data,), max_iterations=1)
    print(f"Memory usage: {round(max(mem_usage) - min(mem_usage), 3)} MB")
