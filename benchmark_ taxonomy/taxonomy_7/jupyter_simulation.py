import pandas as pd
import matplotlib.pyplot as plt
import time, inspect
from memory_profiler import memory_usage

def jupyter_simulation():
    wall_start = time.time()
    cpu_start = time.process_time()

    df = pd.read_csv("../birth_gp_ratios.csv")
    summary = df.describe()

    print("Descriptive Summary:")
    print(summary)

    plt.hist(df["actual_births"].dropna(), bins=30)
    plt.title("Birth Distribution")
    plt.tight_layout()
    plt.savefig("jupyter_hist.png")
    plt.close()

    wall_runtime = round(time.time() - wall_start, 3)
    cpu_runtime = round(time.process_time() - cpu_start, 3)

    print("Printed stats and saved chart as if in notebook.")
    print(f"Wall-clock Runtime: {wall_runtime} seconds")
    print(f"CPU Runtime: {cpu_runtime} seconds")
    print(f"Total Lines of Code: {len(inspect.getsource(jupyter_simulation).splitlines())}")
    logic_lines = [l for l in inspect.getsource(jupyter_simulation).splitlines() if l.strip() and not l.strip().startswith("#")]
    print(f"Core Lines of Code: {len(logic_lines) - 3}")

    return wall_runtime

if __name__ == "__main__":
    mem = memory_usage((jupyter_simulation,), max_iterations=1)
    print(f"Memory usage: {round(max(mem) - min(mem), 3)} MB")
