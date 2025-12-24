import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters
import google.generativeai as genai

# 1. إعداد توكن التليجرام الخاص بك (من BotFather)
TELEGRAM_TOKEN = 'ضع_توكن_التليجرام_هنا'

# 2. إعداد مفتاح جوجل للذكاء الاصطناعي (Gemini API)
genai.configure(api_key="ضع_مفتاح_جيمناي_هنا")
model = genai.GenerativeModel('gemini-1.5-flash')

# إعداد السجلات (Logging) لمراقبة الأخطاء
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    
    # إظهار حالة "جاري الكتابة" في التليجرام
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
    
    try:
        # إرسال سؤال المستخدم للذكاء الاصطناعي
        response = model.generate_content(user_text)
        
        # إرسال إجابة الذكاء الاصطناعي للمستخدم في تليجرام
        await update.message.reply_text(response.text)
    except Exception as e:
        await update.message.reply_text("عذراً، حدث خطأ ما أثناء معالجة طلبك.")
        print(f"Error: {e}")

if __name__ == '__main__':
    application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    
    # جعل البوت يرد على أي رسالة نصية
    text_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message)
    application.add_handler(text_handler)
    
    print("✅ البوت يعمل الآن باستخدام بايثون...")
    application.run_polling()
