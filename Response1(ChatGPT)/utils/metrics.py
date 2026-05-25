from collections import deque
from statistics import mean

class MetricsCollector:

    def __init__(self, max_samples=10000):

        self.processing_times = deque(maxlen=max_samples)
        self.latencies = deque(maxlen=max_samples)

    def add_processing_time(self, value_ms):

        self.processing_times.append(value_ms)

    def add_latency(self, latency_ms):

        self.latencies.append(latency_ms)

    def summary(self):

        processing_times = list(self.processing_times)
        latencies = list(self.latencies)

        return {
            "avg_processing_ms":
                float(mean(processing_times))
                if processing_times else 0,

            "max_processing_ms":
                float(max(processing_times))
                if processing_times else 0,

            "avg_latency_ms":
                float(mean(latencies))
                if latencies else 0
        }