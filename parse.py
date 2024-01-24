import requests
import itertools
import json
import logging

API_KEY = "https://codeforces.com/api/problemset.problems/"


class parser:
    def __init__(self):
        pass

    def __init__(self, attr):
        self.attr = attr

    def __init__(self, api_key, attr):
        self.api_key = api_key
        self.attr = attr

    def _parse(self, attr=[]) -> json:
        return requests.get(self.api_key, attr).json()

    def get_all_problems(self) -> list:
        return json.loads(self._parse())["result"]["problems"]
