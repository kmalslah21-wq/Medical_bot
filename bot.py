import os
from google import genai
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# التوكن والمفتاح
TOKEN = os.environ.get("8696476223:AAEKSlLtQiyTpMapE9dkRepoEWHXERtqW2M")
GEMINI_KEY = os.environ.get("AIzaSyCMXHL7IagagEa_NpfDKtjkHmmgZZ1s7w8")

# طباعة للتأكد
print(f"TOKEN موجود: {bool(TOKEN)}")
print(f"GEMINI_KEY موجود: {bool(GEMINI_KEY)}")

if not TOKEN:
    print("❌ خطأ: TOKEN غير موجود!")
    exit(1)

# إعداد Gemini
try:
    client = genai.Client(api_key=GEMINI_KEY)
    print("✅ Gemini متصل")
except Exception as e:
    print(f"⚠️ Gemini غير متصل: {e}")
    client = None

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome = """🩺 *مساعد الطبيب الذكي*

مرحباً! أنا هنا لأساعدك في أي موضوع طبي.

🧠 *اسألني عن:*
• التشريح والفيسيولوجيا
• الأمراض والعلاجات
• الحالات السريرية
• التحضير للامتحانات

💡 *اكتب سؤالك وسأجيبك!*"""
    
    await update.message.reply_text(welcome, parse_mode='Markdown')

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_question = update.message.text
    await update.message.chat.send_action(action="typing")
    
    # إذا Gemini متصل
    if client:
        try:
            response = client.models.generate_content(
                model="gemini-2.0-flash",
                contents=f"""أنت مساعد طبي متخصص. أجب بشكل علمي دقيق ومبسط.
                استخدم رموز: 📍 🔧 ⚠️ 💊
                
                السؤال: {user_question}"""
            )
            await update.message.reply_text(response.text)
            return
        except Exception as e:
            print(f"خطأ Gemini: {e}")
    
    # رد احتياطي
    await update.message.reply_text(
        f"📚 سألت عن: {user_question}\n\n"
        f"⚠️ الذكاء الاصطناعي غير متصل حالياً.\n"
        f"جاري إصلاح المشكلة..."
    )

app = Application.builder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

print("🚀 البوت يعمل!")
app.run_polling()
