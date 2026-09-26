import os
import threading
from flask import Flask
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# حط التوكن في Secrets باسم BOT_TOKEN
TOKEN = os.getenv("BOT_TOKEN") or os.getenv("TELEGRAM_TOKEN")

# قائمة الكتب
BOOKS = [
    "كتاب تطوير الذات",
    "رواية عربية قصيرة",
    "قصص أطفال",
    "تعلم الإنجليزية بسهولة",
    "وصفات منزلية",
    "كتاب تاريخي",
    "كتاب ديني",
    "كتاب طبخ",
]

# سلة كل مستخدم
user_baskets = {}

# ===== موقع الويب عشان يبطل 404 =====
app = Flask(__name__)

@app.route("/")
def home():
    html = """
    <html dir="rtl" lang="ar">
    <head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
    <title>Dar Qandil - متجر الكتب</title>
    <style>body{font-family:system-ui;background:#f8f5f0;padding:20px;text-align:center} .card{background:white;padding:20px;border-radius:16px;max-width:500px;margin:auto;box-shadow:0 4px 20px rgba(0,0,0,.1)} .btn{background:#2d6a4f;color:white;padding:12px 20px;border-radius:10px;text-decoration:none;display:inline-block;margin:10px}</style>
    </head>
    <body>
      <div class="card">
        <h1>📚 دار قنديل</h1>
        <h2>🎁 عرض 5 كتب بـ 10 دنانير</h2>
        <p>اختر 5 كتب بالضبط. التوصيل 2 دينار ويضاف عند التأكيد.</p>
        <p>الكتب المتوفرة:</p>
        <p>""" + "<br>".join(BOOKS) + """</p>
        <a class="btn" href="https://t.me/Dar_qandil">اطلب عبر تيليجرام</a>
        <p style="margin-top:20px">للطلب واتساب: ابعت اسماء الـ 5 كتب + عنوانك</p>
        <p><b>السعر: 10 + 2 توصيل = 12 دينار</b></p>
      </div>
    </body>
    </html>
    """
    return html

def run_flask():
    port = int(__import__("os").getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

# ===== بوت التيليجرام =====
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_baskets[user_id] = []
    keyboard = []
    for book in BOOKS:
        keyboard.append([InlineKeyboardButton(f"أضف للعرض • {book}", callback_data=f"add:{book}")])
    keyboard.append([InlineKeyboardButton("🧺 عرض سلة العرض", callback_data="show_basket")])
    keyboard.append([InlineKeyboardButton("📚 كتب فردية (3 دنانير)", callback_data="single")])
    keyboard.append([InlineKeyboardButton("🔙 رجوع للرئيسية", callback_data="home")])
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "🎁 عرض 5 كتب بـ 10 دنانير\n\nاختار 5 كتب بالضبط. التوصيل 2 دينار وينضاف عند التأكيد.",
        reply_markup=reply_markup
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    data = query.data
    if user_id not in user_baskets:
        user_baskets[user_id] = []
    
    if data.startswith("add:"):
        book = data[4:]
        if len(user_baskets[user_id]) >= 5:
            await query.message.reply_text("❌ اخترت 5 كتب بالضبط! اعرض السلة للتأكيد.")
            return
        user_baskets[user_id].append(book)
        count = len(user_baskets[user_id])
        await query.message.reply_text(f"✅ أضفت: {book}\nالسلة: {count}/5")
        if count == 5:
            await query.message.reply_text(f"🎉 اكتملت السلة! 5 كتب\nالسعر 10 + توصيل 2 = 12 دينار\nارسل عنوانك ورقم تلفونك للتأكيد.")
    elif data == "show_basket":
        basket = user_baskets.get(user_id, [])
        if not basket:
            await query.message.reply_text("السلة فاضية.")
        else:
            text = "🧺 سلة العرض:\n" + "\n".join([f"{i+1}. {b}" for i,b in enumerate(basket)]) + f"\n\nالعدد: {len(basket)}/5\nالسعر: 10 دنانير + 2 توصيل = 12"
            if len(basket) < 5:
                text += f"\nباقي {5-len(basket)} كتب"
            await query.message.reply_text(text)
    elif data == "home":
        await start(update, context)
    elif data == "single":
        await query.message.reply_text("الكتاب الفردي بـ 3 دنانير + توصيل 2. ابعت اسم الكتاب اللي بدك ياه.")

def main():
    # شغل موقع الويب بخيط لحاله
    threading.Thread(target=run_flask, daemon=True).start()
    
    if not TOKEN:
        print("حط BOT_TOKEN في Secrets!")
        # خلي Flask شغال حتى لو ما في توكن عشان ما يطلع 404
        port = int(__import__("os").getenv("PORT", 5000))
        app.run(host="0.0.0.0", port=port)
        return

    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_handler))
    print("البوت شغال 100%...")
    application.run_polling()

if __name__ == "__main__":
    main()
