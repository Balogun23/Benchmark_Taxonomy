import pandas as pd
import sqlite3
import time
import os
import psutil
from memory_profiler import memory_usage

def sql_merge_task():
    total_lines = 25
    core_lines = 6  # connect, to_sql (2x), SQL JOIN query, read_sql, to_csv

    process = psutil.Process(os.getpid())
    cpu_start = process.cpu_times().user
    wall_start = time.time()

    # Connect to SQLite database
    conn = sqlite3.connect("benchmark.db")

    # Load main table
    df_main = pd.read_csv("../birth_gp_ratios.csv")
    df_main.to_sql("birth_gp_ratios", conn, if_exists="replace", index=False)

    # Create dummy lookup table
    dummy_lookup = pd.DataFrame({
        "gss_code": df_main["gss_code"].dropna().unique()[:10],
        "region_group": [f"Group_{i+1}" for i in range(10)]
    })
    dummy_lookup.to_sql("dummy_lookup", conn, if_exists="replace", index=False)

    # SQL LEFT JOIN
    query = """
    SELECT b.*, l.region_group
    FROM birth_gp_ratios b
    LEFT JOIN dummy_lookup l
    ON b.gss_code = l.gss_code
    """
    merged_df = pd.read_sql_query(query, conn)
    merged_df.to_csv("sql_merged_with_lookup.csv", index=False)

    conn.close()

    wall_end = time.time()
    cpu_end = process.cpu_times().user

    runtime = round(wall_end - wall_start, 3)
    cpu_runtime = round(cpu_end - cpu_start, 3)
    row_count = len(merged_df)

    return runtime, cpu_runtime, row_count, total_lines, core_lines

if __name__ == "__main__":
    mem_usage = memory_usage((sql_merge_task,), max_iterations=1)
    runtime, cpu_runtime, row_count, total_lines, core_lines = sql_merge_task()

    print(f"Runtime (wall-clock): {runtime} seconds")
    print(f"CPU Runtime: {cpu_runtime} seconds")
    print(f"Rows after merge: {row_count}")
    print(f"Memory Usage: {round(max(mem_usage) - min(mem_usage), 3)} MB")
    print(f"Total Lines of Code: {total_lines}")
    print(f"Core Lines of Code: {core_lines}")
