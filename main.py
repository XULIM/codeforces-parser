import atexit
import asyncio
from parser import parser
from db import db


@atexit.register
def exit_handler() -> None:
    print("Exiting Programme.")


async def main():
    try: 
        p = parser()
        d = await p.get_tests(1992, "e")
        print(d["input"])
        print(d["output"])
    except Exception as e:
        print("Error: ", str(e))


asyncio.run(main())
