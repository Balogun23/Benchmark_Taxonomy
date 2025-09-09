import pandas as pd
import sqlite3
import time
import psutil
import os
from scipy.stats import f_oneway
from memory_profiler import memory_usage
import inspect

def sql_anova_task():
    total_lines = 26
    core_lines = 7  # connect, to_sql, SQL SELECT, groupby, f_oneway

    process = psutil.Process(os.getpid())
    cpu_start = process.cpu_times().user
    wall_start = time.time()

    # Step 1: Load data into SQLite
    conn = sqlite3.connect("benchmark.db")
    df = pd.read_csv("../birth_gp_ratios.csv")
    df.to_sql("birth_gp_ratios", conn, if_exists="replace", index=False)

    # Step 2: Query data for ANOVA (filter actual ratio_type and non-null actual_births)
    query = """
    SELECT date, actual_births
    FROM birth_gp_ratios
    WHERE ratio_type = 'actual' AND actual_births IS NOT NULL
    """
    data = pd.read_sql_query(query, conn)
    conn.close()

    # Step 3: Group by date and filter groups with >= 2 values
    grouped = data.groupby("date")["actual_births"].apply(list)
    filtered_groups = [group for group in grouped if len(group) >= 2]

    # Step 4: Run ANOVA
    if len(filtered_groups) >= 2:
        result = f_oneway(*filtered_groups)
        print("ANOVA Result:")
        print(result)
    else:
        print("Cannot run ANOVA: not enough valid date groups")

    # Runtime and code metrics
    wall_end = time.time()
    cpu_end = process.cpu_times().user
    runtime = round(wall_end - wall_start, 3)
    cpu_runtime = round(cpu_end - cpu_start, 3)

    print(f"\nRuntime (wall-clock): {runtime} seconds")
    print(f"CPU Runtime: {cpu_runtime} seconds")
    print(f"Total Lines of Code: {total_lines}")
    print(f"Core Lines of Code: {core_lines}")

    return runtime, cpu_runtime, total_lines, core_lines

if __name__ == "__main__":
    mem = memory_usage((sql_anova_task,), max_iterations=1)
    print(f"Memory usage: {round(max(mem) - min(mem), 3)} MB")
