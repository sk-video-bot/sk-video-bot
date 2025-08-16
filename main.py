import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# --- CONFIG ---
BOT_TOKEN = "8262301075:AAHNJHGbgw8MCK8NPOJlO1BOMM2xVFSxsfY"
ADMIN_ID = 6573815394   # তোমার টেলিগ্রাম আইডি
CHANNEL_ID = -1002912079356  # তোমার প্রাইভেট চ্যানেল আইডি

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(name)


# /start command
def start(update: Update, context: CallbackContext):
    update.message.reply_text("👋 Welcome! Send me a movie name to get started.")


# যখন user মুভি চাইবে (এখানে তুমি movies.json লোড করবে)
def handle_movie_request(update: Update, context: CallbackContext):
    movie_name = update.message.text.strip().lower()

    # TODO: এখানে movies.json থেকে lookup করতে হবে
    # এখন ডেমো হিসেবে শুধু রিপ্লাই করছে
    update.message.reply_text(f"🔍 You searched for: {movie_name}\n(এখন json lookup করতে হবে)")


# --- নতুন ফিচার ---
# যখনই প্রাইভেট চ্যানেলে ভিডিও/ডকুমেন্ট আসবে
def channel_post(update: Update, context: CallbackContext):
    message = update.channel_post

    file_id = None
    file_name = None

    if message.video:
        file_id = message.video.file_id
        file_name = message.caption or "video.mp4"
    elif message.document:
        file_id = message.document.file_id
        file_name = message.document.file_name

    if file_id:
        text = (
            "📂 New Movie Uploaded!\n\n"
            f"File: {file_name}\n"
            f"Channel ID: {CHANNEL_ID}\n"
            f"Message ID: {message.message_id}\n"
            f"File ID: {file_id}"
        )
        # অ্যাডমিনকে পাঠানো হবে
        context.bot.send_message(chat_id=ADMIN_ID, text=text)


def main():
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    # Commands
    dp.add_handler(CommandHandler("start", start))

    # User movie request
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_movie_request))

    # Channel post handler
    dp.add_handler(MessageHandler(Filters.update.channel_posts, channel_post))

    # Start the Bot
    updater.start_polling()
    updater.idle()


if name == "main":
    main()
