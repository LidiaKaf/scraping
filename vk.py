import requests

url = 'https://api.vk.com/method/groups.get?v=5.131&access_token' \
      '=7bf83a56fa02ce7bd9f10f02b96d51549c3e3c34ee3dbf41705b45633ccad3aac3ae5ec25e09920d0afa2&expires_in=86400' \
      '&user_id=376369259'

response = requests.get(url)

print(response.text)
with open('vk.html', 'w', encoding="UTF-8") as f:
    f.write(response.text)
