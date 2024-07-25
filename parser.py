from bs4 import BeautifulSoup as bs, Tag
from exceptions import InvalidURLException, InvalidArgumentException
from enums import methods, class_parameter
from aiohttp import ClientSession
from objects import entry, entries


class parser:
    def __init__(self, html_doc = "index.html"):
        self.API = "https://codeforces.com/api/"
        self.html = html_doc

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

    def find(self, name: str, attrs: dict[str, str] = {}):
        with open(self.html, "r") as f:
            soup = bs(f, "html.parser")
            tag = soup.find(name, attrs)
            return soup.find(name, attrs) if tag else None

    def find_all(self, name: str, attrs: dict[str, str] = {}):
        with open(self.html, "r") as f:
            soup = bs(f, "html.parser")
            tags = soup.find(name, attrs)
            return soup.find_all(name, attrs) if tags else None

    def write(self, html, *args):
        with open(self.html, "w") as f:
            soup = bs(html, "html.parser")
            title = soup.new_tag("title")
            title.attrs = {"id": "problem"}
            title.string = "".join(args)
            soup.append(title)
            f.write(soup.prettify())

    async def get_page(self, contest_id: int, index: str) -> bool:
        parse_url = f"https://codeforces.com/contest/{contest_id}/problem/{index}"
        async with ClientSession() as sesh:
            async with sesh.get(parse_url) as res:
                if res.status == 200:
                    html_doc = await res.content.read()
                    self.write(html_doc, f"{contest_id},{index}")
                else: 
                    print("Error reading page: ", res.status)
                    self.write("")
                    return False
        return True

    async def get_tests(self, contest_id: int, index: str):
        if not await self.get_page(contest_id, index): 
            raise InvalidArgumentException\
            (f"Could not get page content with contest_id: {contest_id}, index: {index}")
        pres = self.find_all("pre")
        if pres is None:
            return None
        for pre in pres:
            for child in pre.children:
                print(child.get_text())
