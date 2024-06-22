import json

import devices
import webcams
import aws_client
from logconfig import logger

devices.connect_devices()
webcams.connect_cameras()

logger.info("Running main program.")

message = json.dumps({"message": "hello"})

def custom_response(topic, message):
    response = json.dumps({"custom" : "response"})
    return response

aws_client.message_callback = custom_response

aws_client.publish(message)

input()