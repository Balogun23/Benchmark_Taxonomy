import joblib, time, inspect
from sklearn.linear_model import LogisticRegression
from memory_profiler import memory_usage

def model_save_task():
    wall_start = time.time()
    cpu_start = time.process_time()

    model = LogisticRegression()
    joblib.dump(model, "saved_model.pkl")
    _ = joblib.load("saved_model.pkl")

    wall_runtime = round(time.time() - wall_start, 3)
    cpu_runtime = round(time.process_time() - cpu_start, 3)

    print("Model saved and reloaded.")
    print(f"Wall-clock Runtime: {wall_runtime} seconds")
    print(f"CPU Runtime: {cpu_runtime} seconds")
    print(f"Total Lines of Code: {len(inspect.getsource(model_save_task).splitlines())}")
    logic_lines = [l for l in inspect.getsource(model_save_task).splitlines() if l.strip() and not l.strip().startswith("#")]
    print(f"Core Lines of Code: {len(logic_lines) - 3}")

    return wall_runtime

def count_lines(func):
    return len([l for l in inspect.getsource(func).split('\n') if l.strip() and not l.strip().startswith("#")]) - 3

if __name__ == "__main__":
    mem = memory_usage((model_save_task,), max_iterations=1)
    print(f"Memory usage: {round(max(mem) - min(mem), 3)} MB")
