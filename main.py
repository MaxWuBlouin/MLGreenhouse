import json

import devices
import webcams
import aws_client
import message_handler
from logconfig import logger

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
    else:
        response = message_handler.encode_message(message_type="custom type", payload={"message": "hello"})
    
    return response

aws_client.message_callback = custom_response

aws_client.publish(message)

input()