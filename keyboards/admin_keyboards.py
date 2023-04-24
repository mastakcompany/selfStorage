from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)


def start_admin_keyboard():
    buttons_data = [
        ('Новые заказы', 'Статистика заказов'),
        ('Просроченные заказы',)
    ]

    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=text) for text in row] for row in buttons_data
        ],
        resize_keyboard=True
    )


def new_orders_keyboard(new_orders):
    buttons = []
    for order in new_orders:
        buttons.append((f'Заказ №{order}', f'new_order_button_{order}'))

    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=text, callback_data=data)] for text, data in buttons
        ]
    )


def assign_cell_number(order_id):
    button = [('Назначить номер ячейки', f'assign_cell_number_{order_id}')]
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=text, callback_data=data)] for text, data in button
        ]
    )


def show_current_links(current_links):
    buttons = []
    for link in current_links:
        buttons.append((f'{link}', f'current_link_{link}'))

    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=text, callback_data=data)] for text, data in buttons
        ]
    )
