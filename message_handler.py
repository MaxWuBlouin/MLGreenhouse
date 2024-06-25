import json
import datetime


SOURCE = "raspberry-pi"
SERVER = "aws-server"
MESSAGE_TYPES = [
    "command",
    "data",
    "status"
]


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


def message_errors(message:str):
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
        error = encode_message(
            message_type="error",
            payload={"message": "Message not in valid JSON format."}
        )
        return error
    
    if "header" not in message:
        error = encode_message(
            message_type="error",
            payload={"message": "JSON file is missing header."}
        )
        return error
    if "payload" not in message:
        error = encode_message(
            message_type="error",
            payload={"message": "JSON file is missing payload."}
        )
        return error
    
    if type(message["header"]) != dict:
        error = encode_message(
            message_type="error",
            payload={"message": "Invalid header format."}
        )
        return error
    if type(message["payload"]) != dict:
        error = encode_message(
            message_type="error",
            payload={"message": "Invalid payload format."}
        )
        return error
    
    if "message_type" not in message["header"]:
        error = encode_message(
            message_type="error",
            payload={"message": "Header missing message type."}
        )
        return error
    if "target" not in message["header"]:
        error = encode_message(
            message_type="error",
            payload={"message": "Header missing target."}
        )
        return error
    # Note: the fields 'source' and 'timestamp' are not checked in the
    # header even though they should be part of the agreed-upon JSON
    # structure. This is because these fields are not necessary for
    # the Raspberry Pi main program to function.

    if message["header"]["message_type"] not in MESSAGE_TYPES:
        error = encode_message(
            message_type="error",
            payload={"message": "Invalid message type."}
        )
        return error

    return None


def decode_message(message):
    if ("header" not in message or "payload" not in message):
        return ""
    pass