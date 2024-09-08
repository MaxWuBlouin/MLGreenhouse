import os
import json
import time

import schedule

import devices
import webcams
import aws_client
import message_handler
import email_sender
import aws_responses
from logconfig import logger


program_running = True


DIRECTORY = os.path.dirname(__file__)

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

    while aws_client.server_active:
        schedule.run_pending()
        time.sleep(5)