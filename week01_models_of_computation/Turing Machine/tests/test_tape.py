from turing_machine.tape import Tape


def test_tape_extends_left_and_right_and_removes_blanks():
    tape = Tape()
    tape.write(-100, "L")
    tape.write(100, "R")
    assert tape.read(-100) == "L"
    assert tape.read(99) == "_"
    assert tape.interval() == (-100, "L" + "_" * 199 + "R")
    tape.write(-100, "_")
    assert tape.nonblank_count == 1


def test_normalization_keeps_internal_blanks():
    tape = Tape.from_string("_1_0__", start=-2)
    assert tape.normalized() == "1_0"
    assert tape.interval() == (-1, "1_0")

