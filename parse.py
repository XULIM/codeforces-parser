import requests
import itertools
import json
import logging
from bs4 import BeautifulSoup

API_KEY = "https://codeforces.com/api/problemset.problems/"
ATTR = ["problemSet.name", "tags"]


class parser:
    def __init__(self, api_key=API_KEY, attr=ATTR):
        self.api_key = api_key
        self.attr = attr

    def _parse(self, attr: list = []) -> json:
        res = requests.get(self.api_key)
        return res.json()

    def get_all_problems(self) -> list:
        return self._parse()["result"]["problems"]

    def get_filtered_problems(self, filters):
        matching_problems: list = self.get_all_problems()
        n = len(matching_problems)

        for key, val in filters.items():
            matching_problems = list(
                filter(lambda x: x[key] == val, matching_problems))

        if len(matching_problems) == n:
            logging.warning("No items filtered, check filter dictionary.")
        elif len(matching_problems) == 0:
            logging.error(
                "Filter failed, check filter dictionary and possibly reduce the number of filters.")
        else:
            logging.info("Filter succeeded.")

        return matching_problems

    def get_problem(contestId: int, index: str):
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

    def get_problems_by_contest(self, contestId):
        all_problems = self.get_all_problems()
        matching_problem = list(
            filter(lambda x: x["contestId"] == contestId, all_problems))
