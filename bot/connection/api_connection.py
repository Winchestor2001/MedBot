import aiohttp
import json


async def add_user(user_id, username=None):
    url = "http://127.0.0.1:8000/api/v1/user/"
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
    url = "http://127.0.0.1:8000/api/v1/user/"
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                return await response.json()
    except Exception as err:
        pass

