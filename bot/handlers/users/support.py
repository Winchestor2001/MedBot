import logging

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from keyboards.inline.support_btn import admin_keyboard, reply
from keyboards.inline.intro import main_keyboard
from states.Admin import Message, Admin
from loader import bot
from connection.api_connection import get_admins_list
from data.config import ADMINS


async def support_text(call: types.CallbackQuery):
    await call.message.delete()
    admins = await get_admins_list()
    btn = await admin_keyboard(f"tg:user?id={admins['admins'][0]}")
    text = f"Вы обратились в службу поддержки клиентов. " \
           f"Если у вас есть какие-либо вопросы, нажмите кнопку ниже 👇"
    await call.message.answer(text, reply_markup=btn)


# async def intro_in_support(call: types.CallbackQuery):
#     await call.message.delete()
#     await call.message.answer("Отправьте сообщение:")
#     await Message.text.set()


# async def send_admin(message: types.Message, state: FSMContext):
#     await message.answer("Ваше сообщение отправлено администратору.")
#     msg = f"Добро пожаловать 👋, {message.from_user.full_name}!"
#     await message.answer(msg, reply_markup=main_keyboard)
#     await state.update_data({
#         "user": message.from_user,
#     })
#     data = await state.get_data()
#     content_type = message.content_type
#     first_name = message.from_user.first_name
#     user_id = message.from_user.id
#     admin_list = await get_admins_list()
#     if admin_list["admins"]:
#         if content_type == "text":
#             for admin in admin_list["admins"]:
#                 await bot.send_message(admin, f"{message.text}\n\n"
#                                               f"Отправитель: "
#                                               f"{first_name} - {user_id}",
#                                        reply_markup=reply)
#         elif content_type == "photo":
#             for admin in admin_list["admins"]:
#                 await bot.send_photo(admin, f"{message.photo[-1].file_id}", caption=f"{message.caption}\n\n"
#                                                                                     f"Отправитель: "
#                                                                                     f"{first_name} - {user_id}",
#                                      reply_markup=reply)
#         elif content_type == "video":
#             for admin in admin_list["admins"]:
#                 await bot.send_video(admin, f"{message.video.file_id}", caption=f"{message.caption}\n\n"
#                                                                                 f"Отправитель: "
#                                                                                 f"{first_name} - {user_id}",
#                                      reply_markup=reply)
#         elif content_type == "audio":
#             for admin in admin_list["admins"]:
#                 await bot.send_audio(admin, f"{message.audio}", caption=f"{message.caption}\n\n"
#                                                                         f"Отправитель: "
#                                                                         f"{first_name} - {user_id}",
#                                      reply_markup=reply)
#         elif content_type == "voice":
#             for admin in admin_list["admins"]:
#                 await bot.send_voice(admin, f"{message.voice['file_id']}", caption=f"Отправитель: "
#                                                                                    f"{first_name} - {user_id}",
#                                      reply_markup=reply)
#     else:
#         logging.info("Error in get admins list or In DB hasn't admins")
#     await state.finish()
#
#
# # when Ответъ btn press, this function work
# # intro send answer to user and require answer for user
# async def get_text(call: types.CallbackQuery, state: FSMContext):
#     await call.answer()
#     first_name, user_id = call.message.html_text.split(":")[-1].split(" - ")
#     await state.update_data({
#         "user_id": user_id
#     })
#     await call.message.answer(f"Ваш ответ к {first_name}: ")
#     await Admin.text.set()
#
#
# # send admin's message to user
# async def send_user(message: types.Message, state: FSMContext):
#     answer = f"Служба Поддержки: \n\n"
#     answer += message.text
#     data = await state.get_data()
#     user_id = data["user_id"]
#     await bot.send_message(user_id, answer)
#     await message.answer("Отправлено ✅")
#     await state.finish()


# this handler used to cancel function in condition state
# async def cancel_func_in_state(message: types.Message, state: FSMContext):
#     await state.finish()
#     if message.get_full_command()[0] == "/start":
#         msg = f"Добро пожаловать 👋, {message.from_user.full_name}!"
#         await message.answer(msg, reply_markup=main_keyboard)
#     elif message.text == "/help":
#         text = f"Вы обратились в службу поддержки клиентов. " \
#                f"Если у вас есть какие-либо вопросы, нажмите кнопку ниже"
#         await message.answer(text, reply_markup=keyboard)


def register_support_handler_py(dp: Dispatcher):
    dp.register_callback_query_handler(support_text, text=["support"])
    # dp.register_callback_query_handler(intro_in_support, text=["support_message"])
    # dp.register_message_handler(cancel_func_in_state, state=Message.text, commands=["start", "help"])
    # dp.register_message_handler(send_admin, state=Message.text, content_types=["text", "photo", "video",
    #                                                                            "audio", "voice"])
    # dp.register_callback_query_handler(get_text, text="admin_reply_btn")
    # dp.register_message_handler(cancel_func_in_state, state=Admin.text, commands=["start", "help"])
    # dp.register_message_handler(send_user, state=Admin.text)
