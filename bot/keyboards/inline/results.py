from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from utils.misc.change_format_date import change_format_date


async def get_results_btn(data):
    keyboard = InlineKeyboardMarkup(row_width=1)
    for i in data["patient_results"]:
        date = i["patient"]["confirance_date"]
        doctor_name = i["patient"]["doctor"]["full_name"]
        patient_id = i["id"]
        changed_date = await change_format_date(date)
        button = InlineKeyboardButton(text=f"👨‍⚕️{changed_date} - {doctor_name}",
                                      callback_data=f"results:{patient_id}")
        keyboard.add(button)
    exit_btn = InlineKeyboardButton(text="Закрыть", callback_data="results:exit")
    keyboard.add(exit_btn)
    return keyboard

