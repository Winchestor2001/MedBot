from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from keyboards.inline.intro import main_keyboard
from keyboards.inline.bookings import get_bookings_btn, back_btn
from connection.api_connection import *
from utils.misc.change_format_date import detail_date


async def profile(call: types.CallbackQuery, state: FSMContext):
    user_id = call.from_user.id
    if call.data == "profile:my_booking":
        booking = await get_my_booking(user_id)
        if booking and booking.get("patient", False):
            await state.update_data({
                "data": booking["patient"]
            })
            btn = await get_bookings_btn(booking)
            await call.message.edit_text("Ваши записи", reply_markup=btn)
        else:
            await call.answer(text="❗️У вас нет записей", show_alert=True)


async def detail_booking(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    patient_id = call.data.split("patient:")[1]
    data = await state.get_data()
    if not patient_id == "back" and not patient_id == "exit":
        for i in data["data"]:
            if int(i["id"]) == int(patient_id):
                date = await detail_date(i["confirance_date"])
                msg = f"Информация о записе\n\n" \
                      f"📋 ID Заказа: {i['id']}\n" \
                      f"👨‍⚕️Доктор: {i['doctor']['full_name'].capitalize()}\n" \
                      f"📆 Дата и время: {date}\n\n" \
                      f"Спасибо, что выбрали наш сервис! Если у вас есть какие-либо вопросы или вам " \
                      f"нужно перенести встречу, свяжитесь с нами. 📞"
                await call.message.answer(msg, reply_markup=back_btn)
    elif patient_id == "back":
        booking = await get_my_booking(call.from_user.id)
        if len(booking["patient"]) > 0:
            await state.update_data({
                "data": booking["patient"]
            })
            btn = await get_bookings_btn(booking)
            await call.message.answer("Ваши записи", reply_markup=btn)
    elif patient_id == "exit":
        msg = f"Добро пожаловать 👋, {call.from_user.full_name}!\n\n"
        await call.message.answer(msg, reply_markup=main_keyboard)


def register_my_bookings_py(dp: Dispatcher):
    dp.register_callback_query_handler(profile, text=["profile:my_booking"])
    dp.register_callback_query_handler(detail_booking, text_contains=["patient:"])
