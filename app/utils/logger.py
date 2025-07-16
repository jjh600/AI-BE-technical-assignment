import logging
import sys
from app.config import LOG_LEVEL

def setup_logger():
    logging.basicConfig(
        level=getattr(logging, LOG_LEVEL, "INFO"),
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[logging.StreamHandler(sys.stdout)]
    )
