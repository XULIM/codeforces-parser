import os
import atexit
import asyncio
from lib import db, ps
from lib.ps import Status, log, file_refresh

type void = None

@atexit.register
def exit_handler() -> None:
    print("Exiting Programme.")

async def populate_table(forced: bool = False) -> void:
    if (not forced and not file_refresh(db.DB_NAME, cd_days=3)):
        log(Status.OK, "from populate_table:", f"file {db.DB_NAME} already exists.", "proceeding.")
        return
    log(Status.WARN, "from populate_table:",
        f"file {db.DB_NAME} needs to be refreshed or the action is forced.",
        f"proceeding with file refresh for {db.DB_NAME}."
    )
    # note that sqlite3 creates the file upon establishing a
    # sqlite3.Connection to the file if it does not exist.
    db.drop_table()
    db.create_table()
    status, problems = await ps.get_problems()
    if (status is Status.OK):
        db.insert(problems)
    else:
        log(Status.ERR, "from populate_table: ", "could not populate table - problems.")
        return
    log(Status.OK, "from populate_table: ", "table population successful.")

async def main() -> void:
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
        await populate_table()
        cid = 1420
        found, li = db.select_contest(cid)
        if (not found):
            log(Status.WARN, f"could not find the contest {cid}.")
        else:
            print(li)
    except Exception as e:
        log(Status.ERR, str(e))

asyncio.run(main())
