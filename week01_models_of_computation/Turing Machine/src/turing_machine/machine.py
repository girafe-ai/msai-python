"""The single source of truth for Turing Machine execution semantics."""

from __future__ import annotations

from collections.abc import Callable, Iterable
from dataclasses import dataclass

from .errors import (
    InvalidInputAlphabetError,
    MissingTransitionError,
    ResourceLimitExceededError,
    StepLimitExceededError,
)
from .parser import Program, TERMINAL_STATES
from .tape import Tape


@dataclass(frozen=True)
class StepInfo:
    step: int
    state_before: str
    state_after: str
    head_before: int
    head_after: int
    read_symbol: str
    written_symbol: str
    move: str


@dataclass(frozen=True)
class RunResult:
    halted: bool
    status: str
    final_state: str
    steps: int
    output: str
    tape_start: int
    tape_contents: str
    head: int


class TuringMachine:
    def __init__(
        self,
        program: Program,
        *,
        blank: str = "_",
        initial_state: str = "q0",
        head_position: int = 0,
        allowed_symbols: Iterable[str] | None = None,
    ) -> None:
        self.program = program
        self.blank = blank
        self.default_initial_state = initial_state
        self.default_head_position = head_position
        self.allowed_symbols = frozenset(allowed_symbols) if allowed_symbols is not None else None
        self.reset()

    def reset(
        self,
        input_data: str = "",
        *,
        initial_state: str | None = None,
        head_position: int | None = None,
        input_start: int = 0,
    ) -> None:
        if self.allowed_symbols is not None:
            invalid = set(input_data) - self.allowed_symbols
            if invalid:
                raise InvalidInputAlphabetError(
                    "Input uses symbols outside the allowed alphabet: "
                    + ", ".join(repr(symbol) for symbol in sorted(invalid))
                )
        self.tape = Tape.from_string(input_data, blank=self.blank, start=input_start)
        self.state = initial_state if initial_state is not None else self.default_initial_state
        self.head = head_position if head_position is not None else self.default_head_position
        self.steps = 0
        self.halted = self.state in TERMINAL_STATES

    def step(self, *, max_nonblank_cells: int | None = None) -> StepInfo:
        if self.halted:
            raise RuntimeError(f"Machine is already halted in state {self.state}")
        state_before = self.state
        head_before = self.head
        read_symbol = self.tape.read(self.head)
        transition = self.program.transitions.get((self.state, read_symbol))
        if transition is None:
            raise MissingTransitionError(self.state, read_symbol, self.steps, self.head)

        self.tape.write(self.head, transition.write_symbol)
        if max_nonblank_cells is not None and self.tape.nonblank_count > max_nonblank_cells:
            raise ResourceLimitExceededError(
                f"Non-blank tape cells exceed limit {max_nonblank_cells} at step {self.steps + 1}"
            )
        self.head += {"L": -1, "R": 1, "S": 0}[transition.move]
        self.state = transition.next_state
        self.steps += 1
        self.halted = self.state in TERMINAL_STATES
        return StepInfo(
            self.steps,
            state_before,
            self.state,
            head_before,
            self.head,
            read_symbol,
            transition.write_symbol,
            transition.move,
        )

    def result(self) -> RunResult:
        start, contents = self.tape.interval()
        status = self.state.lower() if self.state in {"ACCEPT", "REJECT"} else (
            "halted" if self.halted else "running"
        )
        return RunResult(
            self.halted, status, self.state, self.steps, self.tape.normalized(),
            start, contents, self.head,
        )

    def run(
        self,
        input_data: str | None = None,
        *,
        initial_state: str | None = None,
        head_position: int | None = None,
        input_start: int = 0,
        max_steps: int | None = None,
        max_nonblank_cells: int | None = None,
        on_step: Callable[[StepInfo, TuringMachine], None] | None = None,
    ) -> RunResult:
        if input_data is not None:
            self.reset(
                input_data,
                initial_state=initial_state,
                head_position=head_position,
                input_start=input_start,
            )
        elif initial_state is not None or head_position is not None or input_start != 0:
            raise ValueError("input_data is required when overriding initial configuration")
        if max_nonblank_cells is not None and self.tape.nonblank_count > max_nonblank_cells:
            raise ResourceLimitExceededError(
                f"Initial tape has {self.tape.nonblank_count} non-blank cells; "
                f"limit is {max_nonblank_cells}"
            )
        while not self.halted:
            if max_steps is not None and self.steps >= max_steps:
                raise StepLimitExceededError(
                    f"Step limit {max_steps} exceeded in state {self.state!r} "
                    f"at head position {self.head}"
                )
            info = self.step(max_nonblank_cells=max_nonblank_cells)
            if on_step is not None:
                on_step(info, self)
        return self.result()
