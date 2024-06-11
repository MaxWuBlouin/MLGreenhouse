from flask import Blueprint, render_template, Response
import cv2

IMAGE_FORMAT = ".jpg"
CONTENT_TYPE = "multipart/x-mixed-replace; boundary=frame"
IMAGE_HEADER = b"--frame\r\nContent-Type: image/jpeg\r\n\r\n"

WEBCAM_PORTS = [0,2]

# Initialize Flask Blueprint
camera = Blueprint(__name__, "camera")

# Initialize webcam objects
webcam = [cv2.VideoCapture(0, cv2.CAP_V4L2)]

# Toggle between cameras
# Note: The Raspberry Pi 3B+ cannot handle multiple camera streams at once.
#       For this reason, the program must toggle between cameras.
webcam_index = [0]
def toggle_webcam():
    webcam[0].release()
    
    if webcam_index[0] == len(WEBCAM_PORTS):
        webcam_index[0] = 0
    else:
        webcam_index[0] += 1
    
    webcam[0] = cv2.VideoCapture(webcam_index[0], cv2.CAP_V4L2)

# Continuously stream video from webcam
def generate_frames():
    while True:
        success, frame = webcam.read()

        if not success:
            break
        
        frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
        success, frame = cv2.imencode(IMAGE_FORMAT, frame)
        
        yield(IMAGE_HEADER + frame.tobytes())

@camera.route("/")
def homepage():
    webcam[0] = toggle_webcam()
    return render_template("camera.html")

@camera.route("/webcam1")
def stream():
    return Response(generate_frames(), mimetype=CONTENT_TYPE)