import telebot
import json
import os
from flask import Flask, request

# Environment variables
BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = os.getenv("ADMIN_ID")   # তোমার Telegram ID (6573815394)
CHANNEL_ID = os.getenv("CHANNEL_ID")  # তোমার চ্যানেলের ID (-1002912079356)

bot = telebot.TeleBot(BOT_TOKEN)
server = Flask(name)

# movies.json লোড করা
MOVIES_FILE = "movies.json"
if not os.path.exists(MOVIES_FILE):
    with open(MOVIES_FILE, "w") as f:
        json.dump({}, f)

with open(MOVIES_FILE, "r") as f:
    movies = json.load(f)


# ---------- Private Channel Message Capture ----------
@bot.channel_post_handler(content_types=['video', 'document'])
def capture_channel_message(message):
    if str(message.chat.id) == str(CHANNEL_ID):
        info = f"📌 Channel ID: {message.chat.id}\n🆔 Message ID: {message.message_id}"
        bot.send_message(ADMIN_ID, info)   # ADMIN এর কাছে পাঠাবে


# ---------- User Command Handlers ----------
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "🎬 Welcome! Send me a movie name and I will fetch it for you.")


@bot.message_handler(func=lambda msg: True)
def search_movie(message):
    query = message.text.strip().lower()
    if query in movies:
        movie_data = movies[query]
        try:
            bot.copy_message(message.chat.id, movie_data["channel_id"], movie_data["message_id"])
        except Exception as e:
            bot.reply_to(message, f"⚠️ Error fetching movie: {e}")
    else:
        bot.reply_to(message, "❌ Movie not found in database.")


# ---------- Flask Webhook ----------
@server.route("/" + BOT_TOKEN, methods=['POST'])
def getMessage():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "OK", 200


@server.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url="https://YOUR_RENDER_URL/" + BOT_TOKEN)
    return "Webhook set!", 200


if name == "main":
    server.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
