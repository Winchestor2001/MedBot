from aiogram import executor
from loader import dp
from launcher_handler import launch_handlers
# import middlewares, filters, handlers
from utils.set_bot_commands import set_default_commands


async def on_startup(dispatcher):
    # Set Default Commands
    await set_default_commands(dispatcher)
    # launch handlers
    await launch_handlers(dispatcher)


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)
