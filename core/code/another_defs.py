import sqlite3
from information import *
from keyboards import *

async def show_continue_keyboard(message: types.Message):
    global current_quest_index
    if current_quest_index < len(literary_places):










        await message.answer("Продолжим наш путь, Господа!", reply_markup=keyboard_continue_1f)
    else:
        await message.answer('Молодец! Вы нашли место!')

# Функция для обновления информации о количестве фактов для пользователя в базе данных
async def update_facts_sent(user_id: int):
    con = sqlite3.connect("../../dataltq.db")
    cur = con.cursor()
    cur.execute("INSERT OR IGNORE INTO user_facts (user_id) VALUES (?)", (user_id,))
    cur.execute("UPDATE user_facts SET facts_sent = facts_sent + 1 WHERE user_id = ?", (user_id,))
    con.commit()
    con.close()