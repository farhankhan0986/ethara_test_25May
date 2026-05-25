def calculate_obi(order_book):

    bid_volume = order_book.total_bid_volume()
    ask_volume = order_book.total_ask_volume()

    denominator = bid_volume + ask_volume

    if denominator == 0:
        return 0.0

    return (bid_volume - ask_volume) / denominator