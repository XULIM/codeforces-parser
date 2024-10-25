import os
from enum import Enum
from lib.plog import Status, log

DATA = os.path.expanduser("~") + "/.local/share/cfp/"
if not os.path.exists(DATA):
    log(Status.WARN, "default data directory not found.", "creating directory.")
    try:
        os.mkdir(DATA, mode=711)
    except Exception as e:
        log(Status.ERR,
            "an unexpected error happened while creating default data directory.",
            e)
    log(Status.OK, "default data directory created.")
else:
    log(Status.OK, "default data directory detected (dddd).", "proceeding.")

DB_PATH = DATA + "results.db"
DB_TABLE = "problems"

UA_PATH = DATA + "ualist"
HTML_PATH = DATA + "index.html"

TEMPLATE = "template"
TEMPLATE_CPP = DATA + TEMPLATE + ".cpp"
