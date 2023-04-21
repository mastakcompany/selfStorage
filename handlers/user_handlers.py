from aiogram import Router
from aiogram.filters import Command, CommandStart, Text
from aiogram import filters
from aiogram.filters.callback_data import CallbackData
from aiogram.types import Message, CallbackQuery

from keyboards.user_keyboards import start_keyboard, \
    storage_conditions_keyboard, what_can_be_stored_keyboard, \
    send_to_storage_keyboard, item_weight_keyboard, item_dimensions_keyboard, \
    rental_period_keyboard
from lexicon.lexicon_ru import LEXICON_RU

router: Router = Router()


# Этот хэндлер срабатывает на команду /start
@router.message(CommandStart())
async def process_start_command(message: Message):
    await message.answer(
        text=LEXICON_RU['/start'],
        reply_markup=start_keyboard()
    )


# Этот хэндлер срабатывает на команду /help
@router.message(Command(commands=['help']))
async def process_help_command(message: Message):
    await message.answer(
        text=LEXICON_RU['/help'],
    )


@router.message(Text(contains=['Условия хранения']))
async def process_storage_conditions_cmd(message: Message):
    await message.answer(
        text='Ознакомиться с условиями хранения:',
        reply_markup=storage_conditions_keyboard()
    )


@router.message(Text(contains=['Что можно хранить']))
async def process_storage_conditions_cmd(message: Message):
    await message.answer(
        text='Ознакомиться с правилами хранения:',
        reply_markup=what_can_be_stored_keyboard()
    )


@router.message(Text(contains=['Отправить на хранение']))
async def process_send_to_storage_cmd(message: Message):
    await message.answer(
        text=LEXICON_RU['rules'],
        reply_markup=send_to_storage_keyboard()
    )


@router.callback_query(Text(text=['yourself', 'courier']))
async def process_item_weight_cmd(callback: CallbackQuery):
    await callback.message.edit_text(
        text='Каков примерный вес ваших вещей?',
        reply_markup=item_weight_keyboard()
    )
    await callback.answer()


@router.callback_query(Text(text=['10', '25', '40', '70', '100', 'over']))
async def process_item_dimensions_cmd(callback: CallbackQuery):
    await callback.message.edit_text(
        text=LEXICON_RU['dimension'],
        reply_markup=item_dimensions_keyboard()
    )
    await callback.answer()


@router.callback_query(Text(text=['empty_dimension', 'dimension_3', 'dimension_7', 'dimension_10']))
async def process_rental_period_cmd(callback: CallbackQuery):
    await callback.message.edit_text(
        text='Выберите срок аренды:',
        reply_markup=rental_period_keyboard()
    )


@router.callback_query(Text(text=['one_month', 'tree_month', 'six_month', 'twelve_month', ]))
async def get_phone_number(callback: CallbackQuery):
    await callback.message.edit_text(
        text='Введите ваш номер телефона для связи:',
    )
    await callback.answer()
