from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions


class TestUserGet(BaseCase):
    def test_get_user_details_not_auth(self):
        resp = MyRequests.get("/api/user/2", )

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

        resp1 = MyRequests.post("/user/login", data=data)

        auth_sid = self.get_coolie(resp1, "auth_sid")
        token = self.get_header(resp1, "x-csrf-token")
        user_id_from_auth_method = self.get_json_value(resp1, "user_id")

        resp2 = MyRequests.get(f"/user/{user_id_from_auth_method}",
                               headers={"x-csrf-token": token},
                               cookies={"auth_sid": auth_sid})

        expected_keys = ["username", "email", "firstName", "lastName"]
        Assertions.assert_json_has_keys(resp2, expected_keys)
