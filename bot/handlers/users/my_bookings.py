from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from datetime import datetime
from bot.loader import dp, bot
from bot.keyboards.inline.intro import main_keyboard
from bot.keyboards.inline.bookings import get_bookings_btn, back_btn
from bot.connection.api_connection import *
from bot.handlers.users.user_handlers import bot_start


# profile functions
from bot.utils.misc.change_format_date import detail_date


@dp.callback_query_handler(text_contains=["profile:"])
async def profile(call: types.CallbackQuery, state: FSMContext):
    await call.answer(cache_time=30)
    # await call.message.delete()
    user_id = call.from_user.id
    if call.data == "profile:my_booking":
        booking = await get_my_booking(user_id)
        if len(booking["Patient"]) > 0:
            await state.update_data({
                "data": booking["Patient"]
            })
            btn = await get_bookings_btn(booking)
            await call.message.edit_text("Вот ваши заказы", reply_markup=btn)
        else:
            await call.message.edit_text(text="У вас нет заказа", reply_markup=main_keyboard)

    elif call.data == "profile:my_result":
        pass


@dp.callback_query_handler(text_contains="patient:")
async def detail_booking(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    patient_id = call.data.split("patient:")[1]
    data = await state.get_data()
    if not patient_id == "back" and not patient_id == "exit":
        for i in data["data"]:
            if int(i["id"]) == int(patient_id):
                date = await detail_date(i["confirance_date"])
                msg = f"Вот данные вашего заказ\n\n" \
                      f"📋 Заказ ID: {i['id']}\n" \
                      f"👨‍⚕️Доктор: {i['doctor']['full_name'].capitalize()}\n" \
                      f"📆 Дата и время: {date}\n\n" \
                      f"Спасибо, что выбрали наш сервис! Если у вас есть какие-либо вопросы или вам нужно перенести встречу, свяжитесь с нами. 📞"
                await call.message.answer(msg, reply_markup=back_btn)
    elif patient_id == "back":
        # await call.message.delete()
        booking = await get_my_booking(call.from_user.id)
        if len(booking["Patient"]) > 0:
            await state.update_data({
                "data": booking["Patient"]
            })
            btn = await get_bookings_btn(booking)
            await call.message.answer("Вот ваши заказы", reply_markup=btn)
    elif patient_id == "exit":
        # await call.message.delete()
        msg = f"Добро пожаловать 👋, {call.from_user.full_name}!\n\n"
        await call.message.answer(msg, reply_markup=main_keyboard)


# def register_user_handlers_py(dp: Dispatcher):
#     dp.register_callback_query_handler(profile, text_contains="profile:")
