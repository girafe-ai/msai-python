from pathlib import Path

import pytest

from turing_machine import load_machine
from turing_machine.errors import (
    InvalidInputAlphabetError,
    MissingTransitionError,
    ResourceLimitExceededError,
    StepLimitExceededError,
)
from turing_machine.machine import TuringMachine
from turing_machine.parser import parse_program

EXAMPLES = Path(__file__).parents[1] / "examples"


def test_step_and_halt():
    machine = TuringMachine(parse_program("q0 0 -> 1 R HALT"))
    machine.reset("0")
    info = machine.step()
    assert (info.step, info.state_before, info.state_after) == (1, "q0", "HALT")
    assert (machine.tape.read(0), machine.head, machine.halted) == ("1", 1, True)


def test_missing_transition_has_context():
    machine = TuringMachine(parse_program("q0 0 -> 0 R q0"))
    with pytest.raises(MissingTransitionError, match=r"state = q0[\s\S]*step = 0"):
        machine.run("1")


def test_step_and_cell_limits():
    loop = TuringMachine(parse_program("q0 _ -> 1 R q0\nq0 1 -> 1 R q0"))
    with pytest.raises(StepLimitExceededError):
        loop.run("", max_steps=2)
    with pytest.raises(ResourceLimitExceededError):
        loop.run("", max_steps=10, max_nonblank_cells=1)


@pytest.mark.parametrize("source, expected", [("1011", "1100"), ("111", "1000")])
def test_binary_increment_example(source, expected):
    result = load_machine(EXAMPLES / "binary_increment.tm").run(source, max_steps=100)
    assert result.halted
    assert result.output == expected


def test_other_examples():
    assert load_machine(EXAMPLES / "invert_bits.tm").run("001101").output == "110010"
    assert load_machine(EXAMPLES / "unary_addition.tm").run("111+11").output == "11111"


def test_input_alphabet_restriction():
    machine = TuringMachine(parse_program("q0 _ -> _ S HALT"), allowed_symbols={"0", "1", "_"})
    with pytest.raises(InvalidInputAlphabetError):
        machine.run("2")

