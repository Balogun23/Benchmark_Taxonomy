import pandas as pd
from memory_profiler import memory_usage
import time
import inspect

def crosstab_summary():
    wall_start = time.time()
    cpu_start = time.process_time()

    df = pd.read_csv("../birth_gp_ratios.csv")
    tab = pd.crosstab(df["sex"], df["ratio_type"])
    print("Cross-tabulation (sex vs. ratio_type):\n", tab)

    wall_end = time.time()
    cpu_end = time.process_time()

    wall_runtime = round(wall_end - wall_start, 3)
    cpu_runtime = round(cpu_end - cpu_start, 3)

    print(f"Runtime (Wall Clock): {wall_runtime} seconds")
    print(f"CPU Runtime: {cpu_runtime} seconds")

    # Count total and core lines of code
    source_lines = inspect.getsource(crosstab_summary).split('\n')
    total_lines = len(source_lines)
    core_lines = len([line for line in source_lines if line.strip() and not line.strip().startswith("#")])

    print(f"Total Lines of Code: {total_lines}")
    print(f"Core Lines of Code: {core_lines - 3}")  # def, return, print

    return wall_runtime

if __name__ == "__main__":
    mem = memory_usage((crosstab_summary,), max_iterations=1)
    print(f"Memory Usage: {round(max(mem) - min(mem), 3)} MB")
