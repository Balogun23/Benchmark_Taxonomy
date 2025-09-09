import pandas as pd
import time
import psutil
import os
import sqlite3
from memory_profiler import memory_usage

def sql_partial_read_task():
    total_lines = 26
    core_lines = 5  

    process = psutil.Process(os.getpid())
    cpu_start = process.cpu_times().user
    wall_start = time.time()

    # Connect to SQLite database
    conn = sqlite3.connect("benchmark.db")

    # Load data into SQL table
    df = pd.read_csv("../birth_gp_ratios.csv")
    df.to_sql("birth_gp_ratios", conn, if_exists="replace", index=False)

    # Read first 5000 rows via SQL
    query = "SELECT * FROM birth_gp_ratios LIMIT 5000"
    df_partial = pd.read_sql_query(query, conn)
    df_partial.to_csv("sql_partial_rows.csv", index=False)

    conn.close()

    wall_end = time.time()
    cpu_end = process.cpu_times().user

    runtime = round(wall_end - wall_start, 3)
    cpu_runtime = round(cpu_end - cpu_start, 3)

    return runtime, cpu_runtime, len(df_partial), total_lines, core_lines

if __name__ == "__main__":
    mem_usage = memory_usage((sql_partial_read_task,), max_iterations=1, retval=True)
    mem_used = round(max(mem_usage[0]) - min(mem_usage[0]), 3)
    runtime, cpu_runtime, rows_read, total_lines, core_lines = mem_usage[1]

    print(f"Runtime (wall-clock): {runtime} seconds")
    print(f"CPU Runtime: {cpu_runtime} seconds")
    print(f"Rows read: {rows_read}")
    print(f"Memory Usage: {mem_used} MB")
    print(f"Total Lines of Code: {total_lines}")
    print(f"Core Lines of Code: {core_lines}")
