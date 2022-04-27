import time
from dataclasses import dataclass
from datetime import datetime


@dataclass
class Log:
    lat: float
    lon: float
    timestamp: float = None

    def __post_init__(self):
        self.timestamp = self.timestamp or time.time()


class Printer:
    def print(self, log):
        dt = datetime.fromtimestamp(log.timestamp).strftime('%Y/%m/%d %H:%M:%S')
        print(f'User was at ({log.lat}, {log.lon}) at {dt}')


class Tracker:
    def __init__(self):
        self.db: list[Log] = []

    def track(self, log: Log):
        self.db.append(log)
        Printer().print(log)
