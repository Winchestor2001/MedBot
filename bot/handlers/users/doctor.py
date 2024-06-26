from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from utils.misc.change_format_date import change_format_date, detail_date
from keyboards.inline.doctor import *
from connection.api_connection import *
from states.Admin import Payment

from connection.api_connection import stop_chat

data_methods = {
    "qiwi": "Введите Qiwi тел.номер",
    "yoomoney": "Введите Yoomoney тел.номер",
    "payeer": "Введите Payeer номер",
    "perfectmoney": "Введите Perfectmoney номер",
    "cards_ru": "Введите номер карты",
    "cards_ua": "Введите номер карты",
    "bitcoin": "Введите номер кошелька",
    "tether_trc20": "Введите номер кошелька",
}


async def doctor_intro(call: types.CallbackQuery):
    # await call.answer()
    # await call.message.delete()
    msg = f"Здравствуйте👋, {call.from_user.full_name}!\n" \
                 f"Мы рады видеть вас снова. Спасибо, что продолжаете с нами работать над улучшением " \
                 f"здоровья и благополучия наших пациентов."
    data = call.data.split(":")[1]
    if data == "profile":
        d = await get_doctor_info(call.from_user.id)
        text = f"👨‍⚕️ Доктор: {d['doctors']['full_name']}\n" \
               f"🎯 Специальность: {d['doctors']['direction']}\n" \
               f"💸 Цена: {d['doctors']['price']} ₽ \n" \
               f"💲 Ваш баланс: {d['doctors']['balance']} ₽"
        btn = await get_money()
        # await call.message.answer_photo(d["doctors"]["avatar"], caption=text, reply_markup=btn)
        await call.message.edit_text(text, reply_markup=btn)

    elif data == "chats":
        d = await get_doctor_chats(call.from_user.id)
        # print(d)
        if d.get("chats", False):
            btn = await get_chats(d)
            await call.message.edit_text("👤 Пациенты", reply_markup=btn)
        else:
            await call.answer("У Вас нет Пациенты", show_alert=True)
            btn = await basic()
            await call.message.edit_text(msg + f"\nТы доктор.", reply_markup=btn)
            # await welcomer_message(call.message)

    elif data == "get_money":
        methods = await get_payment_methods()
        btn = await payment_method_btn(methods)
        await call.message.edit_text("Выберите способ оплаты 👇", reply_markup=btn)

    elif data == "cancel":
        btn = await basic()
        await call.message.edit_text(msg, reply_markup=btn)


async def payment(call: types.CallbackQuery, state: FSMContext):
    # await call.message.delete()
    await call.answer()
    msg = f"Здравствуйте👋, {call.from_user.full_name}!\n" \
          f"Мы рады видеть вас снова. Спасибо, что продолжаете с нами работать над улучшением " \
          f"здоровья и благополучия наших пациентов."
    method = call.data.split(":")[1]
    if method == "cancel":
        btn = await basic()
        await call.message.edit_text(msg, reply_markup=btn)

    if data_methods.get(method, False):
        cancel = await cancel_btn()
        await call.message.edit_text(f"<b>{data_methods[method]}</b>\n", reply_markup=cancel)
        await Payment.text.set()
        await state.update_data({
            "method": method,
        })


async def get_payment_account(message: types.Message, state: FSMContext):
    text = message.text.replace("+", "")
    data = await state.get_data()
    method = data["method"]

    all_methods = await get_payment_methods()
    cancel = await cancel_btn()
    await message.answer(f"Введите сумму\n"
                         f"<em>Мин сумма: {all_methods['list'][method]['min']}</em>\n"
                         f"<em>Макс сумма: {all_methods['list'][method]['max']}</em>\n"
                         f"<em>Комиссия: {all_methods['list'][method]['commission_percent']}</em>%",
                         reply_markup=cancel)
    await state.update_data({
        "account": text,
        "commission": all_methods['list'][method]['commission_percent']
    })
    await Payment.price.set()


