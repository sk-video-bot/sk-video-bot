from keep_alive import keep_alive
import telebot
from telebot.types import Message
import os
import json
import datetime

# টোকেন লোড করা হচ্ছে
TOKEN = os.getenv("TOKEN")
bot = telebot.TeleBot(TOKEN)

# movies.json ফাইল থেকে মুভির তালিকা লোড করা হচ্ছে
with open("movies.json", "r") as f:
    MOVIES = json.load(f)

# /start কমান্ডের জন্য ফাংশন
@bot.message_handler(commands=['start'])
def send_movie(message: Message):
    # কমান্ড থেকে মুভির কোড আলাদা করার নির্ভরযোগ্য নিয়ম
    parts = message.text.split()
    if len(parts) > 1:
        movie_code = parts[1]
    else:
        movie_code = "default"

    bot.send_message(message.chat.id, "🎬 Welcome to Sk Video Bot!\nPlease wait...")

    # ব্যবহারকারীর তথ্য লগ করা হচ্ছে
    user_id = message.chat.id
    username = message.chat.username
    first_name = message.chat.first_name
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_text = f"{now} - {first_name} (@{username}) - ID: {user_id} - Movie: {movie_code}\n"
    with open("log.txt", "a") as f:
        f.write(log_text)

    # JSON থেকে মুভি পাঠানো হচ্ছে
    movie = MOVIES.get(movie_code, MOVIES["default"])
    try:
        bot.copy_message(chat_id=message.chat.id,
                         from_chat_id=movie["chat_id"],
                         message_id=movie["msg_id"])
    except Exception as e:
        bot.send_message(message.chat.id, f"❌ ভিডিও পাঠানো যায়নি। এরর: {e}")

# keep_alive ফাংশনটি চালু করা হচ্ছে
keep_alive()

# বট সবসময় চালু রাখার জন্য
print("✅ Bot is running...")
bot.infinity_polling(timeout=10, long_polling_timeout=5)
