from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

keyboard = InlineKeyboardMarkup(row_width=2)
btn = InlineKeyboardButton(text="👥 Пользователи", callback_data="admin:users")
btn2 = InlineKeyboardButton(text="📩 Рассылка", callback_data="admin:send_ads")
btn3 = InlineKeyboardButton(text="🔙 Выход", callback_data="admin:exit")
keyboard.add(btn, btn2, btn3)

back_btn = InlineKeyboardMarkup(row_width=1)
b_btn = InlineKeyboardButton(text="🔙 Назад", callback_data="admin:back")
back_btn.add(b_btn)
