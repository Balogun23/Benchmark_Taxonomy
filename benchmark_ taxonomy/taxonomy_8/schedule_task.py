import schedule
import time
from memory_profiler import memory_usage
import inspect

def job():
    print("Running scheduled job...")

def schedule_task():
    wall_start = time.time()
    cpu_start = time.process_time()

    schedule.every(1).seconds.do(job)
    
    for _ in range(3):
        schedule.run_pending()
        time.sleep(1)

    wall_runtime = round(time.time() - wall_start, 3)
    cpu_runtime = round(time.process_time() - cpu_start, 3)

    print(f"Wall-clock Runtime: {wall_runtime} seconds")
    print(f"CPU Runtime: {cpu_runtime} seconds")

    total_lines = len(inspect.getsource(schedule_task).splitlines())
    core_lines = len([l for l in inspect.getsource(schedule_task).splitlines() if l.strip() and not l.strip().startswith("#")]) - 3

    print(f"Total Lines of Code: {total_lines}")
    print(f"Core Lines of Code: {core_lines}")

    return wall_runtime

if __name__ == "__main__":
    mem = memory_usage((schedule_task,), max_iterations=1)
    print(f"Memory usage: {round(max(mem) - min(mem), 3)} MB")
