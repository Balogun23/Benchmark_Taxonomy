import pandas as pd
import time
from memory_profiler import memory_usage
import inspect

def safe_task():
    wall_start = time.time()
    cpu_start = time.process_time()

    attempts = 0
    success = False

    while attempts < 3 and not success:
        try:
            df = pd.read_csv("../birth_gp_ratios.csv")
            print("Data loaded successfully.")
            success = True
        except Exception as e:
            print(f"Attempt {attempts+1} failed: {e}")
            attempts += 1
            time.sleep(1)

    wall_runtime = round(time.time() - wall_start, 3)
    cpu_runtime = round(time.process_time() - cpu_start, 3)

    total_lines = len(inspect.getsource(safe_task).splitlines())
    logic_lines = [l for l in inspect.getsource(safe_task).splitlines() if l.strip() and not l.strip().startswith("#")]
    core_lines = len(logic_lines) - 3

    print(f"\nWall-clock Runtime: {wall_runtime} seconds")
    print(f"CPU Runtime: {cpu_runtime} seconds")
    print(f"Total Lines of Code: {total_lines}")
    print(f"Core Lines of Code: {core_lines}")

    return wall_runtime

if __name__ == "__main__":
    mem = memory_usage((safe_task,), max_iterations=1)
    print(f"Memory usage: {round(max(mem) - min(mem), 3)} MB")
