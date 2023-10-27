from aiogram import executor

from bot.handlers.users.user_handlers import register_user_handlers_py
from bot.loader import dp
import middlewares, filters, handlers
from utils.notify_admins import on_startup_notify
from bot.utils.set_bot_commands import set_default_commands


async def on_startup(dispatcher):
    # await db.create()
    # await db.create_table_users()

    # Birlamchi komandalar (/star va /help)
    await set_default_commands(dispatcher)

    register_user_handlers_py(dispatcher)


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)
