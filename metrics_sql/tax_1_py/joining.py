import pandas as pd
import sqlite3
import time
import os
import psutil
from memory_profiler import memory_usage

def sql_joining_task():
    total_lines = 30
    core_lines = 6  

    process = psutil.Process(os.getpid())
    cpu_start = process.cpu_times().user
    wall_start = time.time()

    # Connect to SQLite DB
    conn = sqlite3.connect("benchmark.db")

    # Load main CSV
    df_main = pd.read_csv("../birth_gp_ratios.csv")
    df_main.to_sql("birth_gp_ratios", conn, if_exists="replace", index=False)

    # Create dummy lookup
    dummy_lookup = pd.DataFrame({
        "gss_code": df_main["gss_code"].dropna().unique()[:10],
        "region": [f"Region_{i+1}" for i in range(10)]
    })
    dummy_lookup.to_sql("dummy_lookup", conn, if_exists="replace", index=False)

    # SQL Join
    query = """
    SELECT b.*, l.region
    FROM birth_gp_ratios b
    LEFT JOIN dummy_lookup l ON b.gss_code = l.gss_code
    """
    joined_df = pd.read_sql_query(query, conn)
    joined_df.to_csv("joined_data_sql.csv", index=False)

    conn.close()

    wall_end = time.time()
    cpu_end = process.cpu_times().user
    runtime = round(wall_end - wall_start, 3)
    cpu_runtime = round(cpu_end - cpu_start, 3)

    print(f"Runtime (wall): {runtime} seconds")
    print(f"CPU Runtime: {cpu_runtime} seconds")
    print(f"Total Lines of Code: {total_lines}")
    print(f"Core Lines of Code: {core_lines}")

    return runtime, cpu_runtime, total_lines, core_lines

if __name__ == "__main__":
    mem_usage = memory_usage((sql_joining_task,), max_iterations=1)
    mem_used = round(max(mem_usage) - min(mem_usage), 3)
    print(f"Memory Usage: {mem_used} MB")
