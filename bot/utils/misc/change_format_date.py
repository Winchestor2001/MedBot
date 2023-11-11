from datetime import datetime
from googletrans import Translator


translator = Translator()


async def change_format_date(date):
    input_datetime = datetime.strptime(date, "%Y-%m-%dT%H:%M:%SZ")
    day = input_datetime.day
    month = input_datetime.strftime("%B")
    changed_type = f"{day} {month}"
    lang_changed = translator.translate(changed_type, dest='ru').text
    return lang_changed


async def detail_date(date):
    input_datetime = datetime.strptime(date, "%Y-%m-%dT%H:%M:%SZ")
    day = input_datetime.day
    month = input_datetime.strftime("%B")
    year = input_datetime.strftime("%Y")
    hour = input_datetime.strftime("%H")
    minute = input_datetime.strftime("%M")
    time_zone = input_datetime.strftime("%Z")
    changed_type = f"{day} {month} {year}, {hour}:{minute} {time_zone}"
    lang_changed = translator.translate(changed_type, dest='ru').text
    return lang_changed
