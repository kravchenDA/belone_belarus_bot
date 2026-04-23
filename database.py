import sqlite3
from datetime import datetime

DB_PATH = "belone.db"

def init_db():
    """Создаёт таблицы при запуске"""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            username TEXT,
            first_name TEXT,
            last_taste TEXT,
            registered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS taste_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            taste TEXT,
            answers TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()

def register_user(user_id: int, username: str = None, first_name: str = None):
    """Регистрирует нового пользователя"""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        INSERT OR IGNORE INTO users (user_id, username, first_name)
        VALUES (?, ?, ?)
    """, (user_id, username, first_name))
    conn.commit()
    conn.close()

def save_taste_result(user_id: int, taste: str, answers: str):
    """Сохраняет результат подбора вкуса"""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        UPDATE users SET last_taste = ? WHERE user_id = ?
    """, (taste, user_id))
    cur.execute("""
        INSERT INTO taste_results (user_id, taste, answers)
        VALUES (?, ?, ?)
    """, (user_id, taste, answers))
    conn.commit()
    conn.close()

def get_user(user_id: int):
    """Получает пользователя по ID"""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
    user = cur.fetchone()
    conn.close()
    return user
