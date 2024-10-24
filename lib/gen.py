import os
import functools
from lib import db
from lib.plog import Status, log
from lib.consts import TEMPLATE_CPP

type void = None

@functools.cache
def catfile(template: str):
    with open(template, "r") as f:
        temp = f.read()
    return temp

def genfile(cid: int, pindex: str, prefix: bool = True) -> void:
    template = catfile(TEMPLATE_CPP)
    filename = f"{cid}{pindex}" if prefix else pindex
    with open(filename, "w") as f:
        f.write(template)
    
"""
generate for problems a, b, c,...
each using template
so we need to know how many problems there are
what each there indexes are,
i.e. if problems like c1, c2 exists
"""
def gencontest(cid: int):
    dir_path = str(cid)
    found, pindices = db.select_contest(cid)
    if (not found):
        log(Status.ERR, f"from gencontest: could not find contest: {cid}.", "aborting.")
    try:
        log(Status.WARN, f"creating directory: {dir_path}.")
        os.mkdir(dir_path)
        for pindex in pindices:
            genfile(contest, pindex)
    except Exception as e:
        log(Status.ERR, f"from gencontest: an unexpected error occurred.", e)
