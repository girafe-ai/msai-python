from turing_machine.machine import TuringMachine
from turing_machine.parser import parse_program
from turing_machine.visualize import Visualizer


def test_visualization_shows_previous_above_tape_and_next_below_it():
    machine = TuringMachine(
        parse_program("q0 0 -> 1 R q1\nq1 0 -> 0 S HALT")
    )
    machine.reset("00")
    visualizer = Visualizer(width=5)

    initial = visualizer._plain(machine, None)
    assert initial.index("Previous transition: none") < initial.index("[0]")
    assert initial.index("[0]") < initial.index("Next transition: q0 0 -> 1 R q1")

    previous = machine.step()
    frame = visualizer._plain(machine, previous)
    assert frame.index("Previous transition: q0 0 -> 1 R q1") < frame.index("[0]")
    assert frame.index("[0]") < frame.index("Next transition: q1 0 -> 0 S HALT")


def test_terminal_frame_has_no_next_transition():
    machine = TuringMachine(parse_program("q0 0 -> 1 S HALT"))
    machine.reset("0")
    previous = machine.step()
    frame = Visualizer()._plain(machine, previous)
    assert "Previous transition: q0 0 -> 1 S HALT" in frame
    assert "Next transition: none (terminal state)" in frame
