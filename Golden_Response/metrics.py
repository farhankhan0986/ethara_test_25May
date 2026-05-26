"""
Real-time streaming metrics tracker utilizing collections.deque for high performance.
Avoids sweeping pandas re-evaluations to conserve compute cycle budgets.
"""
from collections import deque
import numpy as np
from typing import Tuple

class MetricsTracker:
    def __init__(self, window_size_seconds: int = 60):
        self.window_size: int = window_size_seconds
        
        # Windows stored as deques of tuples: (timestamp, value) or (timestamp, price, volume)
        self.vwap_window: deque = deque()
        self.latency_window: deque = deque()
        self.obi_window: deque = deque()

        # Incremental state parameters for fast VWAP
        self.sum_pv: float = 0.0
        self.sum_v: float = 0.0

    def add_trade(self, timestamp: float, price: float, volume: float) -> float:
        """Dynamically incorporates trades into rolling VWAP via incremental tracking."""
        self.vwap_window.append((timestamp, price, volume))
        self.sum_pv += price * volume
        self.sum_v += volume
        self._expire_old_vwap(timestamp)
        return self.sum_pv / self.sum_v if self.sum_v > 0 else price

    def add_latency(self, timestamp: float, latency_ms: float) -> None:
        self.latency_window.append((timestamp, latency_ms))
        self._expire_generic(self.latency_window, timestamp)

    def add_obi(self, timestamp: float, obi: float) -> None:
        self.obi_window.append((timestamp, obi))
        self._expire_generic(self.obi_window, timestamp)

    def _expire_old_vwap(self, current_time: float) -> None:
        while self.vwap_window and (current_time - self.vwap_window[0][0] > self.window_size):
            _, p, v = self.vwap_window.popleft()
            self.sum_pv -= p * v
            self.sum_v -= v

    def _expire_generic(self, window: deque, current_time: float) -> None:
        while window and (current_time - window[0][0] > self.window_size):
            window.popleft()

    def get_recent_latencies(self, count: int = 5) -> list:
        return [item[1] for item in list(self.latency_window)[-count:]]

    def compute_obi_zscore(self) -> float:
        """Computes current OBI Z-Score against the cached rolling window."""
        if len(self.obi_window) < 10:
            return 0.0
        obis = [item[1] for item in self.obi_window]
        mean = np.mean(obis)
        std = np.std(obis)
        if std == 0:
            return 0.0
        return float((obis[-1] - mean) / std)