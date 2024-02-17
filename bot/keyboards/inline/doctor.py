from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from utils.misc.hasher import create_hash
from environs import Env

env = Env()
env.read_env()


async def basic():
    keyboard = InlineKeyboardMarkup(row_width=2)
    btn1 = InlineKeyboardButton("👤 Профиль", callback_data="doctor:profile")
    btn2 = InlineKeyboardButton("👨🏻‍⚕️ Пациенты", callback_data="doctor:chats")
    keyboard.add(btn1, btn2)
    return keyboard


async def get_money():
    keyboard = InlineKeyboardMarkup(row_width=1)
    btn = InlineKeyboardButton("💳 Вывод Средств", callback_data="doctor:get_money")
    back = InlineKeyboardButton("🔙 Назад", callback_data="doctor:cancel")
    keyboard.add(btn, back)
    return keyboard


# list chats
async def get_chats(data):
    keyboard = InlineKeyboardMarkup(row_width=2)
    for i in data["chats"]:
        btn = InlineKeyboardButton(text=f"{i['patient']['full_name']}", callback_data=f"chat_doctor:{i['id']}")
        keyboard.insert(btn)
    back = InlineKeyboardButton("🔙 Назад", callback_data="doctor:cancel")
    keyboard.row(back)
    return keyboard


async def get_patient_chats_btn(data):
    keyboard = InlineKeyboardMarkup(row_width=2)
    for i in data["chats"]:
        btn = InlineKeyboardButton(text=f"{i['patient']['full_name']} - 👨‍⚕️{i['doctor']['full_name']}",
                                   callback_data=f"single_patient_chat:{i['id']}")
        keyboard.insert(btn)
    back = InlineKeyboardButton("🔙 Назад", callback_data="single_patient_chat:cancel")
    keyboard.row(back)
    return keyboard


# detail chat, e.g open, stop, back
async def manage_chat_doctor(status, chat):
    keyboard = InlineKeyboardMarkup(row_width=2)
    stop = InlineKeyboardButton("🛑 Стоп Чат", callback_data="manage_chat:stop")
    back = InlineKeyboardButton("🔙 Назад", callback_data="manage_chat:cancel")
    hash_data = create_hash(
        {"doctor": {"id": chat['patient']['doctor']['id'], "name": chat['patient']['doctor']['full_name']},
         "patient": {"id": chat['patient']['id'], "name": chat['patient']['full_name']}, "type": 'doctor'}
    )
    # simple chat btn
    webapp_url = f"{env.str('UI_DOMEN')}/meeting_chat/{chat['chat_code']}/{hash_data}"
    webapp_main = WebAppInfo(url=webapp_url)
    web_app = InlineKeyboardButton(text=f"💬 Открыть Чат", web_app=webapp_main)
    # video chat btn
    webapp_url_room = f"{env.str('UI_DOMEN')}/meeting_room/{chat['meeting_root']}/{hash_data}"
    webapp_main_r = WebAppInfo(url=webapp_url_room)
    w_r = InlineKeyboardButton(text=f"📹 Открыть Видеочат", web_app=webapp_main_r)
    keyboard.row(web_app, w_r)
    if not status == "close":
        keyboard.add(stop)
    keyboard.add(back)
    return keyboard


async def manage_patient_chat(chat):
    keyboard = InlineKeyboardMarkup(row_width=2)
    back = InlineKeyboardButton("🔙 Назад", callback_data="single_patient_chat:cancel")
    hash_data = create_hash(
        {"doctor": {"id": chat['patient']['doctor']['id'], "name": chat['patient']['doctor']['full_name']},
         "patient": {"id": chat['patient']['id'], "name": chat['patient']['full_name']}, "type": 'patient'}
    )
    webapp_url = f"{env.str('UI_DOMEN')}/meeting_chat/{chat['chat_code']}/{hash_data}"
    webapp_main = WebAppInfo(url=webapp_url)
    web_app = InlineKeyboardButton(text=f"💬 Открыть", web_app=webapp_main)
    keyboard.row(web_app)
    keyboard.add(back)
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
