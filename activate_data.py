"""
читает данные из файлов
    для загрузки в списки формы запроса
"""

import json

def get_cities_dict(file_name):
    """
    читает файл с кодами регионов
    и подгружает их в словарь
    """
    cities_lst = []
    cities_dict = {}
    with open(file_name, 'r') as f:
        cities_lst = json.load(f)

    for town in cities_lst[0]['areas']:
        town_name = str(town['name'])
        cities_dict[town_name] = str(town['id'])

    return cities_dict


