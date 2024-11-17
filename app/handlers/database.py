import sqlite3
from contextlib import closing

def Init_Database():
    with closing(sqlite3.connect("bot_database.db")) as connection:
        with connection :
            cursor = connection.cursor()
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE,
                tenant_id INTEGER,
                phone_number TEXT UNIQUE
            )
            """)
            connection.commit()
def Add_user(username, tenant_id, phone_number):
    """
    Добавляет пользователя в базу данных.
    """
    with closing(sqlite3.connect("bot_database.db")) as connection:
        with connection:
            cursor = connection.cursor()
            try:
                cursor.execute("""
                INSERT INTO users (username, tenant_id, phone_number)
                VALUES (?, ?, ?)
                ON CONFLICT(username) DO UPDATE SET tenant_id=excluded.tenant_id;
                """, (username, tenant_id, phone_number))
                connection.commit()
                print(f"[INFO] Пользователь {username} добавлен/обновлен в БД.")
                return True
            except sqlite3.IntegrityError as e:
                print(f"[ERROR] Ошибка добавления пользователя {username}: {e}")
                return False


def get_user(username):
    with closing(sqlite3.connect("bot_database.db")) as connection:
        cursor = connection.cursor()
        cursor.execute("""
        SELECT tenant_id, phone_number FROM users WHERE username = ?
        """, (username,))
        return cursor.fetchone()
def get_all_users():
    with closing(sqlite3.connect("bot_database.db")) as connection:
        cursor = connection.cursor()
        cursor.execute("""
        SELECT * FROM users
        """)
        return cursor.fetchall()