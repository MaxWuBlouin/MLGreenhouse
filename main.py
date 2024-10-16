import time

import schedule

import devices
import webcams
import aws_client
import message_handler
import aws_responses
import device_log
from logconfig import logger


STARTUP_MESSAGE = message_handler.encode_message(
    message_type="info",
    payload={"message": "Connected Raspberry Pi to server."}
)


if __name__ == "__main__":
    devices.connect_devices()
    webcams.connect_cameras()

    logger.info("Running main program.")

    aws_client.message_callback = aws_responses.custom_response
    aws_client.publish(STARTUP_MESSAGE)

    schedule.every().minute.do(device_log.store_all)
    schedule.every().day.at("09:00").do(aws_responses.status_update)

    while aws_client.server_active:
        schedule.run_pending()
        time.sleep(5)