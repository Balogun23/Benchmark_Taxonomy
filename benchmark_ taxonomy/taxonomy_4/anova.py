import pandas as pd
from scipy.stats import f_oneway
import time
from memory_profiler import memory_usage
import inspect

def anova_task():
    wall_start = time.time()
    cpu_start = time.process_time()

    # Load and filter data
    df = pd.read_csv("../birth_gp_ratios.csv")
    df = df[(df["ratio_type"] == "actual") & df["actual_births"].notna()]

    # Group by year and filter groups with sufficient data
    grouped = df.groupby("date")["actual_births"].apply(list)
    filtered_groups = [g for g in grouped if len(g) >= 2]

    # Perform ANOVA
    if len(filtered_groups) >= 2:
        result = f_oneway(*filtered_groups)
        print("ANOVA Result:")
        print(result)
    else:
        print("Cannot run ANOVA: not enough valid year groups")

    wall_end = time.time()
    cpu_end = time.process_time()

    wall_runtime = round(wall_end - wall_start, 3)
    cpu_runtime = round(cpu_end - cpu_start, 3)

    print(f"\nRuntime (Wall Clock): {wall_runtime} seconds")
    print(f"CPU Runtime: {cpu_runtime} seconds")

    # Count total and core lines of code
    source_lines = inspect.getsource(anova_task).split('\n')
    total_lines = len(source_lines)
    core_lines = len([line for line in source_lines if line.strip() and not line.strip().startswith("#")])
    print(f"Total Lines of Code: {total_lines}")
    print(f"Core Lines of Code: {core_lines - 3}")  # Exclude def + return + print

    return wall_runtime

if __name__ == "__main__":
    mem_usage = memory_usage((anova_task,), max_iterations=1)
    print(f"Memory Usage: {round(max(mem_usage) - min(mem_usage), 3)} MB")
