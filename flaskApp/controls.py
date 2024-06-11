from flask import Blueprint, render_template

# Initialize Flask Blueprint
controls = Blueprint(__name__, "controls")

@controls.route("/")
def homepage():
    return render_template("controls.html")