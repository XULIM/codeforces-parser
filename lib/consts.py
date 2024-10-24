import os
from enum import Enum
from lib.plog import Status, log

DATA = "~/.local/share/cfp/"
if not os.path.exists(DATA):
    try:
        os.makedirs(DATA, 755)
        log(Status.OK, "directory created.")
    except Exception as e:
        log(Status.ERR, "from consts module.", "an unexpected error occurred.", e)
else:
    log(Status.OK, "directory exists.", "proceeding")

DB_PATH = DATA + "results.db"
DB_TABLE = "problems"

UA_PATH = DATA + "ualist"
HTML_PATH = DATA + "index.html"

TEMPLATE = "template"
TEMPLATE_CPP = DATA + TEMPLATE + ".cpp"
