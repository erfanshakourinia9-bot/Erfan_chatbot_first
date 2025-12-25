import os
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters
from openai import OpenAI

# دریافت کلیدها از Environment Variables
TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OPENAI_KEY = os.getenv("OPENAI_API_KEY")

# بررسی اینکه کلیدها تعریف شده باشند
if not TELEGRAM_TOKEN or not OPENAI_KEY:
    raise ValueError("TELEGRAM_BOT_TOKEN یا OPENAI_API_KEY تعریف نشده است!")

# اتصال به OpenAI
client = OpenAI(api_key=OPENAI_KEY)

# تابع پاسخ به پیام‌ها
async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text

    try:
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {"role": "system", "content": "مثل یه دوست باهوش و صمیمی جواب بده."},
                {"role": "user", "content": user_text}
            ]
        )
        reply = response.choices[0].message.content
    except Exception as e:
        reply = "متاسفم، خطایی پیش اومد!"

    await update.message.reply_text(reply)

# ساخت اپلیکیشن تلگرام
async def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    # اضافه کردن Handler برای پیام‌های متنی
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))

    # اجرای بات
    await app.run_polling()

# اجرای برنامه
if __name__ == "__main__":
    asyncio.run(main())
