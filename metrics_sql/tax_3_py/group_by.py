import pandas as pd
import sqlite3
import time
import psutil
import os
from memory_profiler import memory_usage

def sql_grouped_summary():
    total_lines = 22
    core_lines = 5  # connect, to_sql, SQL aggregation, read_sql, print

    process = psutil.Process(os.getpid())
    cpu_start = process.cpu_times().user
    wall_start = time.time()

    # Connect to SQLite and load CSV
    conn = sqlite3.connect("benchmark.db")
    df = pd.read_csv("../birth_gp_ratios.csv")
    df.to_sql("birth_gp_ratios", conn, if_exists="replace", index=False)

    # SQL: Grouped summary by sex
    query = """
    SELECT 
        sex,
        COUNT(actual_births) AS count_births,
        SUM(actual_births) AS total_births,
        AVG(actual_births) AS avg_births
    FROM birth_gp_ratios
    GROUP BY sex;
    """
    summary_df = pd.read_sql_query(query, conn)
    print("Grouped Summary by 'sex':\n", summary_df)

    conn.close()

    wall_end = time.time()
    cpu_end = process.cpu_times().user

    runtime = round(wall_end - wall_start, 3)
    cpu_runtime = round(cpu_end - cpu_start, 3)

    print(f"Runtime (wall-clock): {runtime} seconds")
    print(f"CPU Runtime: {cpu_runtime} seconds")
    print(f"Total Lines of Code: {total_lines}")
    print(f"Core Lines of Code: {core_lines}")

    return runtime, cpu_runtime, total_lines, core_lines

if __name__ == "__main__":
    mem_usage = memory_usage((sql_grouped_summary,), max_iterations=1)
    print(f"Memory Usage: {round(max(mem_usage) - min(mem_usage), 3)} MB")
