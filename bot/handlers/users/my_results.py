from aiogram import types, Dispatcher
from bot.connection.api_connection import *
from bot.keyboards.inline.results import get_results_btn


async def send_request_result(call: types.CallbackQuery):
    # get my results into db
    my_results = await get_my_result(call.from_user.id)
    btn = await get_results_btn(my_results)
    await call.message.edit_text("Это ваши результаты:", reply_markup=btn)


async def get_request_result(call: types.CallbackQuery):
    await call.message.delete()
    await call.message.answer_document("https://css4.pub/2015/icelandic/dictionary.pdf",
                                       caption='Result')


def register_my_results_py(dp: Dispatcher):
    dp.register_callback_query_handler(send_request_result, text=["profile:my_result"])
    dp.register_callback_query_handler(get_request_result, text_contains=["results:"])
