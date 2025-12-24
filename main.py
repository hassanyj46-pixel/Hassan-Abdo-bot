import logging
import google.generativeai as genai
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# --- الإعدادات الخاصة بك ---
# توكن التليجرام الخاص بك (من BotFather)
TELEGRAM_TOKEN = '8516104095:AAFUuC0c79hDTXQ9j73eYf9IqE7HkR5H28k'

# مفتاح جوجل للذكاء الاصطناعي (Gemini API)
# تم وضع المفتاح الذي ظهر في صورتك الأخيرة
API_KEY = "AIzaSyDMIOKTMjnpJ76H1YIqE7HkR5H28k" 

# إعداد نموذج Gemini بشكل صحيح
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# إعداد السجلات لمراقبة عمل البوت في Render
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """معالجة الرسائل النصية الواردة من المستخدم"""
    user_text = update.message.text
    
    # إظهار حالة "جاري الكتابة" في تليجرام
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
    
    try:
        # الحصول على الرد من ذكاء Gemini الاصطناعي
        response = model.generate_content(user_text)
        await update.message.reply_text(response.text)
    except Exception as e:
        logging.error(f"Error: {e}")
        await update.message.reply_text("عذراً، واجهت مشكلة في معالجة طلبك.")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """رسالة الترحيب عند بدء المحادثة"""
    await update.message.reply_text("مرحباً! أنا بوت Hassan AI المدعوم بذكاء Gemini. كيف يمكنني مساعدتك اليوم؟")

if __name__ == '__main__':
    # تشغيل البوت وربطه بتليجرام
    application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    
    # إضافة الأوامر ومعالجة الرسائل
    application.add_handler(CommandHandler('start', start))
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    
    print("✅ Hassan-Abdo-bot يعمل الآن ومستعد للإجابة...")
    application.run_polling()
