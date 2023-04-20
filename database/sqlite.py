import sqlite3 as sq
from dotenv import dotenv_values


async def db_start():
    global db, cursor

    config = dotenv_values('.env')
    database_name = config['DATABASE_NAME']
    db = sq.connect(f'{database_name}')
    cursor = db.cursor()

    cursor.execute('CREATE TABLE IF NOT EXIST orders('
                   '"order_number DECIMAL PRIMARY KEY'
                   'user_id DECIMAL'
                   'phone DECIMAL'
                   'address TEXT'
                   'cell_size TEXT'
                   'weight TEXT'
                   'is_processed TEXT'
                   'cell_number DECIMAL'
                   'storage_time DATETIME'
                   'expiration_time DATETIME")'
                   )
    db.commit()
