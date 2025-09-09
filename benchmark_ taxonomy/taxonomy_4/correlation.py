import pandas as pd
import time
from memory_profiler import memory_usage
import inspect

def correlation_task():
    wall_start = time.time()
    cpu_start = time.process_time()

    # Load and clean data
    df = pd.read_csv("../birth_gp_ratios.csv")
    df = df[(df["ratio_type"] == "actual") & df["actual_births"].notna() & df["gp_count"].notna()]

    # Compute correlation matrix
    corr_matrix = df[["actual_births", "gp_count"]].corr(method="pearson")  # or "spearman"
    print("Correlation matrix:")
    print(corr_matrix)

    wall_end = time.time()
    cpu_end = time.process_time()
    wall_runtime = round(wall_end - wall_start, 3)
    cpu_runtime = round(cpu_end - cpu_start, 3)

    print(f"\nRuntime (Wall Clock): {wall_runtime} seconds")
    print(f"CPU Runtime: {cpu_runtime} seconds")

    # Line counts
    lines = inspect.getsource(correlation_task).split('\n')
    total_lines = len(lines)
    core_lines = len([line for line in lines if line.strip() and not line.strip().startswith("#")])
    print(f"Total Lines of Code: {total_lines}")
    print(f"Core Lines of Code: {core_lines - 3}")  # Minus def, return, final print

    return wall_runtime

if __name__ == "__main__":
    mem_usage = memory_usage((correlation_task,), max_iterations=1)
    print(f"Memory Usage: {round(max(mem_usage) - min(mem_usage), 3)} MB")
