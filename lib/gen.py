import functools
from lib import db
from lib.ps import Status, log, file_refresh

type void = None

@functools.cache
def catfile(template: str):
    with open(template, "r") as f:
        temp = f.read()
    return temp

def genfile(cid: int, pindex: str, template: str) -> void:
    template = catfile(template)
    pass
    
"""
generate for problems a, b, c,...
each using template
so we need to know how many problems there are
what each there indexes are,
i.e. if problems like c1, c2 exists
"""
def gencontest(cid: int):
    pass
