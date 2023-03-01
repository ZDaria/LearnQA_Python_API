import pytest
from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_requests import MyRequests
import allure


@allure.epic("User delete cases")
class TestUserDelete(BaseCase):
    @allure.description("Try to delete default user")
    def test_delete_default_user(self):
        login_data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }
        # LOGIN
        response1 = MyRequests.post("/user/login", data=login_data)

        auth_sid = self.get_cookie(response1, 'auth_sid')
        token = self.get_header(response1, 'x-csrf-token')
        user_id = self.get_json_value(response1, "user_id")

        Assertions.assert_code_status(response1, 200)

        # Try to delete
        response2 = MyRequests.delete(f"/user/{user_id}",
                                      headers={"x-csrf-token": token},
                                      cookies={"auth_sid": auth_sid})

        Assertions.assert_code_status(response2, 400)
        expected_str = "Please, do not delete test users with " \
                       "ID 1, 2, 3, 4 or 5."
        assert response2.content.decode('utf-8') == \
               expected_str, \
            f"Wrong assertion text \n" \
            f"Expected value: {expected_str} \n" \
            f"Actual: {response2.content.decode('utf-8')}"

    def test_delete_user_after_creation(self):
        # CREATE USER
        register_data = self.prepare_registration_data()
        response1 = MyRequests.post("/user", data=register_data)

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, 'id')

        email = register_data['email']
        password = register_data['password']
        user_id = self.get_json_value(response1, 'id')

        # LOGIN

        login_data = {
            'email': email,
            'password': password
        }

        response2 = MyRequests.post("/user/login", data=login_data)

        auth_sid = self.get_cookie(response2, 'auth_sid')
        token = self.get_header(response2, 'x-csrf-token')

        # DELETE
        response2 = MyRequests.delete(f"/user/{user_id}",
                                      headers={"x-csrf-token": token},
                                      cookies={"auth_sid": auth_sid})

        Assertions.assert_code_status(response2, 200)

        login_data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }
        validation_user = MyRequests.post("/user/login", data=login_data)

        auth_sid = self.get_cookie(validation_user, "auth_sid")
        token = self.get_header(validation_user, "x-csrf-token")

        response3 = MyRequests.get(f"/user/{user_id}",
                                   headers={"x-csrf-token": token},
                                   cookies={"auth_sid": auth_sid})

        Assertions.assert_code_status(response3, 404)

        assert response3.content.decode('utf-8') == "User not found", \
            f"Wrong assertion text \n" \
            f"Expected value: Invalid email format \n" \
            f"Actual: {response3.content.decode('utf-8')}"

    def test_delete_user_by_other_user(self):
        # CREATE USER1
        register_data = self.prepare_registration_data()
        user1 = MyRequests.post("/user", data=register_data)

        Assertions.assert_code_status(user1, 200)
        Assertions.assert_json_has_key(user1, 'id')

        email = register_data['email']
        password = register_data['password']

        # CREATE USER2
        register_data = self.prepare_registration_data()
        user2 = MyRequests.post("/user", data=register_data)

        Assertions.assert_code_status(user2, 200)
        Assertions.assert_json_has_key(user2, 'id')

        user_id = self.get_json_value(user2, 'id')

        # LOGIN with USER1
        login_data = {
            'email': email,
            'password': password
        }

        login = MyRequests.post("/user/login", data=login_data)

        auth_sid = self.get_cookie(login, 'auth_sid')
        token = self.get_header(login, 'x-csrf-token')
        # DELETE
        delete = MyRequests.delete(f"/user/{user_id}",
                                   headers={"x-csrf-token": token},
                                   cookies={"auth_sid": auth_sid})

        Assertions.assert_code_status(delete, 404)

        expected_str = "Auth token not supplied"
        assert delete.content.decode('utf-8') == \
               expected_str, \
            f"Wrong assertion text \n" \
            f"Expected value: {expected_str} \n" \
            f"Actual: {delete.content.decode('utf-8')}"
