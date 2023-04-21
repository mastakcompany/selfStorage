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


# Создание нового заказа с заполнением поля user_id
async def create_order(user_id):
    user = cursor.execute(f'SELECT user_id FROM orders WHERE user_id == "{user_id}"')
    if not user:
        cursor.execute(f'INSERT INTO orders(user_id) VALUES({user_id})')
        db.commit()

# Проверка наличия user id в таблице. Возвращает True, если запись есть.
async def is_user_id(user_id):
    return cursor.execute(f'SELECT EXIST(SELECT {user_id} FROM orders)')
