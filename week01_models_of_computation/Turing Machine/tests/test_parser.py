import pytest

from turing_machine.errors import DuplicateTransitionError, InvalidMoveError
from turing_machine.parser import parse_program, validate_program
from turing_machine.errors import InvalidInputAlphabetError, ResourceLimitExceededError


def test_parses_valid_program_comments_and_whitespace():
    program = parse_program("""
        # comment
        q0 0 -> 1 R q1  # inline comment

        q1 _ -> _ S HALT
    """)
    assert program.transitions[("q0", "0")].next_state == "q1"
    assert len(program.transitions) == 2


def test_duplicate_transition():
    with pytest.raises(DuplicateTransitionError, match="first defined on line"):
        parse_program("q0 0 -> 0 R q0\nq0 0 -> 1 S HALT")


def test_invalid_direction():
    with pytest.raises(InvalidMoveError, match="invalid move"):
        parse_program("q0 0 -> 0 X q0")


def test_validation_limits_states_and_alphabet():
    with pytest.raises(ResourceLimitExceededError):
        validate_program("q0 0 -> 0 R q1", max_states=1)
    with pytest.raises(InvalidInputAlphabetError):
        validate_program("q0 x -> x S HALT", allowed_symbols={"0", "_"})

