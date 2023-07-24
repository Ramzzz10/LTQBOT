import aiogram
import random
from another_defs import *

bot = aiogram.Bot(token="5911014461:AAEpNu3TJxxOy5Pr22AXjSn1qJ-f6bex-8A")
dp = aiogram.Dispatcher(bot)

current_quest_index = 0
remaining_facts = 30
facts_ended = False

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    con = sqlite3.connect("../../dataltq.db")
    cur = con.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS user_facts(
                    user_id INTEGER PRIMARY KEY,
                    facts_sent INTEGER DEFAULT 0
                )""")
    con.commit()
    con.close()

    await message.answer('Добро пожаловать в литературный квест по Санкт-Петербургу! Нажмите кнопку "Начать квест", чтобы начать.', reply_markup=keyboard_start)

# Обработчик кнопки "Начать квест"
@dp.message_handler(lambda message: message.text == 'Начать квест')
async def start_quest(message: types.Message):
    global current_quest_index, remaining_facts, facts_ended
    current_quest_index = 0
    remaining_facts = 30
    facts_ended = False
    await firststep(message)

# Функция для вывода информации о текущем месте
async def firststep(message: types.Message):
    global current_quest_index
    place = literary_places[current_quest_index]
    place_name = place['name']
    latitude = place['latitude']
    longitude = place['longitude']

    await message.answer(f'Место: {place_name}\n', reply_markup=keyboard_continue_1)
    await message.answer_location(latitude, longitude)

# Обработчик кнопки "Я в нужной точке"
@dp.message_handler(lambda message: message.text == 'Я в нужной точке')
async def nextstep(message: types.Message):
    global current_quest_index
    place = literary_places[current_quest_index]
    place_description = place['description']
    photo_path = place['photo']

    await message.answer('Молодец! Вы нашли место!')
    with open(photo_path, 'rb') as photo:
        await message.answer_photo(photo)

    await message.answer(place_description, reply_markup=keyboard_continue)
    await update_facts_sent(message.from_user.id)

# Обработчик кнопки "Перейти к следующему месту"
@dp.message_handler(lambda message: message.text == 'Перейти к следующему месту')
async def continue_quest(message: types.Message):
    global current_quest_index, facts_ended
    current_quest_index += 1

    if facts_ended:
        await nextstep(message)
    elif current_quest_index < len(literary_places):
        await firststep(message)
    else:
        await message.answer('Поздравляем! Вы завершили квест.', reply_markup=keyboard_start)

# Обработчик кнопки "Факт"
@dp.message_handler(lambda message: message.text == 'Факт')
async def choose_random_fact(message: types.Message):
    global remaining_facts, facts_ended

    if not remaining_facts:  # Если remaining_facts равно 0, значит факты закончились
        facts_ended = True
        await message.answer("Вы узнали все факты", reply_markup=keyboard_continue_1f)
        await show_continue_keyboard(message)
    else:
        fact = random.choice(facts)
        facts.remove(fact)
        remaining_facts -= 1
        await message.answer(f"Факт: {fact}")
        await message.answer(f"Осталось фактов: {remaining_facts}/30")
        await update_facts_sent(message.from_user.id)