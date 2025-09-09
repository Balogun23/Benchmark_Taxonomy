import pandas as pd
import time
import inspect
from memory_profiler import memory_usage

def joining_task():
    start_wall = time.time()
    start_cpu = time.process_time()

    # Load and join datasets
    df_main = pd.read_csv("../birth_gp_ratios.csv")
    dummy_lookup = pd.DataFrame({
        "gss_code": df_main["gss_code"].dropna().unique()[:10],
        "region": [f"Region_{i+1}" for i in range(10)]
    })
    merged = df_main.merge(dummy_lookup, on="gss_code", how="left")
    merged.to_csv("joined_data.csv", index=False)

    end_wall = time.time()
    end_cpu = time.process_time()

    # Compute metrics
    runtime = round(end_wall - start_wall, 3)
    cpu_time = round(end_cpu - start_cpu, 3)

    source_lines = inspect.getsource(joining_task).split('\n')
    total_lines = len(source_lines)
    core_lines = len([
        line for line in source_lines
        if line.strip() and not line.strip().startswith("#") and not line.strip().startswith("import")
    ]) - 3  # minus def line, start and return

    # Display metrics
    print(f"Wall clock time: {runtime} seconds")
    print(f"CPU time: {cpu_time} seconds")
    print(f"Total lines of code: {total_lines}")
    print(f"Core logic lines of code: {core_lines}")

    return runtime, cpu_time, total_lines, core_lines

if __name__ == "__main__":
    mem_usage = memory_usage((joining_task,), max_iterations=1)
    print(f"Memory usage: {round(max(mem_usage) - min(mem_usage), 3)} MB")
