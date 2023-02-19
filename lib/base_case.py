import json.decoder

from requests import Response


class BaseCase:

    def get_coolie(self, response: Response, cookie_name):
        assert cookie_name in response.cookies, \
            f"Cannot find cookie with name {cookie_name} in the last response."
        return response.cookies[cookie_name]

    def get_header(self, response: Response, headers_name):
        assert headers_name in response.headers, \
            f"Can not find header with name {headers_name} " \
            f"in the last response."
        return response.headers[headers_name]

    def get_json_value(self, response: Response, name):
        try:
            resp_as_dict = response.json()
        except json.decoder.JSONDecodeError:
            assert False, f"Response is in JSON format. " \
                          f"Response text is '{response.text}'."
        assert name in resp_as_dict, \
            f"Response JSON does not have key '{name}'."
        return resp_as_dict[name]
