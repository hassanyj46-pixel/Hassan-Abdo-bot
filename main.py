import logging
import google.generativeai as genai
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters

# --- الإعدادات الخاصة بك ---
# توكن التليجرام الخاص بك من BotFather
TELEGRAM_TOKEN = '8516104095:AAFUuCOc79hDTXQ6VupgpPva0D3RHDtJaF4'

# مفتاح جوجل للذكاء الاصطناعي (Gemini API)
genai.configure(api_key="AIzaSyDMI0KTMjnpJ7L6Z04e2xfP-Uc7XdSZJhE")
model = genai.GenerativeModel('gemini-1.5-flash')

# إعداد السجلات (Logging) لمراقبة عمل البوت
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """دالة لمعالجة الرسائل الواردة باستخدام الذكاء الاصطناعي"""
    user_text = update.message.text
    
    # إظهار حالة "جاري الكتابة" في تليجرام
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
    
    try:
        # إرسال النص إلى Gemini والحصول على رد
        response = model.generate_content(user_text)
        
        # إرسال رد الذكاء الاصطناعي للمستخدم
        await update.message.reply_text(response.text)
    except Exception as e:
        logging.error(f"خطأ في معالجة الرسالة: {e}")
        await update.message.reply_text("عذراً، واجهت مشكلة في معالجة طلبك حالياً.")

if __name__ == '__main__':
    # بناء التطبيق
    application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    
    # معالج الرسائل النصية (يستجيب لجميع الرسائل ما عدا الأوامر)
    text_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message)
    application.add_handler(text_handler)
    
    print("✅ Hassan-Abdo-bot يعمل الآن ومستعد للإجابة...")
    
    # تشغيل البوت بنظام الطلبات المتكررة (Polling)
    application.run_polling()
