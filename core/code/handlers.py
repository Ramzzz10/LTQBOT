import aiogram
import random
from another_defs import *

bot = aiogram.Bot(token="5911014461:AAEpNu3TJxxOy5Pr22AXjSn1qJ-f6bex-8A")

dp = aiogram.Dispatcher(bot)

initialize_user_db()


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer('Добро пожаловать в литературный квест по Санкт-Петербургу! Нажмите кнопку "Начать квест", чтобы начать.', reply_markup=keyboard_start)

@dp.message_handler(lambda message: message.text == 'Начать квест')
async def start_quest(message: types.Message):
    update_user_place_index(message.from_user.id, 0)
    await firststep(message)

async def firststep(message: types.Message):
    place_index = get_user_place_index(message.from_user.id)
    place = literary_places[place_index]
    place_name = place['name']
    latitude = place['latitude']
    longitude = place['longitude']

    await message.answer(f'Место: {place_name}\n', reply_markup=keyboard_continue_1)
    await message.answer_location(latitude, longitude)

# Обработчик кнопки "Я в нужной точке"
@dp.message_handler(lambda message: message.text == 'Я в нужной точке')
async def nextstep(message: types.Message):
    place_index = get_user_place_index(message.from_user.id)
    place = literary_places[place_index]
    place_description = place['description']
    photo_path = place['photo']

    await message.answer('Молодец! Вы нашли место!')
    # with open(photo_path, 'rb') as photo:
    #     await message.answer_photo(photo)

    await message.answer(place_description, reply_markup=keyboard_continue)


# Обработчик кнопки "Перейти к следующему месту"
@dp.message_handler(lambda message: message.text == 'Перейти к следующему месту')
async def continue_quest(message: types.Message):
    place_index = get_user_place_index(message.from_user.id) + 1
    if place_index < len(literary_places):
        update_user_place_index(message.from_user.id, place_index)
        await firststep(message)
    else:
        await message.answer('Поздравляем! Вы завершили квест.', reply_markup=keyboard_start)

# Обработчик кнопки "Факт"
@dp.message_handler(lambda message: message.text == 'Факт')
async def choose_random_fact(message: types.Message):
    user_id = message.from_user.id
    user_facts = get_user_facts(user_id)
    remaining_facts = len(user_facts)
    if remaining_facts > 0:
        fact = random.choice(facts)
        facts.remove(fact)
        await message.answer(f"Факт: {fact}")
        await message.answer(f"Вы услышали: {remaining_facts}/30")
        update_user_facts(user_id)


    else:
        await message.answer("Вы узнали все факты", reply_markup=keyboard_continue_1f)
        await show_continue_keyboard(message)

