from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from med_app.utils import create_hash
from core.settings import env


async def basic():
    keyboard = InlineKeyboardMarkup(row_width=2)
    btn1 = InlineKeyboardButton("👤 Профиль", callback_data="doctor:profile")
    btn2 = InlineKeyboardButton("💬 Чаты", callback_data="doctor:chats")
    keyboard.add(btn1, btn2)
    return keyboard


async def get_money():
    keyboard = InlineKeyboardMarkup(row_width=1)
    btn = InlineKeyboardButton("💳 Вывод Средств", callback_data="doctor:get_money")
    back = InlineKeyboardButton("🔙 Назад", callback_data="doctor:cancel")
    keyboard.add(btn, back)
    return keyboard


async def get_chats(data):
    keyboard = InlineKeyboardMarkup(row_width=1)
    for i in data["chats"]:
        hash_data = create_hash(
            {"doctor": i['doctor'], "patient": i['patient']['doctor'], "type": 'doctor'}
        )
        webapp_url = f"{env.str('UI_DOMEN')}/meeting_chat/{i['chat_code']}/{hash_data}"
        webapp_main = WebAppInfo(url=webapp_url)
        btn = InlineKeyboardButton(text=f"{i['patient']['full_name']}", web_app=webapp_main)
        keyboard.add(btn)
    back = InlineKeyboardButton("🔙 Назад", callback_data="doctor:cancel")
    keyboard.add(back)
    return keyboard
