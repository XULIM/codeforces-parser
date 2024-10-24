import os
import asyncio

from typing import Any
from aiohttp import ClientSession
from bs4 import BeautifulSoup, Tag
from enum import Enum
from re import escape
from time import time, sleep
from datetime import timedelta

from lib.ua import Rotator
from lib.plog import Status, log
from lib.consts import UA_PATH, HTML_PATH

async def get_user_agents():
    """
    Gets user-agents from "https://www.useraggentlist.net/".

    Returns tuple in the form of (Status.OK, user_agents: str),
        where user_agents are separated by "\\n" if parsing is successful.
    Otherwise returns a tuple in the form of (Status.ERR, e: str),
        where e is the error message.
    """
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

if (not os.path.exists(UA_PATH)):
    asyncio.run(get_user_agents())
with open(UA_PATH, "r") as f:
    USER_AGENTS = f.read().splitlines()
ROTATOR = Rotator(USER_AGENTS)
HTML_PATH = "index.html"


class Endpoints(Enum):
    Problems = "problemset.problems?"
    Status = "problemset.recentStatus?"

def dtot(problem: dict[str,Any]) -> tuple:
    """
    Dictionary to tuple for the problems table.
    Returns:
        res (tuple): a conformed tuple for database binding.
    """
    cid: int = problem.get("contestId", -1)
    pindex: str = problem.get("index", "")
    name: str = escape(problem.get("name", ""))
    points: int = problem.get("points", 0)
    rating: int = problem.get("rating", 0)
    ltags = problem.get("tags", [])
    tags = ",".join(tag for tag in ltags)
    solved = 0
    res = (cid, pindex, name, points, rating, tags, solved)
    if cid == -1 or not pindex:
        log(Status.ERR, "could not make tuple:", res)
    return res;

# TODO: fix this, the current method refreshes the file even if the file is not meant to be refreshed.
def file_refresh(file: str, cd_days = 21, cd_hours = 0, cd_minutes = 0, cd_seconds = 0) -> bool:
    """
    Checks if file need to be created/refreshed.
    Default refresh timer is 21 days.
    Initially created to rotate user-agents every 21 days, but works for any file.
    """
    try:
        if (not os.path.exists(file)):
            return True
        cd = timedelta(days=cd_days, hours=cd_hours, minutes=cd_minutes, seconds=cd_seconds)
        delta_t = timedelta(seconds=(time() - os.path.getmtime(file)))
        diff = delta_t - cd
        if diff.total_seconds():
            return True
        return False
    except Exception as e:
        raise Exception("from file_refresh: file access error. Details: ", str(e))


async def get_problems() -> tuple[Status, list]:
    """
    Gets problems from the CodeForces API.
    Returns a tuple in the form of (Status.OK, problems: list),
        where problems is list of tuple that is compliant to database bindings.
    Otherwise returns a tuple in the form of (Status.ERR, []).
    """
    api_url = f"https://codeforces.com/api/{Endpoints.Problems.value}"
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
                return (Status.ERR, [])
    return (Status.OK, [dtot(p) for p in results["result"]["problems"]])

async def get_page(contest_id: int, index: str) -> None:
    """
    Parses the entire problem page given the contest_id and index.
    """
    parse_url = f"https://codeforces.com/contest/{contest_id}/problem/{index}"
    log(Status.OK, "Starting parsing on URL: ", parse_url)
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

async def get_tests(contest_id: int, index: str): 
    print(f"Getting test cases for problem {contest_id} {index}.")
    await get_page(contest_id, index)
    with open(HTML_PATH, "r") as f:
        bs = BeautifulSoup(f, "html.parser")
    samples = bs.find("div", {"class": "sample-test"})
    assert samples is Tag
    # --- 
    def get(name: str, attrs: dict[str,str]):
        res = []
        divs = bs.findAll(name, attrs)
        if not divs:
            log(Status.ERR, f"from get_tests: cannot find {name} with the following attributes: {attrs}.")
            return Status.ERR
        for div in divs:
            ls = []
            pre = div.findChild("pre")
            for child in pre.children:
                if (text := child.get_text().strip()):
                    ls.append(text)
            res.append(ls)
        return res
    # ---
    inputs = get("div", {"class":"input"})
    if (inputs is not Status.ERR):
        log(Status.OK, f"successfully parsed the input for {contest_id} {index}.")
    else:
        log(Status.ERR, f"from get_tests: could not parse input for {contest_id} {index}.")
    outputs = get("div", {"class":"output"})
    if (outputs is not Status.ERR):
        log(Status.OK, f"successfully parsed the output for {contest_id} {index}.")
        return Status.ERR
    else:
        log(Status.ERR, f"from get_tests: could not parse ouput for {contest_id} {index}.")
    return (inputs, outputs)


async def get_tests_old(contest_id: int, index: str) -> tuple[list[str] | Status, list[str] | Status]:
    """
    Gets the test case for the specific problem.
    """
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
