from exceptions import InvalidArgumentException, InvalidURLException
from parse1 import parser
from database import parser_database
from enums import methods, class_parameter
import atexit
from colorama import Fore, Back, Style
import pprint
import asyncio
import aiohttp
import os


@atexit.register
def exit_handler() -> None:
    print(".")
    print(".")
    print("Exiting Programme.")


def err(msg: str):
    print(Fore.RED + msg)


def set_env() -> None:
    print(os.environ)


async def main():
    try:
        # db = parser_database()
        ps = parser()
        params = {str(class_parameter.TAGS.value): ["implementation", "math"]}
        val = await ps.parse_async(method=methods.PROBLEM_SET, params=params)
        for entry in val["result"]["problemStatistics"]:
            print(entry)
        # async with aiohttp.ClientSession() as session:
        #     async with session.get(
        #         f"https://codeforces.com/api/{str(methods.PROBLEM_SET)}"
        #     ) as res:
        #         print(res.status)
        #         res_js = await res.json()
        #         pprint.pprint(res_js["result"])

    except InvalidURLException:
        err("Invalid URL: check if it is a valid format.")
    except InvalidArgumentException:
        err("Invalid argument.")
    except Exception as e:
        err(f"Error: {e}.")


asyncio.run(main())
