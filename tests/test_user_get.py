import requests
from lib.base_case import BaseCase
from lib.assertions import Assertions

url = "https://playground.learnqa.ru/api/user"


class TestUserGet(BaseCase):
    def test_get_user_details_not_auth(self):
        resp = requests.get(url="https://playground.learnqa.ru/api/user/2")
        # {"username":"Vitaliy"}
        Assertions.assert_code_status(resp, 200)
        Assertions.assert_json_has_key(resp, 'username')
        Assertions.assert_json_has_not_key(resp, 'email')
        Assertions.assert_json_has_not_key(resp, 'firstName')
        Assertions.assert_json_has_not_key(resp, 'lastName')

    def test_user_details_auth_as_same_user(self):
        data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }

        resp1 = requests.post("https://playground.learnqa.ru/api/user/login",
                              data=data)

        auth_sid = self.get_coolie(resp1, "auth_sid")
        token = self.get_header(resp1, "x-csrf-token")
        user_id_from_auth_method = self.get_json_value(resp1, "user_id")

        resp2 = requests.get(f"https://playground.learnqa.ru/api/user/"
                             f"{user_id_from_auth_method}",
                             headers={"x-csrf-token": token},
                             cookies={"auth_sid": auth_sid})

        expected_keys = ["username", "email", "firstName", "lastName"]
        Assertions.assert_json_has_keys(resp2, expected_keys)
