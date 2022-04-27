"""
In previous examples Dependency Inversion Principle was violated - Tracker depended on specific printer.

That is also bad, because to replace printer we need to modify Tracker.

Here is the problem solution - Tracker now depends on abstract printer and we can change it outside the Tracker.
"""

import time
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Log:
    lat: float
    lon: float
    timestamp: float = field(default_factory=time.time)


class BasePrinter(ABC):
    @abstractmethod
    def print(self, log):
        ...


class HumanReadablePrinter(BasePrinter, ABC):
    @staticmethod
    def _get_str(log: Log):
        dt = datetime.fromtimestamp(log.timestamp).strftime('%Y/%m/%d %H:%M:%S')
        return f'User was at ({log.lat}, {log.lon}) at {dt}'


class ConsolePrinter(HumanReadablePrinter):
    def print(self, log: Log):
        print(self._get_str(log))


class FilePrinter(HumanReadablePrinter):
    def print(self, log: Log):
        with open('test.txt', 'a') as f:
            f.write(self._get_str(log))
            f.write('\n')


class Tracker:
    def __init__(self, printer: BasePrinter = None):
        self.db: list[Log] = []
        self.printer = printer or ConsolePrinter()

    def track(self, log: Log):
        self.db.append(log)
        self.printer.print(log)
