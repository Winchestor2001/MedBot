from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from connection.api_connection import get_admins_list


async def admin_keyboard(url):
    keyboard = InlineKeyboardMarkup(row_width=1)
    btn = InlineKeyboardButton(text="🗣 Служба Поддержки", url=url)
    keyboard.add(btn)
    return keyboard


reply = InlineKeyboardMarkup(row_width=1)
answer_btn = InlineKeyboardButton(text="Ответить", callback_data="admin_reply_btn")
reply.add(answer_btn)
