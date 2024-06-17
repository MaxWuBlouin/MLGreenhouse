"""
"""
import datetime
import logging
import os


DIRECTORY = os.path.dirname(__file__)
LOGGER_DIRECTORY = DIRECTORY + "/filename.csv"

# Create or get a logger
logger = logging.getLogger("MLGreenhouse_logger")
logger.setLevel(logging.DEBUG)

# Create a FileHandler (default is append mode)
file_handler = logging.FileHandler("logfile.csv")
file_handler.setLevel(logging.DEBUG)

# Create a custom formatter for CSV format
formatter = logging.Formatter("%(asctime)s,%(name)s,%(levelname)s,%(module)s,%(message)s")
file_handler.setFormatter(formatter)

# Add the handler to the logger
logger.addHandler(file_handler)