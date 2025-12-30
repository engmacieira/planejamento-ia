import logging
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path

# Paths
LOG_FILE_NAME = "app.log"
# Adjusting path to be relative to the PROJECT ROOT (app/core/logging > app/core > app > root)
LOG_DIR = Path(__file__).resolve().parent.parent.parent / "logs"
LOG_FILE_PATH = LOG_DIR / LOG_FILE_NAME

# Configuration
LOG_LEVEL = logging.INFO
LOG_FORMAT = "%(asctime)s - %(levelname)s - %(name)s - %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
MAX_BYTES = 10 * 1024 * 1024 # 10MB
BACKUP_COUNT = 3

def setup_logging():
    """
    Configures the application logging with RotatingFileHandler and StreamHandler.
    """
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    
    formatter = logging.Formatter(LOG_FORMAT, datefmt=DATE_FORMAT)
    
    # File Handler
    file_handler = RotatingFileHandler(
        LOG_FILE_PATH,
        maxBytes=MAX_BYTES,
        backupCount=BACKUP_COUNT,
        encoding='utf-8' 
    )
    file_handler.setFormatter(formatter)
    file_handler.setLevel(LOG_LEVEL)

    # Console Handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    console_handler.setLevel(LOG_LEVEL) 

    # Root Logger Configuration
    root_logger = logging.getLogger()
    root_logger.setLevel(LOG_LEVEL) 

    # Avoid duplicate handlers if setup is called multiple times
    if root_logger.hasHandlers():
        root_logger.handlers.clear()

    root_logger.addHandler(file_handler)
    root_logger.addHandler(console_handler)

    logging.info(f"Logging configured. Logs at: {LOG_FILE_PATH}")
