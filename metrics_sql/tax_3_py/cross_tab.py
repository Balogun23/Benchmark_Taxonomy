import pandas as pd
import sqlite3
import time
import psutil
import os
from memory_profiler import memory_usage

def sql_crosstab_summary_sql():
    total_lines = 24
    core_lines = 7  
    
    process = psutil.Process(os.getpid())
    cpu_start = process.cpu_times().user
    wall_start = time.time()

    # Connect to SQLite
    conn = sqlite3.connect("benchmark.db")

    # Load CSV into database
    df = pd.read_csv("../birth_gp_ratios.csv")
    df.to_sql("birth_gp_ratios", conn, if_exists="replace", index=False)

    # Perform crosstab using SQL aggregation (equivalent to pd.crosstab)
    query = """
    SELECT 
        sex,
        SUM(CASE WHEN ratio_type = 'actual' THEN 1 ELSE 0 END) AS actual,
        SUM(CASE WHEN ratio_type = 'expected' THEN 1 ELSE 0 END) AS expected,
        SUM(CASE WHEN ratio_type = 'ratio' THEN 1 ELSE 0 END) AS ratio
    FROM birth_gp_ratios
    GROUP BY sex
    ORDER BY sex
    """
    crosstab_df = pd.read_sql_query(query, conn)
    print("Cross-tabulation (sex vs. ratio_type):\n", crosstab_df)

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
    mem_usage = memory_usage((sql_crosstab_summary_sql,), max_iterations=1)
    print(f"Memory Usage: {round(max(mem_usage) - min(mem_usage), 3)} MB")
