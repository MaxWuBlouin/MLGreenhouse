import json
import sys

import devices
import webcams
import aws_client
import message_handler
from logconfig import logger


program_running = True


#devices.connect_devices()
webcams.connect_cameras()

logger.info("Running main program.")

message = json.dumps({"message": "hello"})

def custom_response(message):
    errors = message_handler.message_errors(message)
    if errors is not None:
        return errors
    message = json.loads(message)

    target = message["header"]["target"]
    if target == "webcams":
        image = webcams.request_image(0)
        
        response = message_handler.encode_message(
            message_type="data",
            source=target,
            payload={"image": image}
        )
    elif target == "shutdown":
        logger.info("Received shutdown command.")
        response = message_handler.encode_message(
            message_type="info",
            payload={"message": "Shutting down."}
        )
        global program_running
        program_running = False
    else:
        response = message_handler.encode_message(message_type="custom type", payload={"message": "hello"})
    
    return response

aws_client.message_callback = custom_response

aws_client.publish(message)

while program_running:
    pass