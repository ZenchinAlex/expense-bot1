import os

import telebot
from dotenv import load_dotenv
import db
import categories

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
db.init_db()

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=["start"])
def start(message):
    bot.reply_to(message, "Привет! Я бот для учёта расходов.")

@bot.message_handler(commands=["list"])
def list_expenses(message):
    rows = db.get_last_expenses(message.from_user.id)
    if len(rows) == 0:
        bot.reply_to(message, "Пока нет расходов")
        return

    lines = []
    for row in rows:
        lines.append(f"{row[0]} — {row[1]}")
    bot.reply_to(message, "\n".join(lines))

@bot.message_handler(content_types=["text"])
def add_expense(message):
    parts = message.text.split()
    if len(parts) < 2:
        bot.reply_to(message, "Напиши так: название сумма, например: кофе 150")
        return

    try:
        amount = float(parts[-1])
    except ValueError:
        bot.reply_to(message, "Сумма должна быть числом, например: кофе 150")
        return

    title = " ".join(parts[:-1])
    category = categories.detect_category(title)
    db.add_expense(message.from_user.id, title, amount, category)
    bot.reply_to(message, f"Записал: {title}, сумма {amount}, категория: {category}")
    
print("Бот запущен")
bot.infinity_polling()