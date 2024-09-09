"""
This module handles formatting-related tasks for sending messages to
and from the AWS server in JSON format.
"""


import json
import datetime

import jsonschema


SOURCE = "raspberry-pi"
SERVER = "aws-server"
TARGETS = ["webcams", "devices", "shutdown", "status"]

SCHEMA = {
    "type": "object",
    "properties": {
        "header": {
            "type": "object",
            "properties": {
                "target": {"type": "string",
                           "enum": TARGETS},
            },
            "required": ["target"]
        },
        "payload": {
            "type": "object"
        }
    },
    "required": ["header", "payload"]
}


def encode_message(message_type:str="none", source=SOURCE, payload:dict={}):
    """
    This function takes a payload to send and automatically generates
    the full response with a proper header. Choosing a custom
    message_type argument is recommended.

    Args:
        message_type (str): Identifier in JSON header.
        payload (dict): Content of JSON message to send.

    Returns:
        str: JSON string to send to AWS server.
    """
    header = {}
    header["message_type"] = message_type
    header["source"] = source
    header["target"] = SERVER
    header["timestamp"] = str(datetime.datetime.now())

    json_file = {"header": header, "payload": payload}
    
    return json.dumps(json_file)


def valid_message(message: str):
    """
    All incoming messages from AWS server are checked for formatting
    errors. Returns True if valid format, False otherwise.

    Args:
        message (str):  The string to check errors for.

    Returns:
        bool:   True if valid format, False otherwise.
    """
    try:
        message = json.loads(message)
    except:
        return False

    try:
        jsonschema.validate(instance=message, schema=SCHEMA)
    except:
        return False
    
    return True