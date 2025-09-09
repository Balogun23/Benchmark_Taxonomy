import pandas as pd
import matplotlib.pyplot as plt
from memory_profiler import memory_usage
import time
import inspect

def plot_histogram():
    wall_start = time.time()
    cpu_start = time.process_time()

    df = pd.read_csv("../birth_gp_ratios.csv")
    df["actual_births"].hist(bins=20)
    plt.title("Distribution of Actual Births")
    plt.xlabel("Actual Births")
    plt.ylabel("Frequency")
    plt.tight_layout()
    plt.savefig("actual_births_histogram.png")

    wall_end = time.time()
    cpu_end = time.process_time()

    wall_runtime = round(wall_end - wall_start, 3)
    cpu_runtime = round(cpu_end - cpu_start, 3)

    print("Histogram saved.")
    print(f"Runtime (Wall Clock): {wall_runtime} seconds")
    print(f"CPU Runtime: {cpu_runtime} seconds")

    # Code metrics
    source_lines = inspect.getsource(plot_histogram).split('\n')
    total_lines = len(source_lines)
    core_lines = len([line for line in source_lines if line.strip() and not line.strip().startswith("#")])
    print(f"Total Lines of Code: {total_lines}")
    print(f"Core Lines of Code: {core_lines - 3}")  # Exclude def + return + print

    return wall_runtime

if __name__ == "__main__":
    mem = memory_usage((plot_histogram,), max_iterations=1)
    print(f"Memory Usage: {round(max(mem) - min(mem), 3)} MB")
