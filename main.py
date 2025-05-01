import os
import requests
from flask import Flask, request, abort

app = Flask(__name__)

# Ваш токен из переменной окружения BOT_TOKEN
TELEGRAM_BOT_TOKEN = os.environ.get("BOT_TOKEN")
if not TELEGRAM_BOT_TOKEN:
    raise RuntimeError("Missing BOT_TOKEN environment variable")

TELEGRAM_API_URL = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}"

@app.route("/", methods=["GET"])
def home():
    return "AlphaBot is alive!", 200

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json(force=True)
    # Для отладки: Railway → Deploy Logs покажет этот print
    print("Received:", data)

    # Обязательно возвращаем 200 ТГ, чтобы он не пытался ретраить
    if "message" not in data:
        return {"ok": True}, 200

    chat_id = data["message"]["chat"]["id"]
    text = data["message"].get("text", "")

    # Простая логика
    if text == "/start":
        reply = "Привет! Я бот AlphaSignals. Готов к работе."
    else:
        reply = f"Ты написал: {text}"

    send_message(chat_id, reply)
    return {"ok": True}, 200

def send_message(chat_id: int, text: str):
    url = f"{TELEGRAM_API_URL}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text,
    }
    resp = requests.post(url, json=payload)
    # Для отладки
    print("Sent:", resp.text)

if __name__ == "__main__":
    # Только для локального запуска
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
