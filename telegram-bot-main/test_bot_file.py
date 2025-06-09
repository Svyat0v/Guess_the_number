import sqlite3


# Создание соединения с базой данных
conn = sqlite3.connect('gamedb.sql')

# Создание курсора для выполнения SQL-запросов
cur = conn.cursor()

# Создание таблицы
cur.execute("""CREATE TABLE IF NOT EXISTS users (user_id INTEGER PRIMARY KEY, username TEXT, games INTEGER, winning INTEGER)""")

# Вставка записи в таблицу
cur.execute("INSERT INTO users (username, games, winning) VALUES ('Петя', 10, 5)")

# Сохранение изменений
conn.commit()

# Выборка данных из таблицы
cur.execute("SELECT * FROM users")
print(cur.fetchall())

conn.close()
