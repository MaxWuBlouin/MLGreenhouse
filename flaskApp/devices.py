"""
This module interfaces with all microcontroller devices connected to
the Raspberry Pi. Microcontrollers must abide by a certain
communication protocol in order to be recognized by the Python module.


All recognized microcontrollers are stored in a dictionary named
'connected_boards'. The key corresponds to the name of the
microcontroller (str) and the value corresponds to the connection 
(Serial object).
"""


import time

import serial
import serial.tools
import serial.tools.list_ports

from logconfig import logger


connected_boards = {}   # Keys are strings, values are Serial connections

BAUDRATE = 9600


def _request_name(serial_connection: serial.Serial):
    """
    Requests name from serial device and returns it. Returns None if
    name not found. Function sends 5 name requests before giving up.
    Note: Function assumes that serial_connection is open. Function
    also does not close serial_connection.

    Args:
        serial_connection (Serial): Connection to serial port.

    Returns:
        str: The name returned by the device (None if name not found).
    """
    logger.info("Requesting device name.")
    
    for i in range(1, 6):
        serial_connection.write(("name").encode())
        time.sleep(0.01)
        serial_response = serial_connection.readline()
        serial_response = serial_response.decode()
        serial_response = serial_response.rstrip()
        
        if (len(serial_response) > 2):
            if (serial_response[0] == "@" and serial_response[-1] == "@"):
                serial_response = serial_response.strip("@")
                logger.info("Found device '" + serial_response
                    + "' after " + str(i) + " attempts.")
                return serial_response
    
    logger.warning("Could not find device name.")
    return None


def connect_devices():
    """
    Clears 'connected_boards' dictionary, then identifies all
    microcontrollers connected to computer via USB and places them in
    'connected_boards' (key corresponds to device name (str), value
    corresponds to connection (Serial object)).

    Args:
        None

    Returns:
        None
    """
    logger.info("Connecting boards.")
    connected_boards.clear()

    ports = serial.tools.list_ports.comports()
    for port in ports:
        if "VID:PID" in port.hwid:
            serial_connection = serial.Serial(
                port=port.device,
                baudrate=BAUDRATE,
                timeout = 1)
            connection_name = _request_name(serial_connection)
            if connection_name != None:
                connected_boards[connection_name] = serial_connection
            serial_connection.close()
    
    logger.info("Connected to " + str(len(connected_boards)) + " devices.")
    return None


def send_message(device_name: str, message: str):
    """
    Sends message (str) to specified device (by name) and returns
    response from device (str).

    Args:
        device_name (str): Name of the device to send message to.
        message (str): Message to send to device.

    Returns:
        str: Response from device (or error message).
    """
    logger.info("Sending message '" + message + "' to device '"
        + device_name + "'")
    
    if device_name not in connected_boards:
        logger.error("Device name not found.")
        return "Error: Device name not found."
    else:
        try:
            connected_boards[device_name].open()
        except:
            logger.error("Could not open connection.")
            return "Error: Could not open connection."
        for i in range(1, 6):
            connected_boards[device_name].write(message.encode())
            time.sleep(0.01)
            serial_response = connected_boards[device_name].readline()
            serial_response = serial_response.decode()
            serial_response = serial_response.rstrip()
            
            if (len(serial_response) > 2):
                if (serial_response[0] == "#" and serial_response[-1] == "#"):
                    serial_response = serial_response.strip("#")
                    connected_boards[device_name].close()
                    logger.info("Received message '" + serial_response
                        + "' after " + str(i) + " attempts.")
                    return serial_response
    
    logger.error("No valid response received.")
    return "Error: No valid response received."