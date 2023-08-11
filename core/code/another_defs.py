from core.code.information import *
from ..code import DATABASE_PATH

import sqlite3
import random


db_connection = sqlite3.connect(DATABASE_PATH)
db_cursor = db_connection.cursor()


def is_user_registred(user_id: int) -> bool:
    """
    Функия для проверкки наличия пользователя в базе даннноа
    """
    db_cursor.execute("SELECT id FROM users WHERE id = ?", (user_id,))
    return True if db_cursor.fetchone() else False


def initialize_user_db() -> None:
    """
    Функция для инициализации базы данных и создания таблицы пользователей
    """
    db_cursor.execute("""
        CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY,
        current_place_index INTEGER DEFAULT 0,
        facts TEXT    
        )
        """)
    db_connection.commit()



def get_user_place_index(user_id):
    """
    Функция для получения текущего места для конкретного пользователя
    """
    db_cursor.execute("SELECT current_place_index FROM users WHERE id = ?", (user_id,))
    row = db_cursor.fetchone()
    return row[0] if row else 0




def update_user_place_index(user_id, place_index) -> None:
    """
    Функция для обновления информации о текущем месте для пользователя в базе данных
    """
    db_cursor.execute("UPDATE users SET current_place_index = ? WHERE id = ?", (place_index, user_id,))
    db_connection.commit()


def create_new_user(user_id) -> None:
    """
    Функция для создания нового пользователя в базе данных
    """
    db_cursor.execute("SELECT id FROM users WHERE id = ?", (user_id,))
    if db_cursor.fetchone() is None:
        facts_list = random.sample(facts, 30)
        db_cursor.execute("INSERT INTO users (id, facts) VALUES (?, ?)", (user_id, ','.join(map(str, facts_list))))
        db_connection.commit()


def get_user_facts(user_id):
    """
    Функция для получения списка фактов для конкретного пользователя
    """
    db_cursor.execute("SELECT facts FROM users WHERE id = ?", (user_id,))
    row = db_cursor.fetchone()
    return row[0].split(',') if row else []


def update_user_facts(user_id, facts_list) -> None:
    """
    Функция для обновления информации о количестве фактов для пользователя в базе данных
    """
    db_cursor.execute("UPDATE users SET facts = ? WHERE id = ?", (','.join(map(str, facts_list)), user_id,))
    db_connection.commit()
