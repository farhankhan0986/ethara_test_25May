from collections import defaultdict

class OrderBook:

    def __init__(self):
        self.bids = defaultdict(int)
        self.asks = defaultdict(int)
        self.orders = {}

    def add_order(self, event):

        self.orders[event.order_id] = event

        if event.side == "BUY":
            self.bids[event.price] += event.quantity
        else:
            self.asks[event.price] += event.quantity

    def cancel_order(self, order_id):

        if order_id not in self.orders:
            return

        order = self.orders.pop(order_id)

        if order.side == "BUY":
            self.bids[order.price] -= order.quantity
        else:
            self.asks[order.price] -= order.quantity

    def update_order(self, event):

        self.cancel_order(event.order_id)
        self.add_order(event)

    def best_bid(self):
        return max(self.bids.keys(), default=None)

    def best_ask(self):
        return min(self.asks.keys(), default=None)

    def total_bid_volume(self):
        return sum(self.bids.values())

    def total_ask_volume(self):
        return sum(self.asks.values())