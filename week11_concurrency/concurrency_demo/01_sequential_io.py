from time import perf_counter

from common import IO_NAMES, io_task, show_elapsed


def main() -> float:
    print("01 | Sequential waiting")
    started = perf_counter()
    for name in IO_NAMES:
        io_task(name)
    return show_elapsed(started)


if __name__ == "__main__":
    main()
