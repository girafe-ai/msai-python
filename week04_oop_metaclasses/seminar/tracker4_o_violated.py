"""
Let's have to types of output for printing - to console or to file.

Here is implementation that violates Open-close principle (what if you want to add 3rd output?).
"""

import time
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Log:
    lat: float
    lon: float
    timestamp: float = field(default_factory=time.time)


class Printer:
    def _get_str(self, log):
        dt = datetime.fromtimestamp(log.timestamp).strftime('%Y/%m/%d %H:%M:%S')
        return f'User was at ({log.lat}, {log.lon}) at {dt}'

    def print_to_console(self, log):
        print(self._get_str(log))

    def print_to_file(self, log):
        with open('test.txt', 'a') as f:
            f.write(self._get_str(log))
            f.write('\n')


class Tracker:
    def __init__(self):
        self.db: list[Log] = []

    def track(self, log: Log):
        self.db.append(log)
        Printer().print_to_console(log)
