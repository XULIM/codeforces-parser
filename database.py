import sqlite3
from enums import tables


class parser_database:
    def __init__(self) -> None:
        print("Initializing database: results.db")
        self.connection = sqlite3.connect("results.db")
        self.cursor = self.connection.cursor()

    def create_table(self, tb_name: tables) -> None:
        print("Creating table: {}", tb_name)
        rows_values = tables.list_values()
        row_str = ""
        for i, x in rows_values:
            row_str += x
            if i + 1 != len(rows_values):
                row_str += ","
        self.cursor.execute("""CREATE TABLE {0}({1})""".format(tb_name, row_str))

    def inject_rows(self, tb_name, rows):
        print("Injecting rows: {}", rows)
        rows_values = tables.list_values()
        values_str = ""
        for i, x in rows_values:
            values_str += ":" + x
            if i + 1 != len(rows_values):
                values_str += ","
        self.cursor.executemany(f"""INSERT INTO {tb_name} VALUES({values_str})""", rows)

    def select_rows(self, rows):
        pass
