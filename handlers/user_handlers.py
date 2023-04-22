from aiogram import Router
from aiogram.filters import Command, CommandStart, Text
from aiogram.types import Message, CallbackQuery

from config_data.config import my_table
from database.utils import database_entry_user_id, database_entry_by_user
from keyboards import user_keyboards
from lexicon.lexicon_ru import LEXICON_RU

router = Router()

users_features = {}
'''Переменная для хранения данных пользователя для последующей их записи в БД.
После отправки данных в БД удалить все записи для текущего user_id.
Словарь может иметь следующие значения:
users_features = {
    'user_id': {
        'phone': user_phone,
        'yourself': Bool,
        'address': user_address, если пустое, то клиент сам привезет свои вещи,
        'cell_size': значение габаритов ячейки, если клиент не хочет сам мерять, то False,
        'weight': масса вещей,
        'is_processed': обработан ли заказ (True) или это новый (False),
        'cell_number': номера ячеек хранения,
        'storage_time': срок аренды ячейки
    }
}
'''


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
    telegram_id = int(message.from_user.id)


@router.callback_query(Text(text=['yourself', 'courier']))
async def get_item_weight(callback: CallbackQuery):
    await callback.message.edit_text(
        text='Каков примерный вес ваших вещей?',
        reply_markup=user_keyboards.item_weight_keyboard()
    )
    await callback.answer()
    telegram_id = callback.message.from_user.id
    print(callback.data)


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


# Ветвь "Мои ячейки"
@router.message(Text(contains=['Мои ячейки']))
async def output_my_cells_menu(message: Message):
    user_id = message.from_user.id
    users_features[user_id] = {}
    cell_number = [101, 102]  # здесь будет результат запроса в БД со списком ячеек для данного пользователя
    users_features[user_id]['cell_number'] = cell_number
    await message.answer(
        text=f'{cell_number}',
        reply_markup=user_keyboards.output_my_cells_keyboard()
    )


@router.callback_query(Text(text=['extend_storage']))
async def get_cell_number(callback: CallbackQuery):
    user_id = callback.from_user.id
    user_cells = users_features[user_id]['cell_number']
    await callback.message.edit_text(
        text='Выберите ячейку, для которой хотите продлить срок хранения:',
        reply_markup=user_keyboards.generate_my_cells_keyboard(user_cells)
    )


@router.callback_query(Text(startswith=['cell_']))
async def extend_rental_period_cmd(callback: CallbackQuery):
    await callback.message.edit_text(
        text='Выберите срок продления аренды:',
        reply_markup=user_keyboards.extend_rental_period_keyboard()
    )


@router.callback_query(Text(startswith=['extend_']))
async def send_success_extend_message(callback: CallbackQuery):
    await callback.message.edit_text(
        text='''Ваш запрос на продление срока аренды принят.
    Менеджер свяжется с вами в ближайшее время для уточнения деталей.'''
    )


@router.callback_query(Text(text=['pick_up_some_things', 'pick_up_all_things']))
async def output_pick_up_things_buttons(callback: CallbackQuery):
    user_id = callback.from_user.id
    if user_id in users_features:
        await callback.message.edit_text(
            text='Заберете вещи сами?',
            reply_markup=user_keyboards.generate_pick_up_things_keyboard()
        )
        if callback.data == 'pick_up_some_things':
            users_features[user_id]['all_things'] = False  # клиент заберет часть вещей
        else:
            users_features[user_id]['all_things'] = True  # клиент заберет все вещи


@router.callback_query(Text(text=['pick_up_myself', 'deliver_home']))
async def output_pick_up_cells_buttons(callback: CallbackQuery):
    user_id = callback.from_user.id
    if user_id in users_features:
        user_cells = users_features[user_id]['cell_number']
        await callback.message.edit_text(
            text='Выберите ячейку, из которой хотите забрать вещи:',
            reply_markup=user_keyboards.generate_pick_up_cells_keyboard(user_cells)
        )
        if callback.data == 'deliver_home':
            users_features[user_id]['deliver'] = True  # доставить вещи клиенту на дом
        else:
            users_features[user_id]['deliver'] = False  # клиент заберет вещи сам


@router.callback_query(Text(startswith=['pick_up_cell_']))
async def output_pick_up_cells_buttons(callback: CallbackQuery):
    user_id = callback.from_user.id
    if user_id in users_features:
        if users_features[user_id]['deliver']:
            await callback.message.edit_text(
                text='Менеджер свяжется с вами в ближайшее время для уточнения деталей доставки ваших вещей.'
            )
        else:
            if users_features[user_id]['all_things']:
                await callback.message.edit_text(
                    text='''Прислать клиенту QR-код с номером (номерами) ячейки и адресом склада.
            QR-код можно генерировать с помощью API bitly'''
                )
            else:
                await callback.message.edit_text(
                    text='''Прислать клиенту QR-код с номером (номерами) ячейки и адресом склада.
            QR-код можно генерировать с помощью API bitly + оповещение, что вещи можно будет вернуть'''
                )
    del users_features[user_id]
