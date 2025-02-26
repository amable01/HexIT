# src/utils/logging.py
import logging

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Export the configured logger
logger = logging.getLogger(__name__)