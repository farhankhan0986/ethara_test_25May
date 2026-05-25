from collections import deque
import time

class RollingVWAP:

    def __init__(self, window_seconds=60):

        self.window_seconds = window_seconds
        self.trades = deque()

        self.total_pv = 0.0
        self.total_volume = 0

    def update(self, price, volume):

        now = time.time()

        self.trades.append((now, price, volume))

        self.total_pv += price * volume
        self.total_volume += volume

        self._evict_old(now)

    def _evict_old(self, now):

        while self.trades:

            ts, price, volume = self.trades[0]

            if now - ts <= self.window_seconds:
                break

            self.trades.popleft()

            self.total_pv -= price * volume
            self.total_volume -= volume

    def value(self):

        if self.total_volume == 0:
            return 0.0

        return self.total_pv / self.total_volume