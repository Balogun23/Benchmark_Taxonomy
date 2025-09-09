import pandas as pd
import sqlite3
import time
import psutil
import os
from memory_profiler import memory_usage

def sql_correlation_task():
    total_lines = 25
    core_lines = 6  # connect, to_sql, SELECT, read_sql, correlation, print

    # Start measuring performance
    process = psutil.Process(os.getpid())
    cpu_start = process.cpu_times().user
    wall_start = time.time()

    # Step 1: Load CSV and insert into SQLite
    conn = sqlite3.connect("benchmark.db")
    df = pd.read_csv("../birth_gp_ratios.csv")
    df.to_sql("birth_gp_ratios", conn, if_exists="replace", index=False)

    # Step 2: SQL query for valid records
    query = """
    SELECT actual_births, gp_count
    FROM birth_gp_ratios
    WHERE ratio_type = 'actual' AND actual_births IS NOT NULL AND gp_count IS NOT NULL
    """
    data = pd.read_sql_query(query, conn)
    conn.close()

    # Step 3: Compute Pearson correlation
    corr_matrix = data[["actual_births", "gp_count"]].corr(method="pearson")
    print("Correlation matrix:")
    print(corr_matrix)

    # Compute runtimes
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
    mem_usage = memory_usage((sql_correlation_task,), max_iterations=1)
    print(f"Memory usage: {round(max(mem_usage) - min(mem_usage), 3)} MB")
