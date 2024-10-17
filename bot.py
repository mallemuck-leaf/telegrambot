import keys
import bot_utils
import bot_data
import asyncio
import logging
from aiogram import Bot, Dispatcher, types, html, F
from aiogram.filters.command import Command

logging.basicConfig(level=logging.INFO)
bot = Bot(token=keys.token)
dp = Dispatcher()


@dp.message(Command('start'))
async def cmd_start(message: types.Message):
    kb = [
        [
            types.KeyboardButton(text='Узнать'),
            types.KeyboardButton(text='Отказываюсь'),
        ]
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder='Показать погоду?'
    )
    await message.reply('Показать погоду?', reply_markup=keyboard)


@dp.message(F.text.lower() == 'узнать')
async def true_key(message: types.Message):
    user = message.from_user.id
    user_in_db = bot_data.get_info(user)
    if user_in_db is not None:
        kb = [
            [
                types.KeyboardButton(text='Тот же'),
                types.KeyboardButton(text='Другой'),
            ]
        ]
        keyboard = types.ReplyKeyboardMarkup(
            keyboard=kb,
            resize_keyboard=True,
            input_field_placeholder='Город тот же?'
        )
        await message.reply(f'Для того же города, как в прошлый раз?',
                            reply_markup=types.ReplyKeyboardMarkup(keyboard=kb))
    else:
        await message.reply('Введите название города', reply_markup=types.ReplyKeyboardRemove())


@dp.message(F.text.lower() == 'другой')
async def true_key(message: types.Message):
    await message.reply('Введите название города', reply_markup=types.ReplyKeyboardRemove())


@dp.message(F.text.lower() == 'тот же')
async def old_user(message: types.Message):
    city_info = bot_data.get_city_id(bot_data.get_info(message.from_user.id)[1])
    weather = bot_utils.call_weather(city_info[1], city_info[2])
    await message.reply(f'Температура: {weather[0]}, ветер: {weather[1]}, {weather[2]}',
                        reply_markup=types.ReplyKeyboardRemove())


@dp.message(F.text.lower() != 'узнать')
async def weather_city(message: types.Message):
    city = message.text
    city_info = bot_data.get_city(city)
    if city_info is None:
        try:
            city_info = bot_utils.call_city(city)
            bot_data.add_city(city_info[0], city_info[1], city_info[2])
        except Exception as e:
            await message.reply(f'Город не найден: {e}', reply_markup=types.ReplyKeyboardRemove())
    weather = bot_utils.call_weather(city_info[1], city_info[2])
    bot_data.add_info(message.from_user.id, city_info[0])
    await message.reply(f'Температура: {weather[0]}, ветер: {weather[1]}, {weather[2]}',
                        reply_markup=types.ReplyKeyboardRemove())


async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
