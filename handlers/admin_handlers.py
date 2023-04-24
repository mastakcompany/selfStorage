from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command, Text
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, CallbackQuery

from lexicon.lexicon_ru import LEXICON_RU
from keyboards import admin_keyboards
from database import database_funcs
from config_data.config import load_config
from utils import utils

from sqlite3_api.Table import Table

router = Router()


class GetCellNumber(StatesGroup):
    cell_number = State()
    order_id = State()


@router.message(Command(commands=['admin']))
async def process_admin_command(message: Message):
    # database_funcs.filling_users_table_test_data()  # Заполнение таблицы Users тестовыми данными
    # database_funcs.filling_links_table_test_data()  # Заполнение таблицы links_table тестовыми данными
    # database_funcs.print_table()
    ids = load_config().admin_ids.ids_list
    if str(message.from_user.id) in ids:
        await message.answer(
            text=LEXICON_RU['/admin'],
            reply_markup=admin_keyboards.start_admin_keyboard()
        )
    else:
        await message.answer(text='У вас не достаточно прав')


@router.message(Text(contains=['Новые заказы']))
async def show_new_orders(message: Message):
    new_orders = database_funcs.get_new_orders()
    await message.answer(
        text=f'{len(new_orders)} новых заказов.\nНажмите на кнопку, чтобы посмотреть детали:',
        reply_markup=admin_keyboards.new_orders_keyboard(new_orders)
    )


@router.callback_query(Text(startswith=['new_order_button_']))
async def show_new_order_details(callback: CallbackQuery):
    order_id = int(callback.data.split(sep="_")[-1])
    order_details = database_funcs.get_new_order_details(order_id)
    await callback.message.edit_text(
        text=f'Заказ № {order_id}\nТелефон: {order_details["phone"]}\nАдрес: {order_details["address"]}',
        reply_markup=admin_keyboards.assign_cell_number(order_id)
    )


@router.callback_query(Text(startswith=['assign_cell_number_']))
async def assign_cell_number(callback: CallbackQuery, state: FSMContext):
    order_id = int(callback.data.split(sep="_")[-1])
    await state.update_data(order_id=order_id)
    await state.set_state(GetCellNumber.cell_number)
    await callback.message.edit_text(
        text='Введите номер ячейки:'
    )
    await callback.answer()


@router.message(GetCellNumber.cell_number)
async def process_assign_cell_number(message: Message, state: FSMContext):
    await state.update_data(cell_number=message.text)
    data = await state.get_data()
    order_id = int(data['order_id'])
    database_funcs.assign_cell_number(order_id, message.text)
    await message.answer(
        text=f'Заказу №{order_id} присвоена ячейка {message.text}'
    )
    await state.clear()


@router.message(Text(contains=['Статистика заказов']))
async def show_links(message: Message):
    current_links = database_funcs.get_current_links()
    if current_links:
        await message.answer(
            text='Выберите интересующую вас ссылку, чтобы посмотреть статистику',
            reply_markup=admin_keyboards.show_current_links(current_links)
        )
    else:
        await message.answer(text='Нет ссылок для сбора статистики.')


@router.callback_query(Text(startswith=['current_link_']))
async def show_link_details(callback: CallbackQuery):
    link_name = callback.data.split(sep="_")[2]
    link = database_funcs.get_link(link_name)
    count_clicks = utils.get_link_clicks(link)
    await callback.message.edit_text(
        text=f'Количество кликов по ссылке {count_clicks} раз.'
    )


@router.message(Text(contains=['Просроченные заказы']))
async def show_new_orders(message: Message):
    await message.answer(
        text='Overdue orders'
    )
