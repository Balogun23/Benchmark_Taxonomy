import pandas as pd
from sklearn.cluster import KMeans
from memory_profiler import memory_usage
import time, inspect

def clustering_task():
    wall_start = time.time()
    cpu_start = time.process_time()

    df = pd.read_csv("../birth_gp_ratios.csv")
    df = df[(df["ratio_type"] == "actual") & df["actual_births"].notna() & df["gp_count"].notna()]
    X = df[["gp_count", "actual_births"]]

    kmeans = KMeans(n_clusters=3, random_state=42)
    df["cluster"] = kmeans.fit_predict(X)

    print("Cluster centers:\n", kmeans.cluster_centers_)

    wall_end = time.time()
    cpu_end = time.process_time()
    wall_runtime = round(wall_end - wall_start, 3)
    cpu_runtime = round(cpu_end - cpu_start, 3)

    print(f"\nRuntime (Wall Clock): {wall_runtime} seconds")
    print(f"CPU Runtime: {cpu_runtime} seconds")

    # Count code lines
    lines = inspect.getsource(clustering_task).split('\n')
    total_lines = len(lines)
    core_lines = len([line for line in lines if line.strip() and not line.strip().startswith("#")])
    print(f"Total Lines of Code: {total_lines}")
    print(f"Core Lines of Code: {core_lines - 3}")  # Exclude def/print/return

    return wall_runtime

if __name__ == "__main__":
    mem_usage = memory_usage((clustering_task,), max_iterations=1)
    print(f"Memory usage: {round(max(mem_usage) - min(mem_usage), 3)} MB")
