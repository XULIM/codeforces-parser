import atexit
import asyncio
from lib import gen, db, ps
from lib.ps import Status, log


@atexit.register
def exit_handler() -> None:
    print("Exiting Programme.")


async def main():
    con,cur = db.establish()
    try: 
        prob1 = {
            "contestId": 123,
            "index": "C",
            "name": "k.makise 'kurigohan'",
            "points": 1000,
            "rating": 1500,
            "tags": ["implementation", "dp", "segment tree"]
        }
        entry = ps.dtot(prob1)
        # db.drop_table()
        # db.create_table()
        # status, problems = await ps.get_problems()
        # if (status == Status.OK):
        #     db.insert(problems)
        # for line in cur.execute("SELECT cid, pindex, name, rating, tags FROM problems;"):
        #     print(line)
        log(Status.WARN, "this is a warning message.", prob1, entry)
    except Exception as e:
        log(Status.ERR, str(e))
    finally:
        db.ccfree(con,cur)

asyncio.run(main())
