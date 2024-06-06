from flask import Blueprint, render_template, Response
import cv2

camera = Blueprint(__name__, "camera")

webcam = cv2.VideoCapture(0)

def generate_frames():
    while True:
        success, frame = webcam.read()
        if not success:
            break
        frame = cv2.rotate(frame, cv2.ROTATE_180)
        ret, buffer = cv2.imencode(".jpg", frame)
        frame = buffer.tobytes()
        yield(b"--frame\r\n"
            b"Content-Type: image/jpeg\r\n\r\n" + frame + b"\r\n")


@camera.route("/")
def homepage():
    return render_template("camera.html")

@camera.route("/webcam")
def stream():
    return Response(generate_frames(), mimetype="multipart/x-mixed-replace; boundary=frame")