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
    if (not os.path.exists(db.DB_NAME)):
        log(Status.WARN, "from populate_table:", f"file {db.DB_NAME} does not exist.")
        try:
            f = open(db.DB_NAME, "w")
            f.write("")
        except Exception as e:
            log(Status.ERR, "from populate_table:", f"file {db.DB_NAME} cannot be created.", "aborting.")
            return
        finally:
            f.close()
        log(Status.OK, "from populate_table: ", f"file {db.DB_NAME} created.")
        await make()
        return
    if (forced or file_refresh(db.DB_NAME, cd_days=3)):
        db.drop_table()
        await make()
        return

async def main() -> void:
    os.remove(db.DB_NAME)
    print(os.path.exists(db.DB_NAME))
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
        print(os.path.exists(db.DB_NAME))
        # await populate_table()
        # cid = 1420
        # found, li = db.select_contest(cid)
        # if (not found):
        #     log(Status.WARN, f"could not find the contest {cid}.")
        # else:
        #     print(li)
    except Exception as e:
        log(Status.ERR, str(e))
    finally:
        db.ccfree(con,cur)

asyncio.run(main())
