from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandHelp

from bot.loader import dp


@dp.message_handler(CommandHelp())
async def help_user(message: types.Message):
    msg = f"Bot Tomonidan foydalanuvchiga yordam ko'rsatish bo'limi\n" \
          f"Buyruqlar:\n/start — Botni ishga tushirish\n" \
          f"/help — Yordam Ko'rsatish va Bot ishlash tartibi\n\n" \
          f"<b>Botni ishlash tartibi</b>\n\n" \
          f"1.Agar Siz yozgan matn biror manoga ega bo'lsa va mazmuni bo'lsa bu bot sizga yozgan matningizni Ingliz tilida tarjimasini qaytaradi.\n" \
          f"2.Agar siz yozgan matn biror bir atama yoki shahar nomi v.h.z. larni yozsangiz ularni ma'nosini qaytaradi.\n" \
          f"3.Agar siz ma'nosiz yoki lug'atda yo'q so'zlarni yozsangiz \"bunday so'z topilmadi\" degan xato chiqadi. " \


    await message.reply(msg)

