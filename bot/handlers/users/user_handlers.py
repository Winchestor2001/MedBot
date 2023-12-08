from aiogram import types, Dispatcher
from bot.keyboards.inline.intro import main_keyboard
from bot.connection.api_connection import *


async def bot_start(message: types.Message):
    user_id = message.from_user.id
    username = message.from_user.username
    # ADD USER IN DB
    user = await add_user(
        user_id=user_id,
        username=username
    )
    args = message.get_args()
    msg = f"Добро пожаловать 👋, {message.from_user.full_name}!\n\n"
    if args:
        await update_doctor(user_id=user_id, username=username, activate_code=args)
        await message.answer(msg + f"Ты доктор.")
    elif not user["user"]["is_doctor"]:
        await message.answer(msg, reply_markup=main_keyboard)
    else:
        # if is_doctor is true, inline keyboards don't show for user
        await message.answer(msg + f"Ты доктор.")


def register_user_handlers_py(dp: Dispatcher):
    dp.register_message_handler(bot_start, commands=['start'])
