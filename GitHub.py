import requests
import json
from pprint import pprint

url = 'https://api.github.com/users/LidiaKaf/repos'

response = requests.get(url)
j_data = response.json()

for i in range(len(j_data)):
    print(j_data[i]['name'])

with open('GitHub.json', 'w', encoding="UTF-8") as f:
    json.dump(j_data, f)
