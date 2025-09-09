import pandas as pd
import sqlite3
import time
import inspect
from memory_profiler import memory_usage

def sql_filtering_task():
    wall_start = time.time()
    cpu_start = time.process_time()

    # Step 1: Load CSV into SQLite
    conn = sqlite3.connect("benchmark.db")
    df = pd.read_csv("../birth_gp_ratios.csv")
    df.to_sql("birth_gp_ratios", conn, if_exists="replace", index=False)

    # Step 2: Run SQL filtering query
    query = """
    SELECT *
    FROM birth_gp_ratios
    WHERE
        ratio_type = 'actual'
        AND gp_count IS NOT NULL
        AND actual_births IS NOT NULL
        AND sex = 'persons'
    """
    filtered_df = pd.read_sql_query(query, conn)
    conn.close()

    # Step 3: Save result
    filtered_df.to_csv("filtered_birth_gp_ratios_sql.csv", index=False)

    wall_runtime = round(time.time() - wall_start, 3)
    cpu_runtime = round(time.process_time() - cpu_start, 3)

    print(f"Wall-clock Runtime: {wall_runtime} seconds")
    print(f"CPU Runtime: {cpu_runtime} seconds")
    print(f"Filtered rows: {len(filtered_df)}")

    # Count total and core lines
    lines = inspect.getsource(sql_filtering_task).splitlines()
    total_lines = len(lines)
    core_lines = len([l for l in lines if l.strip() and not l.strip().startswith("#")]) - 3
    print(f"Total Lines of Code: {total_lines}")
    print(f"Core Lines of Code: {core_lines}")

    return wall_runtime

if __name__ == "__main__":
    mem_usage = memory_usage((sql_filtering_task,), max_iterations=1)
    print(f"Memory usage: {round(max(mem_usage) - min(mem_usage), 3)} MB")
