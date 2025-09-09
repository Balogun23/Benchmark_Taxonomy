import time
import psutil
import pandas as pd
import sqlite3
import os
from memory_profiler import memory_usage

def sql_indexing_task():
    total_lines = 25
    core_lines = 5 
    
    process = psutil.Process(os.getpid())
    cpu_start = process.cpu_times().user
    wall_start = time.time()

    conn = sqlite3.connect("benchmark.db")

    df = pd.read_csv("../birth_gp_ratios.csv")
    df.to_sql("birth_gp_ratios", conn, if_exists="replace", index=False)

    # Perform indexing by ordering
    query = """
    SELECT *
    FROM birth_gp_ratios
    ORDER BY gss_code
    """
    df_indexed = pd.read_sql_query(query, conn)
    df_indexed.to_csv("sql_indexed_data.csv", index=False)

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
    mem_usage_vals = memory_usage((sql_indexing_task,), max_iterations=1)
    mem_used = round(max(mem_usage_vals) - min(mem_usage_vals), 3)
    print(f"Memory Usage: {mem_used} MB")
