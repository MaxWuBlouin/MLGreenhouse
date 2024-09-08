"""
This module interfaces with all webcams connected to the Raspberry Pi.
The indices of all functional webcams are added to connected_webcams.
"""


import os
import time
import base64

import cv2

from logconfig import logger

connected_webcams = []

MAX_CAMERAS = 10
DIRECTORY = os.path.dirname(__file__)


def connect_cameras():
    """
    Searches through the first 10 camera indices and appends indices
    of all available cameras to connected_webcams.

    Args:
        None

    Returns:
        None
    """
    logger.info("Connecting webcams.")
    connected_webcams.clear()
    
    for i in range(MAX_CAMERAS):
        capture = cv2.VideoCapture(i)
        if capture.isOpened():
            connected_webcams.append(i)
            capture.release()
    
    logger.info(f"Connected to {len(connected_webcams)} webcams.")
    return None


def request_image(camera_index: int):
    """
    Captures image from webcam (selected by index from
    connected_webcams) and returns it as .jpg image.
    Note: The index corresponds to the camera index listed in
    connected_webcams, not the index of connected_webcams itself.

    Args:
        camera_index (int): Index in connected_webcams corresponding
            to desired webcam.
    
    Returns:
        str: Status message.
        numpy.ndarray: Image encoded in .jpg format.

    """
    logger.info(f"Requesting image from camera at index {camera_index}.")
    
    if camera_index not in connected_webcams:
        logger.error("Invalid index.")
        status = "Error: Invalid index."
        return status, None
    
    capture = cv2.VideoCapture(camera_index)
    if not capture.isOpened():
        logger.error("Could not open camera.")
        status = "Error: Could not open camera."
        return status, None
    
    result, image = capture.read()
    capture.release()
    
    if not result:
        logger.error("Error occurred while reading webcam.")
        status = "Error: Error occurred while reading webcam."
        return status, None
    
    result, image = cv2.imencode(".jpg", image)    
    image_as_bytes = base64.b64encode(image)
    image_as_text = image_as_bytes.decode()
    status = "Success"
    logger.info(f"Successfully returned image from index {camera_index}.")
    
    return status, image_as_text


def save_image(camera_index: int):
    """
    Captures image from webcam (selected by index from
    connected_webcams) and saves it as .jpg image.
    Note: The index corresponds to the camera index listed in
    connected_webcams, not the index of connected_webcams itself.

    Args:
        camera_index (int): Index in connected_webcams corresponding
            to desired webcam.
    
    Returns:
        str: Status message.
    """
    logger.info(f"Requesting image from camera at index {camera_index}.")
    
    capture = cv2.VideoCapture(camera_index)
    if not capture.isOpened():
        logger.error("Could not open camera.")
        return "Error: Could not open camera."
    
    time.sleep(0.5)
    result, image = capture.read()
    capture.release()

    if not result:
        logger.error("Error occurred while reading webcam.")
        return "Error: Error occurred while reading webcam."
    
    image_path = f"{DIRECTORY}/images/webcam{camera_index}.jpg"
    cv2.imwrite(image_path, image)
    
    return image_path