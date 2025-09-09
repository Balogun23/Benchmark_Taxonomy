import time
from memory_profiler import memory_usage
from sklearn.linear_model import LogisticRegression
import joblib
import inspect

def model_saving_task():
    wall_start = time.time()
    cpu_start = time.process_time()
    
    model = LogisticRegression()
    joblib.dump(model, "logistic_model.pkl")
    loaded = joblib.load("logistic_model.pkl")

    print("Model saved and reloaded successfully.")
    
    wall_runtime = round(time.time() - wall_start, 3)
    cpu_runtime = round(time.process_time() - cpu_start, 3)
    
    print(f"\nWall-clock Runtime: {wall_runtime} seconds")
    print(f"CPU Runtime: {cpu_runtime} seconds")

    lines = inspect.getsource(model_saving_task).split('\n')
    total_lines = len(lines)
    core_lines = len([line for line in lines if line.strip() and not line.strip().startswith("#")])
    print(f"Total Lines of Code: {total_lines}")
    print(f"Core Lines of Code: {core_lines - 3}")  # exclude def, print, return

    return wall_runtime

if __name__ == "__main__":
    mem_usage = memory_usage((model_saving_task,), max_iterations=1)
    print(f"Memory usage: {round(max(mem_usage) - min(mem_usage), 3)} MB")
