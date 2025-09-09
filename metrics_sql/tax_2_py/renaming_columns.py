import pandas as pd
import sqlite3
import time
import psutil
import os
from memory_profiler import memory_usage

def sql_renaming_task():
    total_lines = 21
    core_lines = 5  # connect, to_sql, SELECT AS alias, read_sql, to_csv

    process = psutil.Process(os.getpid())
    cpu_start = process.cpu_times().user
    wall_start = time.time()

    # Connect to SQLite database
    conn = sqlite3.connect("benchmark.db")

    # Load CSV into SQLite table
    df = pd.read_csv("../birth_gp_ratios.csv")
    df.to_sql("birth_gp_ratios", conn, if_exists="replace", index=False)

    # Perform column renaming via SQL aliases
    query = """
    SELECT
    gss_code,
    gss_name,
    geography,
    sex,
    date,
    ratio,
    ratio_lower,
    ratio_upper,
    ratio_type,
    gp_count AS gp_total,
    actual_births AS births_actual
FROM birth_gp_ratios;
    """
    renamed_df = pd.read_sql_query(query, conn)
    renamed_df.to_csv("renamed_columns_sql.csv", index=False)

    conn.close()

    wall_end = time.time()
    cpu_end = process.cpu_times().user

    runtime = round(wall_end - wall_start, 3)
    cpu_runtime = round(cpu_end - cpu_start, 3)

    print(f"Runtime (wall-clock): {runtime} seconds")
    print(f"CPU Runtime: {cpu_runtime} seconds")
    print(f"Total Lines of Code: {total_lines}")
    print(f"Core Lines of Code: {core_lines}")
    print(f"Renamed rows: {len(renamed_df)}")

    return runtime, cpu_runtime, total_lines, core_lines

if __name__ == "__main__":
    mem_usage = memory_usage((sql_renaming_task,), max_iterations=1)
    print(f"Memory Usage: {round(max(mem_usage) - min(mem_usage), 3)} MB")
