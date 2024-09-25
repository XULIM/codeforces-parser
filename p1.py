import os

from typing import Any
from aiohttp import ClientSession
from bs4 import BeautifulSoup, Tag
from ua import Rotator
from enum import Enum
from re import escape
from time import time, sleep
from datetime import timedelta

UA_PATH = "ua_list"
with open(UA_PATH, "r") as f:
    USER_AGENTS = f.read().splitlines()
ROTATOR = Rotator(USER_AGENTS)
HTML_PATH = "index.html"

class Status(Enum):
    OK = (0, "[OK]")
    ERR = (1, "[ERR]")
    WARNING = (2, "[!]")
    def __init__(self, num, string):
        self.num = num
        self.string = string
    def __str__(self):
        return self.string

class Endpoint(Enum):
    Problems = "problemset.problems?"
    Status = "problemset.recentStatus?"

class Entry():
    def __init__(self, problems: dict):
        try:
            self.contest_id = problems["contestId"]
            self.index = problems["index"]
            self.name = escape(problems.get("name", ""))
            self.points = problems.get("points", 0)
            self.rating = problems.get("rating", 0)
            self.tags = problems.get("tags", [])
            self.is_solved = False
        except Exception as e:
            log(Status.ERR, "from Entry.__init__: cannot create entry object.", 
                "Details:", e)

    def __str__(self):
        return (f"{self.contest_id},"
            f"{self.index}," +
            f"{self.name}," +
            f"{self.points}," +
            f"{self.rating}," +
            f"{self.tags}," +
            f"{(1 if self.is_solved else 0)}"
        )

    def conform(self):
        return self.__str__()

def file_refresh(file: str, cd_days = 21, cd_hours = 0, cd_minutes = 0, cd_seconds = 0) -> bool:
    cd = timedelta(days=cd_days, hours=cd_hours, minutes=cd_minutes, seconds=cd_seconds)
    delta_t = timedelta(seconds=(time() - os.path.getmtime(file)))
    diff = delta_t - cd
    if diff.total_seconds():
        return True
    return False

def log(stat: Status, *args):
    print(f"{str(stat)}:", "".join(args))

async def get_user_agents():
    url = "https://www.useragentlist.net/"
    user_agents = []
    sleep(1) # To avoid timeout due to spamming
    try:
        async with ClientSession() as sesh:
            async with sesh.get(url) as res:
                if res.status == 200:
                    soup = BeautifulSoup(await res.text(), "html.parser")
                    for user_agent in soup.select("pre.wp-block-code"):
                        user_agents.append(user_agent.text)
                else:
                    print("Error: ", res.status)
    except Exception as e:
        return (Status.ERR, str(e))

    try:
        with open(UA_PATH, "w") as f:
            for ua in user_agents:
                f.write(ua + "\n")
        return (Status.OK, user_agents)
    except Exception as e:
        return (Status.ERR, str(e))

async def get_problems() -> tuple[Status, dict[str, Any]]:
    api_url = f"https://codeforces.com/api/{Endpoint.Problems.value}"
    header = {"User-Agent": str(ROTATOR.get())}
    print(f"Parsing CodeForces API: {api_url}.")
    sleep(1) # To avoid timeout due to spamming
    async with ClientSession(headers=header) as session:
        async with session.get(api_url) as res:
            if res.status == 200:
                log(Status.OK, f"from get_problems: able to access CodeForces API.")
                results = await res.json()
            else:
                log(Status.ERR, f"from get_problems: unable to access CodeForces API", 
                    f"({res.status}).")
                return (Status.ERR, {})
    return (Status.OK, results["result"]["problems"])

async def get_page(contest_id: int, index: str) -> None:
    parse_url = f"https://codeforces.com/contest/{contest_id}/problem/{index}"
    print("Starting parsing on URL: ", parse_url)
    header = {"User-Agent": str(ROTATOR.get())}
    sleep(1) # To avoid timeout due to spamming
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
