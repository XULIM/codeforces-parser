from bs4 import BeautifulSoup as bs
import requests
from exceptions import InvalidURLException, InvalidArgumentException
from database import tables


class parser:
    def __init__(self):
        self.API = "https://codeforces.com/api/"

    def parse_method(self, suffix: str):
        """
        Parses the CodeForces API with the according method string.

        raises exceptions.InvalidArgumentException when given an invalid argument (suffix string).
        raises exceptions.InvalidURLException when given an invalid URL (caused by suffix string).
        """
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

    def parse_with_parameter(self, method: str, params: dict):
        """
        Parses the CodeForces API with the according method and parameters.

        raises exceptions.InvalidArgumentException when given an invalid argument (methods, params).
        raises exceptions.InvalidURLException when given an invalid URL (caused by methods, params).
        """

        param_str = ""
        for key, value in params.items():
            param_str += "{0}={1}".format(key, (str(i) + "&" for i in value))
        return self.parse_method(method + param_str)

    def get_problem(self, contest_id: int, problem_index: str):
        pass
