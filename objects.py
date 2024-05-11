class entry:
    # FIX: check the json object again, the value access method below is wrong.
    # json -> result -> problems/problemStatistics -> each key : value.
    def __init__(self, jsn):
        problems = (
            jsn["result"]["problems"] if jsn.get("result", 0) else jsn["problems"]
        )
        statistics = (
            jsn["result"]["problemStatistics"]
            if jsn.get("result", 0)
            else jsn["problems"]
        )
        self.contest_id = problems["contestId"]
        self.index = problems["index"]
        self.name = problems["name"]
        self.rating = problems["rating"]
        self.tags = [e for e in problems["tags"]]
        self.solved_count = statistics["solvedCount"]

    def tags_str(self) -> str:
        return "".join(self.tags)

    # def __str__(self) -> str:
    #     s = ""
    #     for k, v in self.__dict__:
    #         s += "\t{:<10}: {:>10}\n".format(k, v)
    #     return s


# FIX: make it initializable from string and dict.
class entries:
    def __init__(self, it):
        self.values = (entry(i) for i in it)

    def __iter__(self):
        for x in self.values:
            yield x
