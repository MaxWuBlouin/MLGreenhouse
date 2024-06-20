import devices
import webcams
from logconfig import logger

logger.info("Running main program.")

devices.connect_devices()
devices.send_message("OUTLET", "A:ON")
devices.send_message("OUTLET", "SOMETHING")