"""
This module interfaces with all webcams connected to the Raspberry Pi.
The indices of all functional webcams are added to connected_webcams.
"""


import datetime
import os

import cv2

connected_webcams = []

MAX_CAMERAS = 10
DIRECTORY = os.path.dirname(__file__)
IMAGE_DIRECTORY = DIRECTORY + "/images/"


if not os.path.exists(IMAGE_DIRECTORY):
        os.makedirs(IMAGE_DIRECTORY)


def connect_cameras():
    """
    Searches through the first 10 camera indices and appends indices
    of all available cameras to connected_webcams.

    Args:
        None

    Returns:
        None
    """
    connected_webcams.clear()
    
    for i in range(MAX_CAMERAS):
        capture = cv2.VideoCapture(i)
        if capture.isOpened():
            connected_webcams.append(i)
            capture.release()
    return None


def _generate_timestamp():
    """
    Generates timestamp (str) in format YYYY-MM-DD_HH-MM-SS. This
    string contains only legal filename characters.

    Args:
        None
    
    Returns:
        str: Generated timestamp string.
    """
    datestamp = str(datetime.datetime.now())
    datestamp = datestamp.split(".")[0]
    datestamp = datestamp.replace(":", "-")
    datestamp = datestamp.replace(" ", "_")
    return datestamp


def request_image(camera_index: int):
    """
    Captures image from webcam (selected by index from
    connected_webcams) and saves it under "images" folder.
    Note: The index corresponds to the camera index listed in
    connected_webcams, not the index of connected_webcams itself.

    Args:
        camera_index (int): Index in connected_webcams corresponding
            to desired webcam.
    
    Returns:
        str: Status of executed function.
    """
    if camera_index not in connected_webcams:
        return "Error: Invalid index."
    capture = cv2.VideoCapture(camera_index)
    if not capture.isOpened():
        return "Error: Could not open camera."
    result, image = capture.read()
    if not result:
        return "Error: Error occurred while reading webcam."
    
    image_name = str(camera_index) + "_" + _generate_timestamp() + ".jpg"
    image_path = IMAGE_DIRECTORY + image_name
    cv2.imwrite(image_path, image)
    capture.release()
    return "Sucess: Image saved at " + image_path