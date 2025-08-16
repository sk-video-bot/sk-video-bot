import os
import telebot

# 🔹 Environment থেকে টোকেন নেবে
BOT_TOKEN = os.getenv("BOT_TOKEN")

# 🔹 ফিক্সড ভ্যালু (তোমার নিজের আইডি আর চ্যানেল আইডি বসাও)
ADMIN_ID = 6573815394
CHANNEL_ID = -1002912079356

# 🔹 বট তৈরি
bot = telebot.TeleBot(BOT_TOKEN)

# ✅ Start Command
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "👋 হ্যালো! আমি SK Video Bot.\n\nযেকোনো মুভি/ভিডিও লিস্ট পেতে কমান্ড ব্যবহার করুন।")

# ✅ চ্যানেল থেকে ভিডিও পাঠানো টেস্ট (শুধু এডমিন করতে পারবে)
@bot.message_handler(commands=['test'])
def send_from_channel(message):
    if message.from_user.id == ADMIN_ID:
        try:
            bot.forward_message(message.chat.id, CHANNEL_ID, 1)  # চ্যানেল থেকে মেসেজ আইডি=1 ফরওয়ার্ড করবে
            bot.reply_to(message, "✅ চ্যানেল থেকে ভিডিও ফরওয়ার্ড হলো।")
        except Exception as e:
            bot.reply_to(message, f"⚠️ সমস্যা: {e}")
    else:
        bot.reply_to(message, "❌ আপনি এই কমান্ড ব্যবহার করতে পারবেন না।")

# ✅ বট চালু রাখা
print("🤖 Bot is running...")
bot.polling(none_stop=True, timeout=60)
