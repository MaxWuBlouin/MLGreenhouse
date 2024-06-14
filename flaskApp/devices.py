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
    for i in range(5):
        serial_connection.write(("name").encode())
        time.sleep(0.01)
        serial_response = serial_connection.readline()
        serial_response = serial_response.decode()
        serial_response = serial_response.rstrip()
        if (len(serial_response) > 2):
            if (serial_response[0] == "@" and serial_response[-1] == "@"):
                serial_response = serial_response.strip("@")
                return serial_response
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
    connected_boards.clear()

    ports = serial.tools.list_ports.comports()
    for port in ports:
        if "VID:PID" in port.hwid:
            serial_connection = serial.Serial(
                port=port.name,
                baudrate=BAUDRATE,
                timeout = 1)
            connection_name = _request_name(serial_connection)
            if connection_name != None:
                connected_boards[connection_name] = serial_connection
            serial_connection.close()
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
    if device_name not in connected_boards:
        return "Error: Device name not found."
    else:
        try:
            connected_boards[device_name].open()
        except:
            return "Error: Could not open connection."
        for i in range(5):
            connected_boards[device_name].write(message.encode())
            time.sleep(0.01)
            serial_response = connected_boards[device_name].readline()
            serial_response = serial_response.decode()
            serial_response = serial_response.rstrip()
            if (len(serial_response) > 2):
                if (serial_response[0] == "#" and serial_response[-1] == "#"):
                    serial_response = serial_response.strip("#")
                    connected_boards[device_name].close()
                    return serial_response
    return "Error: No valid response received."