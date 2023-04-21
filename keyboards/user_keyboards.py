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
                KeyboardButton(text='Что можно хранить ❓'),
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


def what_can_be_stored_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text='Читать 🔍',
                    url='https://telegra.ph/Pravila-hraneniya-04-20'
                )
            ]
        ]
    )


def send_to_storage_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text='Привезете вещи сами?',
                    callback_data='yourself'
                )
            ],
            [
                InlineKeyboardButton(
                    text='Курьером (бесплатно)',
                    callback_data='courier'
                )
            ]
        ]
    )


def item_weight_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(
                text='До 10 кг',
                callback_data='10')],
            [InlineKeyboardButton(
                text='От 10 до 25 кг',
                callback_data='25')],
            [InlineKeyboardButton(
                text='От 25 до 40 кг',
                callback_data='40')],
            [InlineKeyboardButton(
                text='От 40 до 70 кг',
                callback_data='70')],
            [InlineKeyboardButton(
                text='От 70 до 100 кг',
                callback_data='100')],
            [InlineKeyboardButton(
                text='Свыше 100 кг',
                callback_data='over')],
        ]
    )


def item_dimensions_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(
                text='Не хочу! Я плачу бабки, измеряйте сами.',
                callback_data='empty_dimension')],
            [InlineKeyboardButton(
                text='Менее 3 кв.м (1800 руб/мес)',
                callback_data='dimension_3')],
            [InlineKeyboardButton(
                text='От 3 до 7 кв.м (2000 руб/мес)',
                callback_data='dimension_7')],
            [InlineKeyboardButton(
                text='От 7 до 10 кв.м (2200 руб/мес)',
                callback_data='dimension_10')]
        ]
    )


def rental_period_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(
                text='1 месяц',
                callback_data='one_month')],
            [InlineKeyboardButton(
                text='3 месяца',
                callback_data='tree_month')],
            [InlineKeyboardButton(
                text='6 месяцев',
                callback_data='six_month')],
            [InlineKeyboardButton(
                text='12 месяцев',
                callback_data='twelve_month')],

        ]
    )
