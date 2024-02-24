import sqlite3
from sqlite3.dbapi2 import SQLITE_ERROR
from enums import tables


class parser_database:
    def __init__(self) -> None:
        print("Initializing database: results.db")
        self.connection = sqlite3.connect("results.db")
        self.cursor = self.connection.cursor()

    def __construct_str(self, values: list, prefix: str = "", suffix: str = ",") -> str:
        res = ""
        for i, x in values:
            res += prefix + x
            if i + 1 != len(values):
                res += suffix
        return res

    # TODO: create table for each contest
    def __create_contest_table(self, tb_name: str = "contest") -> None:
        print("Creating table: {}", tb_name)

        self.cursor.execute(
            """
            CREATE TABLE ? (
                INT contestId,
                ID VARCHAR index, 
                VARCHAR name,
                VARCHAR(11) type,
                FLOAT points,
                INT rating,
                TEXT tags
            )
        """,
            tb_name,
        )

    # TODO: create table containing contests
    def __create_problems_table(self, tb_name: str = "problems") -> None:
        print("Creating table: {}", tb_name)

        self.cursor.execute(
            """
            CREATE TABLE ? (
                ID INT contestId
            )
        """,
            tb_name,
        )

    def inject_rows(self, tb_name: str, rows: dict[str, str]):
        if tb_name not in tables.list_values():
            # TODO: create an exception for invalid table.
            raise Exception("Error: not a valid table.")

        print("Injecting rows: {}", rows)

        # create string for value binding
        values_str = self.__construct_str(tables.list_values(), ":")

        self.cursor.executemany(f"""INSERT INTO {tb_name} VALUES({values_str})""", rows)
        self.connection.commit()

    def select_rows(self, rows):
        print("Selecting rows: {}", rows)
