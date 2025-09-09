import pandas as pd
import time
from memory_profiler import memory_usage
import inspect

def logging_task():
    wall_start = time.time()
    cpu_start = time.process_time()

    start_time = time.strftime("%Y-%m-%d %H:%M:%S")
    print(f"Started at: {start_time}")

    try:
        df = pd.read_csv("../birth_gp_ratios.csv")
        success = True
    except Exception as e:
        print(f"Error: {e}")
        success = False

    wall_end = time.time()
    cpu_end = time.process_time()

    wall_runtime = round(wall_end - wall_start, 3)
    cpu_runtime = round(cpu_end - cpu_start, 3)

    end_time = time.strftime("%Y-%m-%d %H:%M:%S")
    print(f"Ended at: {end_time}")
    print(f"Success: {success}")
    print(f"Wall-clock Runtime: {wall_runtime} seconds")
    print(f"CPU Runtime: {cpu_runtime} seconds")

    total_lines = len(inspect.getsource(logging_task).splitlines())
    logic_lines = [l for l in inspect.getsource(logging_task).splitlines() if l.strip() and not l.strip().startswith("#")]
    core_lines = len(logic_lines) - 3

    print(f"Total Lines of Code: {total_lines}")
    print(f"Core Lines of Code: {core_lines}")

    return wall_runtime

if __name__ == "__main__":
    mem = memory_usage((logging_task,), max_iterations=1)
    print(f"Memory usage: {round(max(mem) - min(mem), 3)} MB")
