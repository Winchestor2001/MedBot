import random

from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.lib import colors
from datetime import datetime, timedelta
from core.settings import env
import base64
import requests
from googletrans import Translator
import json
from aiogram.types import WebAppInfo
import secrets
from bot.data.config import BOT_TOKEN
import subprocess
import os
from core.settings import PAYMENT_DOMAIN
from uuid import uuid4


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
            [{'text': 'Ответить', 'web_app': web.__dict__['_values']}]
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


def edit_telegram_chat_message(user_id, message_id, doctor):
    base_url = f'https://api.telegram.org/bot{BOT_TOKEN}/'
    response = requests.post(
        base_url + 'editMessageText',
        json={
            'chat_id': user_id,
            'message_id': message_id,
            'text': f'Вам звонил доктор: {doctor}'
        }
    )
    return response.json()


def send_video_api(file_path):
    params = {
        "chat_id": -4008620657
    }

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendVideo"

    with open(file_path, "rb") as video_file:
        files = {"video": video_file}
        response = requests.post(url, params=params, files=files)
    os.unlink(file_path)
    if response.status_code == 200:
        return response.json()
    else:
        print("There some problem in send message video, (file's size big than standard)")
        return "There some problem in send message video, (file's size big than standard)"


def generate_room_code(length=6):
    characters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    room_code = ''.join(secrets.choice(characters) for _ in range(length))

    return room_code


def count_ratings(obj):
    voted_patients = len(obj)
    if voted_patients > 0:
        doctor_all_rate = 0
        for rate in obj:
            doctor_all_rate += rate.rating * 20
        return round(doctor_all_rate / 20 / voted_patients, 1)
    else:
        return 0


def save_recorded_video(f1, f2, output):
    current_direction = os.getcwd()
    file1 = f"{current_direction}/media/{f1}"
    file2 = f"{current_direction}/media/{f2}"
    outp = f"{current_direction}/media/{output}"
    ffmpeg_command = [
        'ffmpeg',
        '-i', file1,
        '-i', file2,
        '-filter_complex',
        '[0:v]setpts=PTS-STARTPTS,scale=qvga[a0];[1:v]setpts=PTS-STARTPTS,scale=qvga[a1];[a0][a1]xstack=inputs=2:layout=0_0|w0_0[outv];[0:a][1:a]amix=inputs=2[aout]',
        '-map', '[outv]',
        '-map', '[aout]',
        '-c:v', 'libvpx',
        '-c:a', 'libvorbis',
        '-y',
        outp,
    ]

    try:
        subprocess.run(ffmpeg_command)
    except Exception as e:
        print("Error in ffmpeg")

    send_to_telegram_and_delete_record_video(f1, f2)
    send_video_api(outp)


def send_to_telegram_and_delete_record_video(f1, f2):
    current_direction = os.getcwd()
    try:
        os.unlink(f"{current_direction}/media/{f1}")
        os.unlink(f"{current_direction}/media/{f2}")
    except:
        pass


def create_pdf(data, output_path):
    left_margin = 0.5 * inch
    right_margin = 0.5 * inch
    top_margin = 0.4 * inch
    patient = data.patient.full_name
    doctor = data.patient.doctor.full_name
    body = data.result_text
    date = data.patient.confirance_date

    doc = SimpleDocTemplate(output_path, pagesize=letter,
                            leftMargin=left_margin, rightMargin=right_margin,
                            topMargin=top_margin)

    article = f"<b><font size='24' color='indigo'>TeleCure.ru</font></b>\n\n" \
              f"<hr></hr>" \
              f"<b>Patient</b>: {patient}\n" \
              f"<b>Doctor</b>: {doctor}\n" \
              f"<b>Diagnosis</b>: {body}\n" \
              f"<em><b>Date</b>: {date}</em>"

    styles = getSampleStyleSheet()

    content = []
    paragraphs = article.split('\n')
    for paragraph in paragraphs:
        content.append(Paragraph(paragraph, styles['BodyText']))
        content.append(Spacer(1, 4))

    doc.build(content)
    print("error in delete files")


def withdraw(my_id, method, amount: int, wallet):
    url = f'{PAYMENT_DOMAIN}/api/create-payoff'
    api_key = env.str("PAYMENT_API_KEY")  # Ключ API из раздела https://aaio.io/cabinet/api
    commission_type = 0  # Тип комиссии

    params = {
        'my_id': f"doctor_{my_id}_{random.randint(10, 1000)}",
        # 'my_id': f"doctor_{my_id}_123",
        'method': method,
        'amount': int(amount),
        'wallet': wallet,
        'commission_type': commission_type,
    }

    headers = {
        'Accept': 'application/json',
        'X-Api-Key': api_key
    }

    response = requests.post(url, data=params, headers=headers, timeout=(15, 60))
    return response.json()
