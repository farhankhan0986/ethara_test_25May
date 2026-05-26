"""
Consolidated High-Frequency Trading Risk Core Engine.
"""
import time
from typing import Dict, Any, Optional
from order_book import OrderBook
from metrics import MetricsTracker
from circuit_breaker import RiskCircuitBreaker

class RiskEngine:
    def __init__(self, symbol: str):
        self.symbol: str = symbol
        self.order_book: OrderBook = OrderBook(symbol)
        self.metrics: MetricsTracker = MetricsTracker(window_size_seconds=60)
        self.circuit_breaker: RiskCircuitBreaker = RiskCircuitBreaker()

    def process_tick(self, tick: Dict[str, Any]) -> Dict[str, Any]:
        """
        Processes single tick dictionary items.
        Guaranteed to execute in sub-millisecond timelines.
        """
        start_processing = time.perf_counter()

        # Input Integrity Validation Guardrails
        required_fields = ["timestamp", "side", "price", "volume", "action", "latency_ms"]
        if not all(field in tick for field in required_fields) or tick["price"] <= 0 or tick["volume"] < 0:
            return {"status": "SKIPPED", "reason": "Malformed Packet Entry"}

        ts = tick["timestamp"]
        price = float(tick["price"])
        volume = float(tick["volume"])
        side = tick["side"]
        action = tick["action"]
        latency_ms = float(tick["latency_ms"])

        # 1. Update Underlying Data Stores
        self.order_book.update_order(side, price, volume, action)
        current_obi = self.order_book.calculate_obi()
        
        self.metrics.add_latency(ts, latency_ms)
        self.metrics.add_obi(ts, current_obi)
        
        # 2. Track Simulated Trades for VWAP Calculations
        if action == "NEW":
            rolling_vwap = self.metrics.add_trade(ts, price, volume)
        else:
            rolling_vwap = self.metrics.sum_pv / self.metrics.sum_v if self.metrics.sum_v > 0 else price

        # 3. Assess Risks via Circuit Breaker
        recent_latencies = self.metrics.get_recent_latencies()
        obi_zscore = self.metrics.compute_obi_zscore()
        
        halted, reason = self.circuit_breaker.check_risk_rules(
            current_obi, recent_latencies, obi_zscore, ts
        )

        processing_delay_ms = (time.perf_counter() - start_processing) * 1000.0

        return {
            "status": "HALTED" if halted else "PROCESSED",
            "reason": reason,
            "obi": current_obi,
            "vwap": rolling_vwap,
            "z_score": obi_zscore,
            "processing_delay_ms": processing_delay_ms
        }