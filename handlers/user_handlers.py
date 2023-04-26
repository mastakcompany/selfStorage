from aiogram import Router
from aiogram.filters import Command, CommandStart, Text
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from config_data.config import my_table
from keyboards import user_keyboards
from lexicon.lexicon_ru import LEXICON_RU
from aiogram3_calendar import DialogCalendar, dialog_cal_callback

from database import database_funcs
from utils.utils import entry_to_database, get_qrcode

router = Router()


class MyCellsState(StatesGroup):
    cell_number = State()
    all_things = State()  # True клиент заберет все вещи, если часть - False


class GetUserInfo(StatesGroup):
    new_user = State()
    weight = State()
    dimension = State()
    rental_period = State()
    phone = State()
    deliver = State()
    yourself_delivery = State()
    courier_delivery = State()
    address = State()


'''
Что сохраняем в БД:

'user_id': 'telegram_id',
'weight': масса вещей,
'cell_size': значение габаритов ячейки, если клиент не хочет сам мерять то False,
'storage_time': срок аренды ячейки,
'phone': user_phone,
'yourself': Bool,
'address': user_address, если пустое, то клиент сам привезет свои вещи,
'is_processed': обработан ли заказ (True) или это новый (False),
'cell_number': номера ячеек хранения,
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
async def process_send_to_storage(message: Message, state: FSMContext):
    await message.answer(
        text=LEXICON_RU['rules'],
        reply_markup=user_keyboards.agree_keyboard()
    )
    user_id = int(message.from_user.id)
    await state.update_data(user_id=user_id)
    await state.set_state(GetUserInfo.new_user)


@router.callback_query(Text(text=['agree']), GetUserInfo.new_user)
async def get_item_weight(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        text='Каков примерный вес ваших вещей?',
        reply_markup=user_keyboards.item_weight_keyboard()
    )
    await state.update_data(weight=callback.data)
    await state.set_state(GetUserInfo.weight)
    await callback.answer()


@router.callback_query(Text(startswith=['weight']), GetUserInfo.weight)
async def get_item_dimensions(callback: CallbackQuery, state: FSMContext):
    weight = callback.data.split()[1]
    await state.update_data(weight=weight)

    await callback.message.edit_text(
        text=LEXICON_RU['dimension'],
        reply_markup=user_keyboards.item_dimensions_keyboard()
    )
    await state.set_state(GetUserInfo.dimension)
    await callback.answer()


@router.callback_query(Text(startswith=['dimension']), GetUserInfo.dimension)
async def get_rental_period(callback: CallbackQuery, state: FSMContext):
    dimension = callback.data.split()[1]
    await state.update_data(dimension=dimension)

    await callback.message.edit_text(
        text='Выберите срок аренды:',
        reply_markup=user_keyboards.rental_period_keyboard()
    )
    await state.set_state(GetUserInfo.rental_period)
    await callback.answer()


@router.callback_query(Text(endswith=['month']), GetUserInfo.rental_period)
async def get_phone_number(callback: CallbackQuery, state: FSMContext):
    storage_time = callback.data.split()[0]
    await state.update_data(storage_time=storage_time)

    await callback.message.edit_text(
        text='Введите ваш номер телефона для связи:'
    )
    await state.set_state(GetUserInfo.phone)
    await callback.answer()


@router.message(GetUserInfo.phone)
async def process_phone(message: Message, state: FSMContext):
    phone = message.text
    await state.update_data(phone=phone)

    await message.answer(
        text='Выберите метод доставки',
        reply_markup=user_keyboards.send_to_storage_keyboard())

    await state.set_state(GetUserInfo.deliver)


@router.callback_query(Text(text=['yourself', 'courier']), GetUserInfo.deliver)
async def check_deliver_method(callback: CallbackQuery, state: FSMContext):
    if callback.data == 'yourself':
        await state.update_data(deliver='yourself')
        await callback.message.edit_text(
            text='Адрес склада: Улица - Пыльная, дом - Не видно.\n'
                 'Укажите дату, когда приедете:',
            reply_markup=await DialogCalendar.start_calendar()
        )
        await state.set_state(GetUserInfo.yourself_delivery)
    elif callback.data == 'courier':
        await state.update_data(deliver='courier')
        await callback.message.edit_text(
            text='Введите адрес, откуда забрать вещи:'
        )
        await state.set_state(GetUserInfo.courier_delivery)
    await callback.answer()


@router.message(GetUserInfo.courier_delivery)
async def process_address(message: Message, state: FSMContext):
    await state.update_data(address=message.text)
    await message.answer(
        text='Наш менеджер свяжется с вами в ближайшее время для уточнения '
             'деталей оплаты  и времени доставки '
    )
    user_data = await state.get_data()
    await entry_to_database(my_table, user_data)
    await state.clear()


@router.callback_query(dialog_cal_callback.filter())
async def process_confirm(callback: CallbackQuery, callback_data: dict,
                          state: FSMContext):
    selected, date = await DialogCalendar().process_selection(callback,
                                                              callback_data)
    if selected:
        message = date.strftime("%d/%m/%Y")
        await callback.message.edit_text(
            text=f'Место для ваших вещей забронировано на складе. '
                 f'Ждем вас {message}'
        )
        await state.update_data(date=message)
        user_data = await state.get_data()
        await entry_to_database(my_table, user_data)
        await state.clear()


# Ветвь "Мои ячейки"
@router.message(Text(contains=['Мои ячейки']))
async def output_my_cells_menu(message: Message):
    user_id = message.from_user.id
    is_user = database_funcs.check_user(user_id)
    if is_user:
        if not database_funcs.get_user_cells(user_id):
            await message.answer(
                text=f'Ваш заказ в обработке.'
            )
        else:
            cell_number = database_funcs.get_user_cells(user_id)
            await message.answer(
                text=f'{cell_number}',
                reply_markup=user_keyboards.output_my_cells_keyboard()
            )
    else:
        await message.answer(
            text=f'У вас нет вещей на хранении.'
        )


@router.callback_query(Text(text=['extend_storage']))
async def get_cell_number(callback: CallbackQuery):
    user_id = callback.from_user.id
    user_cells = database_funcs.get_user_cells(user_id)
    await callback.message.edit_text(
        text='Выберите ячейку, для которой хотите продлить срок хранения:',
        reply_markup=user_keyboards.generate_my_cells_keyboard(user_cells)
    )


@router.callback_query(Text(startswith=['cell_']))
async def extend_rental_period_cmd(callback: CallbackQuery, state: FSMContext):
    await state.update_data(cell_number=callback.data.split(sep="_")[-1])
    # отправить номер ячейки и время продления в админку, раздел "Запросы на продление"
    await callback.message.edit_text(
        text='Выберите срок продления аренды:',
        reply_markup=user_keyboards.extend_rental_period_keyboard()
    )


@router.callback_query(Text(startswith=['extend_']))
async def send_success_extend_message(callback: CallbackQuery):
    await callback.message.edit_text(
        text='Ваш запрос на продление срока аренды принят. \n'
             'Менеджер свяжется с вами в ближайшее время для '
             'уточнения деталей.'
    )


@router.callback_query(Text(text=['pick_up_some_things', 'pick_up_all_things']))
async def output_pick_up_things_buttons(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        text='Заберете вещи сами?',
        reply_markup=user_keyboards.generate_pick_up_things_keyboard()
    )

    if callback.data == 'pick_up_some_things':
        await state.update_data(all_things=False)  # клиент заберет часть вещей
    else:
        await state.update_data(all_things=True)  # клиент заберет все вещи


@router.callback_query(Text(text=['pick_up_myself', 'deliver_home']))
async def output_pick_up_cells_buttons(callback: CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    user_cells = database_funcs.get_user_cells(user_id)
    await callback.message.edit_text(
        text='Выберите ячейку, из которой хотите забрать вещи:',
        reply_markup=user_keyboards.generate_pick_up_cells_keyboard(user_cells)
    )
    if callback.data == 'deliver_home':
        await state.update_data(deliver=True)  # доставить вещи клиенту на дом
    else:
        await state.update_data(deliver=False)  # клиент заберет вещи сам


@router.callback_query(Text(startswith=['pick_up_cell_']))
async def output_pick_up_cells_buttons(callback: CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    data = await state.get_data()
    deliver = data.get('deliver')
    all_things = data.get('all_things')
    cell_number = data.get('cell_number')
    if deliver:
        await callback.message.edit_text(
            text='Менеджер свяжется с вами в ближайшее время для '
            'уточнения деталей доставки ваших вещей.'
        )
    else:
        qr_data = f'user_id={user_id}, cell_number={cell_number}'
        photo = get_qrcode(qr_data)
        if all_things:
            await callback.message.answer_photo(photo, caption='Предьявите QR-код на складе, для получения вещей')
        else:
            await callback.message.answer_photo(photo, caption='Предьявите QR-код на складе, для получения вещей')
    await state.clear()
