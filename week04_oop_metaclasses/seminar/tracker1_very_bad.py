import time
from datetime import datetime


class Tracker:
    def __init__(self):
        self.db = []

    def track(self, lat: float, lon: float, timestamp: float = None):
        timestamp = timestamp or time.time()
        self.db.append((lat, lon, timestamp))
        self.print(lat, lon, timestamp)

    def print(self, lat: float, lon: float, timestamp: float):
        dt = datetime.fromtimestamp(timestamp).strftime('%Y/%m/%d %H:%M:%S')
        print(f'User was at ({lat}, {lon}) at {dt}')
