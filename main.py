import atexit
import asyncio
import gen, d1, p1
from p1 import Status, log


@atexit.register
def exit_handler() -> None:
    print("Exiting Programme.")


async def main():
    con,cur = d1.establish()
    try: 
        prob1 = {
            "contestId": 123,
            "index": "C",
            "name": "k.makise 'kurigohan'",
            "points": 1000,
            "rating": 1500,
            "tags": ["implementation", "dp", "segment tree"]
        }
        entry = p1.dtot(prob1)
        # d1.drop_table()
        # d1.create_table()
        # status, problems = await p1.get_problems()
        # if (status == Status.OK):
        #     d1.insert(problems)
        # for line in cur.execute("SELECT cid, pindex, name, rating, tags FROM problems;"):
        #     print(line)
        log(Status.WARN, "this is a warning message.", prob1, entry)
    except Exception as e:
        log(Status.ERR, str(e))
    finally:
        d1.ccfree(con,cur)

asyncio.run(main())
