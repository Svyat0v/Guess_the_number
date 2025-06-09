import sqlite3


# Появление базы данных(gamebd.sql).
def init_db():
    conn = sqlite3.connect('gamedb.sql')
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            username TEXT,
            games INTEGER DEFAULT 0,
            winning INTEGER DEFAULT 0
        )
    """)
    conn.commit()
    cursor.close()


# Добавления пользователя в gamebd.sql
def add_user(user_id, username):
    conn = sqlite3.connect('gamedb.sql')
    cursor = conn.cursor()
    cursor.execute("""
        INSERT OR IGNORE INTO users(user_id, username)
        VALUES (?, ?)
    """, (user_id, username))
    conn.commit()
    cursor.close()


# Обновление статистики пользователей.
def update_stats(user_id, winning=False):
    conn = sqlite3.connect("gamedb.sql")
    cursor = conn.cursor()

    if winning:
        cursor.execute("""
            UPDATE users
            SET games = games + 1,
                winning = winning + 1
            WHERE user_id = ?
        """, (user_id,))
    else:
        cursor.execute("""
            UPDATE users
            SET games = games + 1
            WHERE user_id = ?
        """, (user_id,))

    conn.commit()
    conn.close()


# Показ статистики пользователей.
def get_stats(user_id):
    conn = sqlite3.connect('gamedb.sql')
    cursor = conn.cursor()
    cursor.execute('SELECT games, winning FROM users WHERE user_id = ?', (user_id,))
    result = cursor.fetchone()
    conn.close()
    return result if result else (0, 0)
