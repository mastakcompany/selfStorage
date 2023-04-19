from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def start_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text='Button #1'),
                KeyboardButton(text='Button #2'),
                KeyboardButton(text='Button #3'),
            ],
            [
                KeyboardButton(text='Button #4'),
                KeyboardButton(text='Button #5'),
            ],
            [
                KeyboardButton(text='Button #6'),
            ]
        ],
        resize_keyboard=True
    )
