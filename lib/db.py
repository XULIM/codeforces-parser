import sqlite3
from sqlite3 import Connection, Cursor
from enum import Enum
from ps import log, Status

type void = None

class Attributes(tuple, Enum):
    def __new__(cls, values):
        obj = tuple.__new__(cls, values[0])
        obj._value_ = values[0]
        return obj
    ID = ("cid", "INTEGER NOT NULL"),
    INDEX = ("pindex", "VARCHAR NOT NULL"),
    NAME = ("name", "TEXT"),
    POINTS = ("points", "INT"),
    RATING = ("rating", "INT"),
    TAGS = ("tags", "TEXT"),
    SOLVED = ("is_solved", "INT"),

DB_NAME = "results.db"
TABLE_NAME = "problems"

def doc_param(*sub):
    """
    Decorator that allows doc strings to accept parameters.
    """
    def dec(obj):
        obj.__doc__ = obj.__doc__.format(*sub)
        return obj
    return dec

@doc_param(DB_NAME)
def establish() -> tuple[Connection, Cursor]:
    """
    Establishes sqlite3 connection to DB_NAME({0}).
    Raises sqlite3.DatabaseError if fails.
    Returns a tuple in the form of (sqlite3.Connection, sqlite3.Cursor).
    """
    try:
        con = sqlite3.connect(DB_NAME)
        cur = con.cursor()
    except sqlite3.Error as e:
        log(Status.ERR, f"could not establish sqlite3 connection on {DB_NAME},", str(e))
        raise sqlite3.DatabaseError("Could not establish sqlite3 connection")
    return (con, cur)

def ccfree(con: Connection | None, cur: Cursor | None = None):
    """
    Closes/Frees any existing sqlite3.Connection and sqlite3.Cursor.
    """
    if (cur):
        cur.close()
    if (con):
        con.commit()
        con.close()

def drop_table() -> void:
    con, cur = establish()
    try:
        cur.execute(f"DROP TABLE IF EXISTS {TABLE_NAME};")
    except sqlite3.Error as e:
        raise sqlite3.DatabaseError(f"Could not drop table {TABLE_NAME}.", str(e))
    finally:
        ccfree(con,cur)

def create_table() -> void:
    """
    Creates the problems table with the attributes in Attributes enum.
    Raises sqlite3.DatabaseError if fails.
    """
    # ---
    cmd = "CREATE TABLE IF NOT EXISTS problems(\n"
    for _, mem in Attributes.__members__.items():
        attr, dtype = mem.value
        cmd += f"\t{attr} {dtype},\n"
    cmd += f"\tPRIMARY KEY ({Attributes.ID.value[0]}, {Attributes.INDEX.value[0]})\n"
    cmd += ");"
    # ---

    con, cur = establish()
    try:
        cur.execute(cmd)
    except sqlite3.DatabaseError as e:
        log(Status.ERR, "from create_table: could not create table.", str(e))
        raise sqlite3.DatabaseError("Could not create table", str(e))
    finally:
        ccfree(con,cur)
    log(Status.OK, "from create_table: successfully created table [problems].")

def insert(entry: list | tuple):
    con, cur = establish()
    log(Status.OK, "connection established")
    cmd = f"INSERT INTO {TABLE_NAME} VALUES(?,?,?,?,?,?,?);"
    try:
        if (type(entry) is list):
            cur.executemany(cmd, entry)
        else:
            cur.execute(cmd, entry)
    except sqlite3.Error as e:
        log(Status.ERR, "could not insert into table.", str(e))
        raise sqlite3.OperationalError("Failed to insert into problems table.")
    finally:
        ccfree(con,cur)
    log(Status.OK, f"inserted values into {TABLE_NAME}.")

