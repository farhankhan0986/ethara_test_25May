from collections import deque

class LatencyMonitor:

    def __init__(self, threshold_ms, breach_limit):

        self.threshold_ms = threshold_ms
        self.breach_limit = breach_limit

        self.breaches = deque(maxlen=breach_limit)

    def update(self, latency):

        breached = latency > self.threshold_ms

        self.breaches.append(breached)

        return sum(self.breaches) >= self.breach_limit