import sqlite3
from enum import Enum


class tables(Enum):
    PROBLEMS = "problems"


class parser_database:
    def __init__(self) -> None:
        self.connection = sqlite3.connect("results.db")
        self.cursor = self.connection.cursor()

    def create_table(self, tb_name: tables):
        self.cursor.execute("""CREATE TABLE ?""", tb_name.value)
