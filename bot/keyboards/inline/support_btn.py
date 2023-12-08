from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


keyboard = InlineKeyboardMarkup(row_width=1)
btn = InlineKeyboardButton(text="🗣 Служба Поддержки", callback_data="support_message")
keyboard.add(btn)

reply = InlineKeyboardMarkup(row_width=1)
answer_btn = InlineKeyboardButton(text="Ответь", callback_data="admin_reply_btn")
reply.add(answer_btn)
