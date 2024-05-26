import sqlite3
from objects import entry
from enums import tables
from exceptions import InvalidDatabaseException
from pprint import pprint

def adapt_entry(en):
    return str(en)

class parser_database:
    """
    Database to store parsed data for faster retrieving (filtered) data.

    Throws error on failed database transaction.
    """

    def __init__(self) -> None:
        """
        Creates the results.db database file along with the problems table.
        """
        print("Initializing database: results.db")
        self.connection = sqlite3.connect("results.db")
        self.cursor = self.connection.cursor()
        self.__create_problems_table()

    def __construct_str(self, values: list, prefix: str = "", suffix: str = ",") -> str:
        """
        Creates a valid string for value binding.
        """
        res = ""
        for i, x in values:
            res += prefix + x
            if i + 1 != len(values):
                res += suffix
        return res

    def __create_problems_table(self) -> None:
        print("Creating: problems table")
        self.cursor.execute(
            """
                CREATE TABLE IF NOT EXISTS problems (
                    contestId INTEGER NOT NULL,
                    problemIndex VARCHAR NOT NULL,
                    name VARCHAR,
                    rating INT,
                    tags TEXT,
                    solvedCount INT,
                    PRIMARY KEY (contestId, index_)
                );
            """
        )
        print("Created table: problems")

    def get_tables(self):
        res = self.cursor.execute("SELECT name FROM sqlite_master;")
        return res.fetchone()

    def insert(self, table: str, en: entry):
        pass

    # FIX: change table to conform with entry object.
    def insert_rows(self, table: str, entries):
        if table not in self.get_tables():
            raise sqlite3.DatabaseError("table " + table + " not found.")

    def select_rows(self, rows):
        print("Selecting rows: {}", rows)
