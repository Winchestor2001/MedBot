from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from utils.misc.change_format_date import change_format_date


async def get_bookings_btn(dicts):
    keyboard = InlineKeyboardMarkup(row_width=1)
    for i in dicts["patient"]:
        date = i["confirance_date"]
        doctor_name = i["doctor"]["full_name"]
        patient_id = i["id"]
        changed_date = await change_format_date(date)
        button = InlineKeyboardButton(text=f"👨‍⚕️{changed_date} - {doctor_name}",
                                      callback_data=f"patient:{patient_id}")
        keyboard.add(button)
    exit_btn = InlineKeyboardButton(text="Закрыть", callback_data="patient:exit")
    keyboard.add(exit_btn)
    return keyboard


back_btn = InlineKeyboardMarkup(row_width=1)
btn = InlineKeyboardButton("🔙 Назад", callback_data="patient:back")
back_btn.add(btn)
