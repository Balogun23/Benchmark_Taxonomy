import pandas as pd
import time, inspect
from memory_profiler import memory_usage

def report_task():
    wall_start = time.time()
    cpu_start = time.process_time()

    df = pd.read_csv("../birth_gp_ratios.csv")
    summary = df.describe().to_html()
    
    with open("report.html", "w") as f:
        f.write("<h1>Descriptive Report</h1>")
        f.write(summary)

    wall_runtime = round(time.time() - wall_start, 3)
    cpu_runtime = round(time.process_time() - cpu_start, 3)

    print("HTML report generated.")
    print(f"Wall-clock Runtime: {wall_runtime} seconds")
    print(f"CPU Runtime: {cpu_runtime} seconds")
    print(f"Total Lines of Code: {len(inspect.getsource(report_task).splitlines())}")
    core_lines = [l for l in inspect.getsource(report_task).splitlines() if l.strip() and not l.strip().startswith("#")]
    print(f"Core Lines of Code: {len(core_lines) - 3}")

    return wall_runtime

if __name__ == "__main__":
    mem = memory_usage((report_task,), max_iterations=1)
    print(f"Memory usage: {round(max(mem) - min(mem), 3)} MB")
