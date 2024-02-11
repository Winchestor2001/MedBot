from aiogram import types, Dispatcher
from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from utils.misc.change_format_date import change_format_date, detail_date
from keyboards.inline.doctor import *
from keyboards.inline.intro import main_keyboard
from connection.api_connection import *


async def chat_patient(call: types.CallbackQuery):
    # await call.answer()
    data = call.data.split(":")[1]
    if data == "chats":
        chats = await get_patient_chats(call.from_user.id)
        if chats.get("chats", False):
            btn = await get_patient_chats_btn(chats)
            await call.message.edit_text("💬 Чаты", reply_markup=btn)
        else:
            await call.answer("У Вас нет Чаты", show_alert=True)


async def s_chat(call: types.CallbackQuery):
    await call.answer()
    data = call.data.split(":")[1]
    if not data == "cancel":
        patient = await get_single_chat(data)
        if patient:
            d = patient['chat'][0]['created_at'][:10]
            date = await change_format_date(d)
            text = f"🆔 {patient['chat'][0]['id']}\n" \
                   f"👨‍⚕️Доктор: {patient['chat'][0]['patient']['doctor']['full_name']}\n" \
                   f"👤 Пациент: {patient['chat'][0]['patient']['full_name']}\n" \
                   f"📅 Дата: {date}\n" \
                   f"📔 Чат: {patient['chat'][0]['chat_code']}"
            btn = await manage_patient_chat(patient["chat"][0])
            await call.message.edit_text(text, reply_markup=btn)
    else:
        msg = f"Добро пожаловать 👋, {call.from_user.full_name}!"
        await call.message.answer(msg, reply_markup=main_keyboard)


def register_chat_patient_handlers_py(dp: Dispatcher):
    dp.register_callback_query_handler(chat_patient, text_contains="chat_patient:")
    dp.register_callback_query_handler(s_chat, text_contains="single_patient_chat:")
