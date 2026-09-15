"""Terminal-only presentation helpers. The execution engine does not import this module."""

from __future__ import annotations

import sys
import time
from dataclasses import dataclass

from .machine import StepInfo, TuringMachine
from .parser import Transition


def tape_window(machine: TuringMachine, width: int = 9, *, rich: bool = False) -> str:
    width = max(3, width)
    left = machine.head - width // 2
    cells: list[str] = []
    for position in range(left, left + width):
        symbol = machine.tape.read(position)
        if position == machine.head:
            cells.append(f"[reverse]{symbol}[/reverse]" if rich else f"[{symbol}]")
        else:
            cells.append(symbol)
    return "... " + " ".join(cells) + " ..."


def trace_line(machine: TuringMachine, info: StepInfo | None, width: int = 9) -> str:
    transition = ""
    if info is not None:
        transition = (
            f"  read={info.read_symbol} write={info.written_symbol} "
            f"move={info.move} -> {info.state_after}"
        )
    return f"{machine.steps:04d}  {machine.state:<8} {tape_window(machine, width)}{transition}"


def _format_previous_transition(info: StepInfo | None) -> str:
    if info is None:
        return "none (initial state)"
    return (
        f"{info.state_before} {info.read_symbol} -> {info.written_symbol} "
        f"{info.move} {info.state_after}"
    )


def _format_next_transition(machine: TuringMachine) -> str:
    if machine.halted:
        return "none (terminal state)"
    read_symbol = machine.tape.read(machine.head)
    transition: Transition | None = machine.program.transitions.get(
        (machine.state, read_symbol)
    )
    if transition is None:
        return f"undefined for {machine.state} {read_symbol}"
    return (
        f"{transition.state} {transition.read_symbol} -> "
        f"{transition.write_symbol} {transition.move} {transition.next_state}"
    )


@dataclass
class Visualizer:
    delay: float = 0.5
    width: int = 9
    interactive: bool = False

    def _plain(
        self, machine: TuringMachine, info: StepInfo | None, *, rich: bool = False
    ) -> str:
        pointer_indent = 4 + (max(3, self.width) // 2) * 2 + (0 if rich else 1)
        return (
            f"Step {machine.steps}\nState: {machine.state}\n\n"
            f"Previous transition: {_format_previous_transition(info)}\n\n"
            f"{tape_window(machine, self.width, rich=rich)}\n"
            f"{' ' * pointer_indent}▲\n\n"
            f"Next transition: {_format_next_transition(machine)}"
        )

    def run(
        self,
        machine: TuringMachine,
        *,
        max_steps: int | None,
        max_nonblank_cells: int | None = None,
        break_states: set[str] | None = None,
        break_steps: set[int] | None = None,
    ) -> None:
        try:
            from rich.console import Console
            from rich.live import Live
            from rich.panel import Panel
        except ImportError:
            self._run_plain(
                machine, max_steps, max_nonblank_cells, break_states, break_steps
            )
            return

        console = Console()
        running = not self.interactive
        with Live(
            Panel(self._plain(machine, None, rich=True), title="Turing Machine"),
            console=console,
        ) as live:
            while not machine.halted:
                if max_steps is not None and machine.steps >= max_steps:
                    machine.run(max_steps=max_steps)  # raise the core engine's canonical error
                if not running:
                    command = console.input("[Enter]=step, r=run, q=quit > ").strip().lower()
                    if command == "q":
                        return
                    if command == "r":
                        running = True
                info = machine.step(max_nonblank_cells=max_nonblank_cells)
                live.update(
                    Panel(self._plain(machine, info, rich=True), title="Turing Machine"),
                    refresh=True,
                )
                if (break_states and machine.state in break_states) or (
                    break_steps and machine.steps in break_steps
                ):
                    running = False
                if running:
                    time.sleep(max(0.0, self.delay))

    def _run_plain(
        self,
        machine: TuringMachine,
        max_steps: int | None,
        max_nonblank_cells: int | None,
        break_states: set[str] | None,
        break_steps: set[int] | None,
    ) -> None:
        print("rich is not installed; falling back to plain trace.", file=sys.stderr)
        print(self._plain(machine, None))
        while not machine.halted:
            if max_steps is not None and machine.steps >= max_steps:
                machine.run(max_steps=max_steps)
            if self.interactive:
                command = input("[Enter]=step, r=run, q=quit > ").strip().lower()
                if command == "q":
                    return
                if command == "r":
                    self.interactive = False
            info = machine.step(max_nonblank_cells=max_nonblank_cells)
            print("\n" + self._plain(machine, info))
            if (break_states and machine.state in break_states) or (
                break_steps and machine.steps in break_steps
            ):
                self.interactive = True
            if not self.interactive:
                time.sleep(max(0.0, self.delay))
