import json

import devices
import webcams
import aws_client
import message_handler
from logconfig import logger


program_running = True


STARTUP_MESSAGE = message_handler.encode_message(
    message_type="info",
    payload={"message": "Connected Raspberry Pi to server."}
)


def image_message(message:dict):
    if "index" not in message["payload"]:
        response = message_handler.encode_message(
            message_type="error",
            payload={"message": "Payload missing index."}
        )
        return response
    
    try:
        index = int(message["payload"]["index"])
    except:
        response = message_handler.encode_message(
            message_type="error",
            payload={"message": "Invalid index given."}
        )
        return response
    
    if index < 0 or index >= len(webcams.connected_webcams):
        response = message_handler.encode_message(
            message_type="error",
            payload={"message": "Invalid index given."}
        )
        return response

    result, image = webcams.request_image(index)
    message_type = "data"
    payload = {}
    payload["message"] = result
    payload["image"] = image

    response = message_handler.encode_message(
        message_type=message_type,
        payload=payload
    )

    return response


def custom_response(message):
    errors = message_handler.message_errors(message)
    if errors is not None:
        return errors
    message = json.loads(message)

    message_type = "none"
    payload = {}

    target = message["header"]["target"]
    if target == "webcams":
        return image_message(message)
    elif target == "shutdown":
        logger.info("Received shutdown command.")
        message_type="info"
        payload["message"] = "Shutting down."
        global program_running
        program_running = False
    else:
        message_type = "custom type"
        payload["message"] = "hello"
    
    response = message_handler.encode_message(
        message_type=message_type,
        payload=payload
    )

    return response


#devices.connect_devices()
webcams.connect_cameras()

logger.info("Running main program.")

aws_client.message_callback = custom_response

aws_client.publish(STARTUP_MESSAGE)

while program_running:
    pass