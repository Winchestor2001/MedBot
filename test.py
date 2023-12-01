from aiohttp import web
import aiohttp
import json


async def handle(request):
    # Ваш токен бота и ID чата
    bot_token = 'token'
    chat_id = 'id'

    # Создайте объект InlineKeyboardMarkup с ссылкой
    inline_keyboard = [[{"text": "Открыть ссылку", "url": "https://webmed-two.vercel.app/"}]]
    inline_markup = {"inline_keyboard": inline_keyboard}

    # Преобразуйте объект в строку JSON
    reply_markup = json.dumps(inline_markup)

    # Формируем URL для отправки сообщения с кнопкой
    url = f'https://api.telegram.org/bot{bot_token}/sendMessage'
    params = {
        'chat_id': chat_id,
        'text': 'Пример сообщения с инлайн-кнопкой',
        'reply_markup': reply_markup
    }

    # Отправляем запрос с использованием aiohttp
    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as response:
            # Обработка ответа, если необходимо
            print(response.json())

    return web.Response(text='Сообщение отправлено')

app = web.Application()
app.router.add_get('/', handle)

if __name__ == '__main__':
    web.run_app(app)
