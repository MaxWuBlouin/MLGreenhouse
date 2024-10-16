"""
This module defines the Raspberry Pi's behaviour given certain AWS
commands. It is primarily to reduce the amount of code in main.py
by bundling together functions with similar purposes.
"""


import os
import json

import message_handler
import webcams
import devices
import email_sender
import aws_client
from logconfig import logger


DIRECTORY = os.path.dirname(__file__) + "/"


def status_update():
    """
    Sends email with images and sensor data from the past day.
    """

    attachments_paths = []

    for webcam in webcams.connected_webcams:
        attachments_paths.append(webcams.save_image(webcam))

    attachments_paths.append(f"{DIRECTORY}data/level.csv")
    attachments_paths.append(f"{DIRECTORY}data/ph.csv")
    attachments_paths.append(f"{DIRECTORY}data/tds.csv")

    email_sender.send_email(attachments=attachments_paths)

    return "Sent status update via email."


def image_response():
    """
    Iterates through all connected webcams and saves an image of
    each to the 'images' directory. Each of these images is then
    attached to an email which is sent to all subscribed email
    recipients.

    Args:
        None
    
    Returns:
        str:    Status update after images have been sent.
    """
    image_paths = []
    for webcam in webcams.connected_webcams:
        image_paths.append(webcams.save_image(webcam))

    email_sender.send_email(attachments=image_paths)

    return "Sent images via email."


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
    if not message_handler.valid_message(message):
        error = message_handler.encode_message(
            message_type="error",
            payload={"message": "Message not in valid JSON format."}
        )
        return error
    
    message = json.loads(message)

    message_type = "none"
    payload = {}

    target = message["header"]["target"]
    if target == "webcams":
        message_type="info"
        payload["message"] = image_response()
    elif target == "devices":
        return device_response(message)
    elif target == "shutdown":
        logger.info("Received shutdown command.")
        message_type="info"
        payload["message"] = "Shutting down."
        aws_client.server_active = False
    elif target == "status":
        status_update()
        message_type="info"
        payload["message"] = "Status update sent."
    else:
        message_type = "error"
        payload["message"] = "Invalid target given."
    
    response = message_handler.encode_message(
        message_type=message_type,
        payload=payload
    )

    return response