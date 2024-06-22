"""
This module handles the connection to the AWS server via AWS Iot Core.
When imported, it automatically establishes a connection with the
server, so it should only be imported by one module.

The client-server connection uses the MQTT communication protocol. All
incoming and outgoing messages are encoded as JSON strings.

To send messages to the server, use the publish() function. To modify
the client's message callback behaviour (what it does when it receives
a message), set the function 'message_callback' to a custom function.
It must have arguments (topic: str, message: str) and return a JSON
string.
"""


import time
import json
import threading
import os
import atexit

import paho.mqtt.client as mqtt

from logconfig import logger


# External modules can modify the client's message callback behaviour
# by replacing message_callback with a custom function. This function
# must have arguments (topic: str, message: str) and return a JSON
# string. Any additional arguments must be given default values.
message_callback = None

_active_threads = []

PUBLISH_TOPIC = "raspi/response"
SUBSCRIBED_TOPICS = ["raspi/command"]

DIRECTORY = os.path.dirname(__file__)

# Certificates needed to establish connection with AWS server
ROOT_CERTIFICATE = DIRECTORY + "/certifications/AmazonRootCA1.pem"
CERTIFICATE = DIRECTORY + "/certifications/certificate.pem.crt"
PRIVATE_KEY = DIRECTORY + "/certifications/private.pem.key"

# AWS server info
HOST_ADDRESS = "airxh5i12mupp-ats.iot.us-east-2.amazonaws.com"
HOST_PORT = 8883
KEEPALIVE_INTERVAL = 60


def _on_connect(client, userdata, flags, return_code, properties=None):
    """
    Callback function for when client connects to the server. This
    function is also responsible for subscribing to all topics listed
    in SUBSCRIBED_TOPIC.
    """
    logger.info(f"Connected to AWS server with return code '{return_code}'.")
    
    for topic in SUBSCRIBED_TOPICS:
        client.subscribe(topic)
        logger.info(f"Subscribed to topic '{topic}'.")


def publish(message: str):
    """
    This function publishes messages to PUBLISH_TOPIC. It automatically
    checks whether the client is connected to the server before
    attempting to publish.
    """
    if client.is_connected():
        client.publish(PUBLISH_TOPIC, payload=message)
        logger.info(f"To {PUBLISH_TOPIC} published: {message}")
        return "Success"
    else:
        logger.error("Client is not connected.")
        return "Error: Client is not connected."


def _on_message(client, userdata, message):
    """
    Callback function for receiving messages from a subscribed topic.
    Function always logs received messages, but only sends a response
    """
    topic = message.topic
    message = message.payload.decode()
    message = json.loads(message)
    logger.info(f"From {topic} received message: {message}")

    response = json.dumps({"Response": "Default"})
    if message_callback is not None:
        response = message_callback(topic, message)
    publish(response)


def cleanup():
    """
    Function is passed to atexit.register for graceful cleanup. When
    main program terminates (whether it's this module or the program
    importing this module), the client disconnects and all active
    threads are joined.

    Note: This only applies for normal program termination. Normal
    program termination includes the main program executing its last
    line of code or os.exit() being called.
    """
    client.disconnect()
    for thread in _active_threads:
        thread.join()
        _active_threads.remove(thread)
    logger.info("Client disconnected from AWS server.")


# Establish client-server connection
client = mqtt.Client(protocol=mqtt.MQTTv5)
client.on_connect = _on_connect
client.on_message = _on_message
client.tls_set(ca_certs=ROOT_CERTIFICATE,
               certfile=CERTIFICATE,
               keyfile=PRIVATE_KEY,
               tls_version=2)
client.tls_insecure_set(True)
client.connect(host=HOST_ADDRESS,
               port=HOST_PORT,
               keepalive=KEEPALIVE_INTERVAL)

atexit.register(cleanup)

connection_thread = threading.Thread(target=client.loop_forever)
connection_thread.daemon = True # Needed for proper program termination.
connection_thread.start()
_active_threads.append(connection_thread)
time.sleep(1) # Let client establish connection before using it.