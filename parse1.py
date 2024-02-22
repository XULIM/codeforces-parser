from bs4 import BeautifulSoup as bs
import requests
from exceptions import InvalidURLException, InvalidArgumentException
from database import parser_database


class parser:
    def __init__(self):
        self.API = "https://codeforces.com/api/"

    def parse_method(self, suffix: str):
        res_js = None
        url = self.API + suffix
        res = requests.get(url)
        if res.status_code == 200:
            res_js = res.json()
        elif res.status_code == 400:
            comment = res.json()["comment"]
            raise InvalidArgumentException(f"Invalid Argument: {comment}")
        else:
            raise InvalidURLException(url, res.status_code)
        return res_js["result"]

    def parse_with_parameter(self, method, params: dict):
        param_str = ""
        for key, value in params.items():
            param_str += "{0}={1}".format(key, (str(i) + "&" for i in value))
        return self.parse_method(method + params)

    def get_problem(self, contest_id: int, problem_index: str):
        pass
