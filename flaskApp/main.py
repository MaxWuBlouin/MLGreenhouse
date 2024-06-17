import devices
import webcams
from logconfig import logger

logger.info("This is a test message")
logger.error("This is a test error message")

devices.connect_devices()
devices.send_message("OUTLET", "test")
devices.send_message("WRONG", "message")