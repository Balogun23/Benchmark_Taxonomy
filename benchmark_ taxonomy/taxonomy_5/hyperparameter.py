import pandas as pd
import time
from memory_profiler import memory_usage
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GridSearchCV
import inspect

def gridsearch_task():
    wall_start = time.time()
    cpu_start = time.process_time()

    df = pd.read_csv("../birth_gp_ratios.csv")
    df = df[(df["ratio_type"] == "actual") & df["actual_births"].notna() & df["gp_count"].notna()]

    median_births = df["actual_births"].median()
    df["high_birth"] = (df["actual_births"] > median_births).astype(int)

    X = df[["gp_count"]]
    y = df["high_birth"]

    model = LogisticRegression()
    grid = GridSearchCV(model, {"C": [0.1, 1, 10]}, cv=3)
    grid.fit(X, y)

    print("Best Params:", grid.best_params_)

    wall_runtime = round(time.time() - wall_start, 3)
    cpu_runtime = round(time.process_time() - cpu_start, 3)

    print(f"\nWall-clock Runtime: {wall_runtime} seconds")
    print(f"CPU Runtime: {cpu_runtime} seconds")

    # Line counts
    lines = inspect.getsource(gridsearch_task).split('\n')
    total_lines = len(lines)
    core_lines = len([line for line in lines if line.strip() and not line.strip().startswith("#")])
    print(f"Total Lines of Code: {total_lines}")
    print(f"Core Lines of Code: {core_lines - 3}")  # exclude def, print, return

    return wall_runtime

if __name__ == "__main__":
    mem_usage = memory_usage((gridsearch_task,), max_iterations=1)
    print(f"Memory usage: {round(max(mem_usage) - min(mem_usage), 3)} MB")
