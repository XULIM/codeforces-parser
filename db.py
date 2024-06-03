import sqlite3 as sql
from objects import entry, entries


class db:
    def __create_table(self):
        self.cur.execute(
                "CREATE TABLE IF NOT EXISTS problems ("
                    "contestId INTEGER NOT NULL,"
                    "problemIndex VARCHAR NOT NULL,"
                    "rating INT,"
                    "tags TEXT,"
                    "solvedCount INT,"
                    "PRIMARY KEY (contestId, problemIndex)"
                ");"
            )

    def __init__(self, file="results.db"):
        self.file = file
        self.con = sql.connect(file)
        self.cur = self.con.cursor()
        try:
            self.__create_table()
        except sql.OperationalError as e:
            print("Erorr creating problems table.")
        except sql.Error as e:
            print("Error: " + str(e))
        finally:
            if self.con:
                self.con.close()

    def insert(self, ens: entries):
        if not self.con:
            self.con = sql.connect(self.file)

