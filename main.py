from keep_alive import keep_alive
import telebot
from telebot.types import Message
import os
import json
import datetime
import threading
import time

# ===== CONFIGURATION =====
TOKEN = os.getenv("TOKEN")
CHANNEL_USERNAME = "@sk_viral_video25"
CHANNEL_ID = -1002912079356
DELETE_DELAY = 3600  # seconds (1 hour)
RETRY_COUNT = 3

bot = telebot.TeleBot(TOKEN)

# Load movies.json
with open("movies.json", "r") as f:
    MOVIES = json.load(f)

# ===== LOGGING =====
def log_event(text):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("log.txt", "a") as f:
        f.write(f"{now} - {text}\n")
    print(f"{now} - {text}")

# ===== MESSAGE DELETE FUNCTION =====
def delete_message_later(chat_id, message_id, delay=DELETE_DELAY, retry=RETRY_COUNT):
    for attempt in range(retry):
        time.sleep(delay if attempt == 0 else 10)  # first attempt delay, retry faster
        try:
            bot.delete_message(chat_id, message_id)
            log_event(f"✅ Deleted message {message_id} from chat {chat_id}")
            break
        except Exception as e:
            log_event(f"❌ Delete failed for {message_id} in chat {chat_id}, attempt {attempt+1}: {e}")

# ===== AUTO FORWARD FUNCTION =====
def auto_forward_new_post(message):
    try:
        for movie_code in MOVIES:
            movie = MOVIES[movie_code]
            if movie["chat_id"] == CHANNEL_ID and message.message_id == movie["msg_id"]:
                log_event(f"🔄 Auto-forward triggered for movie: {movie_code}")
                bot.copy_message(chat_id=message.chat.id, from_chat_id=CHANNEL_ID, message_id=message.message_id)
    except Exception as e:
        log_event(f"❌ Auto-forward failed: {e}")

# ===== START COMMAND =====
@bot.message_handler(commands=['start'])
def send_movie(message: Message):
    parts = message.text.split()
    movie_code = parts[1] if len(parts) > 1 else "default"

    bot.send_message(message.chat.id, "🎬 Welcome to Sk Video Bot!\nPlease wait...")

    user_id = message.chat.id
    username = message.chat.username or "NoUsername"
    first_name = message.chat.first_name or "NoName"
    log_event(f"{first_name} (@{username}) - ID: {user_id} - Movie: {movie_code}")

    movie = MOVIES.get(movie_code, MOVIES.get("default"))
    if not movie:
        bot.send_message(message.chat.id, "❌ No movie found.")
        return

    try:
        sent_msg = bot.copy_message(
            chat_id=message.chat.id,
            from_chat_id=movie["chat_id"],
            message_id=movie["msg_id"]
        )
        threading.Thread(target=delete_message_later, args=(message.chat.id, sent_msg.message_id)).start()
    except Exception as e:
        bot.send_message(message.chat.id, f"❌ ভিডিও পাঠানো যায়নি। এরর: {e}")
        log_event(f"❌ Failed to send movie {movie_code} to {user_id}: {e}")

# ===== CHANNEL LISTENER =====
@bot.channel_post_handler(func=lambda m: True)
def handle_channel_post(message: Message):
    log_event(f"📢 New post detected in channel {CHANNEL_USERNAME}")
    auto_forward_new_post(message)

# ===== MAIN =====
if name == "main":
    keep_alive()
    log_event("✅ Bot is running...")
    bot.infinity_polling(timeout=10, long_polling_timeout=5)
