from bs4 import BeautifulSoup as bs
import requests
from exceptions import InvalidURLException, InvalidArgumentException
from enums import methods, class_parameter
import asyncio
from aiohttp import ClientSession
from misc_utils import loading


# TODO: use async/await for parsing methods.
class parser:
    def __init__(self):
        self.API = "https://codeforces.com/api/"

    async def parse_async(
        self, method: methods, params: dict[str, list[str]] | None = None
    ):
        res_js = None
        url: str = self.API
        query: str = str(method.value)
        if params: 
            for item in params.items():
                query += item[0] + "&".join(item[1])
        url += query
        print(url)

        async with ClientSession() as sesh:
            async with sesh.get(url) as res:
                if res.status:
                    print("Accessing data...")
                    res_js = await res.json()
                elif res.status == 400:
                    res_js = await res.json()
                    print("Check arguments.")
                    raise InvalidArgumentException(f"Bad arguments: {res_js["comment"]}")
                else: 
                    raise InvalidURLException(url, res.status)
                print("Parsing successful...")
        return res_js

    def parse_method(self, method: methods, params: dict[str, list[str]] | None = None):
        """
        Parses the CodeForces API with the according method string.

        raises exceptions.InvalidArgumentException when given an invalid argument (method or params).
        raises exceptions.InvalidURLException when given an invalid URL (caused by method or params).
        """
        res_js = None
        url: str = self.API
        query: str = str(method.value)
        if params:
            for item in params.items():
                query += item[0] + "&".join(item[1])
        url += query
        print("Querying URL: ", url)
        res = requests.get(url)
        if res.status_code == 200:
            print("Accessing data...")
            res_js = res.json()
        elif res.status_code == 400:
            print("Something went wrong.")
            comment = res.json()["comment"]
            raise InvalidArgumentException(f"Invalid Argument: {comment}")
        else:
            raise InvalidURLException(url, res.status_code)
        print("Successfully parsed data.")
        return res_js["result"]

    # TODO: select from database then use bs4 to parse content from website
    def get_problem(self, contest_id: int, problem_index: str):
        pass
