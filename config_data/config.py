from dataclasses import dataclass
from environs import Env
from sqlite3_api.Table import Table


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


class Users(Table):
    user_id: int
    yourself: bool
    weight: str


my_table = Users(db_path='./database.db')
my_table.create_table()
