from bs4 import BeautifulSoup as bs
from exceptions import InvalidURLException, InvalidArgumentException
from enums import methods, class_parameter
from aiohttp import ClientSession
from objects import entry, entries
import json


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
                print(res.status)
                if res.status == 200:
                    print("Accessing data...")
                    res_js = await res.json()
                elif res.status == 400:
                    print("Error code: 400")
                    res_js = await res.json()
                    print("Check arguments.")
                    raise InvalidArgumentException("Bad arguments.")
                elif res.status == 403:
                    print("Probably got IP blocked for too many requests :)")
                else:
                    raise InvalidURLException(url, res.status)
                print("Parsing successful...")

        return entries(res_js["result"]) if res_js else None

    # TODO: select from database then use bs4 to parse content from website
    async def get_page(self, contest_id: int, index: str):
        with open("index.html", "w") as f:
            f.write(f"{contest_id},{index}\n")
        parse_url = f"https://codeforces.com/contest/{contest_id}/problem/{index}"
        async with ClientSession() as sesh:
            async with sesh.get(parse_url) as res:
                if res.status == 200:
                    html_doc = await res.content.read()
                    soup = bs(html_doc, "html.parser")
                    content = soup.find("div", {"class": "problem-statement"})
                    if content:
                        with open("index.html", "a") as f:
                            f.write(str(content))

                    else: 
                        print("No content available.")
                else: 
                    print("Could not read page content.")

    def get_tests(self, html_doc):
        soup = bs(html_doc, "html.parser")
        pres = soup.find_all("pre")
        for pre in pres:
            for child in pre:
                print(child.get_text())
