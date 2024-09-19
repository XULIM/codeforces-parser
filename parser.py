from types import NoneType
from typing import Any
from aiohttp import ClientSession
from bs4 import BeautifulSoup as bs
from bs4 import NavigableString, ResultSet, Tag

from enums import methods
from exceptions import InvalidArgumentException, InvalidURLException
from objects import entries
from ua import Rotator


class CFParser:
    def __init__(self, html_doc = "index.html"):
        """
        Initializes a CFParser object with the following fields:
            - self.API: the codeforces API.
            - self.html: the html doc that will be parsed to.
            - self.user_agents: the list of user-agents to be used for bs4 parsing.
        """
        self.API: str = "https://codeforces.com/api/"
        self.html: str = html_doc
        with open("./ua_list", "r") as f:
            user_agents = f.read().splitlines()
        self.rotator: Rotator = Rotator(user_agents)
        self.user_agent: str = str(self.rotator.get())

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
        header = {"User-Agent": self.user_agent}
        async with ClientSession(headers=header) as sesh:
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
        """
        Finds the first tag with the respective attributes (attrs).
        Returns the Tag | NavigableString object if found, None otherwise.
        """
        with open(self.html, "r") as f:
            soup = bs(f, "html.parser")
            tag = soup.find(name, attrs)
            return soup.find(name, attrs) if tag else None

    def find_all(self, name: str, attrs: dict[str, str] = {}) -> ResultSet[Any] | None:
        """
        Finds all of the tags with the respective name and attributes (attrs).
        Returns a ResultSet of all the matching Tag | NavigableString objects if found, None otherwise.
        """
        with open(self.html, "r") as f:
            soup = bs(f, "html.parser")
            tags = soup.find(name, attrs)
            return soup.find_all(name, attrs) if tags else None

    def write(self, html, *args) -> NoneType:
        """
        Writes html and args to self.html.
        """
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
        url = "https://codeforces.com/contest/1998/problem/C"
        parse_url = f"https://codeforces.com/contest/{contest_id}/problem/{index}"
        print("Parsing URL: ", parse_url)
        header = {"User-Agent": self.user_agent}
        async with ClientSession(headers=header) as sesh:
            async with sesh.get(parse_url) as res:
                print("Current Header: ", sesh.headers)
                if res.status == 200:
                    html_doc = await res.content.read()
                    print(html_doc)
                    problem_statement = self.find("div", {"class": "problem-statement"})
                    if not self.__verify(problem_statement):
                        print(f"Could not parse problem with the given contest_id: {contest_id} and index: {index}.")
                        self.write("")
                        return False
                    self.write(html_doc, f"{contest_id},{index}")
                else: 
                    print("Error reading page: ", res.status)
                    print(res.headers)
                    self.write("")
                    return False
        return True

    async def get_tests(self, contest_id: int, index: str) -> dict[str, list[str]] | None:
        """
        Gets the test cases ("input" and "output") of a CodeForces problem.
        Returns a dict with keys "input" and "output" and their respective values in list[str] if found, 
        None otherwise.
        """
        test = {"input": [], "output": []}
        if not await self.get_page(contest_id, index): 
            print("Could not parse page")
            return None
        input = self.find("div", {"class": "input"})
        output = self.find("div", {"class": "output"})
        if not self.__verify(input) or not self.__verify(output):
            return None
        p_i = input.findChild("pre")
        p_o = output.findChild("pre")
        if self.__verify(p_i):
            for child in p_i.children:
                text = child.get_text().strip()
                if text:
                    test["input"].append(text)
        if self.__verify(p_o):
            text = p_o.get_text().strip()
            if text:
                vec = text.splitlines()
                for i in range(len(vec)):
                    vec[i] = vec[i].strip()
                test["output"] = vec
        return test
