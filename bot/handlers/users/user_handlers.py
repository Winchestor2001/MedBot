from aiogram import types, Dispatcher
from aiogram.dispatcher.filters.builtin import CommandStart
from bot.data.config import ADMINS
from bot.loader import dp, bot
from bot.connection.api_connection import *


async def bot_start(message: types.Message):
    # ADD USER IN DB
    t = await add_user(
        user_id=message.from_user.id,
        username=message.from_user.username
    )
    msg = f"Добро пожаловать 👋, {message.from_user.full_name}!\n\n"
    await message.answer(msg)


def register_user_handlers_py(dp: Dispatcher):
    dp.register_message_handler(bot_start, commands=['start'])
