from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo

main_keyboard = InlineKeyboardMarkup(row_width=2)
webA = WebAppInfo(url="https://github.com/")
btn = InlineKeyboardButton(text="Main Page", web_app=webA)
my_booking = InlineKeyboardButton(text="📋 My Bookings", callback_data="profile:my_booking")
my_result = InlineKeyboardButton(text="📋 My Results", callback_data="profile:my_result")
main_keyboard.add(btn)
main_keyboard.row(my_booking, my_result)
