import pandas as pd
import statsmodels.api as sm
import time
from memory_profiler import memory_usage
import inspect

def full_pipeline():
    wall_start = time.time()
    cpu_start = time.process_time()

    df = pd.read_csv("../birth_gp_ratios.csv")
    df = df[(df["ratio_type"] == "actual") & df["actual_births"].notna() & df["gp_count"].notna()]

    X = sm.add_constant(df["gp_count"])
    y = df["actual_births"]
    model = sm.OLS(y, X).fit()

    df["prediction"] = model.predict(X)
    df[["gss_name", "gp_count", "actual_births", "prediction"]].to_csv("pipeline_report.csv", index=False)

    wall_runtime = round(time.time() - wall_start, 3)
    cpu_runtime = round(time.process_time() - cpu_start, 3)

    print(f"Wall-clock Runtime: {wall_runtime} seconds")
    print(f"CPU Runtime: {cpu_runtime} seconds")

    total_lines = len(inspect.getsource(full_pipeline).splitlines())
    logic_lines = [l for l in inspect.getsource(full_pipeline).splitlines() if l.strip() and not l.strip().startswith("#")]
    core_lines = len(logic_lines) - 3

    print(f"Total Lines of Code: {total_lines}")
    print(f"Core Lines of Code: {core_lines}")

    return wall_runtime

if __name__ == "__main__":
    mem = memory_usage((full_pipeline,), max_iterations=1)
    print(f"Memory usage: {round(max(mem) - min(mem), 3)} MB")
