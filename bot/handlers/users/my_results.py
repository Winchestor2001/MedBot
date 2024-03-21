from aiogram import types, Dispatcher
from connection.api_connection import *
from keyboards.inline.results import get_results_btn
from keyboards.inline.intro import main_keyboard
from loader import bot


async def send_request_result(call: types.CallbackQuery):
    # get my results into db
    my_results = await get_my_result(call.from_user.id)
    if my_results and my_results.get("patient_results", False):
        btn = await get_results_btn(my_results)
        await call.message.edit_text("Ваши результаты:", reply_markup=btn)
    else:
        await call.answer(text="❗️ У вас нет результат", show_alert=True)


async def get_request_result(call: types.CallbackQuery):
    await call.answer()
    await call.message.delete()
    patient_id = call.data.split(":")[1]
    result = await get_result_pdf(patient_id)
    if result["patient_result_pdf"]:
        await call.message.answer_document(result["patient_result_pdf"])
    elif result["patient_result"]:
        await call.message.answer(result["patient_result"])

    msg = f"Добро пожаловать 👋, {call.from_user.full_name}!"
    await call.message.answer(msg, reply_markup=main_keyboard)


async def cancel_result(call: types.CallbackQuery):
    await call.message.delete()
    msg = f"Добро пожаловать 👋, {call.from_user.full_name}!\n\n"
    await call.message.answer(msg, reply_markup=main_keyboard)


def register_my_results_py(dp: Dispatcher):
    dp.register_callback_query_handler(send_request_result, text=["profile:my_result"])
    dp.register_callback_query_handler(cancel_result, text=["results:exit"])
    dp.register_callback_query_handler(get_request_result, text_contains=["results:"])
