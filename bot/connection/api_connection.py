import aiohttp
import json
from data.config import API_URL


async def add_user(user_id, username=None):
    url = API_URL + "/api/v1/user/"
    payload = {
        "user_id": user_id,
        "username": username,
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(url, data=payload) as response:
            if response.status == 200:
                return await response.json()
            else:
                return "REQUEST ERROR"


async def get_users():
    url = API_URL + "/api/v1/user/"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                return await response.json()
            else:
                return "REQUEST ERROR"


async def update_doctor(user_id, username, activate_code):
    url = API_URL + "/api/v1/doctor/"
    payload = {
        "user_id": user_id,
        "username": username,
        "activate_code": activate_code
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(url, data=payload) as response:
            if response.status == 200:
                return await response.json()
            else:
                return "REQUEST ERROR. LOOK AT DRF"


async def get_my_booking(user):
    url = API_URL + "/api/v1/patient/"
    payload = {
        "user": user
    }
    async with aiohttp.ClientSession() as session:
        async with session.get(url, data=payload) as response:
            if response.status == 200:
                return await response.json()
            else:
                return False


async def get_my_result(user):
    url = API_URL + "/api/v1/patient_result"
    payload = {
        "user": user
    }
    async with aiohttp.ClientSession() as session:
        async with session.get(url, data=payload) as response:
            if response.status == 200:
                return await response.json()
            else:
                return False
