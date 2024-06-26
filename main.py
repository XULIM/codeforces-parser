import atexit
import asyncio
import sqlite3
from aiohttp import ClientSession
import json
from parser import parser
from db import db
from database import parser_database
from objects import entry, entries
from enums import methods, class_parameter
from exceptions import InvalidArgumentException, InvalidURLException


@atexit.register
def exit_handler() -> None:
    print("Exiting Programme.")


async def main():
    try:
        # con = sqlite3.connect("results.db")
        # cur = con.cursor()
        # print("Creating: problems table")
        # cur.execute("""
        # DROP TABLE IF EXISTS problems;
        # """)
        # cur.execute(
        #     """
        #         CREATE TABLE IF NOT EXISTS problems (
        #             contestId INTEGER NOT NULL,
        #             problemIndex VARCHAR NOT NULL,
        #             rating INT,
        #             tags TEXT,
        #             solvedCount INT,
        #             PRIMARY KEY (contestId, problemIndex)
        #         );
        #     """
        # )
        # print("Created table: problems")

        # print("Getting tables")
        # cur.execute("SELECT name FROM sqlite_master;")
        # print(f"Tables: {cur.fetchone()}")

        # print("Getting table info")
        # cur.execute("PRAGMA table_info(problems)")
        # print(f"Table info: {cur.fetchall()}")

        d = db()
        ps = parser()
        params = {str(class_parameter.TAGS.value): ["implementation", "math"]}
        val = await ps.parse(method=methods.PROBLEM_SET)
        # cur.executemany("INSERT INTO problems VALUES (?, ?, ?, ?, ?)", val.conform())
        # con.commit()
        # print("done")

        # cur.execute("SELECT * FROM problems;")
        # print(cur.fetchall())
        # con.close()
    except InvalidURLException:
        print("Invalid URL: check if it is a valid format.")
    except InvalidArgumentException:
        print("Invalid argument.")
    except Exception as e:
        print(f"Error: {e}.")


asyncio.run(main())
