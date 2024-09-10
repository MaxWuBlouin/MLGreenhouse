"""
This module records sensor data and stores it in the appropriate CSV.
The CSV files can be found in the 'data' directory.
"""

import logging
import os

import devices


DIRECTORY = os.path.dirname(__file__) + "/data/"
DEVICE_NAME = "WATER"

loggers = {}    #Logger name: command to retrieve data


def create_logger(logger_name:str, logfile_name:str):
    """
    Given a logger name and a file name to store data, function
    creates a logger and returns it.

    Args:
        logger_name (str):  The name of the logger.
        logfile_name(str):  The name of the file to store data in
                            (in the 'data' directory).

    Returns:
        Logger: The created logger.
    """
    created_logger = logging.getLogger(logger_name)
    created_logger.setLevel(logging.DEBUG)

    created_file_handler = logging.FileHandler(DIRECTORY + logfile_name)
    created_file_handler.setLevel(logging.DEBUG)

    created_formatter = logging.Formatter("%(asctime)s,%(message)s")
    created_file_handler.setFormatter(created_formatter)

    created_logger.addHandler(created_file_handler)
    
    return created_logger


def store_data(logger:logging.Logger, command:str):
    """
    Given a logger and a command, sends command to connected microcontroller
    and retrieves serial response. Response is then stored in the appropriate
    CSV file.

    Args:
        logger (logging.Logger):    The logger that stores data.
        command (str):  The command to send to the microcontroller

    Returns:
        None
    """
    if DEVICE_NAME in devices.connected_boards:
        data = devices.send_message(DEVICE_NAME, command)
        logger.info(data)
    return


def store_all():
    """
    Stores data from all loggers listed in loggers. No args, no returns.
    """
    for logger_name in loggers:
        store_data(logger_name, loggers[logger_name])
    return


level_logger = create_logger("Level_logger", "level.csv")
loggers[level_logger] = "level"

ph_logger = create_logger("ph_logger", "ph.csv")
loggers[ph_logger] = "ph_sensor"

tds_logger = create_logger("tds_logger", "tds.csv")
loggers[tds_logger] = "tds_sensor"