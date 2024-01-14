import hashlib
from urllib.parse import urlencode
from uuid import uuid4

import requests
from core.settings import PAYMENT_MERCHANT_ID, PAYMENT_API_KEY, PAYMENT_SECRET_KEY


def create_invoice(amount: str):
    currency = "RUB"
    lang = "ru"
    order_id = str(uuid4())
    sign = f':'.join([
        PAYMENT_MERCHANT_ID,
        amount,
        currency,
        PAYMENT_SECRET_KEY,
        order_id
    ])

    params = {
        'merchant_id': PAYMENT_MERCHANT_ID,
        'amount': amount,
        'currency': currency,
        'order_id': order_id,
        'sign': hashlib.sha256(sign.encode('utf-8')).hexdigest(),
        'desc': "Telecure BOT",
        'lang': lang
    }
    return "https://aaio.io/merchant/pay?" + urlencode(params), order_id


def check_invoice(bill_id: str):
    url = 'https://aaio.io/api/info-pay'
    params = {
        'merchant_id': PAYMENT_MERCHANT_ID,
        'order_id': bill_id
    }

    headers = {
        'Accept': 'application/json',
        'X-Api-Key': PAYMENT_API_KEY
    }

    r = requests.post(url, data=params, headers=headers, timeout=(15, 60))
    print(r.status_code)
    print(r.json())
