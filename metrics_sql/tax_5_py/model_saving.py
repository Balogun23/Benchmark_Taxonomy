import pandas as pd
import sqlite3
import time
from sklearn.linear_model import LogisticRegression
import joblib
import psutil
import os
from memory_profiler import memory_usage

def sql_model_saving_task():
    total_lines = 24
    core_lines = 6  # connect, to_sql, read_sql, model creation, save, load

    process = psutil.Process(os.getpid())
    cpu_start = process.cpu_times().user
    wall_start = time.time()

    # Step 1: Simulate data pull using SQLite
    df = pd.read_csv("../birth_gp_ratios.csv")
    conn = sqlite3.connect("benchmark.db")
    df.to_sql("birth_gp_ratios", conn, if_exists="replace", index=False)

    query = "SELECT gp_count, actual_births FROM birth_gp_ratios WHERE ratio_type = 'actual'"
    dummy = pd.read_sql_query(query, conn)
    conn.close()

    # Step 2: Save and reload model
    model = LogisticRegression()
    joblib.dump(model, "logistic_model_sql.pkl")
    loaded_model = joblib.load("logistic_model_sql.pkl")

    print("Model saved and reloaded successfully.")

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
    mem = memory_usage((sql_model_saving_task,), max_iterations=1)
    print(f"Memory usage: {round(max(mem) - min(mem), 3)} MB")
