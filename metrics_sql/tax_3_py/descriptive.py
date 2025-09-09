import pandas as pd
import sqlite3
import time
import psutil
import os
from memory_profiler import memory_usage

def sql_descriptive_stats_sql():
    total_lines = 24
    core_lines = 7  # connect, to_sql, SQL aggregation, read_sql, print, close, metrics

    process = psutil.Process(os.getpid())
    cpu_start = process.cpu_times().user
    wall_start = time.time()

    # Connect to SQLite
    conn = sqlite3.connect("benchmark.db")

    # Load CSV into SQLite
    df = pd.read_csv("../birth_gp_ratios.csv")
    df.to_sql("birth_gp_ratios", conn, if_exists="replace", index=False)

    # SQL: Descriptive statistics using aggregate functions
    query = """
    SELECT 
        COUNT(actual_births) AS count,
        AVG(actual_births) AS mean,
        MIN(actual_births) AS min,
        MAX(actual_births) AS max,
        SUM(actual_births) AS sum,
        -- Approximation for standard deviation (Bessel's correction)
        ROUND(
            SQRT(
                (SUM(actual_births * actual_births) - SUM(actual_births) * SUM(actual_births) / COUNT(actual_births))
                / (COUNT(actual_births) - 1)
            ), 3
        ) AS std
    FROM birth_gp_ratios
    WHERE actual_births IS NOT NULL
    """
    stats_df = pd.read_sql_query(query, conn)
    print("Descriptive Statistics (via SQL):\n", stats_df)

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
    mem = memory_usage((sql_descriptive_stats_sql,), max_iterations=1)
    print(f"Memory usage: {round(max(mem) - min(mem), 3)} MB")
