import pytest
import requests
import datetime
from datetime import timezone
"""
Необходимо написать тест, который делает запрос на метод: 
https://playground.learnqa.ru/api/homework_header


Этот метод возвращает headers с каким-то значением. 
Необходимо с помощью функции print() понять что за headers и с каким значением,
и зафиксировать это поведение с помощью assert
"""
url = "https://playground.learnqa.ru/api/homework_header"


def test_header_request():
    result = requests.request("POST", url=url).headers
    print(datetime.datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT'))
    assert result['x-secret-homework-header'] == 'Some secret value'
