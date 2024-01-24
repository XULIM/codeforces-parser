import requests
import itertools
import json
import logging
from bs4 import BeautifulSoup

API_KEY = "https://codeforces.com/api/problemset.problems/"


class parser:
    def __init__(self):
        pass

    def __init__(self, attr: list):
        self.attr = attr

    def __init__(self, api_key: str, attr: list):
        self.api_key = api_key
        self.attr = attr

    def _parse(self, attr: list = []) -> json:
        return requests.get(self.api_key, attr).json()

    def get_all_problems(self) -> list:
        return json.loads(self._parse())["result"]["problems"]

    def get_problem(contestId: int, index: str) -> (Iterable[PageElement]) | None:
        link = f"https://codeforces.com/problemset/problem/{contestId}/{index}"
        res = requests.get(link)

        if res:
            bs = BeautifulSoup(res.content.decode('utf-8'), "lxml")
            problem_statement = bs.find("div", {"class": "problem-statement"})
            problem_children = problem_statement.childGenerator()
            return problem_children
        else:
            logging.exception(
                f"Error {res.status_code}: unable to parse page.")
            return None
