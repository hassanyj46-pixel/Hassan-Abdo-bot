import logging
import google.generativeai as genai
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# --- الإعدادات الخاصة بك ---
# توكن التليجرام الخاص بك من BotFather
TELEGRAM_TOKEN = '8516104095:AAFUuC0c79hDTXQ9j73eYf9IqE7HkR5H28k'

# مفتاح جوجل للذكاء الاصطناعي (Gemini API)
# ملاحظة: تأكد من وضع مفتاحك الكامل هنا
genai.configure(api_key="AIzaSyDMIOKTMjnpJ76H...") 
model = genai.GenerativeModel('gemini-1.5-flash')

# إعداد السجلات لمراقبة أداء البوت
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """معالجة الرسائل الواردة باستخدام الذكاء الاصطناعي"""
    user_text = update.message.text
    
    # إظهار حالة "جاري الكتابة" لإعطاء انطباع بالذكاء
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
    
    try:
        # توليد الرد من نموذج Gemini
        response = model.generate_content(user_text)
        if response.text:
            await update.message.reply_text(response.text)
        else:
            await update.message.reply_text("عذراً، لم أستطع تكوين رد مناسب حالياً.")
    except Exception as e:
        logging.error(f"خطأ في Gemini: {e}")
        await update.message.reply_text("أواجه مشكلة بسيطة في الاتصال بعقلي الاصطناعي، حاول ثانية!")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """الرسالة التي تظهر عند كتابة /start"""
    await update.message.reply_text("أهلاً بك! أنا بوت الذكاء الاصطناعي الخاص بحسن عبدو. اسألني عن أي شيء!")

if __name__ == '__main__':
    # بناء وتشغيل تطبيق تليجرام
    application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    
    # تعريف الأوامر والرسائل
    application.add_handler(CommandHandler('start', start))
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    
    # رسالة التأكيد في السجلات
    print("✅ البوت يعمل الآن بنجاح ومستعد لاستقبال الرسائل!")
    application.run_polling()
 
