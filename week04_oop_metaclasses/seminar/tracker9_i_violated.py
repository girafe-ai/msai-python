"""
Example of Interface Segregation Principle violation.

If you want to have multiple outputs at once, it is better to create new Printer using Facade OOP pattern.
Instead, there is Printer with combined interfaces which is not convenient in use.
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


class ConsoleOrFilePrinter(BasePrinter):
    def __init__(self, use_console: bool = True, use_file: bool = True, filename: str = 'test.txt'):
        self.use_console = use_console
        self.use_file = use_file
        self.filename = filename

    @staticmethod
    def _get_str(log: Log):
        dt = datetime.fromtimestamp(log.timestamp).strftime('%Y/%m/%d %H:%M:%S')
        return f'User was at ({log.lat}, {log.lon}) at {dt}'

    def print(self, log: Log):
        if self.use_console:
            print(self._get_str(log))
        if self.use_file:
            with open(self.filename, 'a') as f:
                f.write(self._get_str(log))
                f.write('\n')


class Tracker:
    def __init__(self, printer: BasePrinter = None):
        self.db: list[Log] = []
        self.printer = printer or ConsoleOrFilePrinter(use_file=False)

    def track(self, log: Log):
        self.db.append(log)
        self.printer.print(log)


Tracker(printer=ConsoleOrFilePrinter(filename='test2.txt'))
