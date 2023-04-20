import sqlite3 as sq
from dotenv import dotenv_values

# Создание новой БД с таблицей orders
async def db_start():
    global db, cursor

    config = dotenv_values('.env')
    database_name = config['DATABASE_NAME']
    db = sq.connect(f'{database_name}')
    cursor = db.cursor()

    db.commit()


# Проверка наличия user id в таблице. Возвращает True, если запись есть.
async def is_user_id(user_id):
    return cursor.execute(f'SELECT EXIST(SELECT {user_id} FROM orders)')
