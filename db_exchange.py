"""
Модуль определяет функции для работы с базой данных
для чтения словарей вакансий b регионов и городов,
для перезаписи найденных вакансий
"""

from db_obj_declaration import *
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

def vac_to_db(vac_lst, db_file_name, search_reg_id):
    """
     Функция записывает вакансии из принимаемого списка
     в базу данных
    :param vac_lst: список словарей-вакансий
    :param db_file_name: имя файла базы данных (строковый)
    :param search_reg_id: номер региона, в котором проводился поиск
    :return: None
    """

    return None


def regs_form_db(db_name):
    """
    читает данные из файла 'regions.json'
    возвращает словарь регионов РФ: {имя_региона: код_региона}
    :param db_name: имя файла базы данных
    """
    engine = create_engine(f'sqlite:///{db_name}', echo=False)

    # Создание сессии
    # create a configured "Session" class
    Session = sessionmaker(bind=engine)
    session = Session()

    # Полный словарь регионов
    reg_tuple = session.query(Region.name, Region.id_hh).all()
    reg_dict = {}
    for reg in reg_tuple:
        reg_dict[reg[0]] = reg[1]

    return reg_dict


def vac_to_db(db_name, vacancy_dict_lst, search_reg_id):
    """
    функция заново записывает данные
    о найденных вакансиях в таблицу Vacancy

    :param db_name: имя файла базы данных
    :param vacancy_dict_lst: список словарей вакансий
                словари - в формате hh.ru
    :param search_reg_id: целое число - код макрорегиона,
        по которому проведен поиск и получен в результате этот список
    :return:None
    """
    engine = create_engine(f'sqlite:///{db_name}', echo=False)

    # [пере]_cоздание таблиц
    Base.metadata.create_all(engine)

    # Создание сессии
    # create a configured "Session" class
    Session = sessionmaker(bind=engine)
    session = Session()

    # заполняем таблицу вакансий

    vac_lst = []
    # на случай, если нет данных о заработной плате
    for v in vacancy_dict_lst:
        s_from = None
        s_to = None
        s_cur = None
        if v['salary']:
            if v['salary']['from']:
                s_from = int(v['salary']['from'])
            if v['salary']['to']:
                s_to = int(v['salary']['to'])
            if v['salary']['currency']:
                s_cur = v['salary']['currency']

        # формируем строки для записи в базу вакансий
        vacancy = Vacancy(v['id'], v['name'], search_reg_id,
                          v['area']['id'], s_from, s_to,
                          s_cur, v['snippet']['requirement'],
                          v['snippet']['responsibility'], v['alternate_url'])
        vac_lst.append(vacancy)

    session.add_all(vac_lst)

    session.commit()

    return None

