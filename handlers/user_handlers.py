from aiogram import Router
from aiogram.filters import Command, CommandStart, Text
from aiogram import filters
from aiogram.types import Message

from keyboards.user_keyboards import start_keyboard, \
    storage_conditions_keyboard
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
