from flask import Blueprint, render_template

camera = Blueprint(__name__, "camera")

@camera.route("/")
def homepage():
    return render_template("camera.html")