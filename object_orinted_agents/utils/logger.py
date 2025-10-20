import logging
from typing import Optional

def get_logger(name: str, level: int = logging.INFO, formatter: Optional[logging.Formatter] = None) -> logging.Logger:
    """
    Get a configured logger.

    Args:
        name (str): The name of the logger.
        level (int): The logging level. Default is logging.INFO.
        formatter (Optional[logging.Formatter]): Custom formatter for log messages.

    Returns:
        logging.Logger: Configured logger instance.
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)

    if not logger.hasHandlers:
        handler = logging.StreamHandler()
        handler.setLevel(level)

        if formatter is None:
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger


