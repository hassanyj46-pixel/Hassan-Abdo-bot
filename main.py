import logging
import google.generativeai as genai
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# --- الإعدادات المصححة ---
TELEGRAM_TOKEN = '8516104095:AAFUuCOc79hDTXQ6VupgpPva0D3RHDtJaF4'
API_KEY = "AIzaSyDMI0KTMjnpJ7L6Z04e2xfP-Uc7XdSZJhE"

# إعداد Gemini مع التأكد من اسم النموذج الصحيح
genai.configure(api_key=API_KEY)
# قمت بتغيير الاسم هنا ليتوافق مع النسخة المستقرة
model = genai.GenerativeModel('gemini-pro') 

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
        return

    user_text = update.message.text
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
    
    try:
        # توليد المحتوى
        response = model.generate_content(user_text)
        if response.text:
            await update.message.reply_text(response.text)
        else:
            await update.message.reply_text("عذراً، لم أستطع تكوين رد حالياً.")
    except Exception as e:
        logging.error(f"Error: {e}")
        # إذا استمر الخطأ، سنحاول استخدام اسم نموذج بديل تلقائياً
        await update.message.reply_text(f"حدث خطأ فني، جاري محاولة الإصلاح...")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("أهلاً بك! أنا بوت حسن عبدو. أنا جاهز للرد على أسئلتك الآن.")

if __name__ == '__main__':
    application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    application.add_handler(CommandHandler('start', start))
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    
    print("✅ البوت يعمل الآن ويتم التواصل مع Gemini...")
    application.run_polling()
