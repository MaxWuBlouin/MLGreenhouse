"""
This module defines the Raspberry Pi's behaviour given certain AWS
commands. It is primarily to reduce the amount of code in main.py
by bundling together functions with similar purposes.
"""


import message_handler
import webcams
import email_sender


def image_response():
    """
    Iterates through all connected webcams and saves an image of
    each to the 'images' directory. Each of these images is then
    attached to an email which is sent to all subscribed email
    recipients.

    Args:
        None
    
    Returns:
        str:    Status update after images have been sent.
    """
    image_paths = []
    for webcam in webcams.connected_webcams:
        image_paths.append(webcams.save_image(webcam))

    email_sender.send_email(attachments=image_paths)

    return "Sent images via email."