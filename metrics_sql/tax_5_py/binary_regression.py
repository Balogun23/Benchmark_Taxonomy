import pandas as pd
import sqlite3
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix
from memory_profiler import memory_usage
import time, psutil, os

def sql_logistic_task():
    total_lines = 34
    core_lines = 9  # connect, to_sql, query, preprocessing, model fit/predict, evaluation

    process = psutil.Process(os.getpid())
    cpu_start = process.cpu_times().user
    wall_start = time.time()

    # Load data and save to SQLite
    df = pd.read_csv("../birth_gp_ratios.csv")
    conn = sqlite3.connect("benchmark.db")
    df.to_sql("birth_gp_ratios", conn, if_exists="replace", index=False)

    # Query valid data
    query = """
    SELECT gp_count, actual_births
    FROM birth_gp_ratios
    WHERE ratio_type = 'actual' AND actual_births IS NOT NULL AND gp_count IS NOT NULL
    """
    data = pd.read_sql_query(query, conn)
    conn.close()

    # Binary target creation
    median_births = data["actual_births"].median()
    data["high_birth"] = (data["actual_births"] > median_births).astype(int)

    X = data[["gp_count"]]
    y = data["high_birth"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=42)

    model = LogisticRegression()
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    print("Accuracy:", accuracy_score(y_test, y_pred))
    print("Confusion Matrix:\n", confusion_matrix(y_test, y_pred))

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
    mem_usage = memory_usage((sql_logistic_task,), max_iterations=1)
    print(f"Memory usage: {round(max(mem_usage) - min(mem_usage), 3)} MB")
