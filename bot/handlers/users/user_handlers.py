import logging

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from keyboards.inline.intro import main_keyboard
from keyboards.inline.support_btn import admin_keyboard
from keyboards.inline.doctor import *
from connection.api_connection import get_admins_list
from connection.api_connection import *


async def bot_start(message: types.Message, state: FSMContext):
    await state.finish()
    user_id = message.from_user.id
    username = message.from_user.username
    # ADD USER IN DB
    user = await add_user(
        user_id=user_id,
        username=username
    )
    args = message.get_args()
    msg = f"Здравствуйте👋, {message.from_user.full_name}!\n" \
          f"Мы рады видеть вас снова. Спасибо, что продолжаете с нами работать над улучшением " \
          f"здоровья и благополучия наших пациентов."
    if user == "REQUEST ERROR":
        logging.info("There are some problem in add user")
    else:
        if args:
            await update_doctor(user_id=user_id, username=username, activate_code=args)
            btn = await basic()
            await message.answer(msg, reply_markup=btn)
        elif not user["user"]["is_doctor"]:
            await message.answer(msg, reply_markup=main_keyboard)
        else:
            # if is_doctor is true, inline keyboards don't show for user
            btn = await basic()
            await message.answer(msg, reply_markup=btn)


async def bot_help(message: types.Message, state: FSMContext):
    await state.finish()
    admins = await get_admins_list()
    btn = await admin_keyboard(f"tg:user?id={admins['admins'][0]}")
    text = f"Вы обратились в службу поддержки клиентов. " \
           f"Если у вас есть какие-либо вопросы, нажмите кнопку ниже"
    await message.answer(text, reply_markup=btn)


def register_user_handlers_py(dp: Dispatcher):
    dp.register_message_handler(bot_start, commands=['start'], state="*")
    dp.register_message_handler(bot_help, commands=['help'], state="*")
