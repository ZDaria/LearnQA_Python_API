import requests

url = 'https://playground.learnqa.ru/api/get_text'

responce = requests.get(url)
print(responce.text)
