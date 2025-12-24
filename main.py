import logging
import google.generativeai as genai
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# --- الإعدادات الخاصة بك ---
# توكن التليجرام الخاص بك
TELEGRAM_TOKEN = '8516104095:AAFUuC0c79hDTXQ9j73eYf9IqE7HkR5H28k'

# مفتاح Gemini API الجديد الذي أرسلته
API_KEY = "AIzaSyDMI0KTMjnpJ7L6Z04e2xfP-Uc7XdSZJhE"

# إعداد نموذج Gemini بشكل صحيح
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# إعداد السجلات لمراقبة العمل
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """معالجة الرسائل الواردة باستخدام الذكاء الاصطناعي"""
    user_text = update.message.text
    
    # إظهار حالة "جاري الكتابة" في تليجرام
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
    
    try:
        # الحصول على الرد من Gemini
        response = model.generate_content(user_text)
        if response.text:
            await update.message.reply_text(response.text)
        else:
            await update.message.reply_text("عذراً، لم أستطع تكوين رد حالياً.")
    except Exception as e:
        logging.error(f"Error: {e}")
        # إذا حدث خطأ، سيخبرك البوت بنوع الخطأ لسهولة الإصلاح
        await update.message.reply_text(f"حدث خطأ فني: {str(e)}")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """رسالة الترحيب"""
    await update.message.reply_text("أهلاً بك! أنا بوت حسن عبدو المطور. كيف يمكنني مساعدتك اليوم؟")

if __name__ == '__main__':
    # تشغيل البوت وربطه بتليجرام
    application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    
    # إضافة الأوامر ومعالجة الرسائل
    application.add_handler(CommandHandler('start', start))
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    
    print("✅ البوت يعمل الآن بنجاح...")
    application.run_polling()
