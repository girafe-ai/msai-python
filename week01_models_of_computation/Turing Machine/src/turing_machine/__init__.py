"""Public API for the Turing Machine emulator."""

from pathlib import Path
from typing import Iterable

from .checker import CheckReport, TestResult, check_solution
from .machine import RunResult, StepInfo, TuringMachine
from .parser import Program, Transition, parse_program, validate_program


def load_machine(
    path: str | Path,
    *,
    blank: str = "_",
    initial_state: str = "q0",
    head_position: int = 0,
    max_states: int | None = None,
    allowed_symbols: Iterable[str] | None = None,
) -> TuringMachine:
    """Load, validate, and construct a machine from a UTF-8 program file."""
    symbols = tuple(allowed_symbols) if allowed_symbols is not None else None
    text = Path(path).read_text(encoding="utf-8")
    program = validate_program(text, max_states=max_states, allowed_symbols=symbols)
    return TuringMachine(
        program,
        blank=blank,
        initial_state=initial_state,
        head_position=head_position,
        allowed_symbols=symbols,
    )


__all__ = [
    "CheckReport", "Program", "RunResult", "StepInfo", "TestResult", "Transition",
    "TuringMachine", "check_solution", "load_machine", "parse_program", "validate_program",
]
