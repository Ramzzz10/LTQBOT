import sqlite3
import random
from information import *

# Функция для инициализации базы данных и создания таблицы пользователей
def initialize_user_db():
    con = sqlite3.connect("dataltq.db")
    cur = con.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS users(
                    id INTEGER PRIMARY KEY,
                    current_place_index INTEGER DEFAULT 0,
                    facts TEXT
                    
                )""")
    con.commit()
    con.close()

# Функция для получения текущего места для конкретного пользователя
def get_user_place_index(user_id):
    con = sqlite3.connect("dataltq.db")
    cur = con.cursor()
    cur.execute("SELECT current_place_index FROM users WHERE id = ?", (user_id,))
    row = cur.fetchone()
    con.close()
    return row[0] if row else 0

# Функция для обновления информации о текущем месте для пользователя в базе данных
def update_user_place_index(user_id, place_index):
    con = sqlite3.connect("dataltq.db")
    cur = con.cursor()
    cur.execute("UPDATE users SET current_place_index = ? WHERE id = ?", (place_index, user_id,))
    con.commit()
    con.close()

# Функция для создания нового пользователя в базе данных
def create_new_user(user_id):
    con = sqlite3.connect("dataltq.db")
    cur = con.cursor()
    facts_list = random.sample(facts, 30)
    cur.execute("INSERT INTO users (id, facts) VALUES (?, ?)", (user_id, ','.join(map(str, facts_list))))
    con.commit()
    con.close()

# Функция для получения списка фактов для конкретного пользователя
def get_user_facts(user_id):
    con = sqlite3.connect("dataltq.db")
    cur = con.cursor()
    cur.execute("SELECT facts FROM users WHERE id = ?", (user_id,))
    row = cur.fetchone()
    con.close()
    if row:
        return row[0].split(',')
    return []

# Функция для обновления информации о количестве фактов для пользователя в базе данных
def update_user_facts(user_id, facts_list):
    con = sqlite3.connect("dataltq.db")
    cur = con.cursor()
    cur.execute("UPDATE users SET facts = ? WHERE id = ?", (','.join(map(str, facts_list)), user_id,))
    con.commit()
    con.close()





