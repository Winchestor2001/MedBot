import logging

from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from bot.data.config import ADMINS
from bot.loader import dp, bot
from bot.connection.api_connection import *


@dp.message_handler(commands=["start"])
async def bot_start(message: types.Message):
    # ADD USER IN DB
    t = await add_user(
        user_id=message.from_user.id,
        username=message.from_user.username
    )
    await message.answer(f"Привет 👋, {message.from_user.full_name}!\n<b>MedBot</b> Добро пожоловатъ !")
    if t:
        count = await get_users()
        msg = f"{message.from_user.full_name} добавлен в базу данных.\nВ базе данных {len(count['Users'])} пользователя."
        for user in ADMINS:
            await bot.send_message(user, msg)


