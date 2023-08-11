from ..code import CHANNEL_URL
from aiogram import types


# Subcribe button
keyboard = types.InlineKeyboardMarkup()
keyboard.add(
    types.InlineKeyboardButton(text="Подписаться", url=CHANNEL_URL),
    types.InlineKeyboardButton(text="Проверить", callback_data="check")
)

# Start quest button
keyboard_start = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
keyboard_start.add(
    types.KeyboardButton(text='▶️ Начать квест')
)

# Next place button
keyboard_continue_1 = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
keyboard_continue_1.add(
    types.KeyboardButton(text='➡️ Перейти к следующему месту'),
    types.KeyboardButton(text='🔎 Факт')
)


keyboard_continue_2 = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
keyboard_continue_2.add(
    types.KeyboardButton(text='📍️ Я в нужной точке'),
    types.KeyboardButton(text='🔎 Факт')
)
