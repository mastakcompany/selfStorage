from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def start_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text='Отправить на хранение 🚚'),
                KeyboardButton(text='Мои ячейки 🗄️'),
            ],
            [
                KeyboardButton(text='Что можно хранить на складе ❓'),
                KeyboardButton(text='Условия хранения 📝'),
            ]
        ],
        resize_keyboard=True
    )
