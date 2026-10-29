import sqlite3

DB_NAME = "expenses.db"


def init_db():
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY,
            user_id INTEGER,
            title TEXT,
            amount REAL,
            category TEXT,
            created_at TEXT
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS partners (
            user_id INTEGER PRIMARY KEY,
            partner_id INTEGER,
            share INTEGER DEFAULT 0
        )
    """)
    connection.commit()
    connection.close()


def add_expense(user_id, title, amount, category):
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()
    cursor.execute(
        "INSERT INTO expenses (user_id, title, amount, category, created_at) "
        "VALUES (?, ?, ?, ?, datetime('now'))",
        (user_id, title, amount, category),
    )
    connection.commit()
    connection.close()


def get_last_expenses(user_id, limit=10):
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()
    cursor.execute(
        "SELECT title, amount, created_at FROM expenses "
        "WHERE user_id = ? ORDER BY id DESC LIMIT ?",
        (user_id, limit),
    )
    rows = cursor.fetchall()
    connection.close()
    return rows

def get_totals_by_category(user_id):
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()
    cursor.execute(
        "SELECT category, SUM(amount) FROM expenses "
        "WHERE user_id = ? GROUP BY category ORDER BY SUM(amount) DESC",
        (user_id,),
    )
    rows = cursor.fetchall()
    connection.close()
    return rows

def set_partner(user_id, partner_id):
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()
    cursor.execute(
        "INSERT INTO partners (user_id, partner_id) VALUES (?, ?) "
        "ON CONFLICT(user_id) DO UPDATE SET partner_id = excluded.partner_id",
        (user_id, partner_id),
    )
    connection.commit()
    connection.close()


def set_share(user_id, share):
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()
    cursor.execute(
        "INSERT INTO partners (user_id, share) VALUES (?, ?) "
        "ON CONFLICT(user_id) DO UPDATE SET share = excluded.share",
        (user_id, share),
    )
    connection.commit()
    connection.close()