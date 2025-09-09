import pandas as pd
import sqlite3
import time
import psutil
import os
from memory_profiler import memory_usage

def sql_type_conversion_task():
    total_lines = 21
    core_lines = 5  # connect, to_sql, SQL query with CAST, read_sql, to_csv

    process = psutil.Process(os.getpid())
    cpu_start = process.cpu_times().user
    wall_start = time.time()

    # Step 1: Connect to SQLite
    conn = sqlite3.connect("benchmark.db")

    # Step 2: Load CSV into SQLite
    df = pd.read_csv("../birth_gp_ratios.csv")
    df.to_sql("birth_gp_ratios", conn, if_exists="replace", index=False)

    # Step 3: SQL query with explicit type conversion (SQL-level)
    query = """
    SELECT 
        gss_code,
        CAST(gp_count AS REAL) AS gp_count,
        CAST(actual_births AS REAL) AS actual_births,
        sex,
        ratio_type
    FROM birth_gp_ratios
    """

    df_sql = pd.read_sql_query(query, conn)

    # Step 4: Export result
    df_sql.to_csv("converted_types_sql.csv", index=False)

    conn.close()

    wall_end = time.time()
    cpu_end = process.cpu_times().user

    runtime = round(wall_end - wall_start, 3)
    cpu_runtime = round(cpu_end - cpu_start, 3)

    print(f"Runtime (wall-clock): {runtime} seconds")
    print(f"CPU Runtime: {cpu_runtime} seconds")
    print(f"Total Lines of Code: {total_lines}")
    print(f"Core Lines of Code: {core_lines}")
    print(f"Converted rows: {len(df_sql)}")

    return runtime, cpu_runtime, total_lines, core_lines

if __name__ == "__main__":
    mem_usage = memory_usage((sql_type_conversion_task,), max_iterations=1)
    print(f"Memory Usage: {round(max(mem_usage) - min(mem_usage), 3)} MB")
