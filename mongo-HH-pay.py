from pymongo import MongoClient
from pprint import pprint

client = MongoClient('127.0.0.1', 27017)
db = client['hh-mongo']
vacancy = db.vacancy


data = int(input('Введите сумму зп: '))
print('подбираем вакансии с заработной платой больше введённой суммы...')

for vac in vacancy.find({'$or':
                                 [{'pay.min': {'$gte': data}}, {'pay.max': {'$gte': data}}]
                             }):
    pprint(vac)