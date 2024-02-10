from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from data.config import UI_DOMEN

main_keyboard = InlineKeyboardMarkup(row_width=2)
webA = WebAppInfo(url=UI_DOMEN)
btn = InlineKeyboardButton(text="Запись на консультацию", web_app=webA)
my_booking = InlineKeyboardButton(text="📋 Мои записи", callback_data="profile:my_booking")
my_result = InlineKeyboardButton(text="📋 Мои результаты", callback_data="profile:my_result")
chats = InlineKeyboardButton("💬 Чаты", callback_data="patient:chats")
support_btn = InlineKeyboardButton(text="📨 Поддержка", callback_data="support")
main_keyboard.add(btn)
main_keyboard.row(my_booking, my_result)
main_keyboard.row(chats)
main_keyboard.row(support_btn)
