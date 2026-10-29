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