async def get_payment_price(message: types.Message, state: FSMContext):
    await state.update_data({
        "price": message.text
    })
    data = await state.get_data()
    method = data["method"]
    account = data["account"]
    price = int(data["price"])
    commission = int(data["commission"])
    doctor_info = await get_doctor_info(message.from_user.id)
    balance = doctor_info["doctors"]["balance"]
    msg = f"Здравствуйте👋, {message.from_user.full_name}!\n" \
          f"Мы рады видеть вас снова. Спасибо, что продолжаете с нами работать над улучшением " \
          f"здоровья и благополучия наших пациентов."
    if int(balance) <= int(price + price / 100 * commission):
        await message.answer("❌ Недостаточно вашего баланса")
    else:
        withdraw_info = await withdraw_doctor(method, account, price, message.from_user.id)
        await message.answer("✅ Ваш запрос принят, оплата за ваш аккаунт произойдет как можно скорее.")
    btn = await basic()
    await message.answer(msg, reply_markup=btn)
    await state.finish()


async def cancel_handler(call: types.CallbackQuery, state: FSMContext):
    await call.answer()
    await call.message.delete()
    await state.finish()
    msg = f"Здравствуйте👋, {call.from_user.full_name}!\n" \
          f"Мы рады видеть вас снова. Спасибо, что продолжаете с нами работать над улучшением " \
          f"здоровья и благополучия наших пациентов."
    btn = await basic()
    await call.message.answer(msg, reply_markup=btn)


async def chats(call: types.CallbackQuery, state: FSMContext):
    await call.answer()
    data = call.data.split(":")[1]
    patient = await get_single_chat(data)
    if patient:
        d = patient['chat'][0]['created_at'][:10]
        date = await change_format_date(d)
        status = patient["chat"][0]['patient']["confirance_status"]
        sts_text = "Процесс" if status == "wait" else "Закрыто"
        text = f"🆔 {patient['chat'][0]['id']}\n" \
               f"👨‍⚕️Доктор: {patient['chat'][0]['patient']['doctor']['full_name']}\n" \
               f"👤 Пациент: {patient['chat'][0]['patient']['full_name']}\n" \
               f"📅 Дата регистрации: {date}\n" \
               f"📊 Статус: {sts_text}"
        await state.update_data(chat_code=patient["chat"][0]["chat_code"])
        btn = await manage_chat_doctor(status, patient["chat"][0])
        await call.message.edit_text(text, reply_markup=btn)


async def manage_chats(call: types.CallbackQuery, state: FSMContext):
    await call.answer()
    data = call.data.split(":")[1]
    btn = await basic()
    if data == "cancel":
        d = await get_doctor_chats(call.from_user.id)
        # print(d)
        if d.get("chats", False):
            btn = await get_chats(d)
            await call.message.edit_text("👤 Пациенты", reply_markup=btn)
    elif data == "stop":
        s = await state.get_data()
        chat_code = s["chat_code"]
        resp = await stop_chat(chat_code)  # stop qiladigan funksiya
        await state.finish()
        if resp:
            await call.message.edit_text("✅ Остановлено")
        else:
            await call.message.edit_text("❌ Не Остановлено")
        msg = f"Здравствуйте👋, {call.from_user.full_name}!\n" \
              f"Мы рады видеть вас снова. Спасибо, что продолжаете с нами работать над улучшением " \
              f"здоровья и благополучия наших пациентов."
        await call.message.answer(msg, reply_markup=btn)


def register_doctor_handler_py(dp: Dispatcher):
    dp.register_callback_query_handler(chats, text_contains=["chat_doctor:"])
    dp.register_callback_query_handler(manage_chats, text_contains="manage_chat:")
    dp.register_callback_query_handler(doctor_intro, text_contains=["doctor:"])
    dp.register_callback_query_handler(payment, text_contains=["payment:"])
    dp.register_callback_query_handler(cancel_handler, text=["handler:cancel"], state=Payment.text)
    dp.register_callback_query_handler(cancel_handler, text=["handler:cancel"], state=Payment.price)
    dp.register_message_handler(get_payment_account, state=Payment.text)
    dp.register_message_handler(get_payment_price, state=Payment.price)
