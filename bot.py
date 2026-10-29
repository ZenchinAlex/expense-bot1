import os

import telebot
from dotenv import load_dotenv
import db


load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
db.init_db()

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=["start"])
def start(message):
    bot.reply_to(message, "Привет! Я бот для учёта расходов.")


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
    db.add_expense(message.from_user.id, title, amount)
    bot.reply_to(message, f"Записал: {title}, сумма {amount}")

print("Бот запущен")
bot.infinity_polling()