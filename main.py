import atexit
import asyncio
from parser import parser
from db import db
from enums import methods, class_parameter


@atexit.register
def exit_handler() -> None:
    print("Exiting Programme.")


async def main():
    try: 
        p = parser()
        await p.get_tests(1992, "e")
    except Exception as e:
        print("Error: ", str(e))


asyncio.run(main())
