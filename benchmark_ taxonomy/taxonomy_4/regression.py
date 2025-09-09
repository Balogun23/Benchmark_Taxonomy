import pandas as pd
import statsmodels.api as sm
import time
from memory_profiler import memory_usage
import inspect

def linear_regression_task():
    wall_start = time.time()
    cpu_start = time.process_time()
    
    # Load and filter dataset
    df = pd.read_csv("../birth_gp_ratios.csv")
    df = df[(df["ratio_type"] == "actual") & df["actual_births"].notna() & df["gp_count"].notna()]

    # Prepare X and y
    X = df["gp_count"]
    y = df["actual_births"]
    X = sm.add_constant(X)

    # Run regression
    model = sm.OLS(y, X).fit()
    print(model.summary())

    wall_end = time.time()
    cpu_end = time.process_time()
    wall_runtime = round(wall_end - wall_start, 3)
    cpu_runtime = round(cpu_end - cpu_start, 3)

    print(f"\nRuntime (Wall Clock): {wall_runtime} seconds")
    print(f"CPU Runtime: {cpu_runtime} seconds")

    # Count lines of core logic
    lines = inspect.getsource(linear_regression_task).split('\n')
    total_lines = len(lines)
    core_lines = len([line for line in lines if line.strip() and not line.strip().startswith("#")])
    print(f"Total Lines of Code: {total_lines}")
    print(f"Core Lines of Code: {core_lines - 3}")  # Subtract def, return, print

    return wall_runtime

if __name__ == "__main__":
    mem_usage = memory_usage((linear_regression_task,), max_iterations=1)
    print(f"Memory usage: {round(max(mem_usage) - min(mem_usage), 3)} MB")
