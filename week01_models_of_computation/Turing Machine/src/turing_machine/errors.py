"""Exceptions raised by the emulator."""


class TuringMachineError(Exception):
    """Base class for errors that are safe to show to students."""


class ProgramSyntaxError(TuringMachineError):
    """A transition line cannot be parsed."""


class DuplicateTransitionError(ProgramSyntaxError):
    """Two rules handle the same state and symbol."""


class InvalidMoveError(ProgramSyntaxError):
    """A rule contains an unsupported head movement."""


class MissingTransitionError(TuringMachineError):
    """The running machine has no applicable transition."""

    def __init__(self, state: str, symbol: str, step: int, head: int) -> None:
        super().__init__(
            "No transition defined for:\n"
            f"state = {state}\nsymbol = {symbol}\nstep = {step}\nhead = {head}"
        )


class StepLimitExceededError(TuringMachineError):
    """The configured execution step limit was reached."""


class ResourceLimitExceededError(TuringMachineError):
    """A configured memory/program resource limit was exceeded."""


class InvalidInputAlphabetError(TuringMachineError):
    """Input or program symbols are outside the allowed alphabet."""

