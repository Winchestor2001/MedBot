from aiogram import types, Dispatcher
from keyboards.inline.admin_func import keyboard
from filters.isAdmin import IsAdmin
from keyboards.inline.intro import main_keyboard


async def intro_admin(message: types.Message):
    await message.answer(f"Добро Пожаловать - Админ - {message.from_user.first_name}\n"
                         f"Это команды, которую ты можете сделать.", reply_markup=keyboard)


async def exit_admin_panel(call: types.CallbackQuery):
    msg = f"Добро пожаловать 👋, {call.from_user.full_name}!\n\n"
    await call.message.edit_text(msg, reply_markup=main_keyboard)


def register_admin_intro_handler(dp: Dispatcher):
    dp.register_message_handler(intro_admin, IsAdmin(), commands=["admin"])
    dp.register_callback_query_handler(exit_admin_panel, IsAdmin(), text="admin:exit")
