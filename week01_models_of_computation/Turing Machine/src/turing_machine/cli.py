"""Command-line interface for students."""

from __future__ import annotations

import argparse
import sys
import traceback
from pathlib import Path
import shutil

from . import load_machine
from .errors import TuringMachineError
from .machine import RunResult
from .parser import load_program, validate_program
from .visualize import Visualizer, trace_line


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="tm", description="Run a single-tape Turing Machine")
    parser.add_argument("--debug", action="store_true", help="show Python tracebacks")
    commands = parser.add_subparsers(dest="command", required=True)

    validate = commands.add_parser("validate", help="validate a .tm program")
    validate.add_argument("program", type=Path)
    validate.add_argument("--max-states", type=int)

    run = commands.add_parser("run", help="run a .tm program")
    run.add_argument("program", type=Path)
    run.add_argument("input", nargs="?", default="")
    mode = run.add_mutually_exclusive_group()
    mode.add_argument("--trace", action="store_true")
    mode.add_argument("--visual", action="store_true")
    run.add_argument("--interactive", action="store_true")
    run.add_argument("--delay", type=float, default=0.5)
    run.add_argument("--window", type=int, default=None)
    run.add_argument("--max-steps", type=int, default=10_000)
    run.add_argument("--max-nonblank-cells", type=int)
    run.add_argument("--max-states", type=int)
    run.add_argument("--initial-state", default="q0")
    run.add_argument("--head", type=int, default=0)
    run.add_argument("--input-start", type=int, default=0)
    run.add_argument("--blank", default="_")
    run.add_argument("--break-state", action="append", default=[])
    run.add_argument("--break-step", action="append", type=int, default=[])
    return parser


def _print_result(result: RunResult) -> None:
    print(f"Final tape:   {result.output}")
    print(f"Final state:  {result.final_state}")
    print(f"Steps:        {result.steps}")
    print(f"Status:       {result.status}")


def _run(args: argparse.Namespace) -> int:
    machine = load_machine(
        args.program, blank=args.blank, initial_state=args.initial_state,
        head_position=args.head, max_states=args.max_states,
    )
    machine.reset(
        args.input, initial_state=args.initial_state,
        head_position=args.head, input_start=args.input_start,
    )
    print(f"Initial tape: {args.input}")
    if args.visual or args.interactive or args.break_state or args.break_step:
        Visualizer(args.delay, args.window, args.interactive).run(
            machine,
            max_steps=args.max_steps,
            max_nonblank_cells=args.max_nonblank_cells,
            break_states=set(args.break_state),
            break_steps=set(args.break_step),
        )
        result = machine.result()
    elif args.trace:
        print(trace_line(machine, None, args.window))
        result = machine.run(
            max_steps=args.max_steps,
            max_nonblank_cells=args.max_nonblank_cells,
            on_step=lambda info, current: print(trace_line(current, info, args.window)),
        )
    else:
        result = machine.run(
            max_steps=args.max_steps, max_nonblank_cells=args.max_nonblank_cells
        )
    _print_result(result)
    return 0


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    if args.window is None:
        n = len(args.input)
        size = shutil.get_terminal_size()[0] // 2 - 8
        args.window = min(size, n * 2)
    try:
        if args.command == "validate":
            program = load_program(args.program)
            validate_program(program, max_states=args.max_states)
            print(f"Valid program: {len(program.transitions)} transitions")
            return 0
        return _run(args)
    except (TuringMachineError, OSError, ValueError) as error:
        if args.debug:
            traceback.print_exc()
        else:
            print(f"Error: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
