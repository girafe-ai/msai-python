"""Sparse, unbounded tape representation."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Tape:
    blank: str = "_"
    _cells: dict[int, str] = field(default_factory=dict, repr=False)

    def __post_init__(self) -> None:
        if len(self.blank) != 1:
            raise ValueError("blank symbol must be exactly one character")
        self._cells = {position: value for position, value in self._cells.items() if value != self.blank}

    @classmethod
    def from_string(cls, data: str, *, blank: str = "_", start: int = 0) -> Tape:
        tape = cls(blank=blank)
        for offset, symbol in enumerate(data):
            tape.write(start + offset, symbol)
        return tape

    def read(self, position: int) -> str:
        return self._cells.get(position, self.blank)

    def write(self, position: int, symbol: str) -> None:
        if len(symbol) != 1:
            raise ValueError("tape symbols must be exactly one character")
        if symbol == self.blank:
            self._cells.pop(position, None)
        else:
            self._cells[position] = symbol

    @property
    def nonblank_count(self) -> int:
        return len(self._cells)

    def bounds(self) -> tuple[int, int] | None:
        if not self._cells:
            return None
        return min(self._cells), max(self._cells)

    def interval(self) -> tuple[int, str]:
        """Return (left position, complete non-blank-spanning contents)."""
        bounds = self.bounds()
        if bounds is None:
            return 0, ""
        left, right = bounds
        return left, "".join(self.read(position) for position in range(left, right + 1))

    def normalized(self) -> str:
        return self.interval()[1]

    def snapshot(self) -> dict[int, str]:
        return dict(self._cells)

