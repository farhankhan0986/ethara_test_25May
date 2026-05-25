from dataclasses import dataclass

@dataclass
class MarketEvent:
    order_id: str
    timestamp: float
    symbol: str
    side: str
    price: float
    quantity: int
    latency_ms: float
    event_type: str