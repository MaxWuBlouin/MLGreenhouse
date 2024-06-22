import json

import devices
import webcams
import aws_client
from logconfig import logger

logger.info("Running main program.")

message = json.dumps({"message": "hello"})

aws_client.publish(message)

input()