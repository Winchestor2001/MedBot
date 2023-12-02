from datetime import datetime, timedelta
import base64
import requests
from googletrans import Translator
import json
from aiogram.types import WebAppInfo
import secrets
from bot.data.config import BOT_TOKEN


def check_dates(user_data, doctor_data, month, day):
    user_dates = [(item.confirance_date, item.confirance_time) for item in user_data]
    doctor_dates = [(item.date, item.time_interval) for item in doctor_data.date_set.all()]

    coinciding_dates = []
    new_times = []

    try:
        for d_date in doctor_dates:
            if d_date[0].month == int(month) and d_date[0].day == int(day):
                coinciding_dates.append(d_date)
    except:
        pass

    if coinciding_dates:
        for doc_interval in coinciding_dates:
            if not any(part[1] == doc_interval[1] for part in user_dates):
                new_times.append(doc_interval)

    return new_times


def filter_doctor_direction(data):
    result = []

    for item in data:
        result.append(
            item.direction
        )

    return list(set(result))


def create_hash(data):
    chars = [' ', '!', '"', '#', '$', '%', '&', "'", '(', ')', '*', '+', ',', '-', '.', '/', ':', ';', '<', '=', '>',
             '?', '@', '[', '\\', ']', '^', '_', '`', '{', '|', '}', '~', '0', '1', '2', '3', '4', '5', '6', '7', '8',
             '9', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
             'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O',
             'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    key = ['d', '~', 'x', '4', ':', 'b', 't', '|', '?', '*', '6', 'R', '^', 'M', 'D', 'p', '/', 'w', 'K', '\\', 'a',
           'j', 'r', 'g', ']', 'B', ';', 'W', 'J', 'k', 'S', 'q', 'e', '8', 'U', 'v', '(', '1', 'G', 'z', ')', 'P', '{',
           '0', '&', '2', 'I', 'm', '9', "'", 'N', 'Y', 'C', '%', 'F', 'L', '<', '$', 'H', '+', '}', 's', '[', 'y', '.',
           'u', ',', '"', 'h', '3', '7', 'E', 'i', '`', 'Z', '#', ' ', '>', 'o', 'T', 'l', 'c', 'A', 'n', 'X', '-', 'Q',
           '=', 'V', 'O', '!', '5', 'f', '_', '@']

    plain_text = str(data)
    cipher_text = ""

    for letter in plain_text:
        index = chars.index(letter)
        cipher_text += key[index]

    item = str(cipher_text).encode('utf-8')
    base64_bytes = base64.b64encode(item)
    base64_string = base64_bytes.decode("utf-8")

    return base64_string


def send_message(token, user_id, msg):
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    params = {
        "chat_id": user_id,
        "text": msg
    }
    response = requests.post(url, data=params)
    return response.json()


translator = Translator()


def modify_date_type(date):
    input_datetime = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
    day = input_datetime.day
    month = input_datetime.strftime("%B")
    changed_type = f"{day} {month}"
    lang_changed = translator.translate(changed_type, dest='ru').text
    return lang_changed


def send_message_with_web_app(user_id, url, message):
    base_url = f'https://api.telegram.org/bot{BOT_TOKEN}/'

    web = WebAppInfo(url=f"{url}")
    inline_keyboard = {
        'inline_keyboard': [
            [{'text': 'Go Meeting', 'web_app': web.__dict__['_values']}]
        ]
    }
    inline_keyboard_json = json.dumps(inline_keyboard)
    response = requests.post(
        base_url + 'sendMessage',
        json={
            'chat_id': user_id,
            'text': message,
            'reply_markup': inline_keyboard_json
        }
    )
    return response.json()


def generate_room_code(length=6):
    characters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    room_code = ''.join(secrets.choice(characters) for _ in range(length))

    return room_code

