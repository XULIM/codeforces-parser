from typing import Any
from aiohttp import ClientSession
from bs4 import BeautifulSoup, Tag
from ua import Rotator
from enum import Enum

class Status(Enum):
    OK = (0, "[OK]")
    ERR = (1, "[ERR]")
    WARNING = (2, "[!]")
    def __init__(self, num, string):
        self.num = num
        self.string = string
    def __str__(self):
        return self.string

with open("./ua_list", "r") as f:
    USER_AGENTS = f.read().splitlines()
ROTATOR = Rotator(USER_AGENTS)
HTML_PATH = "index.html"

def log(stat: Status, *args):
    print(f"{str(stat)}:", "".join(args))

async def get_page(contest_id: int, index: str) -> None:
    parse_url = f"https://codeforces.com/contest/{contest_id}/problem/{index}"
    print("Starting parsing on URL: ", parse_url)
    header = {"User-Agent": str(ROTATOR.get())}
    async with ClientSession(headers=header) as session:
        async with session.get(parse_url) as res:
            if res.status == 200:
                log(Status.OK, f"from get_page: able to access website.")
                html_doc = await res.content.read()
                with open(HTML_PATH, "wb") as file:
                    file.write(html_doc)
            else: 
                log(Status.ERR, f"from get_page: unable to access website {res.status}.")

async def get_tests(contest_id: int, index: str) -> tuple[list[str] | Status, list[str] | Status]:
    print(f"Getting test cases for problem {contest_id} {index}.")
    with open(HTML_PATH, "r") as f:
        bs = BeautifulSoup(f, "html.parser")
    # ---
    def get_text(name: str, attrs: dict[str,str]) -> list[str] | Status:
        arr = []
        if ((div := bs.find(name, attrs)) and type(div) == Tag):
            if ((pre := div.findChild("pre")) and type(pre) == Tag):
                for child in pre.children:
                    if (text := child.get_text().strip()):
                        arr.append(text)
            else:
                log(Status.ERR, "from get_text in get_tests: ",
                    f"unable to find \"pre\" tag with the following attrs: {attrs}.")
                return Status.ERR
        else:
            log(Status.ERR, "from get_text in get_tests: ", 
                "unable to parse text with the following attrs: {attrs}.")
            return Status.ERR
        return arr
    # ---
    input = get_text("div", {"class":"input"})
    output = get_text("div", {"class":"output"})
    if (input != Status.ERR and output != Status.ERR):
        log(Status.OK, "from get_tests: parsing successful.")
    return (input, output)
