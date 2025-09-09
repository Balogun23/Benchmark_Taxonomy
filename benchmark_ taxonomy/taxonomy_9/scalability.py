import time, os, psutil
import pandas as pd
from memory_profiler import memory_usage

def benchmark_scalability():
    total_lines, core_lines = 24, 10
    process = psutil.Process(os.getpid())
    cpu_start, wall_start = process.cpu_times().user, time.time()

    # Simulate large dataset
    df = pd.DataFrame({"id": range(1_000_000), "value": range(1_000_000)})
    df["squared"] = df["value"]**2
    rows = len(df)

    wall_end, cpu_end = time.time(), process.cpu_times().user
    runtime, cpu_runtime = round(wall_end - wall_start, 3), round(cpu_end - cpu_start, 3)
    return runtime, cpu_runtime, rows, total_lines, core_lines

if __name__ == "__main__":
    mem_usage = memory_usage((benchmark_scalability,), max_iterations=1)
    runtime, cpu_runtime, rows, total_lines, core_lines = benchmark_scalability()
    print(f"Runtime: {runtime}s | CPU Runtime: {cpu_runtime}s | Rows: {rows}")
    print(f"Memory Usage: {round(max(mem_usage)-min(mem_usage),3)} MB")
    print(f"Total LOC: {total_lines} | Core LOC: {core_lines}")
