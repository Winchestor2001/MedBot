from aiogram import types, Dispatcher
from keyboards.inline.doctor import *
from connection.api_connection import *
from handlers.users.user_handlers import bot_start


async def doctor_intro(call: types.CallbackQuery):
    await call.answer()
    await call.message.delete()
    msg = f"Добро пожаловать 👋, {call.from_user.full_name}!"
    data = call.data.split(":")[1]
    if data == "profile":
        d = await get_doctor_info(call.from_user.id)
        text = f"👨‍⚕️ Доктор: {d['doctors']['full_name']}\n" \
               f"🎯 Специальность: {d['doctors']['direction']}\n" \
               f"💸 Цена: {d['doctors']['price']}\n" \
               f"💲 Ваш баланс: {d['doctors']['balance']}"
        btn = await get_money()
        await call.message.answer_photo(d["doctors"]["avatar"], caption=text, reply_markup=btn)

    elif data == "chats":
        d = await get_doctor_chats(call.from_user.id)
        if d["chats"]:
            btn = await get_chats(d)
            await call.message.answer("💬 Чаты", reply_markup=btn)
        else:
            await call.message.answer("У Вас нет Чаты")
            btn = await basic()
            await call.message.answer(msg + f"\nТы доктор.", reply_markup=btn)

    elif data == "get_money":
        await call.message.answer("Enter QiWi Phone number")

    elif data == "cancel":
        btn = await basic()
        await call.message.answer(msg + f"\nТы доктор.", reply_markup=btn)


def register_doctor_handler_py(dp: Dispatcher):
    dp.register_callback_query_handler(doctor_intro, text_contains=["doctor:"])
