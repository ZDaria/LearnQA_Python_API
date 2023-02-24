from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions
import allure
import pytest


@allure.epic("Registrations cases")
class TestUserRegister(BaseCase):
    exclude_param = [
        ('password'),
        ('username'),
        ('firstName'),
        ('lastName'),
        ('email')
    ]

    @allure.description("Correct user creation")
    def test_create_user_successfully(self):
        data = self.prepare_registration_data()
        response = MyRequests.post("/user", data=data)

        Assertions.assert_code_status(response, 200)
        Assertions.assert_json_has_key(response, 'id')

    @allure.description("Try to create user with existing email")
    def test_create_user_with_existing_email(self):
        email = 'vinkotov@example.com'
        data = self.prepare_registration_data(email=email)

        response = MyRequests.post("/user", data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode('utf-8') == \
               f"Users with email '{email}' already exists", \
            f"Unexpected response content: {response.content}"

    @allure.description("Try to create user with invalid emai: w/o @")
    def test_create_user_with_wrong_email(self):
        email = 'vinkotovexample.com'
        data = self.prepare_registration_data(email=email)

        response = MyRequests.post("/user", data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode('utf-8') == \
               f"Invalid email format", \
            f"Invalid email format were accepted by the system: " \
            f"{response.content}"

    @allure.description("Try to create user w/o mandatory fields")
    @pytest.mark.parametrize('wo_field', exclude_param)
    def test_create_user_wo_mandatory_field(self, wo_field):
        data = self.prepare_registration_data()
        data.pop(wo_field)
        response = MyRequests.post("/user", data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode('utf-8') == \
               f"The following required params are missed: {wo_field}"

    @allure.description("Try to create user with short name: letter")
    def test_create_user_with_one_letter_firstname(self):
        data = self.prepare_registration_data()
        data['firstName'] = 'a'
        response = MyRequests.post("/user", data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode('utf-8') == \
               "The value of 'firstName' field is too short"

    @allure.description("Try to create user with long firstName. With length "
                        "more then 250")
    def test_create_user_with_long_name(self):
        data = self.prepare_registration_data()
        data['firstName'] = "a" * 251
        response = MyRequests.post("/user", data=data)
        Assertions.assert_code_status(response, 400)
        assert response.content.decode('utf-8') == \
               "The value of 'firstName' field is too long"
