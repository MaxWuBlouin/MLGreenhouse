#!/usr/bin/env python3

from flask import Flask
import socket

SERVER_PORT = 8000

# Find current device's local network IP address
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.connect(("8.8.8.8", 80))
server_IP = sock.getsockname()[0]

# Create flask app
app = Flask(__name__)

# Pages
@app.route("/")
def index():
    return "Hello, World!"

# Run flask app
if __name__ == "__main__":
    app.run(host = server_IP, port = SERVER_PORT)