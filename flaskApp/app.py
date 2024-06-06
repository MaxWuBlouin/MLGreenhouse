#!/usr/bin/env python3

from flask import Flask, render_template
import socket

from camera import camera

SERVER_PORT = 8000

# Find current device's local network IP address
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.connect(("8.8.8.8", 80))
server_IP = sock.getsockname()[0]

# Create flask app
app = Flask(__name__)

#Register blueprints
app.register_blueprint(camera, url_prefix="/camera")

# Pages
@app.route("/")
def index():
    return render_template("index.html")

# Run flask app
if __name__ == "__main__":
    app.run(host = server_IP, port = SERVER_PORT)