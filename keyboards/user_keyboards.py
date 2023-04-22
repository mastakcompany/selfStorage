from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)


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
    weights = [('До 10 кг', '10'), ('От 10 до 25 кг', '25'), ('От 25 до 40 кг', '40'),
               ('От 40 до 70 кг', '70'), ('От 70 до 100 кг', '100'), ('Свыше 100 кг', 'over')]
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=text, callback_data=data)] for text, data in weights
        ],
    )


def item_dimensions_keyboard():
    dimensions = [('Не хочу! Я плачу бабки, измеряйте сами.', 'empty_dimension'),
                  ('Менее 3 кв.м (1800 руб/мес)', 'dimension_3'),
                  ('От 3 до 7 кв.м (2000 руб/мес)', 'dimension_7'),
                  ('От 7 до 10 кв.м (2200 руб/мес)', 'dimension_10')]
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=text, callback_data=data)] for text, data in dimensions
        ],
    )


def rental_period_keyboard():
    periods = [('1 месяц', 'one_month'), ('3 месяца', 'tree_month'),
               ('6 месяцев', 'six_month'), ('12 месяцев', 'twelve_month')]
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=text, callback_data=data)] for text, data in periods
        ],
    )
