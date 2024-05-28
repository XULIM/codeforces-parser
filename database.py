import sqlite3
from objects import entry, entries
from enums import tables
from exceptions import InvalidDatabaseException
from pprint import pprint


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
        self.connection.close()

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
                    PRIMARY KEY (contestId, problemIndex)
                );
            """
        )
        print("Created table: problems")

    def get_tables(self):
        """
        Returns the tables in the database.
        """
        res = self.cursor.execute("SELECT name FROM sqlite_master;")
        return res.fetchone()

    # FIX: change table to conform with entry object.
    def insert_rows(self, table: str, entries: entries):
        if table not in self.get_tables():
            raise sqlite3.DatabaseError("table " + table + " not found.")
        self.cursor.execute("INSERT INTO problems VALUES ?", entries.conform_str_insert())

    def select_rows(self, rows):
        print("Selecting rows: {}", rows)
