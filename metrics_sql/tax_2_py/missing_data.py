import pandas as pd
import sqlite3
import time
import psutil
import os
from memory_profiler import memory_usage

def sql_handle_missing_task():
    total_lines = 21
    core_lines = 5  
    process = psutil.Process(os.getpid())
    cpu_start = process.cpu_times().user
    wall_start = time.time()

    conn = sqlite3.connect("benchmark.db")

    df = pd.read_csv("../birth_gp_ratios.csv")
    df.to_sql("birth_gp_ratios", conn, if_exists="replace", index=False)

    
    query = """
    SELECT *
    FROM birth_gp_ratios
    WHERE gp_count IS NOT NULL
      AND actual_births IS NOT NULL
    """
    df_cleaned = pd.read_sql_query(query, conn)
    df_cleaned.to_csv("cleaned_missing_sql.csv", index=False)

    conn.close()

    wall_end = time.time()
    cpu_end = process.cpu_times().user

    runtime = round(wall_end - wall_start, 3)
    cpu_runtime = round(cpu_end - cpu_start, 3)

    print(f"Runtime (wall-clock): {runtime} seconds")
    print(f"CPU Runtime: {cpu_runtime} seconds")
    print(f"Remaining rows: {len(df_cleaned)}")
    print(f"Total Lines of Code: {total_lines}")
    print(f"Core Lines of Code: {core_lines}")

    return runtime, cpu_runtime, total_lines, core_lines

if __name__ == "__main__":
    mem_usage = memory_usage((sql_handle_missing_task,), max_iterations=1)
    print(f"Memory Usage: {round(max(mem_usage) - min(mem_usage), 3)} MB")
