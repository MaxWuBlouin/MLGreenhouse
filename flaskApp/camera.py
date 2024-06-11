from flask import Blueprint, render_template, Response
import cv2

import time

IMAGE_FORMAT = ".jpg"
CONTENT_TYPE = "multipart/x-mixed-replace; boundary=frame"
IMAGE_HEADER = b"--frame\r\nContent-Type: image/jpeg\r\n\r\n"

# Initialize Flask Blueprint
camera = Blueprint(__name__, "camera")

# Initialize webcam objects
webcam1 = cv2.VideoCapture(0)
webcam2 = cv2.VideoCapture(2)

# Continuously stream video from webcam
def generate_frames1():
    while True:
        time.sleep(0.1)
        
        success, frame = webcam1.read()

        if not success:
            break
        
        frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
        success, frame = cv2.imencode(IMAGE_FORMAT, frame)
        
        yield(IMAGE_HEADER + frame.tobytes())

# Continuously stream video from webcam
def generate_frames2():
    while True:
        time.sleep(0.1)
        
        success, frame = webcam2.read()

        if not success:
            break
        
        frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
        success, frame = cv2.imencode(IMAGE_FORMAT, frame)
        
        yield(IMAGE_HEADER + frame.tobytes())

@camera.route("/")
def homepage():
    return render_template("camera.html")

@camera.route("/webcam1")
def stream1():
    return Response(generate_frames1(), mimetype=CONTENT_TYPE)

@camera.route("/webcam2")
def stream2():
    return Response(generate_frames2(), mimetype=CONTENT_TYPE)