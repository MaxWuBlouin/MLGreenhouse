import json

import jsonschema


MESSAGE_TYPES = ["command", "data", "status"]
TARGETS = ["webcams", "devices", "shutdown"]

SCHEMA = {
    "type": "object",
    "properties": {
        "header": {
            "type": "object",
            "properties": {
                "message_type": {"type": "string",
                                 "enum": MESSAGE_TYPES},
                "target": {"type": "string",
                           "enum": TARGETS},
            },
            "required": ["message_type", "target"]
        },
        "payload": {
            "type": "object"
        }
    },
    "required": ["header", "payload"]
}


test1 = {}
test2 = "{}"
test3 = json.dumps({"header": {},
                    "payload": {}})
test4 = json.dumps({
    "header": {
        "message_type": "command",
        "target": "webcams"
    },
    "payload": {}
})


_test_data = test4


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


if __name__ == "__main__":
    print(validate_message(_test_data))