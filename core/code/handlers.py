from another_defs import *
from keyboards import *
from aiogram import Bot, types, Dispatcher
import logging

logging.basicConfig(level=logging.INFO)



bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

initialize_user_db()

@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    create_new_user(message.from_user.id)
    await message.answer("Что-бы начать подпишитесь на канал", reply_markup=keyboard)


@dp.callback_query_handler(lambda c: c.data == 'check')
async def process_callback(callback_query: types.CallbackQuery):
    # проверяем подписку на канал
    member = await bot.get_chat_member('@RaptorsSquad', callback_query.from_user.id)
    if member.status in ['member', 'administrator', 'creator']:
        await bot.answer_callback_query(callback_query.id, "Вы подписаны на канал!")
        await start(callback_query.message)
    else:
        await bot.answer_callback_query(callback_query.id, "Вы не подписаны на канал!")
        await cmd_start(callback_query.message)


async def start(message: types.Message):
    await message.answer(intro, reply_markup=keyboard_start)


@dp.message_handler(lambda message: message.text == 'Начать квест')
async def start_quest(message: types.Message):
    update_user_place_index(message.from_user.id, 0)
    await firststep(message)

async def firststep(message: types.Message):
    place_index = get_user_place_index(message.from_user.id)
    place = literary_places[place_index]
    user_facts = len(get_user_facts(message.from_user.id))
    place_name = place['name']
    latitude = place['latitude']
    longitude = place['longitude']

    await message.answer(f'Место: {place_name}\n', reply_markup=keyboard_continue_1 if user_facts!=0 else keyboard_continue_1f)
    await message.answer_location(latitude, longitude)


@dp.message_handler(lambda message: message.text == 'Я в нужной точке')
async def nextstep(message: types.Message):
    place_index = get_user_place_index(message.from_user.id)
    place = literary_places[place_index]
    user_facts = len(get_user_facts(message.from_user.id))
    place_description = place['description']
    photo_path = place['photo']

    await message.answer('Молодец! Вы нашли место!')
    # with open(photo_path, 'rb') as photo:
    #     await message.answer_photo(photo)

    await message.answer(f'Место: {place_description}\n', reply_markup=keyboard_continue_1 if user_facts!=0 else keyboard_continue_1f)

@dp.message_handler(lambda message: message.text == 'Перейти к следующему месту')
async def continue_quest(message: types.Message):
    place_index = get_user_place_index(message.from_user.id) + 1
    if place_index < len(literary_places):
        update_user_place_index(message.from_user.id, place_index)
        await firststep(message)
    else:
        await message.answer('Поздравляем! Вы завершили квест.', reply_markup=keyboard_start)


@dp.message_handler(lambda message: message.text == 'Факт')
async def choose_random_fact(message: types.Message):
    user_facts = get_user_facts(message.from_user.id)
    if not user_facts:
        create_new_user(message.from_user.id)
        user_facts = get_user_facts(message.from_user.id)

    if len(user_facts) != 0:
        fact = random.choice(user_facts)
        user_facts.remove(fact)
        update_user_facts(message.from_user.id, user_facts)
        await message.answer(f"Факт: {fact}")
        await message.answer(f"Осталось: {len(user_facts)}/30 фактов")

    # Если фактов нет, сразу уведомляем пользователя и переходим к следующему шагу
    if len(user_facts) == 0:
        await message.answer("Вы узнали все факты")
        await show_continue_keyboard(message)


async def show_continue_keyboard(message: types.Message):
    place_index = get_user_place_index(message.from_user.id)

    if place_index < len(literary_places):
        if place_index % 2 == 0:
            await message.answer("Продолжим наш путь, Господа!", reply_markup=keyboard_continue_1f)

        else:
           await message.answer("Продолжим наш путь, Господа!", reply_markup=keyboard_continuef)

    else:
        await message.answer('Молодец! Вы завершили квест!')








