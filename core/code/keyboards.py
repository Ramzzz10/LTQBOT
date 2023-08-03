from aiogram import types

keyboard = types.InlineKeyboardMarkup()
subscribe = types.InlineKeyboardButton(text="Подписаться", url='https://t.me/RaptorsSquad')
check = types.InlineKeyboardButton(text="Проверить", callback_data="check")
keyboard.add(subscribe, check)

keyboard_start = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
button_start = types.KeyboardButton(text='Начать квест')
keyboard_start.add(button_start)

keyboard_continue = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
button_fact = types.KeyboardButton(text='Факт')
button_continue_3 = types.KeyboardButton(text='Перейти к следующему месту')
keyboard_continue.add(button_continue_3, button_fact)

keyboard_continue_1 = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
button_continue_30 = types.KeyboardButton(text='Я в нужной точке')
button_fact = types.KeyboardButton(text='Факт')
keyboard_continue_1.add(button_continue_30, button_fact)

keyboard_continuef = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
button_continue_3 = types.KeyboardButton(text='Перейти к следующему месту')
keyboard_continuef.add(button_continue_3)

keyboard_continue_1f = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
button_continue_30 = types.KeyboardButton(text='Я в нужной точке')
keyboard_continue_1f.add(button_continue_30)

