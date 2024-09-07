import json

import jsonschema


TARGETS = ["webcams", "devices", "shutdown"]

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


def validate_message(message: str):
    """
    All incoming messages from AWS server are checked for formatting
    errors. For each error, the appropriate response is sent back
    to the server. Function returns None if the incoming message has
    been formatted properly.

    Args:
        message (str):  The string to check errors for.

    Returns:
        str:    The error message to send to the server. If no error
                is found, funtion returns None.
    """
    try:
        message = json.loads(message)
    except:
        return "Message not in valid JSON format."

    try:
        jsonschema.validate(instance=message, schema=SCHEMA)
    except:
        return "Error"
    
    return "SUCCESS"