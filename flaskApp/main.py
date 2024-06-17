import devices
import webcams
from logconfig import logger

logger.info("Running main program.")

devices.connect_devices()
devices.send_message("OUTLET", "test")
devices.send_message("WRONG", "message")

webcams.connect_cameras()
webcams.request_image(0)
webcams.request_image(2)