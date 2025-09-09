import pandas as pd
import sqlite3
from sklearn.cluster import KMeans
from memory_profiler import memory_usage
import time, psutil, os

def sql_clustering_task():
    total_lines = 30
    core_lines = 8  # connect, to_sql, SQL SELECT, KMeans fit, predict, print

    process = psutil.Process(os.getpid())
    cpu_start = process.cpu_times().user
    wall_start = time.time()

    # Load CSV into SQLite
    df = pd.read_csv("../birth_gp_ratios.csv")
    conn = sqlite3.connect("benchmark.db")
    df.to_sql("birth_gp_ratios", conn, if_exists="replace", index=False)

    # Run SQL query to filter valid data
    query = """
    SELECT gp_count, actual_births
    FROM birth_gp_ratios
    WHERE ratio_type = 'actual' AND gp_count IS NOT NULL AND actual_births IS NOT NULL
    """
    data = pd.read_sql_query(query, conn)
    conn.close()

    # KMeans clustering
    kmeans = KMeans(n_clusters=3, random_state=42)
    data["cluster"] = kmeans.fit_predict(data[["gp_count", "actual_births"]])

    print("Cluster centers:\n", kmeans.cluster_centers_)

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
    mem = memory_usage((sql_clustering_task,), max_iterations=1)
    print(f"Memory usage: {round(max(mem) - min(mem), 3)} MB")
