from handlers.admins.get_statistics import register_get_statistics_py
from handlers.admins.intro_admin import register_admin_intro_handler
from handlers.users.my_bookings import register_my_bookings_py
from handlers.users.my_results import register_my_results_py
from handlers.users.user_handlers import register_user_handlers_py
from handlers.admins.send_ads import register_send_ads_py
from handlers.users.support import register_support_handler_py
from handlers.users.doctor import register_doctor_handler_py
from handlers.users.patient_chat import register_chat_patient_handlers_py


async def launch_handlers(dispatcher):
    register_doctor_handler_py(dispatcher)
    register_chat_patient_handlers_py(dispatcher)
    register_user_handlers_py(dispatcher)
    register_my_bookings_py(dispatcher)
    register_my_results_py(dispatcher)
    register_admin_intro_handler(dispatcher)
    register_get_statistics_py(dispatcher)
    register_send_ads_py(dispatcher)
    register_support_handler_py(dispatcher)
