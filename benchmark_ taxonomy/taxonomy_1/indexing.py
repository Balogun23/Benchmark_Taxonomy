import pandas as pd
import time
import inspect
from memory_profiler import memory_usage

def indexing_task():
    start_wall = time.time()
    start_cpu = time.process_time()

    # Load and index dataset
    df = pd.read_csv("../birth_gp_ratios.csv")
    indexed = df.set_index("gss_code")
    indexed.to_csv("indexed_data.csv")

    end_wall = time.time()
    end_cpu = time.process_time()

    # Timing results
    runtime = round(end_wall - start_wall, 3)
    cpu_time = round(end_cpu - start_cpu, 3)

    # Line counts
    source_lines = inspect.getsource(indexing_task).split('\n')
    total_lines = len(source_lines)
    core_lines = len([
        line for line in source_lines
        if line.strip() and not line.strip().startswith("#") and not line.strip().startswith("import")
    ]) - 3  # minus def line, start and return

    # Print metrics
    print(f"Wall clock time: {runtime} seconds")
    print(f"CPU time: {cpu_time} seconds")
    print(f"Total lines of code: {total_lines}")
    print(f"Core logic lines of code: {core_lines}")

    return runtime, cpu_time, total_lines, core_lines

if __name__ == "__main__":
    mem_usage = memory_usage((indexing_task,), max_iterations=1)
    print(f"Memory usage: {round(max(mem_usage) - min(mem_usage), 3)} MB")
