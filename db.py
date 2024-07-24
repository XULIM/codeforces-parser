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

    def drop_table(self, table="problems"):
        self.cur.execute("DROP TABLE IF EXISTS ?;", table)

    def get_tables(self):
        try:
            if not self.con:
                self.con = sql.connect(self.file)
                self.cur = self.con.cursor()
            self.cur.execute("SELECT name FROM sqlite_master;")
        except sql.OperationalError as e:
            print("Error selecting tables: " + str(e))
        except sql.Error as e:
            print("Error selecting tables: " + str(e))
        finally:
            res = self.cur.fetchone()
            if self.con:
                self.con.close()
            return res

    def __init__(self, file="results.db") -> None:
        """
        Initializes the database with the given file name (default: results.db).
        Establishes a sqlite3 connection and initializes a cursor object.
        """
        self.file = file
        self.con = sql.connect(file)
        self.cur = self.con.cursor()
        try:
            self.__create_table()
        except sql.OperationalError:
            print("Error creating problems table.")
        except sql.Error as e:
            print("Error: " + str(e))
        finally:
            print(self.con)
            if self.con:
                self.cur.close()
                self.con.close()
                self.con = None

    def insert(self, en: entry) -> None:
        try:
            if not self.con:
                self.con = sql.connect(self.file)
                self.cur = self.con.cursor()
            self.cur.execute("INSERT INTO problems VALUES(?, ?, ?, ?, ?);", en.conform())
            self.con.commit()
        except sql.OperationalError:
            print("Error inserting into table: " + str(en))
        except sql.Error as e:
            print("Error inserting into table: " + str(e))
        finally:
            if self.con:
                self.cur.close()
                self.con.close()
                self.con = None

    def insert_many(self, ens: entries) -> None:
        try:
            if not self.con:
                self.con = sql.connect(self.file)
                self.cur = self.con.cursor()
            if not ens: 
                raise sql.OperationalError("No valid entries given.")
            else: 
                self.cur.executemany(
                    "INSERT INTO problems VALUES(?,?,?,?,?)", ens.conform()
                )
            self.con.commit()
        except sql.OperationalError:
            print("Error inserting into table: " + str(ens))
        except sql.Error as e:
            print("Error inserting into table: " + str(e))
        finally:
            if self.con:
                self.cur.close()
                self.con.close()
                self.con = None
    
    #TODO: complete SELECT operation with aliases?
    def select(self, contest_id: int, index: str):
        try: 
            if not self.con:
                self.con = sql.connect(self.file)
                self.cur = self.con.cursor()
            # continue here.
        except sql.OperationalError:
            print(f"Error selecting from table problem: {contest_id}-{index}")
        except sql.Error as e:
            print("Error selecting from table: " + str(e))
        finally: 
            if self.con: 
                self.cur.close()
                self.con.close()
                self.con = None
