import sqlite3
from enums import tables
from exceptions import InvalidDatabaseException


class parser_database:
    def __init__(self) -> None:
        print("Initializing database: results.db")
        self.connection = sqlite3.connect("results.db")
        self.cursor = self.connection.cursor()
        self.__create_problems_table()

    def __construct_str(self, values: list, prefix: str = "", suffix: str = ",") -> str:
        res = ""
        for i, x in values:
            res += prefix + x
            if i + 1 != len(values):
                res += suffix
        return res

    def __create_problems_table(self) -> None:
        print("Creating table: problems")

        self.cursor.execute(
            """
            CREATE TABLE problems (
                INT contestId NOT NULL,
                VARCHAR index NOT NULL,
                VARCHAR name,
                VARCHAR(11) type,
                FLOAT points,
                INT rating,
                TEXT tags,
                PRIMARY KEY (contestId, index)
            );
        """
        )

    def insert_rows(self, tb_name: str, rows: dict[str, str]):
        if tb_name not in tables.list_values():
            raise InvalidDatabaseException("Error: not a valid table.")

        print("Inserting rows: {}", rows)

        # create string for value binding
        values_str = self.__construct_str(tables.list_values(), ":")

        self.cursor.executemany(f"""INSERT INTO {tb_name} VALUES({values_str})""", rows)
        self.connection.commit()

    def select_rows(self, rows):
        print("Selecting rows: {}", rows)
