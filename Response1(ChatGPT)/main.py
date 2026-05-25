import asyncio
import random
import time

from analytics.anomaly import ZScoreDetector
from analytics.latency import LatencyMonitor
from analytics.obi import calculate_obi
from analytics.vwap import RollingVWAP
from orderbook.models import MarketEvent
from orderbook.order_book import OrderBook
from risk.circuit_breaker import CircuitBreaker
from utils.metrics import MetricsCollector
from utils.timers import time_block
from visualization.charts import (
    plot_obi,
    plot_vwap,
    plot_latency,
    plot_risk_alerts,
)


metrics = MetricsCollector()
order_book = OrderBook()
vwap_engine = RollingVWAP()
latency_monitor = LatencyMonitor(threshold_ms=15, breach_limit=3)
obi_detector = ZScoreDetector()
breaker = CircuitBreaker()
obi_values = []
vwap_values = []
latency_values = []
risk_alert_values = []
breaker_state_values = []


async def market_data_stream(max_events=100):
    for order_id in range(max_events):
        yield MarketEvent(
            order_id=str(order_id),
            timestamp=time.time(),
            symbol="AAPL",
            side=random.choice(["BUY", "SELL"]),
            price=round(random.uniform(100, 101), 2),
            quantity=random.randint(1, 100),
            latency_ms=random.randint(1, 20),
            event_type="NEW",
        )

        await asyncio.sleep(0.001)


def process_event_logic(event):
    order_book.add_order(event)
    vwap_engine.update(event.price, event.quantity)

    obi = calculate_obi(order_book)
    current_vwap = vwap_engine.value()
    obi_values.append(obi)
    vwap_values.append(current_vwap)
    latency_values.append(event.latency_ms)
    latency_breached = latency_monitor.update(event.latency_ms)
    anomaly_detected, z_score = obi_detector.update(obi)
    alert_triggered = latency_breached or anomaly_detected

    if latency_breached:
        breaker.trigger(
            f"Latency breach detected at {event.latency_ms} ms"
        )

    if anomaly_detected:
        breaker.trigger(
            f"OBI anomaly detected with z-score {z_score:.4f}"
        )

    risk_alert_values.append(1 if alert_triggered else 0)
    breaker_state_values.append(1 if breaker.active else 0)

    print(
        f"event={event.order_id} "
        f"obi={obi:.4f} "
        f"vwap={current_vwap:.4f} "
        f"latency_ms={event.latency_ms}"
    )


async def process_market_data(max_events=100):
    async for event in market_data_stream(max_events=max_events):
        with time_block() as elapsed:
            process_event_logic(event)

        processing_time_ms = elapsed()
        metrics.add_processing_time(processing_time_ms)
        metrics.add_latency(event.latency_ms)

        if processing_time_ms > 2:
            print(f"WARNING: Slow processing {processing_time_ms:.4f} ms")

    print("Summary:", metrics.summary())
    plot_obi(obi_values)
    plot_vwap(vwap_values)
    plot_latency(latency_values, threshold_ms=latency_monitor.threshold_ms)
    plot_risk_alerts(risk_alert_values, breaker_state_values)

    import matplotlib.pyplot as plt

    plt.show()


if __name__ == "__main__":
    asyncio.run(process_market_data())