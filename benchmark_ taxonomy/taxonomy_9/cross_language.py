import time, os, psutil, sqlite3
from memory_profiler import memory_usage

def benchmark_cross_lang():
    total_lines, core_lines = 23, 9
    process = psutil.Process(os.getpid())
    cpu_start, wall_start = process.cpu_times().user, time.time()

    conn = sqlite3.connect(":memory:")
    cur = conn.cursor()
    cur.execute("CREATE TABLE numbers (id INTEGER)")
    cur.executemany("INSERT INTO numbers VALUES (?)", [(i,) for i in range(100)])
    conn.commit()

    # Run SQL query inside Python
    cur.execute("SELECT SUM(id) FROM numbers")
    total = cur.fetchone()[0]

    wall_end, cpu_end = time.time(), process.cpu_times().user
    runtime, cpu_runtime = round(wall_end - wall_start, 3), round(cpu_end - cpu_start, 3)
    return runtime, cpu_runtime, total, total_lines, core_lines

if __name__ == "__main__":
    mem_usage = memory_usage((benchmark_cross_lang,), max_iterations=1)
    runtime, cpu_runtime, total, total_lines, core_lines = benchmark_cross_lang()
    print(f"Runtime: {runtime}s | CPU Runtime: {cpu_runtime}s | Sum: {total}")
    print(f"Memory Usage: {round(max(mem_usage)-min(mem_usage),3)} MB")
    print(f"Total LOC: {total_lines} | Core LOC: {core_lines}")
