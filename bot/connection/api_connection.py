import aiohttp
import json
from bot.data.config import API_URL


async def add_user(user_id, username=None):
    url = API_URL + "/api/v1/user/"
    payload = {
        "user_id": user_id,
        "username": username,
    }
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, data=payload) as response:
                return await response.json()
    except Exception as err:
        pass


async def get_users():
    url = API_URL + "/api/v1/user/"
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                return await response.json()
    except Exception as err:
        pass

