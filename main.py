import atexit
import asyncio
from time import asctime, localtime, strftime, sleep
from typing import NoReturn

from aiohttp import ClientSession
from bs4 import BeautifulSoup
from enums import methods
from db import db
from ua_parser import user_agent_parser as uap
from ua import Rotator
from p1 import *


@atexit.register
def exit_handler() -> None:
    print("Exiting Programme.")


async def main():
    try: 
        prob1 = {
            "contestId": 123,
            "index": "C",
            "name": "k.makise",
            "points": 1000,
            "rating": 1500,
            "tags": ["implementation", "math"]
        }
        test_entry = Entry(prob1)
        print(test_entry)
        print(file_refresh(UA_PATH))
    except Exception as e:
        log(Status.ERR, str(e))


asyncio.run(main())
