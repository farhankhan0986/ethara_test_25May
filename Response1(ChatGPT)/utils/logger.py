import logging
from logging.handlers import RotatingFileHandler

def setup_logger(
    name="HFT_RISK_ENGINE",
    log_file="risk_engine.log",
    level=logging.INFO
):

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(message)s"
    )

    handler = RotatingFileHandler(
        log_file,
        maxBytes=10_000_000,
        backupCount=5
    )

    handler.setFormatter(formatter)

    logger = logging.getLogger(name)

    logger.setLevel(level)

    if not logger.handlers:
        logger.addHandler(handler)

    return logger