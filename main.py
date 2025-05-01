
import os
from flask import Flask, request

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return "AlphaBot is live!", 200

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json
    print("Received:", data)
    return "OK", 200


