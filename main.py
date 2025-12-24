import logging
import google.generativeai as genai
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# --- الإعدادات الخاصة بك ---
# توكن التليجرام الخاص بك
TELEGRAM_TOKEN = '8516104095:AAFUuC0c79hDTXQ9j73eYf9IqE7HkR5H28k'

# مفتاح Gemini API (تأكد من وضعه كاملاً بين علامات التنصيص)
API_KEY = "AIzaSyDMIOKTMjnpJ76H..." # ضع مفتاحك الكامل هنا

# إعداد الذكاء الاصطناعي مع الإصدار الصحيح
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# إعداد سجلات المراقبة
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """معالجة الرسائل باستخدام Gemini"""
    user_text = update.message.text
    
    # إظهار حالة الكتابة في تليجرام
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
    
    try:
        # طلب الرد من الذكاء الاصطناعي
        response = model.generate_content(user_text)
        await update.message.reply_text(response.text)
    except Exception as e:
        logging.error(f"خطأ: {e}")
        await update.message.reply_text("عذراً، لم أستطع معالجة رسالتك الآن.")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """ترحيب البوت"""
    await update.message.reply_text("مرحباً! أنا بوت Hassan AI. اسألني أي شيء وسأجيبك فوراً.")

if __name__ == '__main__':
    # تشغيل البوت
    application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    
    application.add_handler(CommandHandler('start', start))
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    
    print("✅ البوت يعمل الآن بنجاح...")
    application.run_polling()
 
