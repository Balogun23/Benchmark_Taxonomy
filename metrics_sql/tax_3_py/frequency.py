import pandas as pd
import sqlite3
import time
import psutil
import os
from memory_profiler import memory_usage

def sql_frequency_mode_task():
    total_lines = 26
    core_lines = 6  # connect, to_sql, frequency query, mode query, print, close

    process = psutil.Process(os.getpid())
    cpu_start = process.cpu_times().user
    wall_start = time.time()

    # Connect to SQLite and load data
    conn = sqlite3.connect("benchmark.db")
    df = pd.read_csv("../birth_gp_ratios.csv")
    df.to_sql("birth_gp_ratios", conn, if_exists="replace", index=False)

    # SQL frequency count for 'ratio_type'
    freq_query = """
    SELECT ratio_type, COUNT(*) AS count
    FROM birth_gp_ratios
    GROUP BY ratio_type
    ORDER BY count DESC;
    """
    freq_df = pd.read_sql_query(freq_query, conn)
    print("Frequency Counts:\n", freq_df)

    # SQL to compute mode of 'ratio_type'
    mode_query = """
    SELECT ratio_type
    FROM birth_gp_ratios
    GROUP BY ratio_type
    ORDER BY COUNT(*) DESC
    LIMIT 1;
    """
    mode_df = pd.read_sql_query(mode_query, conn)
    print("Mode of ratio_type:", mode_df.iloc[0, 0] if not mode_df.empty else "No mode found")

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
    mem_usage = memory_usage((sql_frequency_mode_task,), max_iterations=1)
    print(f"Memory Usage: {round(max(mem_usage) - min(mem_usage), 3)} MB")
