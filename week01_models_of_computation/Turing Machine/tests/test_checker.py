from pathlib import Path

from turing_machine import check_solution

EXAMPLES = Path(__file__).parents[1] / "examples"


def test_checker_passes_binary_increment_cases():
    report = check_solution(
        (EXAMPLES / "binary_increment.tm").read_text(),
        [("0", "1"), ("1", "10"), ("10", "11"), ("11", "100"), ("1011", "1100")],
    )
    assert report.passed
    assert all(test.error is None for test in report.tests)


def test_checker_distinguishes_failures():
    wrong = check_solution("q0 0 -> 0 S REJECT", [("0", "1")])
    assert wrong.tests[0].error_type == "wrong_output"
    state = check_solution(
        "q0 0 -> 1 S REJECT", [("0", "1")], expected_final_state="ACCEPT"
    )
    assert state.tests[0].error_type == "incorrect_final_state"
    missing = check_solution("q0 0 -> 0 S HALT", [("1", "1")])
    assert missing.tests[0].error_type == "missing_transition"
    looping = check_solution("q0 0 -> 0 S q0", [("0", "0")], max_steps=1)
    assert looping.tests[0].error_type == "step_limit_exceeded"
    invalid = check_solution("not a transition", [("0", "1")])
    assert invalid.tests[0].error_type == "invalid_program"
