import atexit
import asyncio
from parser import parser
from database import parser_database
from objects import entry, entries
from enums import methods, class_parameter
from exceptions import InvalidArgumentException, InvalidURLException
from colorama import Fore, Back, Style
from pprint import pprint


@atexit.register
def exit_handler() -> None:
    print("Exiting Programme.")


def err(msg: str):
    print(Fore.RED + msg)


async def main():
    try:
        db = parser_database()
        ps = parser()
        params = {str(class_parameter.TAGS.value): ["implementation", "math"]}
        val = await ps.parse(method=methods.PROBLEM_SET)
        for obj in val.entries:
            input()
            print(obj)
    except InvalidURLException:
        err("Invalid URL: check if it is a valid format.")
    except InvalidArgumentException:
        err("Invalid argument.")
    except Exception as e:
        err(f"Error: {e}.")


asyncio.run(main())
