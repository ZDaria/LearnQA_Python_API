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
    print(f"Server time {result['Date']}")
    date_validation = datetime.datetime.utcnow().\
        strftime('%a, %d %b %Y %H:%M:%S GMT')
    assert result['Date'] == date_validation \
           and result['Content-Type'] == 'application/json' and \
    result['Content-Length'] == '15' and \
    result['Connection'] == 'keep-alive' and \
    result['Keep-Alive'] == 'timeout=10' and \
    result['Server'] == 'Apache' and \
    result['x-secret-homework-header'] == 'Some secret value' and \
    result['Cache-Control'] == 'max-age=0' and \
    result['Expires'] == datetime.datetime.utcnow().\
        strftime('%a, %d %b %Y %H:%M:%S GMT')
