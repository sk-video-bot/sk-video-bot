import os
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes

# Environment থেকে token এবং id নিবে
BOT_TOKEN = os.getenv("BOT_TOKEN")
USER_ID = int(os.getenv("USER_ID", "0"))
CHANNEL_ID = int(os.getenv("CHANNEL_ID", "-1002912079356"))

async def forward_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message:
        # Channel এ মেসেজ এলেই তোমাকে পাঠাবে
        await context.bot.send_message(
            chat_id=USER_ID,
            text=f"Message ID: {update.message.message_id}\nChannel ID: {CHANNEL_ID}"
        )

def main():
    if not BOT_TOKEN:
        print("❌ BOT_TOKEN পাওয়া যায়নি! Render/GitHub এ Environment Variable সেট করো।")
        return

    application = Application.builder().token(BOT_TOKEN).build()

    # সব ধরনের মেসেজ ধরার জন্য হ্যান্ডলার
    application.add_handler(MessageHandler(filters.ALL, forward_message))

    print("✅ Bot is running...")
    application.run_polling()

if name == "main":
    main()
