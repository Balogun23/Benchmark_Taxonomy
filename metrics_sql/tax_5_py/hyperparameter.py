import pandas as pd
import sqlite3
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GridSearchCV
from memory_profiler import memory_usage
import time, psutil, os

def sql_gridsearch_task():
    total_lines = 28
    core_lines = 8  # connect, to_sql, SQL SELECT, GridSearchCV, fit, print

    process = psutil.Process(os.getpid())
    cpu_start = process.cpu_times().user
    wall_start = time.time()

    # Load data into SQLite
    df = pd.read_csv("../birth_gp_ratios.csv")
    conn = sqlite3.connect("benchmark.db")
    df.to_sql("birth_gp_ratios", conn, if_exists="replace", index=False)

    # SQL: filter relevant rows
    query = """
    SELECT gp_count, actual_births
    FROM birth_gp_ratios
    WHERE ratio_type = 'actual' AND gp_count IS NOT NULL AND actual_births IS NOT NULL
    """
    data = pd.read_sql_query(query, conn)
    conn.close()

    # Binary target creation
    median_births = data["actual_births"].median()
    data["high_birth"] = (data["actual_births"] > median_births).astype(int)

    X = data[["gp_count"]]
    y = data["high_birth"]

    # Grid search for logistic regression
    model = LogisticRegression()
    grid = GridSearchCV(model, {"C": [0.1, 1, 10]}, cv=3)
    grid.fit(X, y)

    print("Best Params:", grid.best_params_)

    wall_end = time.time()
    cpu_end = process.cpu_times().user

    runtime = round(wall_end - wall_start, 3)
    cpu_runtime = round(cpu_end - cpu_start, 3)

    print(f"\nRuntime (wall-clock): {runtime} seconds")
    print(f"CPU Runtime: {cpu_runtime} seconds")
    print(f"Total Lines of Code: {total_lines}")
    print(f"Core Lines of Code: {core_lines}")

    return runtime, cpu_runtime, total_lines, core_lines

if __name__ == "__main__":
    mem = memory_usage((sql_gridsearch_task,), max_iterations=1)
    print(f"Memory usage: {round(max(mem) - min(mem), 3)} MB")
