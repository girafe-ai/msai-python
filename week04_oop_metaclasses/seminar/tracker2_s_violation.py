"""
Single Responsibility violated - Tracker responsible for db storing and for writing.

DB can be replaced with SQL DB. Writer can be replaced with file writer or change formatting.
These are 2 reasons for change.
"""

import time
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Log:
    lat: float
    lon: float
    timestamp: float = field(default_factory=time.time)


class Tracker:
    def __init__(self):
        self.db: list[Log] = []

    def track(self, log: Log):
        self.db.append(log)
        self.print(log)

    def print(self, log: Log):
        dt = datetime.fromtimestamp(log.timestamp).strftime('%Y/%m/%d %H:%M:%S')
        print(f'User was at ({log.lat}, {log.lon}) at {dt}')
