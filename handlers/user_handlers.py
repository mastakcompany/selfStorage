from aiogram import Router
from aiogram.filters import Command, CommandStart, Text
from aiogram.types import Message, CallbackQuery

from keyboards import user_keyboards
from lexicon.lexicon_ru import LEXICON_RU

router = Router()


# Этот хэндлер срабатывает на команду /start
@router.message(CommandStart())
async def process_start_command(message: Message):
    await message.answer(
        text=LEXICON_RU['/start'],
        reply_markup=user_keyboards.start_keyboard()
    )


# Этот хэндлер срабатывает на команду /help
@router.message(Command(commands=['help']))
async def process_help_command(message: Message):
    await message.answer(
        text=LEXICON_RU['/help'],
    )


@router.message(Text(contains=['Условия хранения']))
async def process_storage_conditions(message: Message):
    await message.answer(
        text='Ознакомиться с условиями хранения:',
        reply_markup=user_keyboards.storage_conditions_keyboard()
    )


@router.message(Text(contains=['Что можно хранить']))
async def process_what_can_be_stored(message: Message):
    await message.answer(
        text='Ознакомиться с правилами хранения:',
        reply_markup=user_keyboards.what_can_be_stored_keyboard()
    )


@router.message(Text(contains=['Отправить на хранение']))
async def process_send_to_storage(message: Message):
    await message.answer(
        text=LEXICON_RU['rules'],
        reply_markup=user_keyboards.send_to_storage_keyboard()
    )


@router.callback_query(Text(text=['yourself', 'courier']))
async def get_item_weight(callback: CallbackQuery):
    await callback.message.edit_text(
        text='Каков примерный вес ваших вещей?',
        reply_markup=user_keyboards.item_weight_keyboard()
    )
    await callback.answer()


@router.callback_query(Text(text=['10', '25', '40', '70', '100', 'over']))
async def get_item_dimensions(callback: CallbackQuery):
    await callback.message.edit_text(
        text=LEXICON_RU['dimension'],
        reply_markup=user_keyboards.item_dimensions_keyboard()
    )
    await callback.answer()


@router.callback_query(Text(text=['empty_dimension', 'dimension_3', 'dimension_7', 'dimension_10']))
async def get_rental_period(callback: CallbackQuery):
    await callback.message.edit_text(
        text='Выберите срок аренды:',
        reply_markup=user_keyboards.rental_period_keyboard()
    )


@router.callback_query(Text(text=['one_month', 'tree_month', 'six_month', 'twelve_month', ]))
async def get_phone_number(callback: CallbackQuery):
    await callback.message.edit_text(
        text='Введите ваш номер телефона для связи:',
    )
    await callback.answer()
