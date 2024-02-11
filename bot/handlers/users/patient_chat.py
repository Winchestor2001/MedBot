from aiogram import types, Dispatcher
from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from utils.misc.change_format_date import change_format_date, detail_date
from keyboards.inline.doctor import *
from connection.api_connection import *


async def chat_patient(call: types.CallbackQuery):
    await call.answer()
    data = call.data.split(":")[1]
    if data == "chats":
        chats = await get_patient_chats(call.from_user.id)
        if chats.get("chats", False):
            btn = await get_patient_chats_btn(chats)
            await call.message.answer("💬 Чаты", reply_markup=btn)
        else:
            await call.answer("У Вас нет Чаты", show_alert=True)


def register_chat_patient_handlers_py(dp: Dispatcher):
    dp.register_callback_query_handler(chat_patient, text_contains="chat_patient:")
