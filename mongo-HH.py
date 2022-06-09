from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError as dke
from bs4 import BeautifulSoup as bs
import requests
from pprint import pprint

client = MongoClient('127.0.0.1', 27017)
db = client['hh-mongo']


main_url = 'https://hh.ru'
text = input('hh: ')
params = {'text': text,
          'from': 'suggest_post',
          'employment': 'full',
          'clusters': 'true',
          'area': '2020',
          'ored_clusters': 'true',
          'label': 'not_from_agency',
          'search_field': 'name',
          'search_field': 'description',
          'enable_snippets': 'true',
          'items_on_page': 20,
          'page': 0}
headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.0.0 Safari/537.36'}
all_vacancies = []
id = 0
response = requests.get(main_url+'/search/vacancy', params=params, headers=headers)
soup = bs(response.text, 'html.parser')
quantity = soup.find('h1').getText().split()
if quantity[1].isdigit():
    quantity = quantity[0] + quantity[1]
else:
    quantity = quantity[0]

if int(quantity) <= 20:
    pages = 1
else:
    pages = soup.find_all('a', {'class': 'bloko-button'})[-2].getText()
    pages = int(pages)

while params['page'] != pages:
    response = requests.get(main_url+'/search/vacancy', params=params, headers=headers)
    soup = bs(response.text, 'html.parser')
    vacancies = soup.find_all('div', {'class': 'vacancy-serp-item'})
    for vacancy in vacancies:
        vacancy_info = {}
     #   id = id + 1

        vacancy_ancor = vacancy.find_all('span')
        vacancy_name = vacancy_ancor[1].getText()
        vacancy_info['name'] = vacancy_name
        vacancy_href = vacancy_ancor[1].find('a')['href']
        vacancy_info['href'] = vacancy_href
        vacancy_info['_id'] = vacancy_info['href'][22:30]
        vacancy_pay = vacancy.find('span', {'class': 'bloko-header-section-3'})
        try:
            vacancy_pay = vacancy_pay.getText().split()
            if len(vacancy_pay) == 6:
                vacancy_info['pay'] = {'min': int(vacancy_pay[0])*1000, 'max': int(vacancy_pay[3])*1000, 'currency': vacancy_pay[5]}
            if len(vacancy_pay) == 4:
                if vacancy_pay[0] == 'от':
                    vacancy_info['pay'] = {'min': int(vacancy_pay[1])*1000, 'max': None, 'currency': vacancy_pay[3]}
                if vacancy_pay[0] == 'до':
                    vacancy_info['pay'] = {'min': None, 'max': int(vacancy_pay[1])*1000, 'currency': vacancy_pay[3]}
        except:
            vacancy_info['pay'] = {'min': None, 'max': None, 'currency': None}
        try:
            db.vacancy.insert_one(vacancy_info)
        except dke:
            print(f'Вакансия с id = {vacancy_info["_id"]} уже существует в базе')

    params['page'] = params['page'] + 1

