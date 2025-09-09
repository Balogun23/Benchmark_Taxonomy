import pandas as pd
from memory_profiler import memory_usage
import time
import inspect

def reshaping_task():
    wall_start = time.time()
    cpu_start = time.process_time()

    df = pd.read_csv("../birth_gp_ratios.csv")  # Adjust path as needed

    # Pivoting using 'gss_name' and 'date'
    reshaped = df.pivot_table(
        values="actual_births",
        index="gss_name",
        columns="date",
        aggfunc="sum"
    )

    reshaped.to_csv("reshaped_output.csv")

    wall_end = time.time()
    cpu_end = time.process_time()
    
    wall_runtime = round(wall_end - wall_start, 3)
    cpu_runtime = round(cpu_end - cpu_start, 3)

    print(f"Runtime (Wall Clock): {wall_runtime} seconds")
    print(f"CPU Runtime: {cpu_runtime} seconds")
    print(f"Output Shape: {reshaped.shape}")

    # Count total and core lines of code
    source_lines = inspect.getsource(reshaping_task).split('\n')
    total_lines = len(source_lines)
    core_lines = len([line for line in source_lines if line.strip() and not line.strip().startswith("#")])

    print(f"Total Lines of Code: {total_lines}")
    print(f"Core Lines of Code: {core_lines - 3}")  # subtract def line, return, and print

    return wall_runtime

if __name__ == "__main__":
    mem_usage = memory_usage((reshaping_task,), max_iterations=1)
    print(f"Memory Usage: {round(max(mem_usage) - min(mem_usage), 3)} MB")
