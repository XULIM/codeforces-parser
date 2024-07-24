import atexit
import asyncio
import sqlite3
from aiohttp import ClientSession
import json
from parser import parser
from db import db
from objects import entry, entries
from enums import methods, class_parameter
from exceptions import InvalidArgumentException, InvalidURLException


@atexit.register
def exit_handler() -> None:
    print("Exiting Programme.")


async def main():
    try: 
        p = parser()
        await p.get_page(1988, "b")
    except Exception as e:
        print("Error: ", str(e))


asyncio.run(main())
