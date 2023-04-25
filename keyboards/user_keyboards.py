from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)


def start_keyboard():
    buttons_data = [
        ('Отправить на хранение 🚚', 'Мои ячейки 🗄️'),
        ('Что можно хранить ❓', 'Условия хранения 📝')
    ]

    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=text) for text in row] for row in buttons_data
        ],
        resize_keyboard=True
    )


def storage_conditions_keyboard():
    buttons_data = [
        ('Читать 🔍', 'https://telegra.ph/Usloviya-hraneniya-04-20')
    ]

    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=text, url=url)] for text, url in buttons_data
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
    buttons_data = [
        ('Привезете вещи сами?', 'yourself'),
        ('Курьером (бесплатно)', 'courier')
    ]

    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=text, callback_data=data)] for text, data in buttons_data
        ]
    )


def item_weight_keyboard():
    weights = [('До 10 кг', 'weight under10'), ('От 10 до 25 кг', 'weight 10-25'), ('От 25 до 40 кг', 'weight 25-40'),
               ('От 40 до 70 кг', 'weight 40-70'), ('От 70 до 100 кг', 'weight 70-100'), ('Свыше 100 кг', 'weight over100')]
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=text, callback_data=data)] for text, data in weights
        ],
    )


def item_dimensions_keyboard():
    dimensions = [('Не хочу! Я плачу бабки, измеряйте сами.', 'dimension empty'),
                  ('Менее 3 кв.м (1800 руб/мес)', 'dimension under3'),
                  ('От 3 до 7 кв.м (2000 руб/мес)', 'dimension 3-7'),
                  ('От 7 до 10 кв.м (2200 руб/мес)', 'dimension 7-10')]
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=text, callback_data=data)] for text, data in dimensions
        ],
    )


def rental_period_keyboard():
    periods = [('1 месяц', '1 month'), ('3 месяца', '3 month'),
               ('6 месяцев', '6 month'), ('12 месяцев', '12 month')]
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=text, callback_data=data)] for text, data in periods
        ],
    )


def output_my_cells_keyboard():
    buttons_data = [
        ('Продлить хранение', 'extend_storage'),
        ('Забрать часть вещей', 'pick_up_some_things'),
        ('Забрать вещи', 'pick_up_all_things')
    ]

    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=text, callback_data=data)] for text, data in buttons_data
        ]
    )


def generate_my_cells_keyboard(user_cells):
    inline_keyboard = []
    for cell in user_cells:
        cell_button = [
                InlineKeyboardButton(
                    text=f'{cell}',
                    callback_data=f'cell_{cell}'
                )
        ]
        inline_keyboard.append(cell_button)
    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)


def extend_rental_period_keyboard():
    periods = [
        ('1 месяц', 'extend_one_month'),
        ('3 месяца', 'extend_tree_month'),
        ('6 месяцев', 'extend_six_month'),
        ('12 месяцев', 'extend_twelve_month')
    ]

    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=text, callback_data=data)] for text, data in periods
        ]
    )


def generate_pick_up_things_keyboard():
    buttons_data = [
        ('Заберу сам(а)', 'pick_up_myself'),
        ('Доставить на дом', 'deliver_home')
    ]

    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=text, callback_data=data)] for text, data in buttons_data
        ]
    )


def generate_pick_up_cells_keyboard(user_cells):
    buttons = []
    for cell in user_cells:
        buttons.append((f'{cell}', f'pick_up_cell_{cell}'))

    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=text, callback_data=data)] for text, data in buttons
        ]
    )


def agree_keyboard():
    buttons_data = [
        ('Согласен с правилами', 'agree')
    ]

    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=text, callback_data=data)] for text, data in buttons_data
        ]
    )
