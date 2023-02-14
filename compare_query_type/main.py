import requests
from json import JSONDecoder, JSONEncoder
import json


def req_method_validation(meth: str, args: dict):
    url = "https://playground.learnqa.ru/ajax/api/compare_query_type"
    # expected_methods = ["POST", "GET", "PUT", "DELETE"]
    if meth == "GET":
        resp = requests.request(meth, url, params=args)
    else:
        resp = requests.request(meth, url, data=args)

    result = [resp.text, resp.status_code, resp.request.method]
    try:
        result.append(resp.json())
    except JSONEncoder as e:
        return e
    finally:
        return result


def main():
    # 1. Делает http-запрос любого типа без параметра method,
    # описать что будет выводиться в этом случае.
    url = "https://playground.learnqa.ru/ajax/api/compare_query_type"
    res = requests.get(url)
    print(res.text, res.status_code, res.request.method)
    # 2. Делает http - запрос не из списка.Например, HEAD.
    # Описать что будет выводиться в этом случае.
    res = requests.head(url, data={"method": "HEAD"})
    print(res.text, res.status_code, res.request.method)
    # 3.Делает запрос с правильным значением method.
    res = requests.get(url, params={"method": "GET"})
    print(res.text, res.status_code, res.request.method)
    """
    4. С помощью цикла проверяет все возможные сочетания реальных типов 
    запроса и значений параметра method. Например с GET-запросом передает 
    значения параметра method равное ‘GET’, затем ‘POST’, ‘PUT’, ‘DELETE’ 
    и так далее. И так для всех типов запроса. Найти такое сочетание, 
    когда реальный тип запроса не совпадает со значением параметра, 
    но сервер отвечает так, словно все ок. Или же наоборот, когда типы 
    совпадают, но сервер считает, что это не так.
    """
    expected_methods = ["POST", "GET", "PUT", "DELETE"]
    for method in expected_methods:
        for method_2 in expected_methods:
            result = req_method_validation(method, {"method": method_2})
            # print(method, result)
            if method_2 != method and result[1] == 200:
                print(f"Wrong combination {method, method_2}")


main()
