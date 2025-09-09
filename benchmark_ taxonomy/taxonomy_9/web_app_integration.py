import os, time, threading, psutil, socket
from memory_profiler import memory_usage
import requests

from dash import Dash, html, dcc
import plotly.graph_objs as go

def find_free_port():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]

def create_dash_app():
    app = Dash(__name__)
    app.layout = html.Div([
        html.H1("Benchmark Dashboard"),
        dcc.Graph(
            id="example-graph",
            figure=go.Figure(
                data=[go.Bar(x=["A", "B", "C"], y=[3, 1, 2])],
                layout=go.Layout(title="Simple Bar")
            )
        )
    ])
    return app

def run_dash_server(port: int):
    app = create_dash_app()
    # NOTE: Dash >= 2.17 uses app.run (app.run_server is obsolete)
    app.run(host="127.0.0.1", port=port, debug=False, use_reloader=False)

def benchmark_dashboard():
    """
    Measures:
      - Runtime (wall clock) to boot server + first GET /
      - CPU runtime (user time of current process)
      - Memory delta via memory_profiler
      - Total LOC / Core LOC (manual counts)
      - Bytes of HTML retrieved
    """
    total_lines = 92   # update if you change code
    core_lines  = 28   # thread start, wait loop, GET, metrics

    process = psutil.Process(os.getpid())
    cpu_start = process.cpu_times().user
    wall_start = time.time()

    port = find_free_port()
    base_url = f"http://127.0.0.1:{port}/"

    server_thread = threading.Thread(target=run_dash_server, args=(port,), daemon=True)
    server_thread.start()

    # Wait for server to be ready (max ~12s)
    up = False
    for _ in range(240):  # 240 * 0.05 = 12 seconds
        try:
            r = requests.get(base_url, timeout=0.5)
            if r.status_code == 200:
                up = True
                break
        except Exception:
            pass
        time.sleep(0.05)

    if not up:
        raise RuntimeError("Dash server did not start within timeout. "
                           "Check Windows firewall prompts and that Dash is installed correctly.")

    r = requests.get(base_url, timeout=2)
    status = r.status_code
    html_bytes = len(r.content)

    wall_end = time.time()
    cpu_end = process.cpu_times().user

    runtime = round(wall_end - wall_start, 3)
    cpu_runtime = round(cpu_end - cpu_start, 3)

    return runtime, cpu_runtime, status, html_bytes, total_lines, core_lines

if __name__ == "__main__":
    mem_usage = memory_usage((benchmark_dashboard,), max_iterations=1)
    runtime, cpu_runtime, status, html_bytes, total_lines, core_lines = benchmark_dashboard()

    print(f"Runtime (wall-clock): {runtime} s")
    print(f"CPU Runtime: {cpu_runtime} s")
    print(f"HTTP Status: {status} | HTML Bytes: {html_bytes}")
    print(f"Memory Usage: {round(max(mem_usage) - min(mem_usage), 3)} MB")
    print(f"Total Lines of Code: {total_lines}")
    print(f"Core Lines of Code: {core_lines}")
