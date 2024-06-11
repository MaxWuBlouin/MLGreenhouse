from flask import Blueprint, render_template, Response
import cv2

IMAGE_FORMAT = ".jpg"
CONTENT_TYPE = "multipart/x-mixed-replace; boundary=frame"
IMAGE_HEADER = b"--frame\r\nContent-Type: image/jpeg\r\n\r\n"

# Initialize Flask Blueprint
camera = Blueprint(__name__, "camera")

# Initialize webcam objects
webcam1 = cv2.VideoCapture(1)
webcam2 = cv2.VideoCapture(1)

# Continuously stream video from webcam
def generate_frames(webcam):
    while True:
        success, frame = webcam.read()

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
    return Response(generate_frames(webcam1), mimetype=CONTENT_TYPE)

@camera.route("/webcam2")
def stream2():
    return Response(generate_frames(webcam2), mimetype=CONTENT_TYPE)