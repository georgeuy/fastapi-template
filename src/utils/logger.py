import os
import logging
import sys
from logging.handlers import RotatingFileHandler


_logging_configured = False


def setup_logging():
    """Configure application logging (runs only once)"""

    global _logging_configured

    if _logging_configured:
        return

    # Create logs directory if it doesn't exist
    os.makedirs("logs", exist_ok=True)

    # formatter
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

    # handler: console
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)

    # handler: files
    file_handler = RotatingFileHandler("logs/app.log", maxBytes=10485760, backupCount=5)
    file_handler.setFormatter(formatter)

    # root logger configuration
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    root_logger.addHandler(console_handler)
    root_logger.addHandler(file_handler)

    # set specific levels for libraries
    logging.getLogger("uvicorn").setLevel(logging.WARNING)
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)

    _logging_configured = True
