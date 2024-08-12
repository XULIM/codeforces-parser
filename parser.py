from types import NoneType
from typing import Any
from aiohttp import ClientSession
from bs4 import BeautifulSoup as bs
from bs4 import NavigableString, ResultSet, Tag

from enums import methods
from exceptions import InvalidArgumentException, InvalidURLException
from objects import entries


class parser:
    def __init__(self, html_doc = "index.html"):
        self.API = "https://codeforces.com/api/"
        self.html = html_doc

    def __verify(self, tag: Tag | NavigableString | None) -> bool:
        """
        Verifies that the passed in tag is a Tag object.
        Returns True if it is, False otherwise.
        """
        return tag is not None and type(tag) is Tag

    async def parse(self, method: methods, params: dict[str, list[str]] | None = None) -> entries | None:
        '''
        Parses the CodeForces API with the given method and parameters.
        Returns the result (entries object) of the parsed json if successful, throws an error otherwise.
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

    def find(self, name: str, attrs: dict[str, str] = {}) -> Tag | NavigableString | None:
        with open(self.html, "r") as f:
            soup = bs(f, "html.parser")
            tag = soup.find(name, attrs)
            return soup.find(name, attrs) if tag else None

    def find_all(self, name: str, attrs: dict[str, str] = {}) -> ResultSet[Any] | None:
        with open(self.html, "r") as f:
            soup = bs(f, "html.parser")
            tags = soup.find(name, attrs)
            return soup.find_all(name, attrs) if tags else None

    def write(self, html, *args) -> NoneType:
        with open(self.html, "w") as f:
            soup = bs(html, "html.parser")
            title = soup.new_tag("title")
            title.attrs = {"id": "problem"}
            title.string = "".join(args)
            soup.append(title)
            f.write(soup.prettify())

    async def get_page(self, contest_id: int, index: str) -> bool:
        """
        Parses the problem page https://codeforces.com/contest/{contest_id}/problem/{index}.
        The parsed page is stored in self.html (default value of "index.html").
        Returns True if parsing is successful, False otherwise.
        """
        parse_url = f"https://codeforces.com/contest/{contest_id}/problem/{index}"
        async with ClientSession() as sesh:
            async with sesh.get(parse_url) as res:
                if res.status == 200:
                    html_doc = await res.content.read()
                    problem_statement = self.find("div", {"class": "problem-statement"})
                    if not self.__verify(problem_statement):
                        print(f"Could not parse problem with the given contest_id: {contest_id}\
                              and index: {index}.")
                        self.write("")
                        return False
                    self.write(html_doc, f"{contest_id},{index}")
                else: 
                    print("Error reading page: ", res.status)
                    self.write("")
                    return False
        return True

    async def get_tests(self, contest_id: int, index: str) -> dict[str, list[str]] | None:
        test = {"input": [], "output": []}
        if not await self.get_page(contest_id, index): 
            return None
        input = self.find("div", {"class": "input"})
        output = self.find("div", {"class": "output"})
        if not self.__verify(input) or not self.__verify(output):
            return None
        p_i = input.findChild("pre") # type: ignore
        p_o = output.findChild("pre") # type: ignore
        if self.__verify(p_i):
            for child in p_i.children: # type: ignore
                text = child.get_text().strip()
                if text:
                    test["input"].append(text)
        if self.__verify(p_o):
            text = p_o.get_text().strip() # type: ignore
            if text:
                vec = text.splitlines()
                for i in range(len(vec)):
                    vec[i] = vec[i].strip()
                test["output"] = vec
        return test
