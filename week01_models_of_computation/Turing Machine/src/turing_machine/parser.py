"""Parser for the transition-table DSL."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

from .errors import (
    DuplicateTransitionError,
    InvalidInputAlphabetError,
    InvalidMoveError,
    ProgramSyntaxError,
    ResourceLimitExceededError,
)

TERMINAL_STATES = frozenset({"HALT", "ACCEPT", "REJECT"})


@dataclass(frozen=True)
class Transition:
    state: str
    read_symbol: str
    write_symbol: str
    move: str
    next_state: str
    line: int


@dataclass(frozen=True)
class Program:
    transitions: dict[tuple[str, str], Transition]

    @property
    def states(self) -> frozenset[str]:
        result = {transition.state for transition in self.transitions.values()}
        result.update(transition.next_state for transition in self.transitions.values())
        return frozenset(result)


def parse_program(text: str) -> Program:
    transitions: dict[tuple[str, str], Transition] = {}
    for line_number, source_line in enumerate(text.splitlines(), 1):
        line = source_line.split("#", 1)[0].strip()
        if not line:
            continue
        parts = line.split()
        if len(parts) != 6 or parts[2] != "->":
            raise ProgramSyntaxError(
                f"Line {line_number}: expected 'STATE SYMBOL -> SYMBOL MOVE NEXT_STATE'"
            )
        state, read_symbol, _, write_symbol, move, next_state = parts
        if len(read_symbol) != 1 or len(write_symbol) != 1:
            raise ProgramSyntaxError(f"Line {line_number}: tape symbols must be one character")
        if move not in {"L", "R", "S"}:
            raise InvalidMoveError(
                f"Line {line_number}: invalid move {move!r}; expected L, R, or S"
            )
        key = state, read_symbol
        if key in transitions:
            previous = transitions[key]
            raise DuplicateTransitionError(
                f"Line {line_number}: duplicate transition for state {state!r}, "
                f"symbol {read_symbol!r} (first defined on line {previous.line})"
            )
        transitions[key] = Transition(
            state, read_symbol, write_symbol, move, next_state, line_number
        )
    return Program(transitions)


def validate_program(
    program: Program | str,
    *,
    max_states: int | None = None,
    allowed_symbols: Iterable[str] | None = None,
) -> Program:
    parsed = parse_program(program) if isinstance(program, str) else program
    nonterminal_states = parsed.states - TERMINAL_STATES
    if max_states is not None and len(nonterminal_states) > max_states:
        raise ResourceLimitExceededError(
            f"Program uses {len(nonterminal_states)} states; limit is {max_states}"
        )
    if allowed_symbols is not None:
        allowed = set(allowed_symbols)
        invalid = {
            symbol
            for transition in parsed.transitions.values()
            for symbol in (transition.read_symbol, transition.write_symbol)
            if symbol not in allowed
        }
        if invalid:
            raise InvalidInputAlphabetError(
                "Program uses symbols outside the allowed alphabet: "
                + ", ".join(repr(symbol) for symbol in sorted(invalid))
            )
    return parsed


def load_program(path: str | Path, **validation: object) -> Program:
    text = Path(path).read_text(encoding="utf-8")
    return validate_program(text, **validation)

