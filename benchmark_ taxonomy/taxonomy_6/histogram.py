import pandas as pd
import matplotlib.pyplot as plt
import time, inspect
from memory_profiler import memory_usage

def histogram_task():
    wall_start = time.time()
    cpu_start = time.process_time()

    df = pd.read_csv("../birth_gp_ratios.csv")
    df = df[(df["ratio_type"] == "actual") & df["actual_births"].notna()]

    plt.figure()
    plt.hist(df["actual_births"], bins=20)
    plt.title("Histogram of Actual Births")
    plt.xlabel("Births")
    plt.ylabel("Frequency")
    plt.tight_layout()
    plt.savefig("histogram.png")
    plt.close()

    wall_runtime = round(time.time() - wall_start, 3)
    cpu_runtime = round(time.process_time() - cpu_start, 3)

    print(f"\nWall-clock Runtime: {wall_runtime} seconds")
    print(f"CPU Runtime: {cpu_runtime} seconds")
    print(f"Total Lines of Code: {len(inspect.getsource(histogram_task).splitlines())}")
    core_lines = [l for l in inspect.getsource(histogram_task).splitlines() if l.strip() and not l.strip().startswith("#")]
    print(f"Core Lines of Code: {len(core_lines) - 3}")

    return wall_runtime

if __name__ == "__main__":
    mem = memory_usage((histogram_task,), max_iterations=1)
    print(f"Memory usage: {round(max(mem) - min(mem), 3)} MB")
