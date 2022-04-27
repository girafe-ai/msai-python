"""
In this example we wanted to add opportunity to specify file for FilePrinter but made it in bad manner.

Liskov Substitution Principle violated here - it is possible to use FilePrinter instead of any BasePrinter,
but to specify filename we have to determine type of printer. So child seems substitutable but it is not.
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
    def print(self, log: Log, filename: str = 'test.txt'):
        with open(filename, 'a') as f:
            f.write(self._get_str(log))
            f.write('\n')


class Tracker:
    def __init__(self, printer: BasePrinter = None):
        self.db: list[Log] = []
        self.printer = printer or ConsolePrinter()

    def track(self, log: Log):
        self.db.append(log)
        if isinstance(self.printer, FilePrinter):
            self.printer.print(log, 'test2.txt')
        else:
            self.printer.print(log)


Tracker(printer=FilePrinter())
