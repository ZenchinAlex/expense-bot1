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
            created_at TEXT
        )
    """)
    connection.commit()
    connection.close()


def add_expense(user_id, title, amount):
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()
    cursor.execute(
        "INSERT INTO expenses (user_id, title, amount, created_at) "
        "VALUES (?, ?, ?, datetime('now'))",
        (user_id, title, amount),
    )
    connection.commit()
    connection.close()