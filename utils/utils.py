from config_data.config import load_config

import requests
from urllib.parse import urlparse


def strip_scheme(link):
    parsed = urlparse(link)
    bit_url = ''.join([parsed.netloc, parsed.path])
    return bit_url


def get_link_clicks(link):
    bit_url = strip_scheme(link)
    token = load_config().bitly_token.b_token
    site = f'https://api-ssl.bitly.com/v4/bitlinks/{bit_url}/clicks/summary'
    header = {'Authorization': f'Bearer {token}'}
    params = {'unit': 'day', 'units': '-1'}
    response = requests.get(site, headers=header, params=params)
    response.raise_for_status()
    counts = response.json()
    return counts['total_clicks']


async def entry_to_database(table, data):
    table.insert(
        user_id=data.get('user_id'),
        weight=data.get('weight'),
        storage_time=data.get('storage_time'),
        phone=data.get('phone'),
        deliver=data.get('deliver'),
        address=data.get('address'),
        dimension=data.get('dimension')
    )
    print('Данные записаны успешно в БД!')
    return

