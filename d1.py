import p1
import sqlite3
from enum import Enum

type void = None

class Attributes(Enum):
    ID = "contest_id",
    INDEX = "index",
    NAME = "name",
    POINTS = "points",
    RATING = "rating",
    TAGS = "tags",
    SOLVED = "is_solved"

con = sqlite3.connect("results.db")
cur = con.cursor()

def create_table():
    pass
