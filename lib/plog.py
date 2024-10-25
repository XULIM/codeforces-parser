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

class PError(Exception):
    def __init__(self, msg="", *args):
        errmsg: str = f"{str(Status.ERR)}::{msg}"
        for arg in args:
            errmsg += ("\n\t>> " + arg)
        super().__init__(errmsg)

def log(stat: Status | PError, msg="", *args):
    """
    Could throw an error if the passed in args does not have a valid __str__ method.
    """
    if stat is PError:
        print(stat)
        return
    print(f"{str(stat)}::{msg}", *args, sep="\n\t>> ")
