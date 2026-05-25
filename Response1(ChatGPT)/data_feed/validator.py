import logging

REQUIRED_FIELDS = {
    "order_id",
    "timestamp",
    "symbol",
    "side",
    "price",
    "quantity",
    "latency_ms",
    "event_type"
}

def validate_event(event: dict):
    try:
        missing = REQUIRED_FIELDS - event.keys()

        if missing:
            logging.warning(f"Missing fields: {missing}")
            return False

        if event["price"] <= 0:
            return False

        if event["quantity"] <= 0:
            return False

        return True

    except Exception as e:
        logging.error(f"Validation error: {e}")
        return False