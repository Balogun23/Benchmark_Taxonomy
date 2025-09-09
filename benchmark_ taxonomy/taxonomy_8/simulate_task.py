import time
from memory_profiler import memory_usage
import inspect

def simulate_dag():
    wall_start = time.time()
    cpu_start = time.process_time()

    tasks = ["Extract", "Clean", "Model", "Report"]
    for t in tasks:
        print(f"{t} → ", end='')
        time.sleep(0.5)
    print("Done")

    wall_runtime = round(time.time() - wall_start, 3)
    cpu_runtime = round(time.process_time() - cpu_start, 3)

    print(f"Wall-clock Runtime: {wall_runtime} seconds")
    print(f"CPU Runtime: {cpu_runtime} seconds")

    total_lines = len(inspect.getsource(simulate_dag).splitlines())
    core_lines = len([l for l in inspect.getsource(simulate_dag).splitlines() if l.strip() and not l.strip().startswith("#")]) - 3

    print(f"Total Lines of Code: {total_lines}")
    print(f"Core Lines of Code: {core_lines}")

    return wall_runtime

if __name__ == "__main__":
    mem = memory_usage((simulate_dag,), max_iterations=1)
    print(f"Memory usage: {round(max(mem) - min(mem), 3)} MB")
