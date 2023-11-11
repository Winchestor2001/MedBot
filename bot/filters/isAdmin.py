from aiogram import types
from aiogram.dispatcher.filters import BoundFilter
from bot.data.config import ADMINS


class IsAdmin(BoundFilter):
    async def check(self, message: types.Message):
        user_id = str(message.from_user.id)
        return user_id in ADMINS
