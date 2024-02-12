import aiohttp
from data.config import API_URL


async def add_user(user_id, username=None):
    url = API_URL + "/api/v1/user/"
    payload = {
        "user_id": user_id,
        "username": username,
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(url, data=payload) as response:
            if response.status in [200, 201]:
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
            if response.status == 201:
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


async def get_admins_list():
    url = API_URL + "/api/v1/admins_list/"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                return await response.json()
            else:
                return False


async def get_result_pdf(patient):
    url = API_URL + "/api/v1/patient_result_pdf"
    data = {
        "patient": patient
    }
    async with aiohttp.ClientSession() as session:
        async with session.get(url, data=data) as response:
            return await response.json()


async def get_doctor_info(user_id):
    url = API_URL + "/api/v1/doctor_about/"
    data = {
        "user_id": user_id
    }
    async with aiohttp.ClientSession() as session:
        async with session.get(url, data=data) as response:
            return await response.json()


async def get_doctor_chats(user_id):
    url = API_URL + "/api/v1/doctor_chats/"
    data = {
        "user_id": user_id
    }
    async with aiohttp.ClientSession() as session:
        async with session.get(url, data=data) as response:
            return await response.json()


async def get_single_chat(chat_id):
    url = API_URL + "/api/v1/single_chat/"
    data = {
        "chat_id": chat_id
    }
    async with aiohttp.ClientSession() as session:
        async with session.get(url, data=data) as response:
            return await response.json()


async def get_patient_chats(user_id):
    url = API_URL + "/api/v1/patient_chats/"
    data = {
        "user_id": user_id
    }
    async with aiohttp.ClientSession() as session:
        async with session.get(url, data=data) as response:
            if response.status == 200:
                return await response.json()
            else:
                return False


async def get_payment_methods():
    url = "https://aaio.io/api/methods-payoff"
    headers = {
        'Accept': 'application/json',
        'X-Api-Key': "NmNhOTdmNDMtOGI0Yi00YTZjLWFmOTgtZWZlMTdlNGY2OWI2OjdVUzBZZCNCUmhRZ25EWUs2aE5SUEByJUZmUjVsJkZX"
    }
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            return await response.json()


async def withdraw_doctor(method, account, price, user_id):
    url = API_URL + "/api/v1/withdraw/"
    payload = {
        "method": method,
        "account": account,
        "price": price,
        "user_id": user_id
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(url, data=payload) as response:
            return await response.json()


async def get_single_patient(patient_id):
    url = API_URL + "/api/v1/single_patient/"
    data = {
        "patient_id": patient_id
    }
    async with aiohttp.ClientSession() as session:
        async with session.get(url, data=data) as response:
            return await response.json()


async def stop_chat(chat_code):
    url = API_URL + "/api/v1/stop_chat/"
    data = {
        "chat_code": chat_code
    }
    async with aiohttp.ClientSession() as session:
        async with session.get(url, data=data) as response:
            return await response.json()

