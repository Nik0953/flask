"""
Модуль создает новую пустую базу данных,
создает таблицы регионов и городов
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

from db_obj_declaration import *
from activate_regions import *

db_name = 'data/vac_hh.db'

# в начале работы программы удаляем старый файл базы данных
if os.path.exists(db_name) and os.path.isfile(db_name):
    try:
        os.remove(db_name)
    except OSError as e:
        print('Ошибка', e.strerror)


engine = create_engine(f'sqlite:///{db_name}', echo=False)

# [пере]_cоздание таблиц
Base.metadata.create_all(engine)

# Создание сессии
# create a configured "Session" class
Session = sessionmaker(bind=engine)
session = Session()


# заполняем таблицу регионов
reg_dict = get_regions_dict('data/regions.json')

reg_lst = []

for rd in reg_dict:
    region = Region(reg_dict[rd], rd)
    reg_lst.append(region)

session.add_all(reg_lst)

# заполняем таблицу городов
town_dict = get_towns_dict('data/regions.json')

town_lst = []

for t in town_dict:
    town = Town(town_dict[t], t)
    town_lst.append(town)

session.add_all(town_lst)


session.commit()




