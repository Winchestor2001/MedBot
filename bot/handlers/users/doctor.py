from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from keyboards.inline.doctor import *
from connection.api_connection import *
from states.Admin import Payment


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
    await call.answer()
    await call.message.delete()
    msg = f"Добро пожаловать 👋, {call.from_user.full_name}!"
    data = call.data.split(":")[1]
    if data == "profile":
        d = await get_doctor_info(call.from_user.id)
        text = f"👨‍⚕️ Доктор: {d['doctors']['full_name']}\n" \
               f"🎯 Специальность: {d['doctors']['direction']}\n" \
               f"💸 Цена: {d['doctors']['price']} ₽ \n" \
               f"💲 Ваш баланс: {d['doctors']['balance']} ₽"
        btn = await get_money()
        await call.message.answer_photo(d["doctors"]["avatar"], caption=text, reply_markup=btn)

    elif data == "chats":
        d = await get_doctor_chats(call.from_user.id)
        if d["chats"]:
            btn = await get_chats(d)
            await call.message.answer("💬 Чаты", reply_markup=btn)
        else:
            await call.message.answer("У Вас нет Чаты")
            btn = await basic()
            await call.message.answer(msg + f"\nТы доктор.", reply_markup=btn)

    elif data == "get_money":
        methods = await get_payment_methods()
        btn = await payment_method_btn(methods)
        await call.message.answer("Choose payment method", reply_markup=btn)

    elif data == "cancel":
        btn = await basic()
        await call.message.answer(msg + f"\nТы доктор.", reply_markup=btn)


async def payment(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    await call.answer()
    msg = f"Добро пожаловать 👋, {call.from_user.full_name}!"
    method = call.data.split(":")[1]
    if method == "cancel":
        btn = await basic()
        await call.message.answer(msg + f"\nТы доктор.", reply_markup=btn)

    if data_methods.get(method, False):
        cancel = await cancel_btn()
        await call.message.answer(data_methods[method], reply_markup=cancel)
        await Payment.text.set()
        await state.update_data({
            "method": method
        })


async def get_payment_account(message: types.Message, state: FSMContext):
    await state.update_data({
        "account": message.text
    })
    cancel = await cancel_btn()
    await message.answer("Введите сумму", reply_markup=cancel)
    await Payment.price.set()


async def get_payment_price(message: types.Message, state: FSMContext):
    await state.update_data({
        "price": message.text
    })
    data = await state.get_data()
    method = data["method"]
    account = data["account"]
    price = data["price"]
    print(method, account, price)
    d = await withdraw_doctor(method, account, price, message.from_user.id)
    print(d)
    await message.answer("✅ Ваш запрос принят, оплата за ваш аккаунт произойдет как можно скорее.")
    msg = f"Добро пожаловать 👋, {message.from_user.full_name}!"
    btn = await basic()
    await message.answer(msg + f"\nТы доктор.", reply_markup=btn)
    await state.finish()


async def cancel_handler(call: types.CallbackQuery, state: FSMContext):
    await call.answer()
    await call.message.delete()
    await state.finish()
    msg = f"Добро пожаловать 👋, {call.from_user.full_name}!"
    btn = await basic()
    await call.message.answer(msg + f"\nТы доктор.", reply_markup=btn)


def register_doctor_handler_py(dp: Dispatcher):
    dp.register_callback_query_handler(doctor_intro, text_contains=["doctor:"])
    dp.register_callback_query_handler(payment, text_contains=["payment:"])
    dp.register_callback_query_handler(cancel_handler, text=["handler:cancel"], state=Payment.text)
    dp.register_callback_query_handler(cancel_handler, text=["handler:cancel"], state=Payment.price)
    dp.register_message_handler(get_payment_account, state=Payment.text)
    dp.register_message_handler(get_payment_price, state=Payment.price)
