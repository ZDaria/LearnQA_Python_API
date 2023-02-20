import pytest
import requests
"""
Необходимо написать тест, который делает запрос на метод: 
https://playground.learnqa.ru/api/homework_cookie
Этот метод возвращает какую-то cookie с каким-то значением. 
Необходимо с помощью функции print() понять что за cookie и с каким значением, 
и зафиксировать это поведение с помощью assert

Чтобы pytest не игнорировал print() необходимо использовать ключик "-s": 
python -m pytest -s my_test.py 
"""
url = "https://playground.learnqa.ru/api/homework_cookie"


def test_cookie_validation():
    cookie_val = dict(requests.request("POST", url=url).cookies)
    print(cookie_val)
    assert cookie_val['HomeWork'] == "hw_value"
