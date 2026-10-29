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

@bot.message_handler(commands=["stats"])
def stats(message):
    rows = db.get_totals_by_category(message.from_user.id)
    if len(rows) == 0:
        bot.reply_to(message, "Пока нет расходов")
        return

    total = 0
    lines = []
    for row in rows:
        lines.append(f"{row[0]}: {row[1]}")
        total = total + row[1]
    lines.append(f"Всего: {total}")
    bot.reply_to(message, "\n".join(lines))

@bot.message_handler(commands=["myid"])
def myid(message):
    bot.reply_to(message, f"Твой ID: {message.from_user.id}")

@bot.message_handler(commands=["partner"])
def partner(message):
    parts = message.text.split()
    if len(parts) != 2 or not parts[1].isdigit():
        bot.reply_to(message, "Напиши так: /partner ID, например: /partner 123456789")
        return

    db.set_partner(message.from_user.id, int(parts[1]))
    bot.reply_to(message, "Партнёр сохранён")


@bot.message_handler(commands=["share"])
def share(message):
    parts = message.text.split()
    if len(parts) != 2 or parts[1] not in ("on", "off"):
        bot.reply_to(message, "Напиши так: /share on или /share off")
        return

    if parts[1] == "on":
        db.set_share(message.from_user.id, 1)
        bot.reply_to(message, "Партнёр теперь видит твои расходы")
    else:
        db.set_share(message.from_user.id, 0)
        bot.reply_to(message, "Партнёр больше не видит твои расходы")

@bot.message_handler(commands=["family"])
def family(message):
    partner_id = db.get_visible_partner_id(message.from_user.id)
    if partner_id is None:
        bot.reply_to(
            message,
            "Нет доступа: партнёр не указан, не включил /share on "
            "или не добавил тебя как партнёра",
        )
        return

    rows = db.get_totals_by_category(partner_id)
    if len(rows) == 0:
        bot.reply_to(message, "У партнёра пока нет расходов")
        return

    lines = ["Расходы партнёра:"]
    total = 0
    for row in rows:
        lines.append(f"{row[0]}: {row[1]}")
        total = total + row[1]
    lines.append(f"Всего: {total}")
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