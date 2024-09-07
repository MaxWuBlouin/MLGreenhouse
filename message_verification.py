import json

import jsonschema


TARGETS = ["webcams", "devices", "shutdown"]
MAX_WEBCAMS = -1
PAYLOAD_SCHEMAS = {
    "webcams": {
        "type": "object",
        "properties": {
            "index": {"type": "integer",
                      "minimum": 0,
                      "maximum": MAX_WEBCAMS}
        },
        "required": ["index"]
    },
    "devices": {

    },
    "shutdown:": {

    }
}

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


_test_data = json.dumps({
    "header": {
        "message_type": "command",
        "target": "webcams"
    },
    "payload": {
        "index": 1
    }
})


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

        jsonschema.validate(
            instance=message["payload"],
            schema=PAYLOAD_SCHEMAS[message["header"]["target"]])
    except:
        return "Error"
    
    return "SUCCESS"


if __name__ == "__main__":
    print(validate_message(_test_data))