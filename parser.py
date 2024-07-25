from bs4 import BeautifulSoup as bs
from exceptions import InvalidURLException, InvalidArgumentException
from enums import methods, class_parameter
from aiohttp import ClientSession
from objects import entry, entries


class parser:
    def __init__(self):
        self.API = "https://codeforces.com/api/"
        self.html = "index.html"

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

    # TODO: code clean up.
    async def get_page(self, contest_id: int, index: str) -> bool:
        with open(self.html, "r") as f:
            line = f.readline()
            if line == f"{contest_id},{index}":
                return True
        parse_url = f"https://codeforces.com/contest/{contest_id}/problem/{index}"
        async with ClientSession() as sesh:
            async with sesh.get(parse_url) as res:
                if res.status == 200:
                    html_doc = await res.content.read()
                    soup = bs(html_doc, "html.parser")
                    content = soup.find("div", {"class": "problem-statement"})
                    if content:
                        with open(self.html, "w") as f:
                            f.write(f"{contest_id},{index}\n")
                            f.write(str(content))
                    else: 
                        print("No page content available.")
                        with open(self.html, "w") as f:
                            f.write("")
                        return False
                else: 
                    print("Could not read page content.")
                    with open(self.html, "w") as f:
                        f.write("")
                    return False
        return True

    def get_tests(self, contest_id: int, index: str):
        if not self.get_page(contest_id, index): 
            raise InvalidArgumentException\
            (f"Could not get page content with contest_id: {contest_id}, index: {index}")
        soup = bs(self.html, "html.parser")
