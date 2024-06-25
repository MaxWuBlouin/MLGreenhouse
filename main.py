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


def image_response(message:dict):
    """
    This function handles incoming image requests from the AWS server.
    Formatting errors from the incoming request are handled by sending
    the appropriate error response back to the server. Images are
    encoded and sent as b64 strings, which must be properly decoded by
    the server.

    Args:
        message (dict): The incoming image request.

    Returns:
        str:    Response to the AWS server, which contains an image
                string in its payload.
    """
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


def device_response(message:dict):
    """
    This function handles all incoming AWS messages pertaining to the
    Arduino devices. It handles formatting errors by sending the
    appropriate error response back to the server.

    Args:
        message (dict): Incoming JSON message from AWS server.

    Returns:
        str: JSON string representing response to the server.
    """
    if "device" not in message["payload"]:
        response = message_handler.encode_message(
            message_type="error",
            payload={"message": "Payload must contain device."}
        )
        return response
    
    if "message" not in message["payload"]:
        response = message_handler.encode_message(
            message_type="error",
            payload={"message": "Payload must contain message."}
        )
        return response
    
    try:
        target_device = str(message["payload"]["device"])
    except:
        response = message_handler.encode_message(
            message_type="error",
            payload={"message": "Invalid device given."}
        )
        return response
    
    try:
        target_message = str(message["payload"]["message"])
    except:
        response = message_handler.encode_message(
            message_type="error",
            payload={"message": "Invalid message given."}
        )
        return response

    return_message = devices.send_message(target_device, target_message)

    payload = {}
    payload["message"] = return_message
    response = message_handler.encode_message(
        message_type="data",
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
        return image_response(message)
    elif target == "devices":
        return device_response(message)
    elif target == "shutdown":
        logger.info("Received shutdown command.")
        message_type="info"
        payload["message"] = "Shutting down."
        global program_running
        program_running = False
    else:
        message_type = "error"
        payload["message"] = "Invalid target given."
    
    response = message_handler.encode_message(
        message_type=message_type,
        payload=payload
    )

    return response


devices.connect_devices()
webcams.connect_cameras()

logger.info("Running main program.")

aws_client.message_callback = custom_response

aws_client.publish(STARTUP_MESSAGE)

while program_running:
    pass