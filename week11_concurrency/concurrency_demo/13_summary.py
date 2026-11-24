from contextlib import redirect_stdout
from importlib import import_module
from io import StringIO
from time import perf_counter

from common import show_elapsed

EXPERIMENTS = (
    ("Waiting", "Sequential", "01_sequential_io"),
    ("Waiting", "Threads", "02_threads_io"),
    ("Waiting", "Asyncio", "11_async_concurrent"),
    ("CPU", "Sequential", "06_cpu_sequential"),
    ("CPU", "Threads", "07_cpu_threads"),
    ("CPU", "Processes", "08_cpu_processes"),
)


def main() -> None:
    print("13 | Measured timing comparison")
    print("Running six experiments. The CPU process timing includes pool startup and shutdown.")
    started = perf_counter()
    print(f"\n{'Workload':<12} {'Model':<14} {'Time':>9}", flush=True)
    print("-" * 37)
    for workload, model, module_name in EXPERIMENTS:
        # Numbered filenames can be loaded by string through importlib.
        experiment = import_module(module_name)
        with redirect_stdout(StringIO()):
            elapsed = experiment.main()
        print(f"{workload:<12} {model:<14} {elapsed:8.3f}s", flush=True)

    print("\nRule of thumb")
    print("Blocking I/O        -> threads")
    print("Pure-Python CPU     -> processes when work outweighs overhead")
    print("Async-friendly I/O  -> asyncio")
    show_elapsed(started)


if __name__ == "__main__":
    main()
