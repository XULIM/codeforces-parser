from bs4 import BeautifulSoup as bs
from exceptions import InvalidURLException, InvalidArgumentException
from enums import methods, class_parameter
from aiohttp import ClientSession
from objects import entry, entries


class parser:
    def __init__(self):
        self.API = "https://codeforces.com/api/"

    async def parse(self, method: methods, params: dict[str, list[str]] | None = None):
        '''
        Parses the CodeForces API with the given method and parameters.
        Returns the result of the parsed json if successful, throws an error otherwise.
        '''
        res_js = None
        url: str = self.API
        query: str = str(method.value)
        if params:
            for item in params.items():
                query += item[0] + "&".join(item[1])
        url += query
        print(f"Parsing from URL: {url}")

        async with ClientSession() as sesh:
            async with sesh.get(url) as res:
                if res.status:
                    print("Accessing data...")
                    res_js = await res.json()
                elif res.status == 400:
                    res_js = await res.json()
                    print("Check arguments.")
                    raise InvalidArgumentException("Bad arguments.")
                else:
                    raise InvalidURLException(url, res.status)
                print("Parsing successful...")

        return res_js["result"]

    # TODO: select from database then use bs4 to parse content from website
    def get_problem(self, contest_id: int, problem_index: str):
        pass
