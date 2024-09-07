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