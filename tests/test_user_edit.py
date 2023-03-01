from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions
import allure


@allure.title("Edit user validation")
class TestUserEdit(BaseCase):
    @allure.testcase("TEST-001")
    @allure.title("Make sure, that it is possible to edit user (Just created)")
    @allure.story("TEST-002 Endpoint /user")
    def test_edit_just_created_user(self):
        # Register
        register_data = self.prepare_registration_data()

        with allure.step("Create new user"):
            response1 = MyRequests.post("/user", data=register_data)
            Assertions.assert_code_status(response1, 200)
            Assertions.assert_json_has_key(response1, 'id')

        email = register_data['email']
        first_name = register_data['firstName']
        password = register_data['password']
        user_id = self.get_json_value(response1, 'id')

        # LOGIN

        login_data = {
            'email': email,
            'password': password
        }

        with allure.step("Auth with new user"):
            response2 = MyRequests.post("/user/login", data=login_data)
            Assertions.assert_code_status(response2, 200)
        auth_sid = self.get_cookie(response2, 'auth_sid')
        token = self.get_header(response2, 'x-csrf-token')

        # EDIT

        new_name = 'Changed Name'

        response3 = MyRequests.put(f"/user/{user_id}",
                                   headers={"x-csrf-token": token},
                                   cookies={"auth_sid": auth_sid},
                                   data={'firstName': new_name})
        with allure.step("Make sure, that edite were applied: "
                         "status code 200. "):
            Assertions.assert_code_status(response3, 200)

        # GET

        with allure.step("Make sure, that changes were saved"):
            response4 = MyRequests.get(f"/user/{user_id}",
                                       headers={"x-csrf-token": token},
                                       cookies={"auth_sid": auth_sid})
            Assertions.assert_json_value_by_name(response4, 'firstName',
                                                 new_name,
                                                 "Wrong name of the user "
                                                 "after edit.")

    def test_edit_not_authorized_user(self):
        # Register
        register_data = self.prepare_registration_data()
        response1 = MyRequests.post("/user", data=register_data)

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, 'id')

        user_id = self.get_json_value(response1, 'id')

        # EDIT

        new_name = 'Changed Name'

        response3 = MyRequests.put(f"/user/{user_id}",
                                   headers={"x-csrf-token": ""},
                                   cookies={"auth_sid": ""},
                                   data={"firstName": new_name})

        Assertions.assert_code_status(response3, 400)
        assert response3.content.decode('utf-8') == \
               "Auth token not supplied", \
            f"Wrong assertion text \n" \
            f"Expected value: Too short value for field firstName \n" \
            f"Actual: {response3.content.decode('utf-8')}"

    def test_edit_user_by_other_user(self):
        login_data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }
        response1 = MyRequests.post("/user/login", data=login_data)

        auth_sid = self.get_cookie(response1, 'auth_sid')
        token = self.get_header(response1, 'x-csrf-token')

        # Register new user for edit
        register_data = self.prepare_registration_data()
        response2 = MyRequests.post("/user", data=register_data)

        other_user_id = self.get_json_value(response2, 'id')

        # EDIT
        new_name = 'Changed Name'

        response3 = MyRequests.put(f"/user/{other_user_id}",
                                   headers={"x-csrf-token": token},
                                   cookies={"auth_sid": auth_sid},
                                   data={'username': new_name})

        Assertions.assert_code_status(response3, 422)

        # GET
        response5 = MyRequests.post("/user/login", data=login_data)

        other_auth_sid = self.get_cookie(response5, 'auth_sid')
        other_token = self.get_header(response5, 'x-csrf-token')

        response4 = MyRequests.get(f"/user/{other_user_id}",
                                   headers={"x-csrf-token": other_token},
                                   cookies={"auth_sid": other_auth_sid})

        Assertions.assert_json_value_by_name(response4, "username", "learnqa",
                                             "Wrong name of the user after "
                                             "edit.")

    def test_edit_user_email_with_wrong_format(self):
        # Register
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

        # EDIT

        new_email = 'vinkotovexample.com'

        response3 = MyRequests.put(f"/user/{user_id}",
                                   headers={"x-csrf-token": token},
                                   cookies={"auth_sid": auth_sid},
                                   data={'email': new_email})

        Assertions.assert_code_status(response3, 400)
        assert response3.content.decode('utf-8') == "Invalid email format", \
            f"Wrong assertion text \n" \
            f"Expected value: Invalid email format \n" \
            f"Actual: {response3.content.decode('utf-8')}"

    def test_edit_user_firstName_with_short_value(self):
        # Register
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

        # EDIT
        new_name = 'v'

        response3 = MyRequests.put(f"/user/{user_id}",
                                   headers={"x-csrf-token": token},
                                   cookies={"auth_sid": auth_sid},
                                   data={'firstName': new_name})

        Assertions.assert_code_status(response3, 400)

        assert response3.content.decode('utf-8') == \
               "{\"error\":\"Too short value for field firstName\"}", \
            f"Wrong assertion text \n" \
            f"Expected value: Too short value for field firstName \n" \
            f"Actual: {response3.content.decode('utf-8')}"
