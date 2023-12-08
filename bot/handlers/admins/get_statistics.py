from aiogram import types, Dispatcher
from bot.connection.api_connection import *
from bot.filters.isAdmin import IsAdmin
from bot.keyboards.inline.admin_func import back_btn
from bot.handlers.admins.intro_admin import intro_admin


async def get_all_user(call: types.CallbackQuery):
    users = await get_users()
    await call.message.edit_text(f"В базе есть <b>{len(users['users'])}</b> пользователя", reply_markup=back_btn)


async def back(call: types.CallbackQuery):
    await call.message.delete()
    await intro_admin(call.message)


def register_get_statistics_py(dp: Dispatcher):
    dp.register_callback_query_handler(get_all_user, IsAdmin(), text="admin:users")
    dp.register_callback_query_handler(back, IsAdmin(), text="admin:back")
