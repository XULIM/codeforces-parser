import sqlite3


class entry:
    """
    Represents an entry object for database.
    contest_id: int
    index: str
    name: str
    rating: int
    tags: list[str]
    solved_count: int
    """

    def __init__(self, problem: dict, stats: dict):
        """
        contest_id (int): has to be parsed, throws error if it DNE.
        index (str): has to be parsed, throws error if it DNE.
        name (str): defaults to "" if DNE.
        rating (int): defaults to 0 if DNE.
        tags (list[str]): defaults to [] (empty list) if DNE.
        solved_count (int): defaults to 0 if DNE or mismatch in problem and stats.
        """
        self.contest_id: int = problem["contestId"]
        self.index: str = problem["index"]
        self.rating: int = problem.get("rating", 0) or problem.get("points", 0)
        self.tags: list[str] = problem.get("tags", [])
        self.solved_count: int = (
            stats.get("solvedCount", 0)
            if (self.contest_id == stats["contestId"] and self.index == stats["index"])
            else 0
        )

    def __repr__(self):
        return (
            "objects.entry(\n\t"
            f"contest_id = {self.contest_id}\n\t"
            f"index = {self.index}\n\t"
            f"rating = {self.rating}\n\t"
            f"tags = [{",".join(e for e in self.tags)}]\n\t"
            f"solved_count = {self.solved_count}"
            ")"
        )

    def __str__(self):
        return (
            f'({self.contest_id}, "{self.index}", {self.rating}, '
            f'"{",".join(e for e in self.tags)}", {self.solved_count})'
        )

    def conform(self):
        """Returns a conformed tuple for database operations."""
        return (self.contest_id, self.index, self.rating, ",".join(e for e in self.tags), self.solved_count)

    def __conform__(self, protocol):
        if protocol is sqlite3.PrepareProtocol:
            return str(self)


class entries:
    def __init__(self, res: dict):
        self.entries: list[entry] = []
        if len(res["problems"]) != len(res["problemStatistics"]):
            print(
                "WARNING: the problems dictionary and the problemStatistics dictionary are not "
                "matching in value, a default value of 0 for solved_count will be used."
            )

        for i in range(len(res["problems"])):
            self.entries.append(entry(res["problems"][i], res["problemStatistics"][i]))

    def __str__(self):
        return ",".join(str(x) for x in self.entries)

    def conform(self):
        """Returns a list of conformed tuples for database operations."""
        return [x.conform() for x in self.entries]

    def seg(self, l: int = 0, r: int = 0):
        self.entries = self.entries[l:r]
