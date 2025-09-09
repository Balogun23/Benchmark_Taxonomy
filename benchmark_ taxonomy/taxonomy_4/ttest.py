import pandas as pd
from scipy.stats import ttest_ind
import time
from memory_profiler import memory_usage
import inspect
# import os
# import psutil

def t_test_task():
    wall_start = time.time()
    cpu_start = time.process_time()

    df = pd.read_csv("../birth_gp_ratios.csv")
    df = df[df["ratio_type"] == "actual"]

    # Identify two top years with enough data
    counts = df["date"].value_counts()
    top_years = counts.index[:2]  # top 2 years by count

    group1 = df[df["date"] == top_years[0]]["actual_births"].dropna()
    group2 = df[df["date"] == top_years[1]]["actual_births"].dropna()

    if len(group1) > 1 and len(group2) > 1:
        t_stat, p_val = ttest_ind(group1, group2, equal_var=False)
        print(f"T-test between {top_years[0]} and {top_years[1]}:")
        print(f"T-statistic: {t_stat:.3f}")
        print(f"P-value: {p_val:.5f}")
    else:
        print("Not enough data to perform t-test.")

    wall_runtime = round(time.time() - wall_start, 3)
    cpu_runtime = round(time.process_time() - cpu_start, 3)
    print(f"Wall-clock Runtime: {wall_runtime} seconds")
    print(f"CPU Runtime: {cpu_runtime} seconds")

    # Count total and core lines of code
    source_lines = inspect.getsource(t_test_task).split('\n')
    total_lines = len(source_lines)
    core_lines = len([line for line in source_lines if line.strip() and not line.strip().startswith("#")])
    print(f"Total Lines of Code: {total_lines}")
    print(f"Core Lines of Code: {core_lines - 3}")  # minus def, prints, return

    return wall_runtime

if __name__ == "__main__":
    mem_usage = memory_usage((t_test_task,), max_iterations=1)
    print(f"Memory usage: {round(max(mem_usage) - min(mem_usage), 3)} MB")
