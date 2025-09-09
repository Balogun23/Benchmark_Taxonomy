import pandas as pd
import sqlite3
import time
import os
import psutil
from memory_profiler import memory_usage

def sql_select_columns_task():
    total_lines = 23
    core_lines = 5  # connect, to_sql, SELECT query, read_sql, to_csv

    process = psutil.Process(os.getpid())
    cpu_start = process.cpu_times().user
    wall_start = time.time()

    # Connect to SQLite
    conn = sqlite3.connect("benchmark.db")

    # Load CSV into SQL table
    df = pd.read_csv("../birth_gp_ratios.csv")
    df.to_sql("birth_gp_ratios", conn, if_exists="replace", index=False)

    # SQL query to select specific columns
    query = """
    SELECT gss_name, gp_count, actual_births, date
    FROM birth_gp_ratios
    """
    selected = pd.read_sql_query(query, conn)
    selected.to_csv("sql_selected_columns.csv", index=False)
    conn.close()

    wall_end = time.time()
    cpu_end = process.cpu_times().user

    runtime = round(wall_end - wall_start, 3)
    cpu_runtime = round(cpu_end - cpu_start, 3)

    return runtime, cpu_runtime, len(selected), total_lines, core_lines

if __name__ == "__main__":
    mem_values, result = memory_usage((sql_select_columns_task,), max_iterations=1, retval=True)
    runtime, cpu_runtime, row_count, total_lines, core_lines = result
    mem_used = round(max(mem_values) - min(mem_values), 3)

    print(f"Runtime (wall-clock): {runtime} seconds")
    print(f"CPU Runtime: {cpu_runtime} seconds")
    print(f"Selected rows: {row_count}")
    print(f"Memory Usage: {mem_used} MB")
    print(f"Total Lines of Code: {total_lines}")
    print(f"Core Lines of Code: {core_lines}")
