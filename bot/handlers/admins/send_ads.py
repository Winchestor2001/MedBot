import asyncio
from aiogram.dispatcher import FSMContext
from aiogram import types, Dispatcher
from connection.api_connection import get_users
from filters.isAdmin import IsAdmin
from handlers.admins.intro_admin import intro_admin
from keyboards.inline.intro import main_keyboard
from loader import bot
from states.Admin import Ads
from keyboards.inline.admin_func import back_btn


async def enter_ads(call: types.CallbackQuery):
    await call.message.edit_text("Введите Контент, (video, image, gif, etc.)", reply_markup=back_btn)
    await Ads.text.set()


async def send_ads(msg: types.Message, state: FSMContext):
    users = await get_users()
    text_type = msg.content_type
    rep_btn = msg.reply_markup
    text_html = msg.html_text
    send_user = 0
    send_error = 0
    for user in users["users"]:
        user_id = int(user["user_id"])
        try:
            if text_type == 'sticker':
                return
            elif text_type == 'text':
                await bot.send_message(user_id, text_html, reply_markup=rep_btn)
                await asyncio.sleep(0.05)
            elif text_type == 'video':
                await bot.send_video(user_id, msg.video.file_id, caption=text_html, reply_markup=rep_btn)
                await asyncio.sleep(0.05)
            elif text_type == 'photo':
                await bot.send_photo(user_id, msg.photo[-1].file_id, caption=text_html, reply_markup=rep_btn)
                await asyncio.sleep(0.05)
            elif text_type == 'audio':
                await bot.send_audio(user_id, msg.audio, reply_markup=rep_btn)
                await asyncio.sleep(0.05)
            elif text_type == 'location':
                lat = msg.location['latitude']
                lon = msg.location['longitude']
                await bot.send_location(user_id, lat, lon)
                await asyncio.sleep(0.05)
            send_user += 1
        except Exception:
            send_error += 1
            continue
    if send_user == 0:
        await bot.send_message(msg.from_user.id, 'Xech kimga yuborilmadi')
    else:
        await bot.send_message(msg.from_user.id,
                               f"📃 Отправил: до <b>{send_user + send_error}</b> пользователей\n"
                               f"✅ Активные пользователей: <b>{send_user}</b>\n"
                               f"❌ Забаненные пользователей: <b>{send_error}</b>\n")
    await state.finish()


async def cancel_func_start(message: types.Message, state: FSMContext):
    await state.finish()
    msg = f"Добро пожаловать 👋, {message.from_user.full_name}!\n\n"
    await message.answer(msg, reply_markup=main_keyboard)


# async def cancel_func_help(message: types.Message, state: FSMContext):
#     await message.delete()
#     await state.finish()
#     await help()


async def back(call: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await call.message.delete()
    await intro_admin(call.message)


def register_send_ads_py(dp: Dispatcher):
    dp.register_callback_query_handler(enter_ads, IsAdmin(), text="admin:send_ads")
    dp.register_message_handler(send_ads, IsAdmin(), state=Ads.text, content_types=["text", "photo", "video",
                                                                                    "location", "audio", "sticker"])
    dp.register_message_handler(cancel_func_start, commands=["start"], state=Ads.text)
    dp.register_callback_query_handler(back, IsAdmin(), state=Ads.text, text="admin:back")
