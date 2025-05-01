import os
import requests
from flask import Flask, request

app = Flask(__name__)

TELEGRAM_BOT_TOKEN = os.environ.get("BOT_TOKEN")
TELEGRAM_API_URL = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}"

@app.route("/", methods=["GET"])
def home():
    return "AlphaBot is live!", 200

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()
    print("Received:", data)

    if "message" in data:
        chat_id = data["message"]["chat"]["id"]
        text = data["message"].get("text", "")

        if text == "/start":
            reply = "Привет! Я бот AlphaSignals. Готов к работе."
        else:
            reply = f"Ты написал: {text}"

        try:
            send_message(chat_id, reply)
        except Exception as e:
            print("ERROR while sending message:", e)

    return {"ok": True}, 200

def send_message(chat_id, reply):
    url = f"{TELEGRAM_API_URL}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": reply
    }

    response = requests.post(url, json=payload)

    # Выводим ответ от Telegram
    print("Sent message:", response.text)

    # Если ошибка — выведи её
    if response.status_code != 200:
        print("Telegram API error:", response.status_code, response.text)
