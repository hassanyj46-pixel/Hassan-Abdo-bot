import logging
import os
import asyncio
import google.generativeai as genai
from telegram import Update
from telegram.constants import ChatAction
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# ====== الإعدادات ======
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
API_KEY = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
        return

    user_text = update.message.text
    await context.bot.send_chat_action(
        chat_id=update.effective_chat.id,
        action=ChatAction.TYPING
    )

    try:
        response = await asyncio.to_thread(
            model.generate_content,
            user_text
        )

        if response.text:
            await update.message.reply_text(response.text)
        else:
            await update.message.reply_text("❌ لم أستطع إنشاء رد حالياً.")

    except Exception as e:
        logging.error(e)
        await update.message.reply_text("⚠️ حدث خطأ تقني، حاول لاحقاً.")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 أهلاً بك! أنا بوت حسن عبدو المدعوم بـ Gemini 🤖"
    )

if __name__ == '__main__':
    application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    application.add_handler(CommandHandler('start', start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("✅ البوت يعمل الآن...")
    application.run_polling()
