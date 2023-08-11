from aiogram import Bot, types, Dispatcher
from core.code.another_defs import *
from core.code.keyboards import *
from dotenv import load_dotenv
from ..code import CHANNEL_ID

import logging
import os

# Activate Logging
logging.basicConfig(level=logging.INFO)

# Get API Key
load_dotenv()
API_TOKEN = os.getenv('BOT_API_KEY')

# Activate Bot and init database
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

initialize_user_db()


# -------------------------------------------------------------------
# ██╗  ██╗ █████╗ ███╗   ██╗██████╗ ██╗     ███████╗██████╗ ███████╗
# ██║  ██║██╔══██╗████╗  ██║██╔══██╗██║     ██╔════╝██╔══██╗██╔════╝
# ███████║███████║██╔██╗ ██║██║  ██║██║     █████╗  ██████╔╝███████╗
# ██╔══██║██╔══██║██║╚██╗██║██║  ██║██║     ██╔══╝  ██╔══██╗╚════██║
# ██║  ██║██║  ██║██║ ╚████║██████╔╝███████╗███████╗██║  ██║███████║
# ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝╚═════╝ ╚══════╝╚══════╝╚═╝  ╚═╝╚══════╝
# -------------------------------------------------------------------
@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    if is_user_registred(message.from_user.id):
        await start(message)
    else:
        await message.answer("👋 Что-бы начать подпишитесь на канал", reply_markup=keyboard)


@dp.callback_query_handler(lambda c: c.data == 'check')
async def process_callback(callback_query: types.CallbackQuery):
    # проверяем подписку на канал
    member = await bot.get_chat_member(CHANNEL_ID, callback_query.from_user.id)
    if member.status in ['member', 'administrator', 'creator']:
        create_new_user(callback_query.from_user.id)
        await bot.answer_callback_query(callback_query.id, "🎉 Вы подписаны на канал! 🎉")
        await start(callback_query.message)
    else:
        await bot.answer_callback_query(callback_query.id, "Вы не подписаны на канал! 😥")
        await cmd_start(callback_query.message)


async def start(message: types.Message):
    await message.answer(intro, reply_markup=keyboard_start)


@dp.message_handler(lambda message: message.text == '▶️ Начать квест')
async def start_quest(message: types.Message):
    if is_user_registred(message.from_user.id):
        update_user_place_index(message.from_user.id, 0)
        await firststep(message)
    else:
        await cmd_start(message)


async def firststep(message: types.Message):
    place_index = get_user_place_index(message.from_user.id)
    place = literary_places[place_index]
    user_facts = len(get_user_facts(message.from_user.id))
    place_name = place['name']
    latitude = place['latitude']
    longitude = place['longitude']

    await message.answer(f'📢 Место: {place_name}\n', reply_markup=keyboard_continue_2)
    await message.answer_location(latitude, longitude)


@dp.message_handler(lambda message: message.text == '📍️ Я в нужной точке')
async def nextstep(message: types.Message):
    if is_user_registred(message.from_user.id):
        place_index = get_user_place_index(message.from_user.id)
        place = literary_places[place_index]
        user_facts = len(get_user_facts(message.from_user.id))
        place_description = place['description']
        photo_path = place['photo']

        await message.answer('Молодец! Вы нашли место! 🏆')

        with open(photo_path, 'rb') as photo:
            await message.answer_photo(photo)

        await message.answer(f'📌 Место: {place_description}\n', reply_markup=keyboard_continue_1)
    else:
        await cmd_start(message)


@dp.message_handler(lambda message: message.text == '➡️ Перейти к следующему месту')
async def continue_quest(message: types.Message):
    if is_user_registred(message.from_user.id):
        place_index = get_user_place_index(message.from_user.id) + 1
        if place_index < len(literary_places):
            update_user_place_index(message.from_user.id, place_index)
            await firststep(message)
        else:
            await message.answer('🎖️ Поздравляем! Вы завершили квест.', reply_markup=keyboard_start)
    else:
        await cmd_start(message)


@dp.message_handler(lambda message: message.text == '🔎 Факт')
async def choose_random_fact(message: types.Message):
    if is_user_registred(message.from_user.id):
        user_facts = get_user_facts(message.from_user.id)
        if len(user_facts[0]) != 0:
            fact = random.choice(user_facts)
            user_facts.remove(fact)
            update_user_facts(message.from_user.id, user_facts)
            await message.answer(f"📕 Факт: {fact}")
            await message.answer(f"🔸 Осталось: {len(user_facts)}/30 фактов")

        # Если фактов нет, сразу уведомляем пользователя и переходим к следующему шагу
        else:
            await message.answer("✅ Вы уже узнали все факты")
    else:
        await cmd_start(message)
