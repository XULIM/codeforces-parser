import os
import atexit
import asyncio
from lib import db, ps
from lib.ps import Status, log, file_refresh

type void = None

@atexit.register
def exit_handler() -> None:
    print("Exiting Programme.")

# TODO: this function does not cover all edge cases.
# The problems table could be created but without problems.
async def populate_table(forced: bool = False) -> void:
    # ---
    async def make():
        db.create_table()
        status, problems = await ps.get_problems()
        if (status is Status.OK):
            db.insert(problems)
        else:
            log(Status.ERR, "from populate_table: ", "could not populate table - problems.")
            return
        log(Status.OK, "from populate_table: ", "table population successful.")
    # ---
    if (not forced or not file_refresh(db.DB_NAME, cd_days=3)):
        if (not db.table_exists()):
            await make()
        else:
            log(Status.OK, "from populate_table: ", "table exists and populated.")
        return
    os.remove(db.DB_NAME)
    db.drop_table()
    await make()

async def main() -> void:
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
        await populate_table(forced=True)
        cid = 1420
        found, li = db.select_contest(cid)
        if (not found):
            log(Status.WARN, f"could not find the contest {cid}.")
        else:
            print(li)
    except Exception as e:
        log(Status.ERR, str(e))
    finally:
        db.ccfree(con,cur)

asyncio.run(main())
