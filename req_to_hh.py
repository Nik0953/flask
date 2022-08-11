import requests
import json


def get_vacancies(requirements, output_file_name):
    """
    функция получает вакансии с сайта hh.ru
    и возвращает их в виде
    :param requirements - словарь:
        {
        'key_words': = ключевые слова для поиска, string;
        'were_to_find': = регион, string;
        'n_days': = сколько дней назад актуальны вакансии, string;
        }
    :param output_file_name: имя файла вывода
    :return: возвращает список вакансий
    """

    DOMAIN = 'https://api.hh.ru/vacancies/'
    vacancy_filter = {'text': requirements['key_words'],
                      'area': requirements['were_to_find'],   # Москва
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

    # вакансий на страницу в выдаче
    #vac_per_page = int(data['per_page'])

    # общее количество вакансий (возможно, недоступное)
    #vac_found = int(data['found'])

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

    # print('\n\n всего собрано вакансий: ', len(vacancy_list))

    # Сохранение в файл
    with open(output_file_name, 'w') as f:
        json.dump(vacancy_list, f, ensure_ascii=False)

    return vacancy_list



if __name__ == "__main__":
    requirements = {'key_words': "слесарь инструментальщик",
                    'were_to_find': "1",
                    'n_days': '2'
                   }

    output_file_name = 'data/vac_lst.json'

    vac_lst = get_vacancies(requirements, output_file_name)

    print(vac_lst[0])
