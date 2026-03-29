import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = os.environ.get("8696476223:AAEKSlLtQiyTpMapE9dkRepoEWHXERtqW2M")

# قاعدة بيانات طبية شاملة
MEDICAL_KNOWLEDGE = {
    "قلب": """❤️ *القلب*

📍 الموقع: وسط الصدر بين الرئتين
🔧 الوظيفة: ضخ الدم للجسم
🏗️ التركيب: 4 حجرات (أذين أيمن/أيسر، بطين أيمن/أيسر)
💓 معدل النبض: 60-100 نبضة/دقيقة

⚠️ أمراض شائعة: احتشاء عضلة القلب، فشل القلب، اضطراب النظم""",

    "دم": """🩸 *الدم*

🧪 المكونات:
• كريات حمراء (RBC): تنقل الأكسجين
• كريات بيضاء (WBC): المناعة
• صفائح دموية: التجلط
• بلازما: السائل الناقل

📊 الكمية: 5 لترات في الجسم البالغ
🩺 فصيلة الدم: A, B, AB, O""",

    "سكري": """🩺 *السكري*

📌 التعريف: ارتفاع سكر الدم عن الطبيعي

🔴 النوع الأول:
• يبدأ في الطفولة/المراهقة
• نقص كامل في الأنسولين
• العلاج: حقن الأنسولين

🔵 النوع الثاني:
• يبدأ في البلوغ/الشيخوخة
• مقاومة الأنسولين
• العلاج: حبوب + نظام غذائي

⚠️ الأعراض: عطش شديد، تبول متكرر، فقدان وزن، تعب""",

    "ضغط": """🩺 *ضغط الدم*

📊 التصنيف:
• طبيعي: أقل من 120/80
• مرتفع: 140/90 أو أكثر
• منخفض: أقل من 90/60

🔴 الأسباب: التوتر، الملح، السمنة، الوراثة

💊 العلاج: رياضة، نظام غذائي قليل الملح، أدوية""",

    "رئة": """🫁 *الرئة*

📍 الموقع: في الصدر على جانبي القلب
🔧 الوظيفة: تبادل الغازات (O2 داخل، CO2 خارج)
🏗️ التركيب: القصبة الهوائية → الشعب الهوائية → الحويصلات الهوائية

🫁 الحويصلات: 300 مليون حويصلة!
💨 القدرة: تستقبل 500 مليون متر مكعب من الهواء في العمر""",
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome = """🩺 *مساعد الطبيب الذكي*

مرحباً! أنا هنا لأساعدك في دراستك الطبية.

📚 *ما أستطيع الإجابة عنه:*
• ❤️ القلب
• 🩸 الدم
• 🩺 السكري
• 🩺 ضغط الدم
• 🫁 الرئة

💡 *اكتب أي كلمة وسأشرحها لك!*"""
    
    await update.message.reply_text(welcome, parse_mode='Markdown')

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower()
    
    # البحث في القاعدة
    found = False
    for keyword, response in MEDICAL_KNOWLEDGE.items():
        if keyword in text:
            await update.message.reply_text(response, parse_mode='Markdown')
            found = True
            break
    
    # لو ما لقينا الرد
    if not found:
        await update.message.reply_text(
            f"""📚 سألت عن: "{update.message.text}"

🔍 حالياً أستطيع الإجابة عن:
• ❤️ القلب
• 🩸 الدم
• 🩺 السكري
• 🩺 ضغط الدم
• 🫁 الرئة

💡 *جرب أن تسأل:* "ما هو القلب؟" أو "اشرح لي الدم"""",
            parse_mode='Markdown'
        )

app = Application.builder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

print("✅ البوت يعمل!")
app.run_polling()
