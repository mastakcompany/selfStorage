from dataclasses import dataclass
from environs import Env
from sqlite3_api.Table import Table
from pathlib import Path


@dataclass
class DatabaseConfig:
    database: str  # Название базы данных
#     db_host: str          # URL-адрес базы данных
#     db_user: str          # Username пользователя базы данных
#     db_password: str      # Пароль к базе данных


@dataclass
class TgBot:
    token: str  # Токен для доступа к телеграм-боту
    # admin_ids: list  # Список id администраторов бота


@dataclass
class Config:
    tg_bot: TgBot
    db: DatabaseConfig


def load_config() -> Config:
    env: Env = Env()
    env.read_env()

    return Config(
        tg_bot=TgBot(token=env('BOT_TOKEN')),
        db=DatabaseConfig(database=env('DATABASE_NAME'))
    )


# Заполнение таблицы полями. Поле id (создается автоматически, поэтому
# здесь не указано), является PRIMARY KEY. Будем считать, что это номер заказа
class Users(Table):
    user_id: int  # Телеграм id клиента.
    phone: str
    address: str  # Адрес клиента. Если пустое, то клиент
    # привезет свои вещи сам.
    cell_size: str  # Значение габаритов ячейки. Если пустое,
    # то клиент не хочет сам мерять.
    weight: str  # Масса вещей.
    cell_number: list  # Список с номерами ячеек хранения для данного клиента.
    storage_time: str  # Время хранения.
    expiration_time: str  # Время истечения срока хранения.


my_table = Users(db_path=Path(Path.cwd().parent, 'database',
                              load_config().db.database))
