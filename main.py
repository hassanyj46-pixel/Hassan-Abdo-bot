import logging
import google.generativeai as genai
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# --- الإعدادات الخاصة بك ---
# توكن التليجرام الخاص بك من BotFather
TELEGRAM_TOKEN = '8516104095:AAFUuC0c79hDTXQ9j73eYf9IqE7HkR5H28k'

# مفتاح جوجل للذكاء الاصطناعي (Gemini API)
genai.configure(api_key="AIzaSyDMIOKTMjnpJ76H...") # تأكد أن المفتاح كامل هنا
model = genai.GenerativeModel('gemini-1.5-flash')

# لمراقبة عمل البوت (Logging) إعداد السجلات
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """لمعالجة الرسائل الواردة باستخدام الذكاء الاصطناعي"""
    user_text = update.message.text
    
    # إظهار حالة "جاري الكتابة" في تليجرام
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
    
    try:
        # الحصول على رد Gemini
        response = model.generate_content(user_text)
        await update.message.reply_text(response.text)
    except Exception as e:
        logging.error(f"Error: {e}")
        await update.message.reply_text("عذراً، واجهت مشكلة في معالجة طلبك.")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """رسالة الترحيب عند تشغيل البوت"""
    await update.message.reply_text("مرحباً! أنا بوت حسن عبدو المدعوم بالذكاء الاصطناعي. كيف يمكنني مساعدتك اليوم؟")

if __name__ == '__main__':
    # تشغيل البوت
    application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    
    # إضافة الأوامر والرسائل
    application.add_handler(CommandHandler('start', start))
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    
    print("✅ Hassan-Abdo-bot يعمل الآن ومستعد للإجابة...")
    application.run_polling()
