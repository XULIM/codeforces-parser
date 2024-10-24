from enum import Enum

class Status(Enum):
    OK = (0, "[OK]")
    ERR = (1, "[ERR]")
    WARN = (2, "[!]")
    def __init__(self, num, string):
        self.num = num
        self.string = string
    def __str__(self):
        return self.string

def log(stat: Status, msg="", *args):
    """
    Could throw an error if the passed in args does not have a valid __str__ method.
    """
    print(f"{str(stat)}::{msg}", *args, sep="\n\t>> ")
