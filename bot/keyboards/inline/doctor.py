from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from utils.misc.hasher import create_hash
from environs import Env

env = Env()
env.read_env()


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
    keyboard = InlineKeyboardMarkup(row_width=2)
    for i in data["chats"]:
        hash_data = create_hash(
            {"doctor": {"id": i['doctor'], "name": i['full_name']},
             "patient": {"id": i['patient']['id'], "name": i['patient']['full_name']}, "type": 'doctor'}
        )
        webapp_url = f"{env.str('UI_DOMEN')}/meeting_chat/{i['chat_code']}/{hash_data}"
        webapp_main = WebAppInfo(url=webapp_url)
        btn = InlineKeyboardButton(text=f"{i['patient']['full_name']}", web_app=webapp_main)
        keyboard.insert(btn)
    back = InlineKeyboardButton("🔙 Назад", callback_data="doctor:cancel")
    keyboard.row(back)
    return keyboard


async def payment_method_btn(data):
    keyboard = InlineKeyboardMarkup(row_width=2)
    for i in data["list"]:
        btn = InlineKeyboardButton(text=f"{data['list'][i]['name']}", callback_data=f"payment:{i}")
        keyboard.insert(btn)
    back = InlineKeyboardButton("🔙 Назад", callback_data="payment:cancel")
    keyboard.row(back)
    return keyboard


async def cancel_btn():
    keyboard = InlineKeyboardMarkup(row_width=1)
    back = InlineKeyboardButton("🔙 Назад", callback_data="handler:cancel")
    keyboard.add(back)
    return keyboard
