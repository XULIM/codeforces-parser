from exceptions import InvalidArgumentException, InvalidURLException
from parse1 import parser
from database import parser_database
from enums import methods, class_parameter
import atexit
from colorama import Fore, Back, Style
import asyncio
import os
from pprint import pprint


@atexit.register
def exit_handler() -> None:
    print(".")
    print(".")
    print("Exiting Programme.")


def err(msg: str):
    print(Fore.RED + msg)


async def main():
    try:
        # db = parser_database()
        ps = parser()
        params = {str(class_parameter.TAGS.value): ["implementation", "math"]}
        val = await ps.parse(method=methods.PROBLEM_SET, params=params)
        for entry in val["result"]["problems"]:
            pprint(entry)

    except InvalidURLException:
        err("Invalid URL: check if it is a valid format.")
    except InvalidArgumentException:
        err("Invalid argument.")
    except Exception as e:
        err(f"Error: {e}.")


asyncio.run(main())
