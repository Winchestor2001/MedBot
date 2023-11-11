from aiogram import executor

from bot.handlers.users.user_handlers import register_user_handlers_py
from bot.handlers.users.my_bookings import register_my_bookings_py
from bot.handlers.users.my_results import register_my_results_py
from bot.loader import dp
# import middlewares, filters, handlers
from bot.utils.set_bot_commands import set_default_commands


async def on_startup(dispatcher):
    # Set Default Commands
    await set_default_commands(dispatcher)
    # register handlers
    register_user_handlers_py(dispatcher)
    register_my_bookings_py(dispatcher)
    register_my_results_py(dispatcher)


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)
