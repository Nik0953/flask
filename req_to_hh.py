import requests
import json


def get_vacancies(requirements):
    """
    функция получает вакансии с сайта hh.ru
    и возвращает их в виде
    :param requirements - словарь:
        {
        'key_words': = ключевые слова для поиска, string;
        'where_to_find': = регион, string;
        'n_days': = сколько дней назад актуальны вакансии, string;
        }
    :return: возвращает список вакансий
    """

    DOMAIN = 'https://api.hh.ru/vacancies/'
    vacancy_filter = {'text': requirements['key_words'],
                      'area': requirements['where_to_find'],   # Москва
                      # 'only_with_salary': 'true',
                      'period': requirements['n_days'],
                      'page': '0'
                      }

    # запрос к hh.ru
    result = requests.get(DOMAIN, params=vacancy_filter)

    # Успешно - 2XX
    print('Код ответа от сервера: ', result.status_code)

    data = result.json()

    # общее количество страниц выдачи
    vac_pages = int(data['pages'])

    # здесь будет полный список вакансий
    vacancy_list = []

    page_current = 0

    # читаем постранично доступные вакансии
    while page_current < vac_pages:
        print('Вакансии, страница', page_current)
        vacancy_filter['page'] = str(page_current)
        result = requests.get(DOMAIN, params=vacancy_filter)
        data = result.json()
        # дописываем список вакансий с последней страницы к полному списку
        vacancy_list += data['items']
        page_current += 1

    return vacancy_list
