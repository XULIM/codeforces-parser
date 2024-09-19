import atexit
import asyncio
import os
from time import asctime, localtime
from typing import NoReturn

from aiohttp import ClientSession
from bs4 import BeautifulSoup
from enums import methods
from parser import CFParser
from db import db
from ua_parser import user_agent_parser as uap
from ua import Rotator
import p1

@atexit.register
def exit_handler() -> None:
    print("Exiting Programme.")

def get_last_modified_time(file: str):
    return localtime(os.path.getmtime(file))

async def get_user_agents():
    url = "https://www.useragentlist.net/"
    user_agents = []
    async with ClientSession() as sesh:
        async with sesh.get(url) as res:
            if res.status == 200:
                soup = BeautifulSoup(await res.text(), "html.parser")
                for user_agent in soup.select("pre.wp-block-code"):
                    user_agents.append(user_agent.text)
            else:
                print("Error: ", res.status)

    with open("./ua_list", "w") as f:
        for ua in user_agents:
            f.write(ua + "\n")

async def main():
    try: 
        print(asctime(get_last_modified_time("ua_list")))
        input, output = await p1.get_tests(1998, "C")
        print("input: ", input)
        print("output: ", output)
    except Exception as e:
        print("Error: ", str(e))


asyncio.run(main())
