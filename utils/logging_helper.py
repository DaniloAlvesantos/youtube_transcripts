import logging
import os
from typing import Final

LOG_FORMAT: Final = '%(asctime)s - %(levelname)s - %(message)s'

if not os.path.isdir("logs"):
    os.makedirs('logs', exist_ok=True)

def setup_logger(name: str, log_file: str, level: int = logging.INFO):
    handler = logging.FileHandler(f"logs/{log_file}")        
    handler.setFormatter(logging.Formatter(LOG_FORMAT))

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)
    logger.propagate = False
    
    return logger

info_logger = setup_logger('info_logger', 'info.log', logging.INFO)
warn_logger = setup_logger('warn_logger', 'warnings.log', logging.WARNING)
error_logger = setup_logger('error_logger', 'errors.log', logging.ERROR)
debug_logger = setup_logger("debug_logger", "debug.log", logging.DEBUG)

def log_info(message: str) -> None:
    info_logger.info(message)

def log_warn(message: str) -> None:
    warn_logger.warning(message)

def log_error(message: str) -> None:
    error_logger.error(message, exc_info=True)

def log_debug(message: str) -> None:
    debug_logger.debug(message)