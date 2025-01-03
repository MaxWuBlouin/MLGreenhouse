"""
This module handles all configuration settings for using the Python
'logging' library. To use it, run 'from logconfig import logger' and
use the methods from the Python 'logging' library. All logged messages
are saved to 'logfile.csv'.
"""
import logging
import os


DIRECTORY = os.path.dirname(__file__)
LOGFILE_DIRECTORY = DIRECTORY + "/logfile.csv"


# Create or get a logger
logger = logging.getLogger("MLGreenhouse_logger")
logger.setLevel(logging.DEBUG)

# Create a FileHandler (default is append mode)
file_handler = logging.FileHandler(LOGFILE_DIRECTORY)
file_handler.setLevel(logging.DEBUG)

# Create a custom formatter for CSV format
formatter = logging.Formatter("%(asctime)s,%(name)s,%(levelname)s,%(module)s,%(message)s")
file_handler.setFormatter(formatter)

# Add the handler to the logger
logger.addHandler(file_handler)