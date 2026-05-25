"""
Order Book Management Module.
Optimized for O(1) lookups and swift aggregations using native Python dictionaries.
"""
from typing import Dict, Tuple

class OrderBook:
    def __init__(self, symbol: str):
        self.symbol: str = symbol
        # Structure: {price: volume}
        self.bids: Dict[float, float] = {}
        self.asks: Dict[float, float] = {}
        
        # Track aggregate volumes directly for O(1) OBI computation
        self.total_bid_volume: float = 0.0
        self.total_ask_volume: float = 0.0

    def update_order(self, side: str, price: float, volume: float, action: str) -> None:
        """
        Updates the internal order book structure dynamically.
        Supported actions: 'NEW', 'CANCEL', 'MODIFY'
        """
        target_book = self.bids if side.upper() == 'BUY' else self.asks
        old_volume = target_book.get(price, 0.0)

        if action.upper() == 'CANCEL' or volume <= 0:
            if price in target_book:
                self._adjust_total_volume(side, -old_volume)
                del target_book[price]
        elif action.upper() in ('NEW', 'MODIFY'):
            self._adjust_total_volume(side, volume - old_volume)
            target_book[price] = volume

    def _adjust_total_volume(self, side: str, delta: float) -> None:
        if side.upper() == 'BUY':
            self.total_bid_volume = max(0.0, self.total_bid_volume + delta)
        else:
            self.total_ask_volume = max(0.0, self.total_ask_volume + delta)

    def calculate_obi(self) -> float:
        """
        Calculates the Order Book Imbalance (OBI).
        Formula: (Bid Vol - Ask Vol) / (Bid Vol + Ask Vol)
        """
        denom = self.total_bid_volume + self.total_ask_volume
        if denom == 0:
            return 0.0
        return (self.total_bid_volume - self.total_ask_volume) / denom

    def get_best_levels(self) -> Tuple[float, float]:
        """Returns (Best Bid, Best Ask) pricing layer."""
        best_bid = max(self.bids.keys()) if self.bids else 0.0
        best_ask = min(self.asks.keys()) if self.asks else 0.0
        return best_bid, best_ask