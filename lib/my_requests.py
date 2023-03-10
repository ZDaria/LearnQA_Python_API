from requests import request, RequestException
from lib.logger import Logger
import allure
from environment import ENV_OBJECT


class MyRequests:
    @staticmethod
    def post(url: str, data: dict = None, headers: dict = None,
             cookies: dict = None):
        with allure.step(f"POST request to URL '{url}'"):
            return MyRequests._send(url, data, headers, cookies, 'POST')

    @staticmethod
    def get(url: str, data: dict = None, headers: dict = None,
            cookies: dict = None):
        with allure.step(f"GET request to URL '{url}'"):
            return MyRequests._send(url, data, headers, cookies, 'GET')

    @staticmethod
    def put(url: str, data: dict = None, headers: dict = None,
            cookies: dict = None):
        with allure.step(f"PUT request to URL '{url}'"):
            return MyRequests._send(url, data, headers, cookies, 'PUT')

    @staticmethod
    def delete(url: str, data: dict = None, headers: dict = None,
               cookies: dict = None):
        with allure.step(f"DELETE request to URL '{url}'"):
            return MyRequests._send(url, data, headers, cookies, 'DELETE')

    @staticmethod
    def _send(url: str, data: dict, headers: dict, cookies: dict, method: str):

        url = f"{ENV_OBJECT.get_base_url()}{url}"

        if headers is None:
            headers = {}
        if cookies is None:
            cookies = {}

        Logger.add_request(url, data, headers, cookies, method)

        try:
            if method == 'GET':
                response = request(method=method, url=url, params=data,
                                   headers=headers, cookies=cookies)
            else:
                response = request(method=method, url=url, data=data,
                                   headers=headers, cookies=cookies)
        except RequestException as e:
            raise Exception(e)

        Logger.add_response(response)

        return response
