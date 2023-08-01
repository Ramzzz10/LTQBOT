import sqlite3
from information import *
from keyboards import *


# Функция для инициализации базы данных и создания таблицы пользователей
def initialize_user_db():
    con = sqlite3.connect("dataltq.db")
    cur = con.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS users(
                    id INTEGER PRIMARY KEY,
                    facts_sent INTEGER DEFAULT 0,
                    current_place_index INTEGER DEFAULT 0
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



# Функция для получения списка фактов для конкретного пользователя
def get_user_facts(user_id):
    con = sqlite3.connect("dataltq.db")
    cur = con.cursor()
    cur.execute("SELECT facts_sent FROM users WHERE id = ?", (user_id,))
    row = cur.fetchone()
    con.close()
    if row:
        return facts[:row[0]]
    return facts[:]


# Функция для обновления информации о количестве фактов для пользователя в базе данных
def update_user_facts(user_id):
    con = sqlite3.connect("dataltq.db")
    cur = con.cursor()
    cur.execute("INSERT OR IGNORE INTO users (id) VALUES (?)", (user_id,))
    cur.execute("UPDATE users SET facts_sent = facts_sent + 1 WHERE id = ?", (user_id,))
    con.commit()
    con.close()




# Функция для вывода клавиатуры с кнопкой "Продолжим наш путь, Господа!"
async def show_continue_keyboard(message: types.Message):
    place_index = get_user_place_index(message.from_user.id)
    if place_index < len(literary_places):
        await message.answer("Продолжим наш путь, Господа!", reply_markup=keyboard_continue_1f)
    else:
        await message.answer('Молодец! Вы нашли место!')


