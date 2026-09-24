from keep_alive import keep_alive
import telebot, os, json, datetime, threading, time

TOKEN = os.getenv("TOKEN")
bot = telebot.TeleBot(TOKEN)

with open("movies.json", "r", encoding="utf-8") as f:
    MOVIES = json.load(f)

def log_event(text):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("log.txt", "a", encoding="utf-8") as f:
        f.write(f"{now} - {text}\n")

def delete_later(chat_id, msg_id):
    time.sleep(3600)
    try:
        bot.delete_message(chat_id, msg_id)
        log_event(f"Deleted {msg_id} from {chat_id}")
    except Exception as e:
        log_event(f"Delete error: {e}")

def safe_send(chat_id, text):
    try:
        return bot.send_message(chat_id, text)
    except Exception as e:
        log_event(f"Send error: {e}")

@bot.message_handler(commands=["start"])
def send_movie(message):
    try:
        parts = message.text.split()
        code = parts[1] if len(parts) > 1 else "default"

        safe_send(
            message.chat.id,
            "🎬 Welcome to Viral Video Bot!\nPlease wait..."
        )

        log_event(
            f"{message.chat.first_name} (@{message.chat.username}) "
            f"ID:{message.chat.id} Movie:{code}"
        )

        movie = MOVIES.get(code, MOVIES["default"])

        sent = bot.copy_message(
            message.chat.id,
            movie["chat_id"],
            movie["msg_id"]
        )

        threading.Thread(
            target=delete_later,
            args=(message.chat.id, sent.message_id),
            daemon=True
        ).start()

    except Exception as e:
        safe_send(
            message.chat.id,
            "❌ ভিডিও পাঠানো যায়নি। পরে আবার চেষ্টা করো।"
        )
        log_event(f"Movie error: {e}")

keep_alive()

# 409 Conflict fix
try:
    bot.delete_webhook(drop_pending_updates=False)
    print("✅ Webhook deleted")
except Exception as e:
    print(f"Webhook error: {e}")

print("✅ Bot is running...")

while True:
    try:
        bot.infinity_polling(
            timeout=60,
            long_polling_timeout=30,
            skip_pending=False
        )
    except Exception as e:
        log_event(f"Polling error: {e}")
        print(f"❌ Error: {e}")
        time.sleep(5)
