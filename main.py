from flask import Flask, render_template, request
from activate_data import get_cities_dict
from req_to_hh import get_vacancies

app = Flask(__name__)


#    *****  Главная страница    *****
@app.route("/")
def index():
    pass
    return render_template('index.html')


#    *****  Страница запросовс

@app.route('/req/', methods=['GET', 'POST'])
def run():
    # это будет список словарей-вакансий
    vac_lst = []

    # чтение словаря регионов с кодами региона
    input_file_name = 'data/regions.json'
    regions_dict = get_cities_dict(input_file_name)

    if request.method == 'POST':
        # Получть данные формы
        req_form = {}
        req_form['key_words'] = request.form['query_str']
        req_form['were_to_find'] = request.form['where_to_find']
        req_form['n_days'] = request.form['n_days']

        # запрос к hh.ru и сохранение вакансий
        output_file_name = 'data/vac_lst.json'
        vac_lst = get_vacancies(req_form, output_file_name)
        # информация для публикации в html
        vac_number = len(vac_lst)     # общее количество вакансий
        # находим имя региона по номеру
        vac_region = [reg for reg in regions_dict if regions_dict[reg] == req_form['were_to_find']][0]
        #print(vac_region)

        return render_template('results.html', vac_lst=vac_lst, req=req_form, vac_number=vac_number, vac_region=vac_region)

    elif request.method == 'GET':
        # выводим  html с формой запроса
        return render_template('req.html', regions_dict=regions_dict)





@app.route("/results/")
def results():
    pass
    return render_template('results.html')

@app.route("/contacts/")
def contacts():
    pass
    return render_template('contacts.html')

if __name__ == "__main__":
    app.run(debug=True)