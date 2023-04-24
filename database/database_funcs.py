from bot import my_table, links_table

from sqlite3_api.Table import Table
from sqlite3_api.field_types import List


def filling_users_table_test_data():
    my_table.insert(
        user_id=100,
        phone='4455',
        address='nowhere',
        dimension='3-7',
        weight='40-70',
        cell_number='12,13',
        storage_time='6',
        expiration_time='10.10.2020',
        is_processed='True'
    )


def filling_links_table_test_data():
    links_table.insert(
        name='Рекламное объявление 2',
        link='https://bit.ly/43XkAWZ'
    )


def get_new_orders():
    new_orders = []
    for obj in my_table.filter(is_processed='False'):
        new_orders.append(obj.id)
    return new_orders


def get_new_order_details(order_id):
    order_details = {}
    obj = my_table.filter(id=order_id, address_no='')
    order_details['phone'] = obj.phone
    order_details['address'] = obj.address
    return order_details


def assign_cell_number(order_id, cell_number):
    obj = my_table.filter(id=order_id)
    obj.cell_number.append(int(cell_number))
    obj.save()


def get_current_links():
    current_links = []
    for obj in links_table.filter():
        current_links.append(obj.name)
    return current_links


def get_link(link_name):
    obj = links_table.filter(name=link_name)
    return obj.link


def print_table():
    for obj in my_table.filter():
        print(obj, '\n')
    print('-' * 50)
