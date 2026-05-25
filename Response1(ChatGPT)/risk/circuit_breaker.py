from utils.logger import setup_logger
from utils.exporters import export_alert
from datetime import datetime

logger = setup_logger()

class CircuitBreaker:

    def __init__(self):

        self.active = False

    def trigger(self, reason):

        if self.active:
            return

        self.active = True

        alert = {
            "timestamp": datetime.utcnow().isoformat(),
            "event": "TRADING_HALTED",
            "reason": reason
        }

        logger.critical(alert)

        export_alert(alert)

        print("CIRCUIT BREAKER ACTIVATED")
        print(alert)