import os
import json
import telebot

# -----------------------------
# ENVIRONMENT থেকে BOT_TOKEN লোড
# Render / Railway / Heroku তে BOT_TOKEN নামে রাখবে
# -----------------------------
TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = -1002912079356   # তোমার প্রাইভেট চ্যানেলের ID বসাও

bot = telebot.TeleBot(TOKEN, parse_mode="HTML")

MOVIES_FILE = "movies.json"

# -----------------------------
# movies.json না থাকলে তৈরি করবে
# -----------------------------
if not os.path.exists(MOVIES_FILE):
    with open(MOVIES_FILE, "w", encoding="utf-8") as f:
        json.dump([], f, ensure_ascii=False, indent=4)


# -----------------------------
# movies.json এ নতুন এন্ট্রি সেভ
# -----------------------------
def save_movie(message):
    with open(MOVIES_FILE, "r", encoding="utf-8") as f:
        movies = json.load(f)

    movie_entry = {
        "message_id": message.message_id,
        "file_id": None,
        "caption": message.caption if message.caption else ""
    }

    # ভিডিও বা ডকুমেন্ট হলে file_id নিবে
    if message.video:
        movie_entry["file_id"] = message.video.file_id
    elif message.document:
        movie_entry["file_id"] = message.document.file_id

    movies.append(movie_entry)

    with open(MOVIES_FILE, "w", encoding="utf-8") as f:
        json.dump(movies, f, ensure_ascii=False, indent=4)

    print(f"[✅] Saved Movie -> {movie_entry}")


# -----------------------------
# চ্যানেলে নতুন পোস্ট আসলেই সেভ করবে
# -----------------------------
@bot.channel_post_handler(func=lambda m: True)
def get_channel_post(message):
    try:
        save_movie(message)
    except Exception as e:
        print(f"[❌] Error: {e}")


# -----------------------------
# /start কমান্ড
# -----------------------------
@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "🎬 Welcome! Send me a movie name to search.")


# -----------------------------
# মুভি সার্চ সিস্টেম
# -----------------------------
@bot.message_handler(func=lambda m: True)
def search_movie(message):
    query = message.text.strip().lower()

    with open(MOVIES_FILE, "r", encoding="utf-8") as f:
        movies = json.load(f)

    results = [m for m in movies if query in m["caption"].lower()]

    if not results:
        bot.reply_to(message, "❌ Movie not found!")
        return

    for movie in results:
        try:
            if movie["file_id"]:
                bot.send_video(
                    message.chat.id,
                    movie["file_id"],
                    caption=movie["caption"]
                )
            else:
                # যদি file_id না থাকে তাহলে ফরওয়ার্ড করবে
                bot.forward_message(
                    message.chat.id,
                    CHANNEL_ID,
                    movie["message_id"]
                )
        except Exception as e:
            bot.reply_to(message, f"⚠️ Error sending movie: {e}")


# -----------------------------
print("🤖 Bot is running... Watching channel + serving users.")
bot.infinity_polling()
