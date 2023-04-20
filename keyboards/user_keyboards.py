from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton
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
                KeyboardButton(text='Условия хранения 📝', ),
            ]
        ],
        resize_keyboard=True
    )


def storage_conditions_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text='Читать 🔍',
                    url='https://telegra.ph/Usloviya-hraneniya-04-20'
                )
            ]
        ]
    )
