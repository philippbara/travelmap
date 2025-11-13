# app/logger.py
import logging
import sys
from pathlib import Path

LOG_FORMAT = "[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s"
LOG_LEVEL = logging.INFO  # or DEBUG in dev mode

def setup_logger(name: str = None, log_file: str = None) -> logging.Logger:
    """
    Creates and configures a logger that works across modules.
    - Logs to both console and (optionally) a file.
    - Keeps consistent formatting and levels.
    """
    logger = logging.getLogger(name)
    logger.setLevel(LOG_LEVEL)
    logger.propagate = False  # prevent double logging if root logger also prints

    # If logger already has handlers (e.g. during reload), skip setup
    if logger.handlers:
        return logger

    # --- Handlers ---
    formatter = logging.Formatter(LOG_FORMAT)

    # Console handler
    ch = logging.StreamHandler(sys.stdout)
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    # Optional file handler
    if log_file:
        Path(log_file).parent.mkdir(parents=True, exist_ok=True)
        fh = logging.FileHandler(log_file)
        fh.setFormatter(formatter)
        logger.addHandler(fh)

    return logger
