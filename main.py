import os
from flask import Flask

# Flask app - لازم يكون اسمه app عشان gunicorn يلاقيه
app = Flask(__name__)

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

@app.route("/")
def home():
    books_html = "<br>".join(BOOKS)
    html = f"""
    <html dir="rtl" lang="ar">
    <head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
    <title>Dar Qandil - متجر الكتب</title>
    <style>
        body{{font-family:system-ui;background:#f8f5f0;padding:20px;text-align:center}}
        .card{{background:white;padding:20px;border-radius:16px;max-width:500px;margin:auto;box-shadow:0 4px 20px rgba(0,0,0,.1)}}
        .btn{{background:#2d6a4f;color:white;padding:12px 20px;border-radius:10px;text-decoration:none;display:inline-block;margin:10px}}
    </style>
    </head>
    <body>
      <div class="card">
        <h1>📚 دار قنديل</h1>
        <h2>🎁 عرض 5 كتب بـ 10 دنانير</h2>
        <p>اختر 5 كتب بالضبط. التوصيل 2 دينار ويضاف عند التأكيد.</p>
        <p>الكتب المتوفرة:</p>
        <p>{books_html}</p>
        <a class="btn" href="https://t.me/Dar_qandil">اطلب عبر تيليجرام</a>
        <p style="margin-top:20px">للطلب واتساب: ابعت اسماء الـ 5 كتب + عنوانك</p>
        <p><b>السعر: 10 + 2 توصيل = 12 دينار</b></p>
        <p style="color:green;margin-top:20px">✅ الموقع شغال 100%</p>
      </div>
    </body>
    </html>
    """
    return html

# هذا للمحلي فقط - Render بستخدم gunicorn
if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)


