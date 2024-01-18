from aiogram.dispatcher.filters.state import State, StatesGroup


class Ads(StatesGroup):
    text = State()


class Message(StatesGroup):
    text = State()


class Admin(StatesGroup):
    text = State()


class Payment(StatesGroup):
    text = State()
    price = State()
