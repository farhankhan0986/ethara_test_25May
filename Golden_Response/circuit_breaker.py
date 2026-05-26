"""
Circuit Breaker Monitoring Engine.
Flags extreme anomalies and locks execution states safely.
"""
import json
import logging
from typing import Optional, Dict, Any

logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')

class RiskCircuitBreaker:
    def __init__(self, obi_threshold: float = 0.9, max_latency_ms: float = 15.0, latency_consecutive_ticks: int = 5):
        self.obi_threshold: float = obi_threshold
        self.max_latency_ms: float = max_latency_ms
        self.latency_consecutive_ticks: int = latency_consecutive_ticks
        
        self.is_halted: bool = False
        self.halt_reason: Optional[str] = None
        self.triggered_at: Optional[float] = None

    def check_risk_rules(self, current_obi: float, recent_latencies: list, obi_zscore: float, current_time: float) -> Tuple[bool, Optional[str]]:
        """Evaluates thresholds to determine if a hard halt is necessary."""
        if self.is_halted:
            return True, self.halt_reason

        # Rule 1: Extreme Absolute OBI Imbalance
        if abs(current_obi) >= self.obi_threshold:
            self._trigger_halt(f"Extreme Order Book Imbalance: {current_obi:.2f}", current_time)
            return True, self.halt_reason

        # Rule 2: Multi-tick consecutive Latency spike
        if len(recent_latencies) >= self.latency_consecutive_ticks:
            if all(latency > self.max_latency_ms for latency in recent_latencies):
                self._trigger_halt(f"Persistent Latency Spike: {recent_latencies} ms", current_time)
                return True, self.halt_reason

        # Rule 3: Statistical Deviation Outlier (Z-Score)
        if abs(obi_zscore) > 3.5:
            self._trigger_halt(f"Statistical OBI Anomaly Z-Score: {obi_zscore:.2f}", current_time)
            return True, self.halt_reason

        return False, None

    def _trigger_halt(self, reason: str, timestamp: float) -> None:
        self.is_halted = True
        self.halt_reason = reason
        self.triggered_at = timestamp
        
        alert_payload = {
            "event": "TRADING_HALT",
            "reason": reason,
            "timestamp": timestamp,
            "status": "CRITICAL"
        }
        logging.error(f"!!! RISK CIRCUIT BREAKER TRIGGERED !!! -> {json.dumps(alert_payload)}")
        
        # Save alert directly to external audit file
        with open("risk_alerts.json", "a") as f:
            f.write(json.dumps(alert_payload) + "\n")

    def reset(self) -> None:
        self.is_halted = False
        self.halt_reason = None
        self.triggered_at = None
        logging.info("Circuit breaker system reset. Resuming monitoring actions.")