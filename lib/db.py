import sqlite3
from sqlite3 import Connection, Cursor
from enum import Enum
from lib.consts import DB_PATH, DB_TABLE
from lib.plog import Status, log

type void = None

class Attributes(tuple, Enum):
    """
    For each name there is a tuple value in the form of
        (col_name, dtype)
        where col_name is the column name in database,
        and dtype is the datatype used upon table creation.

    Members:
        first (str): returns col_name.
        second (str): returns dtype.
    """
    # def __new__(cls, values):
    #     obj = tuple.__new__(cls, values[0])
    #     obj._value_ = values[0]
    #     return obj
    def __init__(self, tup_val):
        self._value_ = tup_val[0]
        self.first = self._value_[0]
        self.second = self._value_[1]
    ID = ("cid", "INTEGER NOT NULL"),
    INDEX = ("pindex", "VARCHAR NOT NULL"),
    NAME = ("name", "TEXT"),
    POINTS = ("points", "INT"),
    RATING = ("rating", "INT"),
    TAGS = ("tags", "TEXT"),
    SOLVED = ("solved", "INT"),

def doc_param(*sub):
    """
    Decorator that allows doc strings to accept parameters.
    """
    def dec(obj):
        obj.__doc__ = obj.__doc__.format(*sub)
        return obj
    return dec

@doc_param(DB_PATH)
def establish() -> tuple[Connection, Cursor]:
    """
    Establishes sqlite3 connection to DB_PATH({0}).
    Raises sqlite3.DatabaseError if fails.
    Returns a tuple in the form of (sqlite3.Connection, sqlite3.Cursor).
    """
    try:
        con = sqlite3.connect(DB_PATH)
        cur = con.cursor()
    except sqlite3.Error as e:
        log(Status.ERR, f"could not establish sqlite3 connection on {DB_PATH},", str(e))
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
    """
    Drops the problems table.
    Raises sqlite3.OperationalError if fails.
    """
    con, cur = establish()
    try:
        log(Status.WARN, f"dropping table [{DB_TABLE}]")
        cur.execute(f"DROP TABLE IF EXISTS {DB_TABLE};")
    except sqlite3.Error as e:
        raise sqlite3.OperationalError(f"Could not drop table [{DB_TABLE}].", str(e))
    finally:
        ccfree(con,cur)
    log(Status.OK, "from drop_table:", f"table [{DB_TABLE}] has been dropped successfully.")

def create_table() -> void:
    """
    Creates the problems table with the attributes in Attributes enum.
    Raises sqlite3.DatabaseError if fails.
    """
    # ---
    cmd = f"CREATE TABLE IF NOT EXISTS {DB_TABLE}(\n"
    for _, mem in Attributes.__members__.items():
        attr, dtype = mem.value
        cmd += f"\t{attr} {dtype},\n"
    cmd += f"\tPRIMARY KEY ({Attributes.ID.first}, {Attributes.INDEX.first})\n"
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
    log(Status.OK, f"from create_table: successfully created table [{DB_TABLE}].")

def table_exists() -> bool:
    con, cur = establish()
    cmd = f"SELECT name FROM sqlite_master WHERE type='table' AND name='{DB_TABLE};'"
    try:
        res = cur.execute(cmd).fetchone()
        if (not res):
            return False
    except sqlite3.DatabaseError as e:
        log(Status.ERR, "from table_exists: operation failed.", e)
        raise sqlite3.OperationalError("could not execute command to find whether table exists.", 
                                       f"Command: {cmd}")
    except Exception as e:
        log(Status.ERR, "from table_exists: unexpected error occurred", e)
        raise Exception("from table_exists: ", e)
    finally:
        ccfree(con,cur)
    log(Status.OK, f"from table_exists: table found {DB_TABLE}.")
    return True

def insert(entry: list | tuple):
    con, cur = establish()
    log(Status.OK, "connection established")
    cmd = f"INSERT INTO {DB_TABLE} VALUES(?,?,?,?,?,?,?);"
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
    log(Status.OK, f"inserted values into {DB_TABLE}.")

def select_contest(cid: int) -> tuple:
    con, cur = establish()
    li = []
    try:
        cmd = f"SELECT {Attributes.INDEX.first} FROM {DB_TABLE} WHERE cid == ?;"
        res = cur.execute(cmd, (cid,)).fetchall()
        if (not res):
            return (False, li)
        for line in res:
            li.append(line[0])
    except sqlite3.Error as e:
        log(Status.ERR, f"could not get contest {cid} -", e)
        raise sqlite3.OperationalError(f"Could not get contest {cid}.")
    except Exception as e:
        log(Status.ERR, f"an unexpected error occurred -", e)
    finally:
        ccfree(con,cur)
    log(Status.OK, f"contest found.")
    return (True, li)

# TODO: finish this bih
def select_problem(cid: int, pindex: str):
    con, cur = establish()
    try:
        cmd = (f"SELECT {Attributes.NAME.first}," + 
            f"{Attributes.RATING.first}," +
            f"{Attributes.TAGS.first}," +
            f"{Attributes.SOLVED.first}" +
            f"from {DB_TABLE};"
        )
        print(cmd)
    except sqlite3.Error as e:
        pass
    finally:
        ccfree(con,cur)
