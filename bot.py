import os
import google.generativeai as genai
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# إعدادات البوت
TOKEN = os.environ.get("8696476223:AAEKSlLtQiyTpMapE9dkRepoEWHXERtqW2M")
GEMINI_KEY = os.environ.get("AIzaSyCMXHL7IagagEa_NpfDKtjkHmmgZZ1s7w8")

# إعداد Gemini
genai.configure(api_key=GEMINI_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome = """🩺 *مساعد الطبيب الذكي - النسخة المتقدمة*

مرحباً! أنا هنا لأساعدك في أي موضوع طبي.

🧠 *أستطيع الإجابة عن:*
• أي سؤال في التشريح
• الفيسيولوجيا والأمراض
• الأدوية والعلاجات
• الحالات السريرية
• التحضير للامتحانات

💡 *فقط اكتب سؤالك وسأجيبك!*"""
    
    await update.message.reply_text(welcome, parse_mode='Markdown')

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_question = update.message.text
    
    # إظهار "يكتب..."
    await update.message.chat.send_action(action="typing")
    
    try:
        # إرسال السؤال للذكاء الاصطناعي
        prompt = f"""أنت مساعد طبي متخصص لطلاب الطب. 
        قدم إجابة علمية دقيقة ومبسطة.
        استخدم الرموز التوضيحية مثل: 📍 🔧 ⚠️ 💊
        قسم الإجابة إلى نقاط واضحة.
        
        سؤال الطالب: {user_question}"""
        
        response = model.generate_content(prompt)
        answer = response.text
        
        # إرسال الإجابة
        if len(answer) > 4000:
            # تقسيم الرد الطويل
            parts = [answer[i:i+4000] for i in range(0, len(answer), 4000)]
            for part in parts:
                await update.message.reply_text(part)
        else:
            await update.message.reply_text(answer)
            
    except Exception as e:
        await update.message.reply_text(
            "⚠️ عذراً، حدث خطأ في الاتصال بالذكاء الاصطناعي.\n"
            "جرب مرة أخرى أو تأكد من المفتاح."
        )

# تشغيل البوت
app = Application.builder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

print("🤖 البوت الذكي يعمل!")
app.run_polling()
