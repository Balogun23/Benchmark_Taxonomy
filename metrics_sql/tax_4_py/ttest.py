import pandas as pd
import sqlite3
from scipy.stats import ttest_ind
import time
import psutil
import os
from memory_profiler import memory_usage

def sql_t_test_task():
    total_lines = 27
    core_lines = 7  # connect, to_sql, SQL SELECTs, read_sqls, t-test, print result

    process = psutil.Process(os.getpid())
    cpu_start = process.cpu_times().user
    wall_start = time.time()

    # Load dataset and insert into SQLite
    df = pd.read_csv("../birth_gp_ratios.csv")
    conn = sqlite3.connect("benchmark.db")
    df.to_sql("birth_gp_ratios", conn, if_exists="replace", index=False)

    # Extract data for 2015 and 2016 where ratio_type is 'actual'
    query_2015 = """
    SELECT actual_births FROM birth_gp_ratios
    WHERE ratio_type = 'actual' AND date = 2015 AND actual_births IS NOT NULL
    """
    query_2016 = """
    SELECT actual_births FROM birth_gp_ratios
    WHERE ratio_type = 'actual' AND date = 2016 AND actual_births IS NOT NULL
    """

    group1 = pd.read_sql_query(query_2015, conn)["actual_births"]
    group2 = pd.read_sql_query(query_2016, conn)["actual_births"]
    conn.close()

    if len(group1) > 1 and len(group2) > 1:
        t_stat, p_val = ttest_ind(group1, group2, equal_var=False)
        print(f"T-statistic: {t_stat:.3f}")
        print(f"P-value: {p_val:.5f}")
    else:
        print("Not enough data to perform t-test.")

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
    mem_usage = memory_usage((sql_t_test_task,), max_iterations=1)
    print(f"Memory Usage: {round(max(mem_usage) - min(mem_usage), 3)} MB")
