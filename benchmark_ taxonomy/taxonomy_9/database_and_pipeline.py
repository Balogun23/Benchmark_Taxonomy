import time, os, psutil, sqlite3
from memory_profiler import memory_usage

def benchmark_db_pipeline():
    total_lines, core_lines = 22, 8
    process = psutil.Process(os.getpid())
    cpu_start, wall_start = process.cpu_times().user, time.time()

    conn = sqlite3.connect(":memory:")
    cur = conn.cursor()
    cur.execute("CREATE TABLE test (id INTEGER, name TEXT)")
    cur.executemany("INSERT INTO test VALUES (?,?)", [(i, f"Name_{i}") for i in range(1000)])
    conn.commit()

    # Query
    cur.execute("SELECT COUNT(*) FROM test")
    count = cur.fetchone()[0]

    wall_end, cpu_end = time.time(), process.cpu_times().user
    runtime, cpu_runtime = round(wall_end - wall_start, 3), round(cpu_end - cpu_start, 3)
    return runtime, cpu_runtime, count, total_lines, core_lines

if __name__ == "__main__":
    mem_usage = memory_usage((benchmark_db_pipeline,), max_iterations=1)
    runtime, cpu_runtime, count, total_lines, core_lines = benchmark_db_pipeline()
    print(f"Runtime: {runtime}s | CPU Runtime: {cpu_runtime}s | Rows: {count}")
    print(f"Memory Usage: {round(max(mem_usage)-min(mem_usage),3)} MB")
    print(f"Total LOC: {total_lines} | Core LOC: {core_lines}")
