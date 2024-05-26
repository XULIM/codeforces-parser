import atexit
import asyncio
from parser import parser
from database import parser_database
from objects import entry
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
        # val = await ps.parse(method=methods.PROBLEM_SET, params=params)
        fake_problem = {
            "contestId": 1,
            "index": 'A',
            "name": "hello world",
            "type": "PROGRAMMING",
            "rating": 800,
            "tags": ['implementation', 'math']
        }
        fake_stats = {
            "contestId": 1,
            "index": 'A',
            "solvedCount": 1500
        }
        en = entry(fake_problem, fake_stats)
        print(en.conform_str())
        print(repr(en))

    except InvalidURLException:
        err("Invalid URL: check if it is a valid format.")
    except InvalidArgumentException:
        err("Invalid argument.")
    except Exception as e:
        err(f"Error: {e}.")


asyncio.run(main())
