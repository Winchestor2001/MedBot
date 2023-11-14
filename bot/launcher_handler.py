from bot.handlers.admins.get_statistics import register_get_statistics_py
from bot.handlers.admins.intro_admin import register_admin_intro_handler
from bot.handlers.users.my_bookings import register_my_bookings_py
from bot.handlers.users.my_results import register_my_results_py
from bot.handlers.users.user_handlers import register_user_handlers_py
from bot.handlers.admins.send_ads import register_send_ads_py


async def launch_handlers(dispatcher):
    register_user_handlers_py(dispatcher)
    register_my_bookings_py(dispatcher)
    register_my_results_py(dispatcher)
    register_admin_intro_handler(dispatcher)
    register_get_statistics_py(dispatcher)
    register_send_ads_py(dispatcher)

