import pandas as pd
import time, inspect
from memory_profiler import memory_usage

def export_task():
    wall_start = time.time()
    cpu_start = time.process_time()

    df = pd.read_csv("../birth_gp_ratios.csv")
    df_summary = df.groupby("date")["actual_births"].sum().reset_index()
    df_summary.to_csv("summary_export.csv", index=False)
    df_summary.to_excel("summary_export.xlsx", index=False)

    wall_runtime = round(time.time() - wall_start, 3)
    cpu_runtime = round(time.process_time() - cpu_start, 3)

    print("Exported CSV and Excel files.")
    print(f"Wall-clock Runtime: {wall_runtime} seconds")
    print(f"CPU Runtime: {cpu_runtime} seconds")
    print(f"Total Lines of Code: {len(inspect.getsource(export_task).splitlines())}")
    core_lines = [l for l in inspect.getsource(export_task).splitlines() if l.strip() and not l.strip().startswith("#")]
    print(f"Core Lines of Code: {len(core_lines) - 3}")

    return wall_runtime

if __name__ == "__main__":
    mem = memory_usage((export_task,), max_iterations=1)
    print(f"Memory usage: {round(max(mem) - min(mem), 3)} MB")
